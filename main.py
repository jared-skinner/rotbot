from composter import Composter
from time import sleep
import logging
import os
import sys
logger = logging.getLogger(__name__)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

from gpio import MockGPIOInput as PiInput, MockGPIOOutput as PiOutput
#from gpio import GPIOZeroInput as PiInput, GPIOZeroOutput as PiOutput


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
    os.system('cls' if os.name == 'nt' else 'clear')

    while True:
        print_header()

        logger.debug("Disable Prox Switch - For Safety")
        # disable prox sensor every cycle for safety
        composter.disable_prox_switch()

        print("\n")
        logger.debug("Reset Auto Run Flag - Just after midnight")
        # reset auto run if necessary
        composter.reset_auto_run()

        # clear forward/reverse, if necessary
        print("\n")
        logger.debug("Clear forward/reverse")
        if not composter.read_input("forward") or not composter.read_input("manual"):
            composter.disable_forward()

        if not composter.read_input("reverse") or not composter.read_input("manual"):
            composter.disable_reverse()


        print("\n")
        logger.debug("Manual Actions")
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

        print("\n")
        logger.debug("Auto Actions")
        if composter.read_input("auto"):
            composter.auto_run()
        else: # off
            pass

        sleep(sleep_time)

        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    composter = Composter(PiInput, PiOutput)

    main(composter=composter, sleep_time=.01)
