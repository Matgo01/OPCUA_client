import mysql.connector
from mysql.connector import Error
import random
import datetime

# Define the possible values for the last column
last_column_values = [
    ('n=1,i=1000'),
    ('n=2,i=1002'),
    ('n=3,i=1003'),
    ('n=4,i=1004')
]

try:
    # Connect to MySQL database
    connection = mysql.connector.connect(
        host="localhost",  # Change this to just 'localhost'
        port="3306",  # Add port separately if needed
        user="Matthew",
        password="Matteo2004x!",
        database="database_lastra_project"
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # Define the SQL INSERT statement
        sql_insert_query = "INSERT INTO pressure (pressure, timestamp, error, node_id) VALUES (%s, %s, %s, %s)"

        # Start from 2024-05-30 00:00:00
        start_date = datetime.datetime(2024, 5, 30, 0, 0, 0)
        #current_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # Generate data for each hour, 10 data points per hour
        for day in range(365):  # Iterate for 365 days
            for hour in range(24):  # Iterate for each hour of the day
                for _ in range(10):  # Insert 10 data points for each hour
                    value1 = random.uniform(60, 120)
                    value2 = start_date + datetime.timedelta(days=day, hours=hour)
                    value3 = random.choice([True, False])
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