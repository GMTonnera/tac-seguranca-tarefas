import requests

from trabalho1.src.dataclasses.User import User

def main():
    token = None
    user = None
    
    while True:
        print(
"""
+----------------------------------------------------------------+
|   TRABALHO 1 - TAC                                             |
|                                                                |
|                                                                |
|   1) Autenticação                                              |
|   2) Informações da Conta                                      |
|   3) Sair                                                      |
|                                                                |
+----------------------------------------------------------------+
"""
        )
        code = input(">>> ")
        if code == '1':
            print(">>> Digite as cerdenciais:")
            name = input("      Nome: ")
            password = input("      Senha: ")
            response = requests.post('http://localhost:8000/auth', data={'name': name,'password': password})
            if response.status_code == 200:
                token = response.headers.get('Authorization')[7:]
                user = response.json()['User']
            
            print(response.json()['Message'])
            print(response.json()['Error'])
        
        elif code == '2':
            print(user)
            headers = {
                "Authorization": f"Bearer {token}"
            }
            response = requests.get(f'http://localhost:8000/contacartao/{user['fk_account_id']}/info', headers=headers)
            if response.status_code == 200:
                print(">>> " + response.json()['Info'])
            
            print(">>> " + response.json()['Message'] + response.json()['Error'])
        

        elif code == '3':
            break
        
        else:
            print(">>> Vamo colocar uma opção válida???")
    
if __name__ == "__main__":
    main()