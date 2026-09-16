import os
import sys
import time
import re
import threading
import subprocess
import webbrowser

# Ensure UTF-8 output on Windows consoles
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

from waitress import serve
from app import app, init_db, ADMIN_PASSWORD
import qrcode

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLOUDFLARED = os.path.join(BASE_DIR, 'cloudflared.exe')
LINK_FILE = os.path.join(BASE_DIR, 'sayt_manzili.txt')
QR_FILE = os.path.join(BASE_DIR, 'sayt_qr_kod.png')

init_db()

print("="*75, flush=True)
print("     SO'ROVNOMA VA NATIJALAR PORTALI CLOUDFLARE ORQALI ULANYAPTI...", flush=True)
print("="*75, flush=True)

# 1. Waitress WSGI server
def run_waitress():
    serve(app, host='127.0.0.1', port=5000, threads=8, channel_timeout=60)

server_thread = threading.Thread(target=run_waitress, daemon=True)
server_thread.start()
print("[1/2] Ichki veb-server (Waitress WSGI) muvaffaqiyatli ishga tushdi.", flush=True)

# 2. Cloudflare tunnel
print("[2/2] Cloudflare tarmog'idan xavfsiz HTTPS havola olinmoqda (5-10 soniya)...", flush=True)

cf_cmd = [
    CLOUDFLARED, 'tunnel',
    '--url', 'http://127.0.0.1:5000',
    '--no-autoupdate'
]

cf_proc = subprocess.Popen(
    cf_cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    encoding='utf-8',
    errors='ignore',
    cwd=BASE_DIR
)

public_url = None
found_event = threading.Event()

def read_tunnel_output():
    global public_url
    while True:
        line = cf_proc.stdout.readline()
        if not line:
            break
        if not public_url:
            match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
            if match:
                public_url = match.group(0)
                found_event.set()

output_thread = threading.Thread(target=read_tunnel_output, daemon=True)
output_thread.start()

if found_event.wait(timeout=40) and public_url:
    time.sleep(3)

    survey_url = f"{public_url}/"
    admin_url = f"{public_url}/admin"

    banner = f"""
****************************************************************************
           TABRIKLAYMIZ! SAYT INTERNETDA TO'LIQ ISHLAMOQDA!
****************************************************************************

[+] O'QUVCHILAR UCHUN SO'ROVNOMA (Saytga kirganda FAQAT shu ochiladi):
    >> {survey_url}

[+] MAXFIY ADMIN PANELI (Faqat siz uchun, parolli):
    >> {admin_url}
    Parol: {ADMIN_PASSWORD}

[+] LOKAL KOMPYUTERDA ISHLATISH UCHUN:
    So'rovnoma: http://localhost:5000
    Admin:      http://localhost:5000/admin (Parol: {ADMIN_PASSWORD})

****************************************************************************
[INFO] Barcha havolalar "sayt_manzili.txt" fayliga saqlandi!
[INFO] QR-kod "sayt_qr_kod.png" fayliga saqlandi!
****************************************************************************
[DIQQAT] Ushbu QORA OYNANI YOPMANG!
         Oyna yopilsa sayt internetda to'xtaydi. Oynani svernut qilib qo'ying!
****************************************************************************
"""
    print(banner, flush=True)

    with open(LINK_FILE, 'w', encoding='utf-8') as f:
        f.write(f"O'quvchilar uchun ommaviy so'rovnoma havolasi:\n{survey_url}\n\nMaxfiy admin paneli:\n{admin_url}\nParol: {ADMIN_PASSWORD}\n")

    try:
        qr = qrcode.make(survey_url)
        qr.save(QR_FILE)
    except Exception as e:
        print(f"QR kod saqlashda xatolik: {e}")

    try:
        webbrowser.open(survey_url)
    except:
        pass

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSayt to'xtatildi.", flush=True)
        cf_proc.terminate()
else:
    print("\n[XATOLIK] Cloudflare havolasi olinmadi. Internet tarmog'ini tekshiring.", flush=True)
    cf_proc.terminate()
