import sys
from http.server import HTTPServer

from trabalho1.src.RestAPIHandlerSHA import RestAPIHandlerSHA
from trabalho1.src.RestAPIHandlerRSA import RestAPIHandlerRSA

def main(algorithm):
    server_address = ('', 8000)
    if algorithm == 'RSA':
        httpd = HTTPServer(server_address, RestAPIHandlerRSA)
    elif algorithm == 'SHA':
        httpd = HTTPServer(server_address, RestAPIHandlerSHA)
    else:
        print("Aalgoritmo especificado não é uma opção válida!\nOpções: RSA ou SHA.")
    
    print(f"Starting server at http://localhost:{8000}")
    httpd.serve_forever()
    
if __name__ == "__main__":
    if len(sys.args[1]) == 2:
        main(sys.args[1])
    else:
        print("Especifique o algoritmo de assinatura do Token!\nOpções: RSA ou SHA.")