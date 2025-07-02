from abc import ABC, abstractmethod
import logging
from logging import exception
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

class GPIOInputInterface(ABC):
    def __init__(self, name, pin_number):
        self.pin_number = pin_number
        self.name = name

    @abstractmethod
    def read(self) -> bool:
        """Read the state of the GPIO input pin."""
        exception("This method should be overridden in subclasses.")


class GPIOOutputInterface(ABC):
    def __init__(self, name, pin_number):
        self.pin_number = pin_number
        self.name = name

    @abstractmethod
    def enable(self) -> None:
        """Enable the GPIO output pin."""
        exception("This method should be overridden in subclasses.")

    @abstractmethod
    def disable(self) -> None:
        """Disable the GPIO output pin."""
        exception("This method should be overridden in subclasses.")


import json

class MockGPIOInput(GPIOInputInterface):
    def __init__(self, name, pin_number):
        super().__init__(name, pin_number)

    def read(self) -> bool:
        """Mock reading the state of the GPIO input pin."""

        # For testing purposes, we can return a fixed value or simulate a state
        with open("mock_io.json", 'r') as file:
            data = json.load(file)

            if data[str(self.pin_number)] == "on":
                logger.info(f"Input {self.name} read: True on pin {self.pin_number}")
                return True
            else:
                logger.info(f"Input {self.name} read: False on pin {self.pin_number}")
                return False

class MockGPIOOutput(GPIOOutputInterface):
    def __init__(self, name, pin_number):
        super().__init__(name, pin_number)

    def enable(self) -> None:
        """Mock enabling the GPIO output pin."""
        # For testing purposes, we can just print or log the action
        logger.info(f"Output {self.name} enabled on pin {self.pin_number}")

    def disable(self) -> None:
        """Mock disabling the GPIO output pin."""
        # For testing purposes, we can just print or log the action
        logger.info(f"Output {self.name} disabled on pin {self.pin_number}")

# enable once installed via pip
#
# """
# Using gpiozero library to create a GPIO interface.
# https://gpiozero.readthedocs.io/
# """
# from gpiozero import LED, Button
#
# class GPIOZeroInput(GPIOInputInterface):
#     def __init__(self, name, pin_number):
#         super().__init__(name, pin_number)
#         self.pin = Button(pin_number)
#
#     def read(self) -> bool:
#         """Read the state of the GPIO input pin."""
#         return self.pin.is_pressed
#
# class GPIOZeroOutput(GPIOOutputInterface):
#     def __init__(self, name,pin_number):
#         super().__init__(name, pin_number)
#         self.pin = LED(pin_number)
#
#     def enable(self) -> None:
#         """Enable the GPIO output pin."""
#         self.pin.on()
#
#     def disable(self) -> None:
#         """Disable the GPIO output pin."""
#         self.pin.off()

