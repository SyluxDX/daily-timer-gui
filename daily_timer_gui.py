""" Daily timer with graphical interface """
import argparse
import threading

import src.ui
import src.configurations
import src.interfaces
import src.core

_parser = argparse.ArgumentParser(description='Timer for Daily Timer.')
_parser.add_argument("-c", "--config", default="team.json", help='path for configuration')

ARGS = _parser.parse_args()

if __name__ == "__main__":

    try:
        config = src.configurations.Configurations(ARGS.config)
        stat_filename = f"{ARGS.config[:-5]}_stats.csv"
        ### TODO
        core = src.core.Core(config, src.interfaces.UiInterface())
        start_time = 0 if config.stopwatch else config.time
        root = src.ui.interface("dark", core, start_time)
        # start core thread
        run_thread = threading.Thread(target=core.mainloop)#, args=(1.0,))
        run_thread.start()
        # start ui blocking
        root.window.mainloop()
        # set thread flag to false and wait
        core.loop_run = False
        run_thread.join()
    except src.configurations.ConfigurationExeception as error:
        print(error, end="\n\n")
        input("Press Enter to exit")

    
