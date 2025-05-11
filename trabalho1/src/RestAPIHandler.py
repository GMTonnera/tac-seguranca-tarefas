from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json
import bcrypt
import jwt
import time
import re
from dataclasses import asdict

from UserModel import UserModel
from AccountModel import AccountModel
from User import User

class RestAPIHandler(BaseHTTPRequestHandler):
    userModel = UserModel()
    accountModel = AccountModel()
    expTokenTime = 600
    secretKey = ""
    
    # perguntar ao gpto o que isso faz com detalhes 
    def do_GET(self):
        #
        match = re.match(r"^/contacartao/(\d+)/([a-zA-Z_]+)$", self.path)
        if match:
            account_id = match.group(1)
            method = match.group(2)
            token = self.headers.get('Authorization')[7:]
            
            try:
                decoded = jwt.decode(token, self.secretKey, algorithms=["HS256"])
                print("✅ Valid token:", decoded)
                
            except jwt.ExpiredSignatureError:
                print("❌ Token expired")
                self.send_response(401)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"Message": "Erro de autenticação!", "Error": "Token expirado."}).encode())
            except jwt.InvalidTokenError:
                print("❌ Invalid token")
                self.send_response(401)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"Message": "Erro de autenticação!", "Error": "Token inválido."}).encode())
            
            if method == 'info':
                if not account_id.isdigit():
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "ID mal informado!"}).encode())    
                
                info = self.accountModel.getInfo(int(account_id))
                if not info:
                    self.send_response(404)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Conta não encontrada!"}).encode())    
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"Info": asdict(info),"Message": "Token valido!", "Error": None}).encode())

            else:
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Not found"}).encode())
        else:
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Not found"}).encode())
    
    
    # perguntar ao gpto o que isso faz com detalhes
    def do_POST(self):       
        if self.path == "/auth":
            print("Autenticação em execução...")
            body = self.rfile.read(int(self.headers["Content-Length"])).decode()
            
            print("🔸 POST Path:", self.path)
            print("🔸 Headers:\n", self.headers)
            print("🔸 Body:", body)
            
            params = parse_qs(body)
            name = params.get("name", [""])[0]
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
                
                # gerando token JWT
                token = jwt.encode(payload, self.secretKey, algorithm="HS256")
                          
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
                
                
                
                
                
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"Error": "Not found"}).encode())
                
            
            