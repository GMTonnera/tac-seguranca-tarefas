from http.server import HTTPServer

from RestAPIHandler import RestAPIHandler
from UserModel import UserModel
from AccountModel import AccountModel

def main():
    UserModel().initModel()
    AccountModel().initModel()
    print("Banco de dados inicializado!")
    
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RestAPIHandler)
    print(f"Starting server at http://localhost:{8000}")
    httpd.serve_forever()

    
if __name__ == "__main__":
    main()