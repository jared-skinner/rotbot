from datetime import datetime, time

import logging
from logging.handlers import RotatingFileHandler

from time import sleep

log_file = "composter.log"
max_log_size = 1024 * 1024  # 1 MB
backup_count = 5

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(log_file, maxBytes=max_log_size, backupCount=backup_count)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

MIDNIGHT = time(0, 0)

class Composter:
    def __init__(self, Input, Output) -> None:
        logger.info("Initializing Composter")
        self.rotation_counter = 0

        self.auto_ran_today = False
        self.auto_run_start_time = time(2, 0)  # 2:00 AM in 24-hour format
        self.auto_run_ignore_time = time(6, 0)  # 6:00 AM in 24-hour format
        self.auto_run_cycle_count = 4

        self.inputs = {
            "auto": Input("auto", 10),
            "manual": Input("manual", 9),
            "forward": Input("forward", 11),
            "reverse": Input("reverse", 5),
            "prox": Input("prox", 6),
            "ext_run": Input("ext_run", 13)
        }

        self.outputs = {
            "forward": Output("forward", 2),
            "reverse": Output("reverse", 3),
            "prox": Output("prox", 4),
            "day_counter": Output("day_counter", 17)
        }

    def read_input(self, input_name: str) -> bool:
        return self.inputs[input_name].read()

    def increment_day_counter(self) -> None:
        self.outputs["day_counter"].enable()
        sleep(1)
        self.outputs["day_counter"].disable()
        logger.info("Incremented day counter")

    def run(self, cycle_count = None, time_seconds: int | None = None) -> None:
        assert cycle_count is not None or time_seconds is not None, "Either cycle_count or time_seconds must be provided"
        if cycle_count is not None:
            logger.info(f"Running composter for {cycle_count} cycles")
            self.enable_forward()
            prox_enabled = False
            while cycle_count > 0:
                # TODO: play with this
                sleep(.01)

                # this block is written to prevent rereading the same contact.
                if self.read_input("prox") and prox_enabled == False:
                    prox_enabled = True
                    cycle_count -= 1
                    sleep(5)
                elif not self.read_input("prox") and prox_enabled == True:
                    prox_enabled =  False

        elif time_seconds is not None: # time_seconds is not None
            logger.info(f"Running composter for {time_seconds} seconds")
            self.enable_forward()
            sleep(time_seconds)
            self.disable_forward()

    def auto_run(self) -> None:
        #if self.can_run_in_auto():
        if True:
            self.auto_ran_today = True
            self.enable_prox_switch()
            self.run(cycle_count = self.auto_run_cycle_count)
            self.increment_day_counter()
            self.disable_prox_switch()
            logger.info("Auto run executed")
        else:
            logger.debug("Cannot run in auto mode at this time")

    def reset_auto_run(self) -> None:
        now = datetime.now().time()
        if self.auto_ran_today and now >= MIDNIGHT and now < self.auto_run_start_time:
            self.auto_ran_today = False
            logger.info("Resetting auto_ran_today flag")

    def can_run_in_auto(self) -> bool:
        now = datetime.now().time()
        if self.auto_ran_today == False and now > self.auto_run_start_time and now < self.auto_run_ignore_time:
            return True
        else:
            return False

    def enable_prox_switch(self) -> None:
        self.outputs["prox"].enable()
        logger.info("Proximity switch enabled")

    def disable_prox_switch(self) -> None:
        self.outputs["prox"].disable()
        logger.debug("Proximity switch disabled")

    def enable_forward(self) -> None:
        logger.debug(f"Running forward ")
        self.outputs["forward"].enable()

    def disable_forward(self) -> None:
        logger.debug(f"Stopping forward")
        self.outputs["forward"].disable()

    def enable_reverse(self) -> None:
        logger.debug(f"Running reverse")
        self.outputs["reverse"].enable()

    def disable_reverse(self) -> None:
        logger.debug(f"Stopping reverse")
        self.outputs["reverse"].disable()
