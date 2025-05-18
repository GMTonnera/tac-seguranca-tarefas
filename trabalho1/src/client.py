import requests

from models.User import User

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
            
            response = requests.post('https://localhost:8000/auth', data={'name': name,'password': password}, verify='trabalho1/src/keys/cert.pem')
            
            if response.status_code == 200:
                token = response.headers.get('Authorization')[7:]
                user = response.json()['User']
                print("Autenticação realizada com sucesso!")
            else:
                print(">>>", response.json()['Message'], response.json()['Error'])
            
        elif code == '2':
            if not token:
                print(">>> É necessário se autenticar para acessar as informações da conta!")
            headers = {
                "Authorization": f"Bearer {token}"
            }
            response = requests.get(f'https://localhost:8000/contacartao/{user['fk_account_id']}/info', headers=headers, verify='trabalho1/src/keys/cert.pem')
            if response.status_code == 200:
                print(">>> Informações da Conta:")
                for k, v in response.json()['Info'].items():
                    print(f"\t- {k}: {v}") 
            else:
                print(">>>", response.json()['Message'], response.json()['Error'])

        elif code == '3':
            break
        
        else:
            print(">>> Vamo colocar uma opção válida???")
    
if __name__ == "__main__":
    main()