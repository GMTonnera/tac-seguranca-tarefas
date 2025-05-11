import sqlite3

from User import User
from seeds import userSeed

class UserModel:
    def initModel(self):
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
            conn.commit()
        print("model user criada")
        userSeed()
            
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
    