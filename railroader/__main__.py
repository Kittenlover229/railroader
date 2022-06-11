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
        current_story = plot.begin

        while True:
            print(current_story.desc)
            if len(current_story.nexts) <= 0:
                break

            for i, option in current_story.nexts.items():
                print(f"  {i} {option[0] or '*continue*'}")
            inp = int(input("> ").strip() or 0)
            current_story = plot.get_story_by_name(current_story.nexts.get(inp)[1])


if __name__ == "__main__":
    if len(args) >= 2:
        filename = args[1]
    else:
        filename = None
    main(filename)
