import logging
import os
import json
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from gpio.gpio_interface import GPIOInputInterface, GPIOOutputInterface

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MockGPIOInput(GPIOInputInterface):
    def __init__(self, name, pin_number):
        super().__init__(name, pin_number)

    def read(self) -> bool:
        """Mock reading the state of the GPIO input pin."""

        # For testing purposes, we can return a fixed value or simulate a state
        with open(os.path.join(os.path.dirname(__file__), "mock_io.json"), 'r') as file:
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


