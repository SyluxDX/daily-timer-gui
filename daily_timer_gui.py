""" Daily timer with graphical interface """
import argparse
import threading

from src import (
    ui,
    configurations,
    interfaces,
    core,
)

_parser = argparse.ArgumentParser(description='Timer for Daily Timer.')
_parser.add_argument("-c", "--config", default="team.json", help='path for configuration')

ARGS = _parser.parse_args()

if __name__ == "__main__":

    try:
        config = configurations.Configurations(ARGS.config)
        stat_filename = f"{ARGS.config[:-5]}_stats.csv"

        timer_core = core.Core(config, interfaces.UiInterface(), stat_filename)
        start_time = 0 if config.stopwatch else config.time
        ui_root = ui.Interface(config.theme, timer_core, start_time)

        # start timer thread
        run_thread = threading.Thread(target=timer_core.mainloop)#, args=(1.0,))
        run_thread.start()

        # start ui blocking
        ui_root.window.mainloop()

        # set thread flag to false and wait
        timer_core.loop_run = False
        run_thread.join()
        print("exit")
    except configurations.ConfigurationExeception as error:
        print(error, end="\n\n")
        input("Press Enter to exit")
