import sqlite3

# Custom class-based context manager
class DatabaseConnection:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        return self.conn # Provides connection the with block
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()

# Use the context manager to fetch users
with DatabaseConnection('users.db') as conn:
    cursor = conn.cusor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    for row in results:
        print(row)