import argparse
import yaml

from .models import Plot, StoryBit
from .analyzer import data_to_plot

parser = argparse.ArgumentParser(description="")
parser.add_argument("filename", type=str)
parser.add_argument("mode", choices=["cli", "html"])


def main_interactive(plot: Plot):
    while True:
        current_story = plot.begin
        print(
            f"{len(plot.stories)} stories, {len(plot.concepts)} concepts loaded, starting at `{plot.begin.name}`"
        )
        print(current_story.desc)
        if len(current_story.nexts) <= 0:
            break

        for i, option in current_story.nexts.items():
            print(f"  {i} {option[0] or '*continue*'}")
        inp = int(input("> ").strip() or 0)
        current_story = plot.get_story_by_name(current_story.nexts.get(inp)[1])

    print("The End.")


def render_story_to_html(story: StoryBit):
    return (
        f"""
<html>
    <head>
        <title>{story.name}</title>
        <style>
            main {'{'}
                font-family: "Consolas";
                font-size: 150%;
                padding-top: 10%;
                padding-left: 20%;
                padding-right: 20%;
            {'}'}
        </style>
    </head>
    <body>
        <main>
            <p>{story.desc}</p>
            <ul>
            {''.join(f'<li><a href="{link}.html">{flavourtext or "*continue*"}</a></li>' for flavourtext, link in story.nexts.values())}
            </ul>
        </main>
    </body>
</html>
    """.strip()
        + "\n"
    )


def main_html_render(plot: Plot):
    import tempfile
    import shutil
    import os

    parser.add_argument("--out", metavar="out", type=str, default="out")
    out = parser.parse_args().out

    with tempfile.TemporaryDirectory() as tmpdir:
        for story in plot.stories:
            path = os.path.join(tmpdir, f"{story.name}.html")
            with open(path, "w") as f:
                html = render_story_to_html(story)
                f.write(html)
        shutil.make_archive(out, "zip", tmpdir)


def main(filename: str, mode: str, *args, **kwargs):
    with open(filename) as file:
        plot = data_to_plot(yaml.safe_load(file))
        if mode == "cli":
            main_interactive(plot)
        elif mode == "html":
            main_html_render(plot)
        else:
            exit(-1)


if __name__ == "__main__":
    args = parser.parse_args()
    filename = args.filename
    mode = args.mode

    main(filename, mode)
