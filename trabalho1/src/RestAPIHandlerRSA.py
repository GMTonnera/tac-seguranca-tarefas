from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json
import bcrypt
import jwt
import time
import re
from dataclasses import asdict

from trabalho1.src.models.UserModel import UserModel
from trabalho1.src.models.AccountModel import AccountModel
from trabalho1.src.dataclasses.User import User

class RestAPIHandlerRSA(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        # inicializando interfaces de comunicação com o banco de dados
        self.userModel = UserModel()
        self.accountModel = AccountModel()
        
        # tempo de expiracao do token
        self.expTokenTime = 600
        
        # inicializacao das chaves
        self.privateKey = None
        self.publicKey = None    
        self.initKeys()
    
    
    def do_GET(self):
        # aplicar regex na URL (/contacartao/{id da conta}/{metodo})
        match = re.match(r"^/contacartao/(\d+)/([a-zA-Z_]+)$", self.path)
        if match:
            # pegando o id da conta
            account_id = match.group(1)
            # pegando o metodo
            method = match.group(2)
            # pegando o token
            token = self.headers.get('Authorization')[7:]
            
            # validar o token
            try:
                # decodificando o token via RSA
                decoded = jwt.decode(token, self.publicKey, algorithms=["RS256"])
                print("✅ Valid token:", decoded)
            
            # token expirado
            except jwt.ExpiredSignatureError:
                print("❌ Token expired")
                self.send_response(401)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"Message": "Erro de autenticação!", "Error": "Token expirado."}).encode())
            
            # token invalido
            except jwt.InvalidTokenError:
                print("❌ Invalid token")
                self.send_response(401)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"Message": "Erro de autenticação!", "Error": "Token inválido."}).encode())
            
            # verificar o metodo relacionado com a contal cartao
            if method == 'info':
                # verificar se o id da conta especificado é um valor numerico
                if not account_id.isdigit():
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"Message": "Erro de parâmetro.","Error": "ID mal informado!"}).encode())    
                
                # verificar se existe uma conta com o id especificado
                info = self.accountModel.getInfo(int(account_id))
                if not info:
                    # se nao foi encontrada
                    self.send_response(404)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"Message": "Erro de parâmetro.", "Error": "Conta não encontrada!"}).encode())    
                
                # se foi encontrado, enviar informacoes da conta
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"Info": asdict(info),"Message": "Token valido!", "Error": None}).encode())

            # se o metodo foi mal especificado
            else:
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
            self.wfile.write(json.dumps({"Message": "Erro na URL.", "Error": "Not found"}).encode())
        
        # se a url nao segue o padrao
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"Message": "Erro na URL.", "Error": "Not found"}).encode())

    
    def do_POST(self):       
        # verificar se a url segue o padrao da rota de autenticacao
        if self.path == "/auth":
            print("Autenticação em execução...")
            body = self.rfile.read(int(self.headers["Content-Length"])).decode()
            
            print("🔸 POST Path:", self.path)
            print("🔸 Headers:\n", self.headers)
            print("🔸 Body:", body)
            
            params = parse_qs(body)
            # nome do usuario
            name = params.get("name", [""])[0]
            # senha do usuario
            password = params.get("password", [""])[0]
            
            print(f"Usuário {name} está tentando se autenticar...")
            
            # procurar usuario no banco de dados
            user = self.userModel.getUserByName(name)
            
            # se o usuário foi encontrado no banco de dados e o hash da senha bate com o hash armazenado no banco de dados
            if user and bcrypt.checkpw(password.encode(), user.password):
                print("Autenticação realizada com sucesso! Gerando token JWT...")
                # gerando payload do token
                payload = {
                    "sub": name,
                    "iat": int(time.time()),
                    "exp": int(time.time() + 600)
                }
                
                # gerando token JWT e assinando por RSA
                token = jwt.encode(payload, self.privateKey, algorithm="RS256")          

                # enviando o token no cabecalho
                self.send_response(200)
                self.send_header("Authorization", f"Bearer {token}")
                self.end_headers()
                self.wfile.write(json.dumps({"User": asdict(User(user.id, user.fk_account_id, user.name, None)),"Message": "Autenticação efetuada com sucesso!", "Error": None}).encode())
                
            
            # se o usuario nao foi encontrado ou a senha estiver errada
            else:
                # enviar a resposta com erro 401
                print("Erro na autenticação")
                self.send_response(401)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"Message": "Autenticação não realizada!", "Error": "Usuário ou senha inválidos"}).encode())
        
        # se nao segue o padrao, retornar 404        
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"Message": "Erro na URL.", "Error": "Not found"}).encode())
                
    def initKeys(self):
        # carregar as chaves
        with open("src/keys/private.pem", "rb") as f:
            self.privateKey = f.read()

        with open("src/keys/public.pem", "rb") as f:
            self.public_key = f.read()

            