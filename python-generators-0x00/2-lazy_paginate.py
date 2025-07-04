import mysql.connector

def paginate_users(page_size, offset):
    """
    Fetch one page of users starting from a specific offset.
    Returns a list of rows (or an empty list if done).
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


def lazy_paginate(page_size):
    """
    Generator that lazily loads and yields pages of users.
    Only fetches the next page when needed.
    """
    offset = 0
    while True:  # Only one loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page  # Yield a full page (list of users)
        offset += page_size
