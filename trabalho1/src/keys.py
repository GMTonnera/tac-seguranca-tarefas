def initPrivateKey():
    # carregar chave privada
    with open("trabalho1/src/keys/private.pem", "rb") as f:
        return f.read()

def initPublicKey():
    # carregar chave publica
    with open("trabalho1/src/keys/public.pem", "rb") as f:
        return f.read()