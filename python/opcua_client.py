#!/usr/bin/env python3
import asyncio
from asyncua import Client
from sql_alchemy_db import create_my_engine, create_my_session, insert_temperature_data, insert_pressure_data, db_close
import yaml
from Event import event
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

async def read_temperature(temperature_node, session,t_event:event, frquence:int):
    """
        This function reads the temperature value from the temperature_node and prints it to the console.
        The temperature value is also inserted into the database using the session object.
        The t_event object is used to set the alarm state based on the temperature value.
        The function then sleeps for 60 seconds before repeating.
        """
    while True:
        temperature_value = await temperature_node.read_value()
        print(f"Temperature: {temperature_value}")
        logging.info(f"Temperature: {temperature_value}")
        insert_temperature_data(session, temperature_value)
        t_event.notify_alarm_state(frquence)
        t_event.set_alarm_state(temperature_value)
        await asyncio.sleep(frquence)  # Read temperature every 60 seconds

async def read_pressure(pressure_node, session, p_event:event, frequence:int):
    """
        This function reads the pressure value from the pressure_node and prints it to the console.
        The pressure value is also inserted into the database using the session object.
        The p_event object is used to set the alarm state based on the pressure value.
        The function then sleeps for 5 seconds before repeating.
        """

    while True:
        pressure_value = await pressure_node.read_value()
        print(f"Pressure: {pressure_value}")
        logging.info(f"Pressure: {pressure_value}")
        insert_pressure_data(session, pressure_value)
        p_event.notify_alarm_state(frequence)
        p_event.set_alarm_state(pressure_value)
        await asyncio.sleep(frequence)  # Read pressure every 5 seconds
def load_temp_config(filename='config_temperature.yaml'):
    with open(filename, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            return config.get('temperature_node', {})  # Using .get() to avoid KeyError
        except yaml.YAMLError as exc:
            print(exc)
def load_pressure_config(filename='config_pressure.yaml'):
    with open(filename, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            return config.get('pressure_node', {})  # Using .get() to avoid KeyError
        except yaml.YAMLError as exc:
            print(exc)


async def main():
    """
    This function sets up the asynchronous OPC UA client and starts the temperature and pressure reading tasks.
    If the tasks are cancelled, the function will close the database session and exit.
    """
    session = None
    temperature_task = None  # Initialize to None
    pressure_task = None  # Initialize to None
    limit_temperature = 265
    limit_pressure = 90

    # Load temperature node configuration
    temp_config = load_temp_config()
    # Load pressure configuration from config_pressure.yaml
    pressure_config = load_pressure_config()

    try:
        # Create database session
        engine = create_my_engine()
        session = create_my_session(engine)

        # Get temperature and pressure node IDs from configuration
        temperature_node_id = temp_config['node_id']
        pressure_node_id = pressure_config['node_id']
        temperature_event = event(temp_config['description'], 0, limit_temperature)
        pressure_event = event(pressure_config['description'], 0, limit_pressure)

        async with Client('opc.tcp://192.168.25.61:53530/OPCUA/SimulationServer') as client:
            temperature_node = client.get_node(temperature_node_id)
            pressure_node = client.get_node(pressure_node_id)

            if not (temperature_node and pressure_node):
                logging.info("error: could not find specified variable nodes.")
                print("Error: Could not find specified variable nodes.")
                return

            temperature_task = asyncio.create_task(read_temperature(temperature_node, session, temperature_event,10))
            pressure_task = asyncio.create_task(read_pressure(pressure_node, session, pressure_event,5))

            await asyncio.gather(temperature_task, pressure_task)
    except asyncio.CancelledError:
        logging.info("One of the sensor tasks was cancelled.")
        print("One of the sensor tasks was cancelled.")
    finally:
        if session:
            await db_close(session)
        if temperature_task and not temperature_task.done():
            temperature_task.cancel()
        if pressure_task and not pressure_task.done():
            pressure_task.cancel()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit, TypeError):
        logging.info("Exiting...")
        print("Exiting...")


