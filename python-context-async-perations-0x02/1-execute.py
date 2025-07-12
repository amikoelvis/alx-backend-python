import sqlite3

class ExecuteQuery:
    def __init__(self, db_file, query, params=None):
        self.db_file = db_file
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall() 
        return self.results # Returned to the with-block
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()

# Example usage with query and parameter
query = "SELECT * FROM users WHERE age > ?"
param = (25,)

with ExecuteQuery('users.db', query, param) as results:
    for row in results:
        print(row)