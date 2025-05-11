import sqlite3
import bcrypt
import random

def userSeed():
    users = [
        (1, "alice.brown", "G8xT1eRz")  
        , (2, "bob.taylor", "kW93jdQp")  
        , (3, "carol.johnson", "Vn71CkL2")  
        , (4, "dave.martin", "r5QW8zEm")  
        , (5, "eve.anderson", "UJ3n2c9B")  
        , (6, "frank.white", "mX5Tz1Ap")  
        , (7, "grace.jackson", "Qz78VwH3")  
        , (8, "heidi.smith", "A6kLp9Jr")  
        , (9, "ivan.harris", "yN4E3gWt")  
        , (10, "judy.thomas", "Dq2RMfX7")
    ]
    try:
        with sqlite3.connect("trabalho1/src/database/trab1db.db") as conn:
            cursor = conn.cursor()
            for user in users:
                cursor.execute("INSERT INTO User (fk_account_id, name, password) VALUES (?, ?, ?)", (user[0], user[1], bcrypt.hashpw(user[2].encode('utf-8'), bcrypt.gensalt())))
            conn.commit()
    except sqlite3.IntegrityError:
        print("Banco de dados já inicializado!!!")
        
def accountSeed():
    accounts = [
        (1, '73492018')  
        , (2, '28510476')  
        , (3, '91034752')  
        , (4, '12869345')  
        , (5, '67021984')  
        , (6, '49372056')  
        , (7, '80213497')  
        , (8, '35980261')  
        , (9, '74629583')  
        , (10, '21840769')
    ]

    try:
        with sqlite3.connect("trabalho1/src/database/trab1db.db") as conn:
            cursor = conn.cursor()
            for account in accounts:
                balance = random.randint(0, 10000)
                limit = random.randint(5000, 10000)//100 * 100
                used_limit = random.randint(0, limit)
                
                cursor.execute("INSERT INTO Account (fk_user_id, cd_account, vr_account_balance, vr_account_limit, vr_account_limit_used) VALUES (?, ?, ?, ?, ?)", (account[0], account[1], balance, limit, used_limit))
            conn.commit()
    except sqlite3.IntegrityError:
        print("Banco de dados já inicializado!!!")