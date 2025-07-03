import logging

from logging.handlers import RotatingFileHandler
from time import sleep

from composter import Composter
from gpio_zero import GPIOZeroInput as PiInput, GPIOZeroOutput as PiOutput

log_file = "rotbot.log"
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
  _______     ______  ___________      _______     ______  ___________      ___      ___  ____              ______    
 /"      \   /    " \("     _   ")    |   _  "\   /    " \("     _   ")    |"  \    /"  |/  " \            /    " \   
|:        | // ____  \)__/  \\__/     (. |_)  :) // ____  \)__/  \\__/      \   \  //  //__|| |           // ____  \  
|_____/   )/  /    ) :)  \\_ /        |:     \/ /  /    ) :)  \\_ /          \\  \/. ./    |: |          /  /    ) :) 
 //      /(: (____/ //   |.  |        (|  _  \\(: (____/ //   |.  |           \.    //    _\  |    _____(: (____/ //  
|:  __   \ \        /    \:  |        |: |_)  :)\        /    \:  |            \\   /    /" \_|\  ))_  ")\        /   
|__|  \___) \"_____/      \__|        (_______/  \"_____/      \__|             \__/    (_______)(_____(  \"_____/    

- A Skinner Project


""")

def main(composter: Composter, sleep_time:float = 0.1) -> None:
    print_header()

    while True:
        logger.debug("STARTING LOOP")
        logger.debug("Disable Prox Switch - For Safety")
        # disable prox sensor every cycle for safety
        composter.disable_prox_switch()

        logger.debug("\nReset Auto Run Flag - Just after midnight")
        # reset auto run if necessary
        composter.reset_auto_run()

        # clear forward/reverse, if necessary
        logger.debug("\nClear forward/reverse")
        if not composter.read_input("forward") or not composter.read_input("manual"):
            composter.disable_forward()

        if not composter.read_input("reverse") or not composter.read_input("manual"):
            composter.disable_reverse()

        logger.debug("\nManual Actions")
        if composter.read_input("manual"):
            if composter.read_input("forward"):
                # make it so this doesn't start and stop
                composter.enable_forward()
            elif composter.read_input("reverse"):
                # make it so this doesn't start and stop
                composter.enable_reverse()
            elif composter.read_input("ext_run"):
                #run_time = 15 * 60 # 15 minutes
                run_time = 10 # 10 seconds for testing
                composter.run(time_seconds = run_time) # 15 minutes

        logger.debug("Auto Actions")
        if composter.read_input("auto"):
            composter.auto_run()
        else: # off
            pass

        sleep(sleep_time)
        logger.debug("ENDING LOOP\n\n")

if __name__ == "__main__":
    composter = Composter(PiInput, PiOutput)

    main(composter=composter, sleep_time=.01)
