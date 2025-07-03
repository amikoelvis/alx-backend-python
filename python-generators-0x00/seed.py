import csv
import mysql.connector
import uuid
from mysql.connector import errorcode

DB_NAME = "ALX_prodev"

# 0. Connect to MySQL Server (no specific DB yet)
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password"  # replace with your actual root password
    )

# 1. Create the ALX_prodev DB if it doesn't exist
def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' ensured.")
    finally:
        cursor.close()

# 2. Connect to ALX_prodev DB
def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",  # replace with your actual root password
        database=DB_NAME
    )

# 3. Create user_data table if not exists
def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
        age DECIMAL(5, 2) NOT NULL,
        INDEX (user_id)
    )
    """
    cursor.execute(create_table_query)
    connection.commit()
    print("Table 'user_data' ensured.")
    cursor.close()

# 4. Insert data from CSV if not already present
def insert_data(connection, data):
    cursor = connection.cursor()
    check_query = "SELECT COUNT(*) FROM user_data WHERE email = %s"
    insert_query = "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"

    inserted_count = 0

    for row in data:
        cursor.execute(check_query, (row['email'],))
        if cursor.fetchone()[0] == 0:
            user_id = str(uuid.uuid4())
            cursor.execute(insert_query, (user_id, row['name'], row['email'], row['age']))
            inserted_count += 1

    connection.commit()
    print(f"{inserted_count} new records inserted.")
    cursor.close()

# 5. Read from CSV
def load_csv(filename="user_data.csv"):
    with open(filename, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

# Main Execution
if __name__ == "__main__":
    conn = connect_db()
    create_database(conn)
    conn.close()

    conn_prodev = connect_to_prodev()
    create_table(conn_prodev)

    data = load_csv()
    insert_data(conn_prodev, data)

    conn_prodev.close()
