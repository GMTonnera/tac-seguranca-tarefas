import sys
import ssl
from http.server import HTTPServer

from RestAPIHandlerSHA import RestAPIHandlerSHA
from RestAPIHandlerRSA import RestAPIHandlerRSA

def main(algorithm):
    server_address = ('', 8000)
    if algorithm == 'RSA':
        httpd = HTTPServer(server_address, RestAPIHandlerRSA)
    elif algorithm == 'SHA':
        httpd = HTTPServer(server_address, RestAPIHandlerSHA)
    else:
        print("Algoritmo especificado não é uma opção válida!\nOpções: RSA ou SHA.")
    
    # context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # context.load_cert_chain(certfile='trabalho1/src/keys/cert.pem', keyfile='trabalho1/src/keys/key.pem')
    # httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    
    
    print(f"Starting server at http://localhost:{8000}")
    httpd.serve_forever()
    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Especifique o algoritmo de assinatura do Token!\nOpções: RSA ou SHA.")