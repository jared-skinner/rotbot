from datetime import datetime, time

import logging
from logging.handlers import RotatingFileHandler

from time import sleep

log_file = "logs/fountain.log"
max_log_size = 1024 * 1024  # 1 MB
backup_count = 5

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(log_file, maxBytes=max_log_size, backupCount=backup_count)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

MIDNIGHT = time(0, 0)

class Fountain:
    def __init__(self, Input, Output) -> None:
        logger.info("Initializing Fountain")

        self.inputs = {
            "auto": Input("auto", 10),
            "manual": Input("manual", 9),
        }

        self.outputs = {
            "fountain_output": Output("fountain_output", 2),
        }

        self.clear_outputs()

    def clear_outputs(self) -> None:
        logger.info("Clearing outputs")
        for output in self.outputs.values():
            output.disable()

    def read_input(self, input_name: str) -> bool:
        return self.inputs[input_name].read()

    def start(self) -> None:
        logger.debug(f"Starting fountain")
        self.outputs["fountain_output"].enable()

    def stop(self) -> None:
        logger.debug(f"Stopping fountain")
        self.outputs["fountain_output"].disable()
