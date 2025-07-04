import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that yields rows from user_data table in batches of given size.
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch  # yields one batch (list of rows) at a time

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """
    Processes each batch and yields users over age 25
    """
    for batch in stream_users_in_batches(batch_size):       # loop 1
        for user in batch:                                  # loop 2
            if float(user['age']) > 25:
                yield user                                  # generator yield
        return