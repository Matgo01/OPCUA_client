from sqlalchemy import create_engine, text
import yaml
def load_config():
    """
        Load the configuration from the config.yaml file.

        Returns:
            dict: The configuration parameters from the config.yaml file.
        """
    with open('db_config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config
def main():
    db_config = load_config()['database']
    connection_string = f"mysql+mysqlconnector://{db_config['username']}:{db_config['password']}@{db_config['hostname']}/{db_config['database_name']}"
    engine = create_engine(connection_string)
    # Establish a connection to the MySQL server
    connection = engine.connect()
    # Execute SQL queries to create database if not exists and switch to it
    create_database_query = text("CREATE DATABASE IF NOT EXISTS my_sensors_database DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;")
    use_database_query = text("USE my_sensors_database;")
    connection.execute(create_database_query)
    connection.execute(use_database_query)
    # Close the connection
    connection.close()

# Call the main function
if __name__ == "__main__":
    main()


