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
