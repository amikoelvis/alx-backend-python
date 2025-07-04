import mysql.connector

def stream_user_ages():
    """
    Generator that yields user ages one by one from the user_data table.
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="ALX_prodev"
    )
    cursor = connection.cursor()

    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:  # Loop 1
        yield float(age)

    cursor.close()
    connection.close()


def compute_average_age():
    """
    Uses the stream_user_ages generator to calculate average age without loading all data.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():  # Loop 2
        total_age += age
        count += 1

    average = total_age / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")
