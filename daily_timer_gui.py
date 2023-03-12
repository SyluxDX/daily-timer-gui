""" Daily timer with graphical interface """
import argparse

import src.ui
import src.configurations

_parser = argparse.ArgumentParser(description='Timer for Daily Timer.')
_parser.add_argument("-c", "--config", default="team.json", help='path for configuration')

ARGS = _parser.parse_args()

if __name__ == "__main__":

    try:
        config = src.configurations.Configurations(ARGS.config)
        stat_filename = f"{ARGS.config[:-5]}_stats.csv"
        ### TODO
        # add core functionality
        # create ui and link to core
    except src.configurations.ConfigurationExeception as error:
        print(error, end="\n\n")
        input("Press Enter to exit")
