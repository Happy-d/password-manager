import base64
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import sqlite3
from random import randint


class Database:
    """
    Handler for sqlite functions.
    """
    def __init__(self, db_dir):
        self.conn = sqlite3.connect('{}app.db'.format(db_dir))
        self.c = self.conn.cursor()
        self.path = db_dir
        self.key = None     # Run the open function to get key
        self.f = None   # Run open function to use fernet

    def setup(self, theme, pin, b_path, b_tog):     # Run Once

        # Save path
        with open('{}path.txt'.format(self.path), 'w') as file:
            file.write(self.path)
            file.close()

        # Get pin as password
        pin_provided = pin
        password = pin_provided.encode()

        # Generate salt
        salt = os.urandom(16)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )

        key = base64.urlsafe_b64encode(kdf.derive(password))

        f = Fernet(key)

        encrypted_password = f.encrypt(password)

        # Creates config table
        self.c.execute('CREATE TABLE IF NOT EXISTS config(type TEXT, value TEXT)')

        # Creates passwords table
        self.c.execute('CREATE TABLE IF NOT EXISTS passwords(id INT, site TEXT, username TEXT, password TEXT)')

        self.c.execute('DELETE FROM config')
        self.c.execute('DELETE FROM passwords')

        # Enter info from setup into table
        self.c.execute("INSERT INTO config VALUES('theme', ?)", (theme,))
        self.c.execute("INSERT INTO config VALUES('salt', ?)", (salt,))
        self.c.execute("INSERT INTO config VALUES('pin', ?)", (encrypted_password,))
        self.c.execute("INSERT INTO config VALUES('backup', ?)", (b_tog,))
        self.c.execute("INSERT INTO config VALUES('b_path', ?)", (b_path,))
        self.c.execute("INSERT INTO config VALUES('hide', 'no')")
        self.c.execute("INSERT INTO config VALUES('setup', 'no')")
        self.conn.commit()

    def open(self, pin):
        # Get pin as password
        pin_provided = str(pin)
        password = pin_provided.encode()

        # Get Salt
        self.c.execute("SELECT * FROM config WHERE type='salt'")
        # print(self.c.fetchall())
        col_type, salt = self.c.fetchall()[0]

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )

        self.key = base64.urlsafe_b64encode(kdf.derive(password))

        self.f = Fernet(self.key)

        self.c.execute("SELECT * FROM config WHERE type='pin'")
        col_type, pin = self.c.fetchall()[0]

        try:
            self.f.decrypt(pin).decode()
            return 'Pin Successful'
        except cryptography.fernet.InvalidToken:
            return 'Invalid Pin'

    def get_theme(self):
        # Get theme
        self.c.execute("SELECT * FROM config WHERE type='theme'")
        col_type, theme = self.c.fetchall()[0]
        return theme

    def set_theme(self, theme):
        self.c.execute("DELETE FROM config WHERE type='theme'")
        self.c.execute("INSERT INTO config VALUES('theme', ?)", (theme,))
        self.conn.commit()

    def get_backup_tog(self):
        self.c.execute("SELECT * FROM config WHERE type='backup'")
        col_type, tog = self.c.fetchall()[0]
        return tog

    def set_backup_tog(self, tog):
        self.c.execute("DELETE FROM config WHERE type='backup'")
        self.c.execute("INSERT INTO config VALUES('backup', ?)", (tog,))
        self.conn.commit()

    def get_backup_path(self):
        self.c.execute("SELECT * FROM config WHERE type='b_path'")
        col_type, tog = self.c.fetchall()[0]
        return tog

    def set_backup_path(self, path):
        self.c.execute("DELETE FROM config WHERE type='b_path'")
        self.c.execute("INSERT INTO config VALUES('b_path', ?)", (path,))
        self.conn.commit()

    def get_hide_tog(self):
        self.c.execute("SELECT * FROM config WHERE type='hide'")
        col_type, tog = self.c.fetchall()[0]
        return tog

    def set_hide_tog(self, tog):
        self.c.execute("DELETE FROM config WHERE type='hide'")
        self.c.execute("INSERT INTO config VALUES('hide', ?)", (tog,))
        self.conn.commit()

    def get_setup_tog(self):
        self.c.execute("SELECT * FROM config WHERE type='setup'")
        try:
            col_type, tog = self.c.fetchall()[0]
        except IndexError:
            tog = 'yes'
        return tog

    def insert(self, site, username, password):    # MUST run open function to run this
        encrypted = self.f.encrypt(password.encode())

        self.c.execute("SELECT * FROM passwords")

        id_list = []

        for row in self.c.fetchall():
            id_list.append(row[0])

        new_id = randint(9999, 99999)
        while new_id in id_list:
            new_id = randint(9999, 99999)

        self.c.execute("INSERT INTO passwords VALUES(?, ?, ?, ?)", (new_id, site, username, encrypted,))
        self.conn.commit()

    def get_info(self):
        self.c.execute("SELECT * FROM passwords")

        db_list = []

        for row in self.c.fetchall():
            decrypted = self.f.decrypt(row[3]).decode()
            new_row = row[:3] + (decrypted,)
            db_list.append(new_row)

        return db_list

    def get_encrypted_info(self):
        self.c.execute("SELECT * FROM passwords")
        return self.c.fetchall()

    def delete(self, id_str):
        self.c.execute("DELETE FROM passwords WHERE id=?", (int(id_str),))
        self.conn.commit()

    def update(self, id_str, site, username, new_password):
        encrypted = self.f.encrypt(new_password.encode())

        self.c.execute("UPDATE passwords SET site=?, username=?, password=? WHERE id=?",
                       (site, username, encrypted, int(id_str),))

    def query(self, keyword_type, keyword):
        self.c.execute("SELECT * FROM passwords")

        db_list = []

        new_list = []

        for row in self.c.fetchall():
            decrypted = self.f.decrypt(row[3]).decode()
            new_row = row[:3] + (decrypted,)
            db_list.append(new_row)

        if keyword_type == 'Site':
            for row in db_list:
                if keyword in row[1]:
                    new_list.append(row)
        elif keyword_type == 'Username':
            for row in db_list:
                if keyword in row[2]:
                    new_list.append(row)
        elif keyword_type == 'Password':
            for row in db_list:
                if keyword in row[3]:
                    new_list.append(row)
        elif keyword_type == "All":
            for row in db_list:
                if keyword in row[1]:
                    new_list.append(row)
                elif keyword in row[2]:
                    new_list.append(row)
                elif keyword in row[3]:
                    new_list.append(row)

        elif keyword_type == '':
            new_list = db_list

        return new_list

    def encrypted_query(self, keyword_type, keyword):
        self.c.execute("SELECT * FROM passwords")

        db_list = self.c.fetchall()

        new_list = []

        if keyword_type == 'Site':
            for row in db_list:
                if keyword in row[1]:
                    new_list.append(row)
        elif keyword_type == 'Username':
            for row in db_list:
                if keyword in row[2]:
                    new_list.append(row)
        elif keyword_type == 'Password':
            for row in db_list:
                decrypted = self.f.decrypt(row[3]).decode()
                new_row = row[:3] + (decrypted,)
                if keyword in new_row[3]:
                    new_list.append(row)
        elif keyword_type == "All":
            for row in db_list:
                decrypted = self.f.decrypt(row[3]).decode()
                new_row = row[:3] + (decrypted,)
                if keyword in row[1]:
                    new_list.append(row)
                elif keyword in row[2]:
                    new_list.append(row)
                elif keyword in new_row[3]:
                    new_list.append(row)

        elif keyword_type == '':
            new_list = db_list

        return new_list
