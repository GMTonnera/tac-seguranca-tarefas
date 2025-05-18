import sqlite3
import random

from models.Info import Info
from models.Account import Account

class AccountModel:
    def __init__(self):
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
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Account (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        fk_user_id INTEGER NOT NULL UNIQUE,
                        cd_account TEXT NOT NULL UNIQUE,
                        vr_account_balance INTEGER NOT NULL,
                        vr_account_limit INTEGER NOT NULL,
                        vr_account_limit_used INTEGER NOT NULL
                    )
                """)
                
                for account in accounts:
                    balance = random.randint(0, 10000)
                    limit = random.randint(5000, 10000)//100 * 100
                    used_limit = random.randint(0, limit)
                    
                cursor.execute("INSERT INTO Account (fk_user_id, cd_account, vr_account_balance, vr_account_limit, vr_account_limit_used) VALUES (?, ?, ?, ?, ?)", (account[0], account[1], balance, limit, used_limit))    
                conn.commit()
                print("Tabela de contas inicializada!")
        
        except sqlite3.IntegrityError:
            print("Tabela de contas já existe!")

            
    def getAccountById(self, id):
        with sqlite3.connect("trabalho1/src/database/trab1db.db") as conn:
            cursor = conn.execute("SELECT * FROM Account WHERE id = ?", (id,))
            data = cursor.fetchone()
            return Account(data[0], data[1], data[2], data[3], data[4]) if data else None
    
    def getAccountByCode(self, account_code):
        with sqlite3.connect("trabalho1/src/database/trab1db.db") as conn:
            cursor = conn.execute("SELECT * FROM Account WHERE cd_account = ?", (account_code,))
            data = cursor.fetchone()
            return Account(data[0], data[1], data[2], data[3], data[4]) if data else None
        
    def getInfo(self, id):
        with sqlite3.connect("trabalho1/src/database/trab1db.db") as conn:
            cursor = conn.execute("SELECT User.name, Account.cd_account, Account.vr_account_balance, Account.vr_account_limit, Account.vr_account_limit_used FROM User LEFT JOIN Account ON User.id = Account.fk_user_id WHERE Account.id = (?)", (id,))
            data = cursor.fetchone()
            return Info(data[0], data[1], data[2], data[3], data[4])
        
    def createAccount(self, account):
        with sqlite3.connect("trabalho1/src/database/trab1db.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Account (fk_user_id, cd_account, vr_account_balance, vr_account_limit, vr_account_limit_used) VALUES (?, ?, ?, ?, ?)", (account.fk_user_id, account.cd_account, account.vr_account_balance, account.vr_account_limit, account.vr_account_limit_used))
            conn.commit()
            return Account(cursor.lastrowid, account.fk_user_id, account.cd_account, account.vr_account_balance, account.vr_account_limit, account.vr_account_limit_used)