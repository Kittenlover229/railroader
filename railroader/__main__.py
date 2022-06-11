from sys import argv as args
import yaml

from .analyzer import data_to_plot

def main(filename, *args, **kwargs):
    with open(filename) as file:
        plot = data_to_plot(yaml.safe_load(file))

    print(plot)

if __name__ == '__main__':
    main(*args[1:])
