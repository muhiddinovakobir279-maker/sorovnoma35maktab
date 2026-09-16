import os
import sys

from app import app, ADMIN_PASSWORD

client = app.test_client()

# 1. Check root page returns the survey form
res_root = client.get('/')
assert res_root.status_code == 200
assert 'O\'quvchilarning qiziqish va iqtidorini aniqlash so\'rovnomasi'.encode('utf-8') in res_root.data
print("Test 1: Root / displays survey form directly: PASSED")

# 2. Check /admin redirects to /admin/login when not authenticated
res_admin_anon = client.get('/admin')
assert res_admin_anon.status_code == 302
assert '/admin/login' in res_admin_anon.location
print("Test 2: /admin redirects anonymous visitors to login: PASSED")

# 3. Check /api/entries without authentication returns 401
res_api_anon = client.get('/api/entries')
assert res_api_anon.status_code == 401
print("Test 3: /api/entries protected from public view: PASSED")

# 4. Check public POST to /api/entries works (students submitting survey)
payload = {
    'fish': 'Alisher Navoiy',
    'sinf': '11-sinf',
    'til': "O'zbek",
    'kasb': 'Shoir va Mutafakkir'
}
res_post = client.post('/api/entries', json=payload)
assert res_post.status_code == 201
entry_id = res_post.get_json()['data']['id']
print("Test 4: Public survey submission works: PASSED")

# 5. Check login with wrong password
res_bad_login = client.post('/admin/login', data={'password': 'wrongpassword'})
assert b"noto&#39;g&#39;ri" in res_bad_login.data
print("Test 5: Wrong password rejected: PASSED")

# 6. Check login with correct password
with client.session_transaction() as sess:
    sess['is_admin'] = True

res_admin_auth = client.get('/admin')
assert res_admin_auth.status_code == 200
assert b'Sorovnoma Natijalar' in res_admin_auth.data
print("Test 6: Authenticated admin can view table: PASSED")

# 7. Check authenticated admin can access API and delete test entry
res_api_auth = client.get('/api/entries')
assert res_api_auth.status_code == 200
res_del = client.delete(f'/api/entries/{entry_id}')
assert res_del.status_code == 200
print("Test 7: Authenticated admin API CRUD and cleanup: PASSED")

print("\n>>> ALL SECURITY AND SURVEY TESTS PASSED! <<<")
