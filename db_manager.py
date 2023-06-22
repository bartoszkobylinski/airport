import os
import sqlite3
import time


class DbManager:
    def __init__(self, db_name):
        self.db_filename = db_name + ".db"
        if not os.path.exists(self.db_filename):
            self.create_database()
        self.column_names = ['airplane_id', 'x', 'y', 'z', 'fuel', 'status']

    def connect(self):
        return sqlite3.connect(self.db_filename)

    def create_database(self):
        connection = self.connect()
        try:
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE airplanes
                            ( id INTEGER PRIMARY KEY AUTOINCREMENT,
                            airplane_id TEXT,
                            x REAL,
                            y REAL,
                            z REAL,
                            fuel INTEGER,
                            status TEXT CHECK(status IN ('WAITING',
                                                           'APPROACHING',
                                                           'DESCENDING',
                                                           'LANDED',
                                                           'CRASHED')))''')
            connection.commit()
        except Exception as e:
            print(f"Exception when creating table: {e}")
        finally:
            connection.close()

    def add_row(self, **incoming_data):
        with self.connect() as connection:
            cursor = connection.cursor()
            print(incoming_data.items())
            a = "airplane_ID"
            print(f"a: {a} i po: {a.lower()}")
            filtered_data = \
                {key.lower(): value for key, value in incoming_data.items() if key.lower() in self.column_names}
            print(filtered_data)
            columns = ', '.join(filtered_data.keys())
            print(columns)
            placeholders = ', '.join('?' for _ in filtered_data)
            print(placeholders)
            sql = f'INSERT INTO airplanes ({columns}) VALUES ({placeholders})'
            cursor.execute(sql, tuple(filtered_data.values()))
            connection.commit()
