from gpio_interface import GPIOInputInterface, GPIOOutputInterface
import logging
import sys

from gpiozero import LED, Button

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

"""
Using gpiozero library to create a GPIO interface.
https://gpiozero.readthedocs.io/
"""

class GPIOZeroInput(GPIOInputInterface):
    def __init__(self, name, pin_number):
        super().__init__(name, pin_number)
        self.pin = Button(pin_number)

    def read(self) -> bool:
        """Read the state of the GPIO input pin."""
        return self.pin.is_pressed

class GPIOZeroOutput(GPIOOutputInterface):
    def __init__(self, name,pin_number):
        super().__init__(name, pin_number)
        self.pin = LED(pin_number)

    def enable(self) -> None:
        """Enable the GPIO output pin."""
        self.pin.on()

    def disable(self) -> None:
        """Disable the GPIO output pin."""
        self.pin.off()

