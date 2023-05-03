import sqlite3
import os

class DB_Manager:

    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        if not os.path.exists(self.db_name):
            self.create_database()

    def create_database(self):
        self.connection = sqlite3.connect(self.db_name)
        self.create_table()
        self.connection.close()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE airplanes
                        (airplane_id TEXT PRIMARY KEY,
                        x REAL,
                        y REAL,
                        z REAL,
                        fuel INTEGER,
                        status TEXT CHECK(status IN ('accepted for approach',
                                                       'rejected for approach',
                                                       'approaching',
                                                       'inbounding to runway',
                                                       'landed',
                                                       'collided')))''')
        self.connection.commit()


