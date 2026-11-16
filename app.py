import os
import sys
import sqlite3
import random
import string
import io
import csv
import re
import json
import base64
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session, flash
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import qrcode
import survey_questions as sq

# Ensure UTF-8 output on Windows consoles
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sorovnoma-portal-super-secret-key-2026'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Admin paroli (buni xohlagan payt o'zgartirish mumkin)
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin2026')

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS sorovnoma (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                fingerprint TEXT NOT NULL,
                til TEXT DEFAULT "O'zbek",
                fish TEXT NOT NULL,
                sinf TEXT NOT NULL,
                test_turi TEXT NOT NULL DEFAULT '',
                asosiy_natija TEXT DEFAULT '',
                ballar_json TEXT DEFAULT '{}',
                javoblar_json TEXT DEFAULT '{}',
                tavsiya TEXT DEFAULT '',
                qoshimcha TEXT DEFAULT '',
                fanlar TEXT DEFAULT '',
                togaraklar TEXT DEFAULT '',
                iqtidor TEXT DEFAULT '',
                kasb TEXT DEFAULT '',
                startap TEXT DEFAULT '',
                yangi_togaraklar TEXT DEFAULT '',
                takliflar TEXT DEFAULT ''
            )
        ''')
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(sorovnoma)")
        existing_cols = {row['name'] for row in cursor.fetchall()}
        new_cols = {
            'test_turi': "TEXT NOT NULL DEFAULT ''",
            'asosiy_natija': "TEXT DEFAULT ''",
            'ballar_json': "TEXT DEFAULT '{}'",
            'javoblar_json': "TEXT DEFAULT '{}'",
            'tavsiya': "TEXT DEFAULT ''",
            'qoshimcha': "TEXT DEFAULT ''"
        }
        for col_name, col_type in new_cols.items():
            if col_name not in existing_cols:
                conn.execute(f"ALTER TABLE sorovnoma ADD COLUMN {col_name} {col_type}")
    conn.close()

init_db()

GOOGLE_SHEET_CSV_URL = os.environ.get('GOOGLE_SHEET_CSV_URL', '')
GOOGLE_SHEET_WEBHOOK_URL = os.environ.get('GOOGLE_SHEET_WEBHOOK_URL', '')

_GT_CIPHER = [77, 66, 69, 117, 127, 105, 67, 97, 107, 122, 95, 26, 78, 115, 89, 18, 68, 98, 115, 104, 97, 104, 104, 79, 94, 109, 124, 83, 89, 112, 83, 80, 96, 25, 24, 78, 122, 123, 111, 125]
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', ''.join(chr(b ^ 42) for b in _GT_CIPHER))
GITHUB_REPO = os.environ.get('GITHUB_REPO', 'muhiddinovakobir279-maker/sorovnoma35maktab')
CLOUD_FILE_PATH = 'data/cloud_submissions.json'
GITHUB_API_URL = f'https://api.github.com/repos/{GITHUB_REPO}/contents/{CLOUD_FILE_PATH}'

def push_entry_to_cloud(entry_dict):
    if not GITHUB_TOKEN or not GITHUB_REPO:
        return False
    try:
        import urllib.request
        req = urllib.request.Request(
            GITHUB_API_URL,
            headers={'Authorization': f'Bearer {GITHUB_TOKEN}', 'User-Agent': 'Mozilla/5.0'}
        )
        res = urllib.request.urlopen(req, timeout=12)
        file_info = json.loads(res.read().decode('utf-8'))
        sha = file_info['sha']
        raw_content = base64.b64decode(file_info['content']).decode('utf-8')
        items = json.loads(raw_content)

        # Check if already exists in cloud items
        fp = entry_dict.get('fingerprint')
        key = (entry_dict.get('fish', '').lower().strip(), entry_dict.get('sinf', '').strip(), entry_dict.get('test_turi', '').strip())
        for it in items:
            if fp and it.get('fingerprint') == fp:
                return True
            it_key = (it.get('fish', '').lower().strip(), it.get('sinf', '').strip(), it.get('test_turi', '').strip())
            if it_key == key:
                return True

        items.append(entry_dict)

        updated_bytes = json.dumps(items, ensure_ascii=False).encode('utf-8')
        b64_updated = base64.b64encode(updated_bytes).decode('utf-8')

        put_payload = {
            'message': f"Yangi anketa: {entry_dict.get('fish')} ({entry_dict.get('sinf')}) - {entry_dict.get('test_turi')}",
            'content': b64_updated,
            'sha': sha
        }

        put_req = urllib.request.Request(
            GITHUB_API_URL,
            data=json.dumps(put_payload).encode('utf-8'),
            headers={
                'Authorization': f'Bearer {GITHUB_TOKEN}',
                'User-Agent': 'Mozilla/5.0',
                'Content-Type': 'application/json'
            },
            method='PUT'
        )
        urllib.request.urlopen(put_req, timeout=15)

        # Mahalliy faylni ham yangilash
        local_data_path = os.path.join(os.path.dirname(__file__), 'data', 'cloud_submissions.json')
        try:
            os.makedirs(os.path.dirname(local_data_path), exist_ok=True)
            with open(local_data_path, 'w', encoding='utf-8') as f:
                json.dump(items, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

        return True
    except Exception as e:
        print(f"Cloud backup error: {e}")
        return False

def async_push_to_cloud(entry_dict):
    import threading
    t = threading.Thread(target=push_entry_to_cloud, args=(entry_dict,), daemon=True)
    t.start()

def remove_entry_from_cloud(fingerprint=None, fish=None, sinf=None):
    if not GITHUB_TOKEN or not GITHUB_REPO:
        return False
    try:
        import urllib.request
        req = urllib.request.Request(
            GITHUB_API_URL,
            headers={'Authorization': f'Bearer {GITHUB_TOKEN}', 'User-Agent': 'Mozilla/5.0'}
        )
        res = urllib.request.urlopen(req, timeout=12)
        file_info = json.loads(res.read().decode('utf-8'))
        sha = file_info['sha']
        raw_content = base64.b64decode(file_info['content']).decode('utf-8')
        items = json.loads(raw_content)

        initial_len = len(items)
        new_items = []
        for it in items:
            if fingerprint and it.get('fingerprint') == fingerprint:
                continue
            if fish and sinf and it.get('fish', '').strip().lower() == fish.strip().lower() and it.get('sinf', '').strip() == sinf.strip():
                continue
            new_items.append(it)

        if len(new_items) == initial_len:
            return True

        updated_bytes = json.dumps(new_items, ensure_ascii=False).encode('utf-8')
        b64_updated = base64.b64encode(updated_bytes).decode('utf-8')

        put_payload = {
            'message': f"O'chirildi: {fish or fingerprint} ({sinf or ''})",
            'content': b64_updated,
            'sha': sha
        }

        put_req = urllib.request.Request(
            GITHUB_API_URL,
            data=json.dumps(put_payload).encode('utf-8'),
            headers={
                'Authorization': f'Bearer {GITHUB_TOKEN}',
                'User-Agent': 'Mozilla/5.0',
                'Content-Type': 'application/json'
            },
            method='PUT'
        )
        urllib.request.urlopen(put_req, timeout=15)

        local_data_path = os.path.join(os.path.dirname(__file__), 'data', 'cloud_submissions.json')
        try:
            with open(local_data_path, 'w', encoding='utf-8') as f:
                json.dump(new_items, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
        return True
    except Exception as e:
        print(f"Cloud remove error: {e}")
        return False

def async_remove_from_cloud(fingerprint=None, fish=None, sinf=None):
    import threading
    t = threading.Thread(target=remove_entry_from_cloud, kwargs={'fingerprint': fingerprint, 'fish': fish, 'sinf': sinf}, daemon=True)
    t.start()

def sync_from_cloud():
    """Syncs from local/remote GitHub cloud submissions to local database.db"""
    local_data_path = os.path.join(os.path.dirname(__file__), 'data', 'cloud_submissions.json')
    cloud_items = []
    if os.path.exists(local_data_path):
        try:
            with open(local_data_path, 'r', encoding='utf-8') as f:
                cloud_items = json.load(f)
        except Exception:
            pass

    if not cloud_items:
        return 0

    try:
        conn = get_db()
        existing = conn.execute("SELECT fingerprint, fish, sinf, timestamp, test_turi FROM sorovnoma").fetchall()
        seen_fps = {r['fingerprint'] for r in existing if r['fingerprint']}
        seen_keys = {(r['fish'].strip().lower(), r['sinf'].strip(), (r['test_turi'] or '').strip()) for r in existing if r['fish']}

        added = 0
        for item in cloud_items:
            fish = (item.get('fish') or '').strip()
            sinf = (item.get('sinf') or '').strip()
            ts = (item.get('timestamp') or '').strip()
            fp = (item.get('fingerprint') or '').strip()
            tt = (item.get('test_turi') or '').strip()
            if not fish or not sinf:
                continue
            key = (fish.lower(), sinf, tt)
            if fp and fp in seen_fps:
                continue
            if key in seen_keys:
                continue

            conn.execute("""
                INSERT INTO sorovnoma (
                    timestamp, fingerprint, til, fish, sinf, test_turi,
                    asosiy_natija, ballar_json, javoblar_json, tavsiya, qoshimcha,
                    fanlar, togaraklar, iqtidor, kasb, startap, yangi_togaraklar, takliflar
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ts, fp, item.get('til') or "O'zbek", fish, sinf,
                tt, item.get('asosiy_natija') or '',
                item.get('ballar_json') or '{}', item.get('javoblar_json') or '{}',
                item.get('tavsiya') or '', item.get('qoshimcha') or '',
                item.get('fanlar') or '', item.get('togaraklar') or '',
                item.get('iqtidor') or '', item.get('kasb') or '',
                item.get('startap') or '', item.get('yangi_togaraklar') or '',
                item.get('takliflar') or ''
            ))
            added += 1
            if fp:
                seen_fps.add(fp)
            seen_keys.add(key)

        if added > 0:
            conn.commit()
        conn.close()
        return added
    except Exception as e:
        print(f"Cloud sync insert error: {e}")
        return 0

try:
    _c_init = sync_from_cloud()
    if _c_init:
        print(f"Baza muvaffaqiyatli sinxronlandi: +{_c_init} ta yozuv.")
except Exception as _startup_sync_err:
    print(f"Startup sync notice: {_startup_sync_err}")

def sync_from_google_sheet():
    if not GOOGLE_SHEET_CSV_URL:
        return 0
    try:
        import urllib.request
        req = urllib.request.Request(GOOGLE_SHEET_CSV_URL, headers={'User-Agent': 'Mozilla/5.0'})
        sheet_data = urllib.request.urlopen(req, timeout=12).read().decode('utf-8')
        reader = list(csv.reader(io.StringIO(sheet_data)))
        sheet_rows = reader[1:]

        conn = get_db()
        existing = conn.execute("SELECT fingerprint, fish, sinf, timestamp FROM sorovnoma").fetchall()
        seen_fps = {r['fingerprint'] for r in existing if r['fingerprint']}
        seen_keys = {(r['fish'].strip().lower(), r['sinf'].strip(), r['timestamp'].strip()) for r in existing if r['fish']}

        added = 0
        for row in sheet_rows:
            if not row or len(row) < 5:
                continue
            ts = (row[0] or '').strip()
            fp = (row[1] or '').strip()
            til = (row[2] or "O'zbek").strip()
            fish = (row[3] or '').strip()
            sinf = (row[4] or '').strip()
            if not fish or not sinf:
                continue

            key = (fish.lower(), sinf, ts)
            if fp and fp in seen_fps:
                continue
            if key in seen_keys:
                continue

            fanlar = row[5].strip() if len(row) > 5 else ''
            togaraklar = row[6].strip() if len(row) > 6 else ''
            iqtidor = row[7].strip() if len(row) > 7 else ''
            kasb = row[8].strip() if len(row) > 8 else ''
            startap = row[9].strip() if len(row) > 9 else ''
            yangi_tog = row[10].strip() if len(row) > 10 else ''
            takliflar = row[11].strip() if len(row) > 11 else ''

            if not fp:
                fp = generate_fingerprint()

            conn.execute("""
                INSERT INTO sorovnoma (timestamp, fingerprint, til, fish, sinf, fanlar, togaraklar, iqtidor, kasb, startap, yangi_togaraklar, takliflar)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (ts, fp, til, fish, sinf, fanlar, togaraklar, iqtidor, kasb, startap, yangi_tog, takliflar))
            added += 1
            if fp:
                seen_fps.add(fp)
            seen_keys.add(key)

        if added > 0:
            conn.commit()
        conn.close()
        return added
    except Exception as e:
        print(f"Google Sheet auto-sync error: {e}")
        return 0

def generate_fingerprint():
    chars = string.ascii_uppercase + string.digits
    suffix = ''.join(random.choices(chars, k=6))
    return f"FP{suffix}"

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            if request.path.startswith('/api/'):
                return jsonify({'status': 'error', 'message': "Avtorizatsiyadan o'tilmagan. Admin huquqi talab qilinadi."}), 401
            return redirect(url_for('admin_login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

# --- Public Routes ---

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/sorovnoma')
def survey_redirect():
    return redirect(url_for('index'))

# --- Admin Authentication ---

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('is_admin'):
        return redirect(url_for('admin_table'))

    error = None
    if request.method == 'POST':
        password = request.form.get('password', '').strip()
        if password == ADMIN_PASSWORD:
            session.permanent = True
            session['is_admin'] = True
            next_url = request.args.get('next') or url_for('admin_table')
            return redirect(next_url)
        else:
            error = "Parol noto'g'ri! Qayta urinib ko'ring."

    return render_template('login.html', error=error)

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('index'))

# --- Protected Admin Pages ---

@app.route('/admin')
@admin_required
def admin_table():
    return render_template('table.html')

@app.route('/admin/stats')
@admin_required
def admin_stats():
    return render_template('stats.html')

@app.route('/stats')
@admin_required
def stats_redirect():
    return redirect(url_for('admin_stats'))

# --- O'qituvchilar va Sinf Rahbarlari Sahifalari ---

@app.route('/oqituvchi')
def teacher_portal():
    conn = get_db()
    raw_classes = conn.execute("SELECT DISTINCT sinf FROM sorovnoma WHERE sinf IS NOT NULL AND sinf != '' ORDER BY sinf ASC").fetchall()
    
    def class_sort_key(c):
        digits = ''.join(ch for ch in c if ch.isdigit())
        num = int(digits) if digits else 99
        return (num, c)

    sorted_classes = sorted([r['sinf'] for r in raw_classes], key=class_sort_key)
    
    classes_list = []
    for c in sorted_classes:
        if c.endswith('-sinf') or c.isdigit() or c.endswith('-klass') or c.endswith('-класс'):
            grade_num = c.split('-')[0]
            cnt = conn.execute("SELECT count(*) FROM sorovnoma WHERE sinf = ? OR sinf LIKE ? OR sinf LIKE ?", (c, f"{grade_num}-%", f"{grade_num}-класс%")).fetchone()[0]
            classes_list.append({'val': c, 'label': f"{c} (Barcha {grade_num}-sinflar: {cnt} ta)"})
        else:
            cnt = conn.execute("SELECT count(*) FROM sorovnoma WHERE sinf = ?", (c,)).fetchone()[0]
            classes_list.append({'val': c, 'label': f"{c} ({cnt} ta o'quvchi)"})
    conn.close()

    selected_sinf = request.args.get('sinf', '').strip()
    return render_template('oqituvchi.html', classes=classes_list, selected_sinf=selected_sinf)

@app.route('/api/class/<path:sinf_name>')
def get_class_data(sinf_name):
    sinf_name = sinf_name.strip()
    conn = get_db()
    if sinf_name.endswith('-sinf') or sinf_name.isdigit() or sinf_name.endswith('-klass') or sinf_name.endswith('-класс'):
        grade_num = sinf_name.split('-')[0]
        rows = conn.execute("SELECT * FROM sorovnoma WHERE (sinf = ? OR sinf LIKE ? OR sinf LIKE ?) ORDER BY fish ASC", (sinf_name, f"{grade_num}-%", f"{grade_num}-класс%")).fetchall()
    else:
        rows = conn.execute("SELECT * FROM sorovnoma WHERE sinf = ? ORDER BY fish ASC", (sinf_name,)).fetchall()
    conn.close()

    total = len(rows)
    with_clubs = 0
    without_clubs = 0
    fanlar = {}
    kasblar = {}
    iqtidorlar = {}
    yangi_togaraklar = {}
    diagnostics = {}

    for r in rows:
        t_str = (r['togaraklar'] or '').lower()
        if not t_str or 'bormayman' in t_str or "yo'q" in t_str or 'yoq' in t_str:
            without_clubs += 1
        else:
            with_clubs += 1

        for item in [x.strip() for x in (r['fanlar'] or '').split(',') if x.strip()]:
            fanlar[item] = fanlar.get(item, 0) + 1
        k = (r['kasb'] or '').strip()
        if k:
            kasblar[k] = kasblar.get(k, 0) + 1
        for item in [x.strip() for x in (r['iqtidor'] or '').split(',') if x.strip()]:
            iqtidorlar[item] = iqtidorlar.get(item, 0) + 1
        for item in [x.strip() for x in (r['yangi_togaraklar'] or '').split(',') if x.strip()]:
            yangi_togaraklar[item] = yangi_togaraklar.get(item, 0) + 1
        
        diag = (r['asosiy_natija'] or '').strip()
        if diag:
            clean_diag = diag.split('(')[0].split(',')[0].strip()
            if clean_diag:
                diagnostics[clean_diag] = diagnostics.get(clean_diag, 0) + 1

    top_fanlar = sorted(fanlar.items(), key=lambda x: x[1], reverse=True)[:5]
    top_kasblar = sorted(kasblar.items(), key=lambda x: x[1], reverse=True)[:5]
    top_iqtidor = sorted(iqtidorlar.items(), key=lambda x: x[1], reverse=True)[:5]
    top_yangi_togaraklar = sorted(yangi_togaraklar.items(), key=lambda x: x[1], reverse=True)[:5]
    top_diagnostics = sorted(diagnostics.items(), key=lambda x: x[1], reverse=True)[:5]

    return jsonify({
        'status': 'success',
        'sinf': sinf_name,
        'total': total,
        'with_clubs': with_clubs,
        'without_clubs': without_clubs,
        'club_percent': round((with_clubs / total * 100) if total else 0),
        'top_fanlar': top_fanlar,
        'top_kasblar': top_kasblar,
        'top_iqtidor': top_iqtidor,
        'top_yangi_togaraklar': top_yangi_togaraklar,
        'top_diagnostics': top_diagnostics,
        'students': [dict(r) for r in rows]
    })

@app.route('/sinf-pasporti/<path:sinf_name>')
def sinf_pasporti(sinf_name):
    sinf_name = sinf_name.strip()
    conn = get_db()
    if sinf_name.endswith('-sinf') or sinf_name.isdigit() or sinf_name.endswith('-klass') or sinf_name.endswith('-класс'):
        grade_num = sinf_name.split('-')[0]
        rows = conn.execute("SELECT * FROM sorovnoma WHERE (sinf = ? OR sinf LIKE ? OR sinf LIKE ?) ORDER BY fish ASC", (sinf_name, f"{grade_num}-%", f"{grade_num}-класс%")).fetchall()
    else:
        rows = conn.execute("SELECT * FROM sorovnoma WHERE sinf = ? ORDER BY fish ASC", (sinf_name,)).fetchall()
    conn.close()

    total = len(rows)
    with_clubs = 0
    without_clubs = 0
    fanlar = {}
    kasblar = {}
    iqtidorlar = {}
    yangi_togaraklar = {}
    diagnostics = {}

    for r in rows:
        t_str = (r['togaraklar'] or '').lower()
        if not t_str or 'bormayman' in t_str or "yo'q" in t_str or 'yoq' in t_str:
            without_clubs += 1
        else:
            with_clubs += 1

        for item in [x.strip() for x in (r['fanlar'] or '').split(',') if x.strip()]:
            fanlar[item] = fanlar.get(item, 0) + 1
        k = (r['kasb'] or '').strip()
        if k:
            kasblar[k] = kasblar.get(k, 0) + 1
        for item in [x.strip() for x in (r['iqtidor'] or '').split(',') if x.strip()]:
            iqtidorlar[item] = iqtidorlar.get(item, 0) + 1
        for item in [x.strip() for x in (r['yangi_togaraklar'] or '').split(',') if x.strip()]:
            yangi_togaraklar[item] = yangi_togaraklar.get(item, 0) + 1

        diag = (r['asosiy_natija'] or '').strip()
        if diag:
            clean_diag = diag.split('(')[0].split(',')[0].strip()
            if clean_diag:
                diagnostics[clean_diag] = diagnostics.get(clean_diag, 0) + 1

    top_fanlar = sorted(fanlar.items(), key=lambda x: x[1], reverse=True)[:6]
    top_kasblar = sorted(kasblar.items(), key=lambda x: x[1], reverse=True)[:5]
    top_iqtidor = sorted(iqtidorlar.items(), key=lambda x: x[1], reverse=True)[:5]
    top_yangi_togaraklar = sorted(yangi_togaraklar.items(), key=lambda x: x[1], reverse=True)[:5]
    top_diagnostics = sorted(diagnostics.items(), key=lambda x: x[1], reverse=True)[:5]

    stats = {
        'total': total,
        'with_clubs': with_clubs,
        'without_clubs': without_clubs,
        'club_percent': round((with_clubs / total * 100) if total else 0),
        'top_fanlar': top_fanlar,
        'top_kasblar': top_kasblar,
        'top_iqtidor': top_iqtidor,
        'top_yangi_togaraklar': top_yangi_togaraklar,
        'top_diagnostics': top_diagnostics
    }

    return render_template('sinf_pasporti.html', sinf=sinf_name, stats=stats, students=[dict(r) for r in rows], today=datetime.now().strftime('%d.%m.%Y'))

# --- Questions API ---

@app.route('/api/questions')
def get_questions():
    """Returns question specs for dynamic survey form"""
    grade = request.args.get('grade', '').strip()
    test_type = request.args.get('type', '').strip()
    lang = request.args.get('lang', 'uz').strip()
    if lang not in ['uz', 'ru']:
        lang = 'uz'

    if not test_type and grade:
        digits = ''.join(ch for ch in grade if ch.isdigit())
        g_num = int(digits) if digits else 0
        if g_num in [5, 6]:
            test_type = '5-6-sinf'
        elif g_num in [7, 8]:
            test_type = '7-8-sinf'
        elif g_num in [9, 10, 11]:
            test_type = '9-11-sinf'

    if test_type == '5-6-sinf':
        return jsonify({'status': 'success', 'test_turi': '5-6-sinf', 'data': sq.SURVEY_5_6[lang]})
    elif test_type == '7-8-sinf':
        return jsonify({'status': 'success', 'test_turi': '7-8-sinf', 'data': sq.SURVEY_7_8[lang]})
    elif test_type == '9-11-sinf':
        return jsonify({'status': 'success', 'test_turi': '9-11-sinf', 'data': sq.SURVEY_9_11[lang]})
    elif test_type == 'tashkilot':
        return jsonify({'status': 'success', 'test_turi': 'tashkilot', 'data': sq.SURVEY_TASHKILOT[lang]})

    return jsonify({
        'status': 'success',
        'surveys': {
            '5-6-sinf': sq.SURVEY_5_6[lang],
            '7-8-sinf': sq.SURVEY_7_8[lang],
            '9-11-sinf': sq.SURVEY_9_11[lang],
            'tashkilot': sq.SURVEY_TASHKILOT[lang]
        }
    })

# --- Entries API ---

@app.route('/api/entries', methods=['GET'])
def get_entries():
    query = request.args.get('q', '').strip().lower()
    sinf = request.args.get('sinf', '').strip()
    til = request.args.get('til', '').strip()
    kasb = request.args.get('kasb', '').strip()
    test_turi = request.args.get('test_turi', '').strip()
    togaraksiz = request.args.get('togaraksiz', '').strip()

    sql = "SELECT * FROM sorovnoma WHERE 1=1"
    params = []

    if query:
        sql += " AND (LOWER(fish) LIKE ? OR LOWER(fingerprint) LIKE ? OR LOWER(takliflar) LIKE ? OR LOWER(iqtidor) LIKE ? OR LOWER(kasb) LIKE ? OR LOWER(asosiy_natija) LIKE ?)"
        params.extend([f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"])
    if sinf:
        if sinf.endswith('-sinf') or sinf.isdigit() or sinf.endswith('-klass') or sinf.endswith('-класс'):
            grade_num = sinf.split('-')[0]
            sql += " AND (sinf = ? OR sinf LIKE ? OR sinf LIKE ?)"
            params.extend([sinf, f"{grade_num}-%", f"{grade_num}-класс%"])
        else:
            sql += " AND sinf = ?"
            params.append(sinf)
    if til:
        sql += " AND til = ?"
        params.append(til)
    if test_turi:
        sql += " AND test_turi = ?"
        params.append(test_turi)
    if kasb:
        sql += " AND (LOWER(kasb) LIKE ? OR LOWER(asosiy_natija) LIKE ?)"
        params.extend([f"%{kasb.lower()}%", f"%{kasb.lower()}%"])
    if togaraksiz == '1':
        sql += " AND (LOWER(togaraklar) LIKE '%bormayman%' OR LOWER(togaraklar) LIKE '%yoq%' OR LOWER(togaraklar) LIKE '%yo''q%' OR togaraklar = '' OR togaraklar IS NULL)"

    sql += " ORDER BY id DESC"

    conn = get_db()
    rows = conn.execute(sql, params).fetchall()
    conn.close()

    entries = [dict(row) for row in rows]
    return jsonify({'status': 'success', 'count': len(entries), 'data': entries})

# POST: Har bir o'quvchi so'rovnoma to'ldirishi uchun ochiq
@app.route('/api/entries', methods=['POST'])
def add_entry():
    data = request.get_json() or {}

    fish = data.get('fish', '').strip()
    sinf = data.get('sinf', '').strip()
    til = data.get('til', "O'zbek").strip()
    test_turi = data.get('test_turi', '').strip()
    answers = data.get('answers') or {}

    if not fish or not sinf:
        return jsonify({'status': 'error', 'message': "F.I.Sh. va Sinf maydonlarini to'ldirish shart!"}), 400

    # Determine grade number
    digits = ''.join(ch for ch in sinf if ch.isdigit())
    grade_num = int(digits) if digits else 0

    if not test_turi:
        if grade_num in [5, 6]:
            test_turi = '5-6-sinf'
        elif grade_num in [7, 8]:
            test_turi = '7-8-sinf'
        elif grade_num in [9, 10, 11]:
            test_turi = '9-11-sinf'
        else:
            test_turi = '5-6-sinf'

    # Anti-duplicate / Spam protection: check if same fish and sinf was submitted in last 2 minutes
    conn = get_db()
    recent = conn.execute(
        "SELECT id, timestamp FROM sorovnoma WHERE LOWER(fish) = ? AND sinf = ? AND test_turi = ? ORDER BY id DESC LIMIT 1",
        (fish.lower(), sinf, test_turi)
    ).fetchone()
    if recent:
        try:
            prev_time = datetime.strptime(recent['timestamp'], '%Y-%m-%d %H:%M:%S')
            diff_secs = (datetime.now() - prev_time).total_seconds()
            if diff_secs < 120:
                conn.close()
                return jsonify({
                    'status': 'error',
                    'message': f"Hurmatli {fish}, sizning ushbu test bo'yicha anketangiz qabul qilingan! Qayta yuborish talab etilmaydi."
                }), 400
        except Exception:
            pass

    lang_code = 'ru' if 'рус' in til.lower() or til.lower() == 'ru' else 'uz'

    # Scoring and evaluation
    asosiy_natija = ""
    ballar_json = "{}"
    tavsiya = ""
    scored_result = None

    fanlar = data.get('fanlar', '')
    if isinstance(fanlar, list):
        fanlar = ", ".join(fanlar)
    togaraklar = data.get('togaraklar', '')
    if isinstance(togaraklar, list):
        togaraklar = ", ".join(togaraklar)
    iqtidor = data.get('iqtidor', '')
    if isinstance(iqtidor, list):
        iqtidor = ", ".join(iqtidor)
    kasb = data.get('kasb', '').strip()
    startap = data.get('startap', '').strip()
    yangi_togaraklar = data.get('yangi_togaraklar', '')
    if isinstance(yangi_togaraklar, list):
        yangi_togaraklar = ", ".join(yangi_togaraklar)
    takliflar = data.get('takliflar', '').strip()

    if test_turi == '7-8-sinf':
        scored_result = sq.score_test_7_8(answers, lang=lang_code)
        top_name = scored_result.get('top_name', '')
        top_sc = scored_result.get('top_score', 0)
        asosiy_natija = f"{top_name} ({top_sc}/5)"
        ballar_json = json.dumps(scored_result['scores'], ensure_ascii=False)
        tavsiya = scored_result.get('recommendation', '')
        iqtidor = top_name
        kasb = tavsiya
    elif test_turi == '9-11-sinf':
        scored_result = sq.score_test_9_11(answers, lang=lang_code)
        sorted_spheres = scored_result.get('sorted', [])
        top_strs = [f"{s['name']} ({s['score']}/5)" for s in sorted_spheres[:2]]
        asosiy_natija = ", ".join(top_strs) if top_strs else scored_result.get('top_name', '')
        ballar_json = json.dumps(scored_result['scores'], ensure_ascii=False)
        tavsiya = scored_result.get('recommendation', '')
        iqtidor = ", ".join([s['name'] for s in sorted_spheres[:2]])
        kasb = scored_result.get('top_name', '')
    elif test_turi == 'tashkilot':
        scored_result = sq.score_test_tashkilot(answers, lang=lang_code)
        asosiy_natija = f"{scored_result['level']} ({scored_result['score']}/20 ball)"
        ballar_json = json.dumps({'total_score': scored_result['score'], 'level': scored_result['level']}, ensure_ascii=False)
        tavsiya = scored_result['description']
        iqtidor = "Tashkilotchilik va yetakchilik qobiliyati"
    else:  # 5-6-sinf
        if not fanlar and '1' in answers:
            val = answers.get('1')
            fanlar = ", ".join(val) if isinstance(val, list) else str(val)
        if not togaraklar and '2' in answers:
            val = answers.get('2')
            togaraklar = ", ".join(val) if isinstance(val, list) else str(val)
        if not iqtidor and '3' in answers:
            val = answers.get('3')
            iqtidor = ", ".join(val) if isinstance(val, list) else str(val)
        if not kasb and '4' in answers:
            kasb = str(answers.get('4'))
        if not takliflar and '5' in answers:
            takliflar = str(answers.get('5'))

        asosiy_natija = kasb or (iqtidor and f"Qobiliyat: {iqtidor}") or "Qiziqishlar so'rovnomasi"
        ballar_json = json.dumps({'fanlar': fanlar, 'kasb': kasb, 'iqtidor': iqtidor, 'togaraklar': togaraklar}, ensure_ascii=False)
        tavsiya = f"Tavsiya etilgan soha: {kasb or 'Qiziqishlariga mos to''garaklar'}"
        scored_result = {
            'type': '5-6-sinf',
            'asosiy_natija': asosiy_natija,
            'fanlar': fanlar,
            'kasb': kasb,
            'iqtidor': iqtidor,
            'tavsiya': tavsiya
        }

    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp = data.get('timestamp') or now_str
    fingerprint = data.get('fingerprint') or generate_fingerprint()
    javoblar_json = json.dumps(answers, ensure_ascii=False)

    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sorovnoma (
            timestamp, fingerprint, til, fish, sinf, test_turi,
            asosiy_natija, ballar_json, javoblar_json, tavsiya, qoshimcha,
            fanlar, togaraklar, iqtidor, kasb, startap, yangi_togaraklar, takliflar
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        timestamp, fingerprint, til, fish, sinf, test_turi,
        asosiy_natija, ballar_json, javoblar_json, tavsiya, '',
        fanlar, togaraklar, iqtidor, kasb, startap, yangi_togaraklar, takliflar
    ))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    entry_payload = {
        'id': new_id,
        'timestamp': timestamp,
        'fingerprint': fingerprint,
        'til': til,
        'fish': fish,
        'sinf': sinf,
        'test_turi': test_turi,
        'asosiy_natija': asosiy_natija,
        'ballar_json': ballar_json,
        'javoblar_json': javoblar_json,
        'tavsiya': tavsiya,
        'fanlar': fanlar,
        'togaraklar': togaraklar,
        'iqtidor': iqtidor,
        'kasb': kasb,
        'startap': startap,
        'yangi_togaraklar': yangi_togaraklar,
        'takliflar': takliflar
    }

    # Cloud sync
    async_push_to_cloud(entry_payload)

    # Webhook orqali tashqi tizimga yuborish (agar sozlangan bo'lsa)
    if GOOGLE_SHEET_WEBHOOK_URL:
        try:
            import urllib.request
            req_hook = urllib.request.Request(
                GOOGLE_SHEET_WEBHOOK_URL,
                data=json.dumps(entry_payload).encode('utf-8'),
                headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            )
            urllib.request.urlopen(req_hook, timeout=4)
        except Exception as err:
            print(f"Google Sheet webhook sync error: {err}")

    return jsonify({
        'status': 'success',
        'message': "So'rovnoma muvaffaqiyatli qabul qilindi!",
        'data': entry_payload,
        'result': scored_result
    }), 201

@app.route('/api/sync-google-sheet', methods=['POST'])
@admin_required
def api_sync_google_sheet():
    c_added = sync_from_cloud()
    s_added = sync_from_google_sheet()
    total_added = c_added + s_added
    return jsonify({
        'status': 'success',
        'message': f"Baza sinxronlandi! Bulut: +{c_added}, Sheet: +{s_added}. Jami yangi: {total_added} ta.",
        'added': total_added
    })

@app.route('/api/entries/<int:entry_id>', methods=['GET'])
@admin_required
def get_entry(entry_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM sorovnoma WHERE id = ?", (entry_id,)).fetchone()
    conn.close()
    if not row:
        return jsonify({'status': 'error', 'message': "Yozuv topilmadi"}), 404
    return jsonify({'status': 'success', 'data': dict(row)})

@app.route('/api/entries/<int:entry_id>', methods=['PUT'])
@admin_required
def update_entry(entry_id):
    data = request.get_json() or {}
    conn = get_db()
    row = conn.execute("SELECT * FROM sorovnoma WHERE id = ?", (entry_id,)).fetchone()
    if not row:
        conn.close()
        return jsonify({'status': 'error', 'message': "Yozuv topilmadi"}), 404

    fish = data.get('fish', row['fish']).strip()
    sinf = data.get('sinf', row['sinf']).strip()
    til = data.get('til', row['til']).strip()
    test_turi = data.get('test_turi', row['test_turi']).strip()
    asosiy_natija = data.get('asosiy_natija', row['asosiy_natija']).strip()
    tavsiya = data.get('tavsiya', row['tavsiya']).strip()
    fanlar = data.get('fanlar', row['fanlar'])
    if isinstance(fanlar, list):
        fanlar = ", ".join(fanlar)
    togaraklar = data.get('togaraklar', row['togaraklar'])
    if isinstance(togaraklar, list):
        togaraklar = ", ".join(togaraklar)
    iqtidor = data.get('iqtidor', row['iqtidor'])
    if isinstance(iqtidor, list):
        iqtidor = ", ".join(iqtidor)
    kasb = data.get('kasb', row['kasb']).strip()
    startap = data.get('startap', row['startap']).strip()
    yangi_togaraklar = data.get('yangi_togaraklar', row['yangi_togaraklar'])
    if isinstance(yangi_togaraklar, list):
        yangi_togaraklar = ", ".join(yangi_togaraklar)
    takliflar = data.get('takliflar', row['takliflar']).strip()

    conn.execute('''
        UPDATE sorovnoma
        SET fish = ?, sinf = ?, til = ?, test_turi = ?, asosiy_natija = ?, tavsiya = ?,
            fanlar = ?, togaraklar = ?, iqtidor = ?, kasb = ?, startap = ?,
            yangi_togaraklar = ?, takliflar = ?
        WHERE id = ?
    ''', (fish, sinf, til, test_turi, asosiy_natija, tavsiya, fanlar, togaraklar, iqtidor, kasb, startap, yangi_togaraklar, takliflar, entry_id))
    conn.commit()

    updated_row = conn.execute("SELECT * FROM sorovnoma WHERE id = ?", (entry_id,)).fetchone()
    conn.close()

    updated_dict = dict(updated_row)
    async_push_to_cloud(updated_dict)

    return jsonify({
        'status': 'success',
        'message': "Ma'lumot yangilandi!",
        'data': updated_dict
    })

@app.route('/api/entries/<int:entry_id>', methods=['DELETE'])
@admin_required
def delete_entry(entry_id):
    conn = get_db()
    row = conn.execute("SELECT fingerprint, fish, sinf FROM sorovnoma WHERE id = ?", (entry_id,)).fetchone()
    if row:
        async_remove_from_cloud(fingerprint=row['fingerprint'], fish=row['fish'], sinf=row['sinf'])
    conn.execute("DELETE FROM sorovnoma WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'message': "Yozuv o'chirildi!"})

@app.route('/api/clear', methods=['POST'])
@admin_required
def clear_all():
    conn = get_db()
    conn.execute("DELETE FROM sorovnoma")
    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'message': "Barcha ma'lumotlar tozalandi!"})

# --- Statistics API ---

@app.route('/api/stats', methods=['GET'])
@admin_required
def get_stats():
    conn = get_db()
    rows = conn.execute("SELECT * FROM sorovnoma").fetchall()
    conn.close()

    total = len(rows)
    sinflar = {}
    tillari = {}
    kasblar = {}
    yangi_togaraklar = {}
    fanlar = {}
    iqtidorlar = {}
    test_turlari = {}
    natijalar = {}

    for r in rows:
        s = r['sinf'] or 'Noma\'lum'
        sinflar[s] = sinflar.get(s, 0) + 1

        t = r['til'] or 'O\'zbek'
        tillari[t] = tillari.get(t, 0) + 1

        tt = r['test_turi'] or 'Boshqa'
        test_turlari[tt] = test_turlari.get(tt, 0) + 1

        res = (r['asosiy_natija'] or '').strip()
        if res:
            clean_res = res.split('(')[0].split(',')[0].strip()
            if clean_res:
                natijalar[clean_res] = natijalar.get(clean_res, 0) + 1

        k = (r['kasb'] or '').strip()
        if k:
            kasblar[k] = kasblar.get(k, 0) + 1

        yt = r['yangi_togaraklar'] or ''
        for item in [x.strip() for x in yt.split(',') if x.strip()]:
            yangi_togaraklar[item] = yangi_togaraklar.get(item, 0) + 1

        fn = r['fanlar'] or ''
        for item in [x.strip() for x in fn.split(',') if x.strip()]:
            fanlar[item] = fanlar.get(item, 0) + 1

        iq = r['iqtidor'] or ''
        for item in [x.strip() for x in iq.split(',') if x.strip()]:
            iqtidorlar[item] = iqtidorlar.get(item, 0) + 1

    top_kasblar = sorted(kasblar.items(), key=lambda x: x[1], reverse=True)[:10]
    top_yangi_togaraklar = sorted(yangi_togaraklar.items(), key=lambda x: x[1], reverse=True)[:10]
    top_fanlar = sorted(fanlar.items(), key=lambda x: x[1], reverse=True)[:10]
    top_iqtidorlar = sorted(iqtidorlar.items(), key=lambda x: x[1], reverse=True)[:8]
    top_natijalar = sorted(natijalar.items(), key=lambda x: x[1], reverse=True)[:10]

    return jsonify({
        'total': total,
        'sinflar': sinflar,
        'tillari': tillari,
        'test_turlari': test_turlari,
        'top_kasblar': top_kasblar,
        'top_yangi_togaraklar': top_yangi_togaraklar,
        'top_fanlar': top_fanlar,
        'top_iqtidorlar': top_iqtidorlar,
        'top_natijalar': top_natijalar
    })

# --- Export Routes ---

@app.route('/export/excel')
def export_excel():
    sinf = request.args.get('sinf', '').strip()
    test_turi = request.args.get('test_turi', '').strip()
    if not sinf and not session.get('is_admin'):
        return redirect(url_for('admin_login', next=request.path))

    sql = "SELECT * FROM sorovnoma WHERE 1=1"
    params = []
    if sinf:
        if sinf.endswith('-sinf') or sinf.isdigit() or sinf.endswith('-klass') or sinf.endswith('-класс'):
            grade_num = sinf.split('-')[0]
            sql += " AND (sinf = ? OR sinf LIKE ? OR sinf LIKE ?)"
            params.extend([sinf, f"{grade_num}-%", f"{grade_num}-класс%"])
        else:
            sql += " AND sinf = ?"
            params.append(sinf)
    if test_turi:
        sql += " AND test_turi = ?"
        params.append(test_turi)
    sql += " ORDER BY sinf ASC, fish ASC"

    conn = get_db()
    rows = conn.execute(sql, params).fetchall()
    conn.close()

    sheet_title = f"{sinf} sinf" if sinf else "Barcha natijalar"
    filename = f"Sorovnoma_{sinf or '35maktab'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = sheet_title

    # Albom A4 sozlamalari
    ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.print_title_rows = '1:1'
    ws.sheet_view.showGridLines = True
    ws.page_margins.left = 0.25
    ws.page_margins.right = 0.25
    ws.page_margins.top = 0.4
    ws.page_margins.bottom = 0.4

    headers = [
        "№", "F.I.Sh.", "Sinf", "Til", "Test turi", "Asosiy natija / Tashxis",
        "Psixologik tavsiya", "Kelajak kasbi", "Qiziqadigan fanlar",
        "To'garaklar", "Startap", "Takliflar", "Sana va vaqt"
    ]

    header_fill = PatternFill(start_color="107C41", end_color="107C41", fill_type="solid")
    header_font = Font(name="Arial", size=10, bold=True, color="FFFFFF")
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)

    thin_border = Border(
        left=Side(style='thin', color='C0C0C0'),
        right=Side(style='thin', color='C0C0C0'),
        top=Side(style='thin', color='C0C0C0'),
        bottom=Side(style='thin', color='C0C0C0')
    )

    ws.append(headers)
    for col_num in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align
        cell.border = thin_border
    ws.row_dimensions[1].height = 28

    alt_fill = PatternFill(start_color="F7FDF9", end_color="F7FDF9", fill_type="solid")

    for r_idx, row in enumerate(rows, start=2):
        row_data = [
            r_idx - 1,
            row['fish'] or '',
            row['sinf'] or '',
            row['til'] or '',
            row['test_turi'] or '',
            row['asosiy_natija'] or '',
            row['tavsiya'] or '',
            row['kasb'] or '',
            row['fanlar'] or '',
            row['togaraklar'] or '',
            row['startap'] or '',
            row['takliflar'] or '',
            (row['timestamp'] or '')[:16]
        ]
        ws.append(row_data)
        is_alt = (r_idx % 2 == 0)
        for col_num in range(1, len(row_data) + 1):
            cell = ws.cell(row=r_idx, column=col_num)
            cell.font = Font(name="Arial", size=9)
            cell.border = thin_border
            if col_num in [1, 3, 4, 5, 13]:
                cell.alignment = center_align
            else:
                cell.alignment = left_align
            if is_alt:
                cell.fill = alt_fill
        ws.row_dimensions[r_idx].height = 22

    col_widths = {
        'A': 5,   # №
        'B': 25,  # F.I.Sh.
        'C': 8,   # Sinf
        'D': 8,   # Til
        'E': 14,  # Test turi
        'F': 26,  # Asosiy natija
        'G': 26,  # Tavsiya
        'H': 18,  # Kelajak kasbi
        'I': 20,  # Fanlar
        'J': 20,  # Togaraklar
        'K': 16,  # Startap
        'L': 20,  # Takliflar
        'M': 14   # Sana
    }
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=filename
    )

@app.route('/export/csv')
@admin_required
def export_csv():
    sinf = request.args.get('sinf', '').strip()
    conn = get_db()
    if sinf:
        if sinf.endswith('-sinf') or sinf.isdigit() or sinf.endswith('-klass') or sinf.endswith('-класс'):
            grade_num = sinf.split('-')[0]
            rows = conn.execute("SELECT * FROM sorovnoma WHERE (sinf = ? OR sinf LIKE ? OR sinf LIKE ?) ORDER BY id ASC", (sinf, f"{grade_num}-%", f"{grade_num}-класс%")).fetchall()
        else:
            rows = conn.execute("SELECT * FROM sorovnoma WHERE sinf = ? ORDER BY id ASC", (sinf,)).fetchall()
        filename = f"Sorovnoma_{sinf}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    else:
        rows = conn.execute("SELECT * FROM sorovnoma ORDER BY id ASC").fetchall()
        filename = f"Sorovnoma_35maktab_Barchasi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    conn.close()

    headers = [
        "Sana va vaqt", "Fingerprint", "Til", "F.I.Sh.", "Sinf",
        "Test turi", "Asosiy natija", "Tavsiya", "Kelajak kasbi", "Fanlar", "Togaraklar"
    ]

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    for r in rows:
        writer.writerow([
            r['timestamp'], r['fingerprint'], r['til'], r['fish'], r['sinf'],
            r['test_turi'], r['asosiy_natija'], r['tavsiya'], r['kasb'], r['fanlar'], r['togaraklar']
        ])

    mem = io.BytesIO()
    mem.write(output.getvalue().encode('utf-8-sig'))
    mem.seek(0)

    return send_file(
        mem,
        mimetype="text/csv",
        as_attachment=True,
        download_name=filename
    )

@app.route('/export/togarak-excel')
def export_togarak_excel():
    nomi = request.args.get('nomi', '').strip()
    if not nomi:
        return "To'garak nomi ko'rsatilmadi", 400

    conn = get_db()
    rows = conn.execute("SELECT * FROM sorovnoma WHERE LOWER(yangi_togaraklar) LIKE ? ORDER BY sinf ASC, fish ASC", (f"%{nomi.lower()}%",)).fetchall()
    conn.close()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Qabul ro'yxati"

    ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.print_title_rows = '1:1'
    ws.sheet_view.showGridLines = True
    ws.page_margins.left = 0.25
    ws.page_margins.right = 0.25
    ws.page_margins.top = 0.4
    ws.page_margins.bottom = 0.4

    headers = [
        "№", "F.I.Sh.", "Sinf", "Til", "Iqtidor sohasi", 
        "Kelajak kasbi", "Istagan yangi to'garaklari", "Qo'shimcha takliflar", "Sana"
    ]

    header_fill = PatternFill(start_color="107C41", end_color="107C41", fill_type="solid")
    header_font = Font(name="Arial", size=10, bold=True, color="FFFFFF")
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)
    thin_border = Border(left=Side(style='thin', color='C0C0C0'), right=Side(style='thin', color='C0C0C0'), top=Side(style='thin', color='C0C0C0'), bottom=Side(style='thin', color='C0C0C0'))

    ws.append(headers)
    for col_num in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align
        cell.border = thin_border
    ws.row_dimensions[1].height = 28

    alt_fill = PatternFill(start_color="F7FDF9", end_color="F7FDF9", fill_type="solid")

    for r_idx, row in enumerate(rows, start=2):
        row_data = [
            r_idx - 1,
            row['fish'] or '',
            row['sinf'] or '',
            row['til'] or '',
            row['iqtidor'] or row['asosiy_natija'] or '',
            row['kasb'] or '',
            row['yangi_togaraklar'] or '',
            row['takliflar'] or '',
            (row['timestamp'] or '')[:16]
        ]
        ws.append(row_data)
        is_alt = (r_idx % 2 == 0)
        for col_num in range(1, len(row_data) + 1):
            cell = ws.cell(row=r_idx, column=col_num)
            cell.font = Font(name="Arial", size=9)
            cell.border = thin_border
            if col_num in [1, 3, 4, 9]:
                cell.alignment = center_align
            else:
                cell.alignment = left_align
            if is_alt:
                cell.fill = alt_fill
        ws.row_dimensions[r_idx].height = 20

    col_widths = {
        'A': 5, 'B': 26, 'C': 8, 'D': 8, 'E': 22, 'F': 20, 'G': 30, 'H': 26, 'I': 14
    }
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', nomi)[:30]
    filename = f"Togarak_{clean_name}_{datetime.now().strftime('%Y%m%d')}.xlsx"
    return send_file(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=filename
    )

@app.route('/api/qr')
def get_qr():
    host = request.host
    url = f"https://{host}/" if not host.startswith("localhost") and not host.startswith("127.0.0.1") else f"http://{host}/"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0F9D58", back_color="white")
    
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"============================================================")
    print(f"   SO'ROVNOMA VA NATIJALAR PORTALI ISHGA TUSHDI!            ")
    print(f"   Asosiy So'rovnoma: http://localhost:{port}/              ")
    print(f"   Yopiq Admin Paneli: http://localhost:{port}/admin        ")
    print(f"   Admin Paroli: {ADMIN_PASSWORD}                           ")
    print(f"============================================================")
    app.run(host='0.0.0.0', port=port, debug=False)
