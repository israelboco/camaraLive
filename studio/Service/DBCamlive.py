import sqlite3

class DatabaseManager:

    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_table(self):
        try:
            create_table_sql = """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER
                );
                """
            self.cursor.execute(create_table_sql)
        except sqlite3.Error as e:
            print(e)

    def insert_data(self, insert_sql, data):
        try:
            self.cursor.execute(insert_sql, data)
            self.connection.commit()
        except sqlite3.Error as e:
            print(e)

    def update_data(self, update_sql, data):
        try:
            self.cursor.execute(update_sql, data)
            self.connection.commit()
        except sqlite3.Error as e:
            print(e)

    def fetch_data(self, select_sql):
        try:
            self.cursor.execute(select_sql)
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(e)
            return None

    def close_connection(self):
        self.connection.close()

# if __name__ == "__main__":
#     db_manager = DatabaseManager("example.db")
    
#     create_table_sql = """
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY,
#         name TEXT NOT NULL,
#         age INTEGER
#     );
#     """
#     db_manager.create_table(create_table_sql)

#     insert_sql = "INSERT INTO users (name, age) VALUES (?, ?)"
#     db_manager.insert_data(insert_sql, ("Alice", 30))
#     db_manager.insert_data(insert_sql, ("Bob", 25))

#     update_sql = "UPDATE users SET age = ? WHERE name = ?"
#     db_manager.update_data(update_sql, (31, "Alice"))

#     select_sql = "SELECT * FROM users"
#     rows = db_manager.fetch_data(select_sql)
#     for row in rows:
#         print(row)

#     db_manager.close_connection()
