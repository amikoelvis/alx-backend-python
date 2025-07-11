import time
import sqlite3
import functools

# TTL in seconds (e.g., cache expires after 5 seconds)
CACHE_TTL = 5

# Cache format: {query: (result, timestamp)}
query_cache = {}

# Decorator for DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Cache decorator with TTL
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else None)
        current_time = time.time()

        if query in query_cache:
            result, timestamp = query_cache[query]
            if current_time - timestamp < CACHE_TTL:
                print("[CACHE HIT] Returning cached result.")
                return result
            else:
                print("[CACHE EXPIRED] Re-fetching and updating cache.")

        print("[CACHE MISS] Querying database and caching result.")
        time.sleep(2)  # Simulate a slow query
        result = func(conn, *args, **kwargs)
        query_cache[query] = (result, current_time)
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call — slow query + cache it
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# Second call — instant if within TTL
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)

# Wait for cache to expire and retry
print("\n Waiting for cache to expire...")
time.sleep(CACHE_TTL + 1)

users_after_expiry = fetch_users_with_cache(query="SELECT * FROM users")
print(users_after_expiry)
