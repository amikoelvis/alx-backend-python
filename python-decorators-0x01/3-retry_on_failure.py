import re
import time
import sqlite3
import functools

# Decorator to handle DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            # Pass the connection as the first argument
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# retry_on_failure decorator
def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    print(f"[RETRY] Attempt {attempt} of {retries}")
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"[ERROR] {e} — Retrying in {delay} second(s)...")
                    time.sleep(delay)
            print("[FAILURE] Max retries reached. Raising the last exception.")
            raise last_exception
        return wrapper
    
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")  # Modify this to simulate failure if testing retry
    return cursor.fetchall()

# Attempt to fetch users with automatic retry
users = fetch_users_with_retry()
print(users)