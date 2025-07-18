import sqlite3
import functools
from datetime import datetime

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the SQL query from the function arguments (assuming 'query' is passed as a keyword argument or positional argument)
        query = kwargs.get('query') or (args[0] if args else None)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if query:
            print(f"[{timestamp}] Executing SQL query: {query}")
        else:
            print(f"[{timestamp}] No SQL query found to log.")
        return func(*args, **kwargs)
    return wrapper

# Function to execute a SQL query with logging
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# fetch users while logging the query
users = fetch_all_users("SELECT * FROM users")

# Print the fetched users
for user in users:
    print(user)