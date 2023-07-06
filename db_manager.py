import os
import sqlite3


class DbManager:
    def __init__(self, db_name=None):
        if db_name is None:
            current_dir = os.path.dirname(os.path.realpath(__file__))
            db_name = os.path.join(current_dir, "db.sqlite3")
            self.db_filename = db_name
        self.column_names = ['airplane_id', 'x', 'y', 'z', 'fuel', 'status']

    def connect(self):
        return sqlite3.connect(self.db_filename)

    def add_row(self, **incoming_data):
        with self.connect() as connection:
            cursor = connection.cursor()
            filtered_data = \
                {key.lower(): value for key, value in incoming_data.items() if key.lower() in self.column_names}
            columns = ', '.join(filtered_data.keys())
            placeholders = ', '.join('?' for _ in filtered_data)
            sql = f'INSERT INTO airport_app_airplane ({columns}) VALUES ({placeholders})'
            cursor.execute(sql, tuple(filtered_data.values()))
            connection.commit()
