
import logging
import os
import sys

from logging.handlers import RotatingFileHandler
from datetime import datetime, time
from time import sleep

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fountain import Fountain
from gpio.gpio_zero import GPIOZeroInput as PiInput, GPIOZeroOutput as PiOutput
#from gpio.gpio_mock import MockGPIOInput as PiInput, MockGPIOOutput as PiOutput

log_file = "logs/splashstart.log"
max_log_size = 1024 * 1024  # 1 MB
backup_count = 2

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(log_file, maxBytes=max_log_size, backupCount=backup_count)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def print_header():
    logger.info(r"""
spashstart

- A Skinner Project


""")

def main(fountain: Fountain, sleep_time:float = 0.1) -> None:
    print_header()

    morning_start_time = time(6, 0)
    morning_end_time = time(8, 0)

    evening_start_time = time(17, 0)
    evening_end_time = time(22, 0)

    while True:
        logger.debug("STARTING LOOP")

        logger.debug("\nManual Actions")

        if not fountain.read_input("manual"):
            fountain.stop()

        if fountain.read_input("manual"):
            fountain.start()

        logger.debug("Auto Actions")
        now = datetime.now().time()
        if fountain.read_input("auto"):
            if (now >= morning_start_time and now < morning_end_time) or (now >= evening_start_time and now < evening_end_time):
                fountain.start()
            else:
                fountain.stop()

        sleep(sleep_time)
        logger.debug("ENDING LOOP\n\n")

if __name__ == "__main__":
    fountain = Fountain(PiInput, PiOutput)

    main(fountain=fountain, sleep_time=.01)
