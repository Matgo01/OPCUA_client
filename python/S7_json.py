import mysql.connector
import json



# Connect to MySQL database
connection = mysql.connector.connect(
    host="localhost",  # Change this to just 'localhost'
    port="3306",       # Add port separately if needed
    user="Matteo",
    password="Matteo2004x!",
    database="my_sensors_database"
)
cursor = connection.cursor()

# Execute SQL query to fetch data
query = "SELECT * FROM S7_configuration"
cursor.execute(query)

# Fetch all rows from the result
rows = cursor.fetchall()

# Convert data into a list of dictionaries
data = []
for row in rows:
    config_data = {
        'id': row[0],
        'addressS7Server': row[1],
        'rack': row[2],
        'slot': row[3],
        'dbNumber': row[4],
        'nodeConfigs': []  # Initialize nodeConfigs list
    }
    # Fetch nodeConfigs for current configuration
    node_query = "SELECT  name, frequency FROM s7configuration_node_config_params; WHERE s7configuration_id = %s"
    cursor.execute(node_query, (row[0],))  # Pass configuration id as parameter
    nodes = cursor.fetchall()
    for node in nodes:
        config_data['nodeConfigs'].append({
            'nodeId': node[0],
            'name': node[0],
            'frequency': node[1]
        })
    data.append(config_data)

# Write JSON data into a file
with open('s7_configurations.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

# Close cursor and connection
cursor.close()
connection.close()

print("JSON file created successfully.")