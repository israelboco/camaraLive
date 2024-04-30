import sqlite3

class Database(sqlite3):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.con = self.connect("camLive.db")

    
    def create_table(self):
        cur = self.con.cursor()
        cur.execute("""
            CREATE TABLE favorite(title, url)
        """)
    
    def get_data(self, table=None, id=None):
        new_cur = self.con.cursor()
        res = new_cur.execute(f"SELECT * FROM {table} ORDER BY score DESC")
        return res.fetchone()
        

    def set_data(self, table=None, values=None):
        cur = self.con.cursor()
        cur.execute(f"INSERT INTO {table} VALUES(?, ?, ?)", values)
        self.con.commit()
