#!/usr/bin/env python3
import datetime
import json
from typing import List

from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import DeclarativeBase, relationship
from flask import g
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import yaml
import logging
import time



# Configure logging
logging.basicConfig(level=logging.INFO)

class Base(DeclarativeBase):
    pass
class Temperature(Base):
    """
        The Temperature class represents the temperature measurements in the database.

        Attributes:
            id (int): The primary key of the temperature measurement.
            temperature (float): The temperature value in degrees Celsius.
            timestamp (datetime.datetime): The timestamp of the temperature measurement.
            error (bool): A boolean indicating whether the temperature measurement was accurate.

        """
    __tablename__ = 'temperature'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    temperature = Column(Float)
    timestamp = Column(DateTime)
    error = Column(Boolean)

    def __repr__(self) -> str:
        return f'Pressure(id={self.id}, pressure={self.temperature}, timestamp={self.timestamp}, error={self.error})'

    def serialize(self):
        """
        Convert the Temperature object to a dictionary.
        """
        return {
            'id': self.id,
            'temperature': self.temperature,
            'timestamp': self.timestamp.isoformat(),
            'error': self.error
        }

class Pressure(Base):
    """
        The Pressure class represents the pressure measurements in the database.

        Attributes:
            id (int): The primary key of the pressure measurement.
            pressure (float): The pressure value in Pascals.
            timestamp (datetime.datetime): The timestamp of the pressure measurement.
            error (bool): A boolean indicating whether the pressure measurement was accurate.

        """
    __tablename__ = 'pressure'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    pressure = Column(Float)
    timestamp = Column(DateTime)
    error = Column(Boolean)

    def __repr__(self) -> str:
        return f'Pressure(id={self.id}, pressure={self.pressure}, timestamp={self.timestamp}, error={self.error})'

    def serialize(self):
        """
        Serialize the Temperature object to a dictionary.
        """
        return {
            'id': self.id,
            'temperature': self.pressure,
            'timestamp': self.timestamp.isoformat(),
            'error': self.error
        }




class Node_id(Base):
    """
        The Node_id class represents the node_id table in the database.

        Attributes:
            identifier (int): The primary key of the node_id.
            temp_id (str): The node_id of the temperature sensor.
            press_id (str): The node_id of the pressure sensor.

        """
    __tablename__ = 'node_id'
    __table_args__ = {'extend_existing': True}

    # Define columns using standard SQLAlchemy syntax
    identifier = Column(Integer, primary_key=True, autoincrement=True)
    temp_id = Column(String(30))
    press_id = Column(String(30))

    def __repr__(self) -> str:
        return f'Node_id(identifier={self.identifier}, temp_id={self.temp_id}, press_id={self.press_id})'



# Load configuration from config.yaml
def load_config():
    """
        Load the configuration from the config.yaml file.

        Returns:
            dict: The configuration parameters from the config.yaml file.
        """
    with open('db_config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config


def create_my_engine():
    #logging.info(f"Attendo 50 secondi")
    #time.sleep(50)
    try:
            # Attempt to connect to MySQL
            #engine = create_engine("mysql+mysqlconnector://root:root@mysql:3306/my_sensors_database")
            engine = create_engine("mysql+mysqlconnector://Matteo:Matteo2004x!@localhost:3306/my_sensors_database")
            if not database_exists(engine.url):
                create_database(engine.url)
                print(f"Created database")
                logging.info(f"Created database my_sensors_database")
            # Assicurati di avere importato Base dal tuo modulo SQLAlchemy
            Base.metadata.create_all(engine)
            logging.info(f"connect to database")
            return engine
    except DatabaseError as e:
        if "Can't connect to MySQL server" in str(e):
                logging.error(f"Can't connect to MySQL server")
        else:

         raise

def create_my_session(engine):
    session = Session(bind=engine)
    return session



def opcua_configurations_to_dict(opcua_configurations):
    return [
        {
            "addressOpcuaServer": opcua_config.address_opcua_server,
            "nodeConfigs": [
                {
                    "nodeId": node.nodeId,
                    "name": node.name,
                    "frequency": node.frequency
                }
                for node in opcua_config.node_configs
            ]
        }
        for opcua_config in opcua_configurations
    ]


def write_to_json_file(data, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def insert_temperature_data(session, temperature):
    """
        Add a new temperature measurement to the database.

        Args:
            session (Session): The SQLAlchemy session object.
            temperature (float): The temperature value in degrees Celsius.

        Returns:
            None: None.
        """
    if temperature > 265:
        error = True
    else:
        error = False
    timestamp = datetime.datetime.now()
    new_temperature = Temperature(temperature=temperature,timestamp=timestamp, error=error)
    session.add(new_temperature)
    session.commit()

def insert_pressure_data(session, pressure):
    """
        Add a new pressure measurement to the database.

        Args:
            session (Session): The SQLAlchemy session object.
            pressure (float): The pressure value in Pascals.

        Returns:
            None: None.
        """
    if pressure > 90:
        error = True
    else:
        error = False
    timestamp = datetime.datetime.now()
    new_pressure = Pressure(pressure=pressure,timestamp=timestamp, error=error)
    session.add(new_pressure)
    session.commit()

def read_data_temperature(session):
    data = session.query(Temperature).all()
    serialized_data = [temperature.serialize() for temperature in data]
    return serialized_data

def read_data_pressure(session):
    data = session.query(Pressure).all()
    serialized_data = [pressure.serialize() for pressure in data]
    return serialized_data

def insert_tem_node_id(session, temp_node_id):
    new_node_id = Node_id(temp_id=temp_node_id)
    session.add(new_node_id)
    session.commit()

def insert_press_node_id(session, press_node_id):
    new_node_id = Node_id(press_id=press_node_id)
    session.add(new_node_id)
    session.commit()

def insert_node_ids(session, temp_node_id, press_node_id):
    new_node_id = Node_id(temp_id=temp_node_id, press_id=press_node_id)
    session.add(new_node_id)
    session.commit()

def read_node_id_temperature(session):
    temp_node_id = session.query(Node_id.temp_id).all()
    return temp_node_id

def read_node_id_pressure(session):
    press_node_id = session.query(Node_id.press_id).all()
    return press_node_id

def db_close(session):
    print('closing database connection...')
    logging.info("Closing database connection")
    session.close()

def get_database():
    """
        Get the instance of the SQLAlchemy engine for the sensor data database.

        Returns:
            SQLAlchemy engine: The instance of the SQLAlchemy engine.
        """
    if not hasattr(g, 'my_sensor_database_db'):
        g.my_sensors_database_db = create_my_engine()
    return g.my_sensors_database_db



def read_timestamp_temperature(session):
    try:
        timestamps = session.query(Temperature.timestamp).all()
        timestamps = [value[0] for value in timestamps]

        temperatures = session.query(Temperature.temperature).all()
        temperatures = [value[0] for value in temperatures]

        return timestamps, temperatures
    except Exception as e:
        print("Error reading temperature timestamp values:", e)
        return [], []


def read_timestamp_pressure(session):
    try:
        timestamps = session.query(Pressure.timestamp).all()
        timestamps = [value[0] for value in timestamps]

        pressures = session.query(Pressure.pressure).all()
        pressures = [value[0] for value in pressures]

        return timestamps, pressures
    except Exception as e:
        print("Error reading pressure timestamp values:", e)
        return [], []


