from sys import argv as args
from pprint import pprint
import yaml
from .analyzer import data_to_plot


def main(filename, *args, **kwargs):
    with open(filename) as file:
        plot = data_to_plot(yaml.safe_load(file))
        current_story = plot.begin
        print(
            f"{len(plot.stories)} stories, {len(plot.concepts)} concepts loaded, starting at `{plot.begin.name}`"
        )

        while True:
            print(current_story.desc)
            if len(current_story.nexts) <= 0:
                break

            for i, option in current_story.nexts.items():
                print(f"  {i} {option[0] or '*continue*'}")
            inp = int(input("> ").strip() or 0)
            current_story = plot.get_story_by_name(current_story.nexts.get(inp)[1])

        print("The End.")

if __name__ == "__main__":
    if len(args) >= 2:
        filename = args[1]
    else:
        filename = None
    main(filename)
