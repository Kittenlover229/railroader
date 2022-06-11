from sys import argv as args
from pprint import pprint
from enum import Enum
import yaml


class AppState(Enum):
    STARTUP = 1
    REPORTING = 2


from .analyzer import data_to_plot


def main(filename, *args, **kwargs):
    state = AppState.STARTUP
    with open(filename) as file:
        plot = data_to_plot(yaml.safe_load(file))
        pprint(plot)


if __name__ == "__main__":
    if len(args) >= 2:
        filename = args[1]
    else:
        filename = None
    main(filename)
