from composter import Composter
from time import sleep
import logging
import sys
logger = logging.getLogger(__name__)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

from gpio import MockGPIOInput as PiInput, MockGPIOOutput as PiOutput
#from gpio import GPIOZeroInput as PiInput, GPIOZeroOutput as PiOutput

def main(composter: Composter, sleep_time:float = 0.1) -> None:
    logger.debug("Composter main loop running...")
    while True:
        # disable prox sensor every cycle for safety
        composter.disable_prox_switch()

        # reset auto run if necessary
        composter.reset_auto_run()

        # clear forward/reverse, if necessary
        logger.debug("Clear motor")
        if not composter.read_input("forward"):
            composter.disable_forward()

        if not composter.read_input("reverse"):
            composter.disable_reverse()

        if composter.read_input("manual"):
            if composter.read_input("forward"):
                # make it so this doesn't start and stop
                composter.enable_forward()
            elif composter.read_input("reverse"):
                # make it so this doesn't start and stop
                composter.enable_reverse()
            elif composter.read_input("ext_run"):
                composter.run(time_seconds = 15 * 60) # 15 minutes

        elif composter.read_input("auto"):
            composter.auto_run()
        else: # off
            pass

        sleep(sleep_time)

if __name__ == "__main__":
    composter = Composter(PiInput, PiOutput)

    main(composter=composter, sleep_time=3)
