import psycopg2


def update_to_current_database(host, database, user, password):
    try:
        # Connect to the database using a context manager
        with psycopg2.connect(host=host, database=database, user=user, password=password) as conn:
            with conn.cursor() as cur:

                # Check if the city and user_data tables exist
                cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'city')")
                city_table_exists = cur.fetchone()[0]
                cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'user_data')")
                user_data_table_exists = cur.fetchone()[0]

                if not city_table_exists or not user_data_table_exists:
                    # One or both tables are missing, so create them
                    cur.execute("""CREATE TABLE city (
                                        city_id SERIAL PRIMARY KEY,
                                        city_name VARCHAR(255),
                                        lat FLOAT,
                                        lng FLOAT
                                    );
                                    CREATE TABLE USER_DATA (
                                        discord VARCHAR(255) UNIQUE,
                                        city_id INT REFERENCES city(city_id),
                                        stack VARCHAR(255) 
                                    );""")
                    print("Tables created successfully.")

                else:
                    # Both tables exist, so check if they have the correct columns
                    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'city'")
                    city_columns = set([row[0] for row in cur.fetchall()])
                    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'user_data'")
                    user_data_columns = set([row[0] for row in cur.fetchall()])

                    if city_columns != {'city_id', 'city_name', 'lat', 'lng'} or \
                            user_data_columns != {'discord', 'city_id', 'stack'}:
                        # One or more columns are missing, so drop and recreate both tables
                        cur.execute("DROP TABLE IF EXISTS user_data CASCADE")
                        cur.execute("DROP TABLE IF EXISTS city CASCADE")
                        cur.execute("""CREATE TABLE city (
                                            city_id SERIAL PRIMARY KEY,
                                            city_name VARCHAR(255),
                                            lat FLOAT,
                                            lng FLOAT
                                        );
                                        CREATE TABLE USER_DATA (
                                            discord VARCHAR(255) UNIQUE,
                                            city_id INT REFERENCES city(city_id),
                                            stack VARCHAR(255) 
                                        );""")
                        print("Tables recreated successfully.")

                    else:
                        # Tables and columns are correct, so nothing to do
                        print("Database is up to date.")

    except Exception as e:
        print("Error:", e)


update_to_current_database(database='z2j_map', user='bartoszkobylinski', password='bartoszkobylinski', host='localhost')
