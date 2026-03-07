import requests

s = requests.Session()
r = s.get('http://127.0.0.1:8000/login/')
csrf = [line for line in r.text.split('\n') if 'csrfmiddlewaretoken' in line][0].split('value="')[1].split('"')[0]
s.post('http://127.0.0.1:8000/login/', data={'username': 'testuser', 'password': 'testpass123', 'csrfmiddlewaretoken': csrf})
r2 = s.get('http://127.0.0.1:8000/dashboard/')
print('CSRF in dashboard:', 'csrfmiddlewaretoken' in r2.text)
print('Dashboard length:', len(r2.text))
if 'csrfmiddlewaretoken' in r2.text:
    print('\nDashboard has CSRF token - logout form is present')
else:
    print('\nDashboard missing CSRF token - logout form not updated')
