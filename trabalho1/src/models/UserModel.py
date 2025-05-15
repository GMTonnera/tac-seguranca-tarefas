import sqlite3
import bcrypt

from trabalho1.src.dataclasses.User import User

class UserModel:
    def __init__(self):
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
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS User (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        fk_account_id INTEGER NOT NULL UNIQUE,
                        name TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL
                    )
                """)
    
                for user in users:
                    cursor.execute("INSERT INTO User (fk_account_id, name, password) VALUES (?, ?, ?)", (user[0], user[1], bcrypt.hashpw(user[2].encode('utf-8'), bcrypt.gensalt())))
                conn.commit()
                print("Tabela de usuários inicializada!")
        except sqlite3.IntegrityError:
            print("Tabela de usuários já existe!")
    
    def getUserById(self, id):
        with sqlite3.connect("trabalho1/src/database/trab1db.db") as conn:
            cursor = conn.execute("SELECT * FROM User WHERE id = ?", (id,))
            data = cursor.fetchone()
            return User(data[0], data[1], data[2], None) if data else None
    
    def getUserByName(self, name):
        with sqlite3.connect("trabalho1/src/database/trab1db.db") as conn:
            cursor = conn.execute("SELECT * FROM User WHERE name = ?", (name,))
            data = cursor.fetchone()
            print(data)
            return User(data[0], data[1], data[2], data[3]) if data else None
    
    def createUser(self, user):
        with sqlite3.connect("trabalho1/src/database/trab1db.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO User (fk_account_id, name, password) VALUES (?, ?, ?)", (user.fk_account_id, user.name, user.password))
            conn.commit()
            return User(cursor.lastrowid, user.fk_account_id, user.name, None)
    