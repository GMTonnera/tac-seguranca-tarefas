import sqlite3

from seeds import accountSeed
from Info import Info
from Account import Account

class AccountModel:
    def initModel(self):
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
            conn.commit()
        accountSeed()
            
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
            cursor.execute("INSERT INTO Account (fk_user_id, cd_account, vr_account_balance, vr_account_limit, vr_account_limit_used) VALUES (?, ?, ?, ?, ?)", (user.name, user.password))
            conn.commit()
            return Account(cursor.lastrowid, account.fk_user_id, account.cd_account, account.vr_account_balance, account.vr_account_limit, account.vr_account_limit_used)
    