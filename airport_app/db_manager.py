import os
import sqlite3
import logging
import time


class DbManager:
    def __init__(self):
        print(f"I'm in init")
        time.sleep(4)
        db_path = os.getenv("AIRPORT_DJANGO_DB_PATH")
        if not os.path.isfile(db_path):
            print(f"No database file found at {db_path}")
            raise FileNotFoundError("Database file not found.")  # Raise an exception if the file does not exist
        self.db_filename = db_path
        print(f"Database file path: {self.db_filename}")  # Print the database path
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='airport_app_airplane';")
            result = cursor.fetchone()
            if result is None:
                logging.warning("The table 'airport_app_airplane' does not exist in the database.")

    def connect(self):
        print(f"I'm connecting")
        time.sleep(4)
        return sqlite3.connect(self.db_filename)

    def add_row(self, **incoming_data):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("PRAGMA table_info(airport_app_airplane);")
            result = cursor.fetchall()
            self.column_names = [column[1] for column in result]
            filtered_data = \
                {key.lower(): value for key, value in incoming_data.items() if key.lower() in self.column_names}
            columns = ', '.join(filtered_data.keys())
            placeholders = ', '.join('?' for _ in filtered_data)
            sql = f'INSERT INTO airport_app_airplane ({columns}) VALUES ({placeholders})'
            cursor.execute(sql, tuple(filtered_data.values()))
            print("I have added a row to database")
            connection.commit()
