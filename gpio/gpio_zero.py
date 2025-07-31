"""
Using gpiozero library to create a GPIO interface.
https://gpiozero.readthedocs.io/
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from gpio.gpio_interface import GPIOInputInterface, GPIOOutputInterface
from gpiozero import Button, OutputDevice
from gpiozero.pins.rpigpio import RPiGPIOFactory

factory = RPiGPIOFactory()

log_file = "logs/gpiozero.log"
max_log_size = 1024 * 1024  # 1 MB
backup_count = 5

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(log_file, maxBytes=max_log_size, backupCount=backup_count)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class GPIOZeroInput(GPIOInputInterface):
    def __init__(self, name, pin_number):
        super().__init__(name, pin_number)
        self.pin = Button(pin_number, pin_factory=factory)

    def read(self) -> bool:
        """Read the state of the GPIO input pin."""
        logger.debug(f"Input {self.name} read: {self.pin.is_pressed} on pin {self.pin_number}")
        return self.pin.is_pressed

class GPIOZeroOutput(GPIOOutputInterface):
    def __init__(self, name,pin_number):
        super().__init__(name, pin_number)
        self.pin = OutputDevice(pin_number, active_high=False, initial_value=False, pin_factory=factory)

    def enable(self) -> None:
        """Enable the GPIO output pin."""
        self.pin.on()
        logger.debug(f"Output {self.name} on pin {self.pin_number} turned on")

    def disable(self) -> None:
        """Disable the GPIO output pin."""
        self.pin.off()
        logger.debug(f"Output {self.name} on pin {self.pin_number} turned off")
