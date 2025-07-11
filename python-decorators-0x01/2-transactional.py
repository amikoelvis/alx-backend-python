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

# Transaction management decorator
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit the transaction if successful
            return result
        except Exception as e:
            conn.rollback() # Rollback the transaction on error
            print(f"[TRANSACTION ERROR] Rolled back due to: {e}")
            raise # Re-raise the exception after rollback
    return wrapper

def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

update_user_email = with_db_connection(transactional(update_user_email))

# Update user's email with automatic transaction handling
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')