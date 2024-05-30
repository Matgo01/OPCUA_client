#!/usr/bin/env python3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
class event():
    """
    Initialize an Event object.

    Args:
        description (str): A description of the event.
        alarm_state (int): The current alarm state of the event. 0 for normal, 1 for high temperature, and 2 for high pressure.
    """

    def __init__(self, description: str, alarm_state: int, limit_value:float):
        """
                Initialize an Event object.

                Args:
                    description (str): A description of the event.
                    alarm_state (int): The current alarm state of the event. 0 for normal, 1 for danger event , and 2 for high danger event.
                """
        self.description = description
        self.alarm_state = alarm_state
        self.limit_value = limit_value
        self.timer = 0

    def get_description(self):
        return self.description

    def set_description(self, description: str):
        self.description = description

    def get_alarm_state(self):
        return self.alarm_state

    def set_alarm_state(self,  value: float):
        """
            Set the alarm state based on the monitored value.

            Args:
                value (float): The current monitored value.


            Raises:
                ValueError: If the value is outside of the specified range.

            Returns:
                None

            """
        self.check_monitored_value(value)
        if self.alarm_state == 1:
            print(f"{self.description} is high. Lower the value within 15 minutes.")
            logging.info(f" {self.description} is high. Lower the value within 15 minutes.")
        elif self.alarm_state == 0:
            self.reset_alarm()
    def reset_alarm(self):
        """
            Cancels the existing timer and sets the timer attribute to None.

            Returns:
                None
            """
        if self.alarm_state == 0:
            self.timer = 0
            print(f"timer:{self.timer}")
            logging.info(f"Timer:{self.timer}")

    def check_monitored_value(self, value: float):
        """
            Check if the monitored value is above the specified limit.

            Args:
                value (float): The current monitored value.

            Raises:
                ValueError: If the value is outside of the specified range.

            Returns:
                None
            """
        if self.alarm_state == 2 and value >= self.limit_value:
            (print(f"Alarm state is still high after 15 minutes. Resetting to normal: {self.alarm_state} description: {self.description}"))
            logging.info(f"Alarm state is still high after 15 minutes. Resetting to normal: {self.alarm_state} description: {self.description}")
        elif value >= self.limit_value:
            self.alarm_state = 1
            print(f"alarm_state {self.alarm_state} for {self.description}")
            logging.info(f"alarm_state {self.alarm_state} for {self.description}")

        else:
            self.alarm_state = 0
            print(f"alarm_state {self.alarm_state} for {self.description}")
            logging.info(f"alarm_state {self.alarm_state} for {self.description}")

    def set_alarm_state_on_higth_danger(self):
        self.alarm_state = 2

    def notify_alarm_state(self, frequence: int):
        """
        Notify the user if the alarm state is high.

        If the alarm state is high, print a message to the user and start a timer. If the alarm state remains high after the timer expires, print a message to reset the alarm state to normal.
        """
        if self.alarm_state == 1:
            print(f" Danger. Lower the value within 15 minutes: {self.description}")
            logging.info(f" Danger. Lower the value within 15 minutes: {self.description}")
            self.timer+=1*frequence
            print(f"timer: {self.timer}, description: {self.description}")
            logging.info(f"timer: {self.timer}, description: {self.description}")
            if self.timer > 10:
                self.set_alarm_state_on_higth_danger()
