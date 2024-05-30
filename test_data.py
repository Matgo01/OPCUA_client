import mysql.connector
from mysql.connector import Error
import random
import datetime

# Define the possible values for the last column
last_column_values = [
    'n=1,i=1000',
    'n=2,i=1002',
    'n=3,i=1003',
    'n=4,i=1004'
]

try:
    # Connect to MySQL database
    connection = mysql.connector.connect(
        host="192.168.25.211",  # Change this to just 'localhost'
        port="3306",  # Add port separately if needed
        user="root",
        password="admin",
        database="database_lastra_project"
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # Define the SQL INSERT statement
        sql_insert_query = "INSERT INTO pressure (pressure, timestamp, error, node_id) VALUES (%s, %s, %s, %s)"

        # Calculate the start and end dates
        start_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = datetime.datetime(2026, 12, 31, 23, 59, 59)

        # Calculate the total number of seconds in the range
        total_seconds = int((end_date - start_date).total_seconds())

        # Calculate the interval in seconds between each data point
        interval_seconds = total_seconds // 100000

        # Generate 100,000 data points
        for i in range(100000):
            # Random values for the first three columns
            value1 = random.uniform(60, 120)
            # Increment the timestamp by the calculated interval
            value2 = start_date + datetime.timedelta(seconds=(i * interval_seconds))
            value3 = random.choice([True, False])
            # Random value for the last column
            last_column_value = random.choice(last_column_values)
            data = (value1, value2.strftime('%Y-%m-%d %H:%M:%S'), value3, last_column_value)

            cursor.execute(sql_insert_query, data)

        # Commit changes to the database
        connection.commit()
        print("Data inserted successfully")

except Error as e:
    print(f"Error inserting data: {e}")

finally:
    # Close the database connection
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
