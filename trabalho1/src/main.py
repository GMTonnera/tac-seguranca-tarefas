import requests

from User import User

def main():
    response = requests.post('http://localhost:8000/auth', data={'name': 'bob.taylor','password': 'kW93jdQp'})
    token = response.headers.get('Authorization')[7:]
    user = response.json()['User']
    print(user)
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(f'http://localhost:8000/contacartao/{user['fk_account_id']}/info', headers=headers)
    info = response.json()['Info']
    
    print(info)
    
if __name__ == "__main__":
    main()