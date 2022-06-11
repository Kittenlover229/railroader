from .models import Plot, StoryBit, Concept
from typing import Dict
import re

def fill_in_concept_references(story: StoryBit, concepts: Dict[str, Concept]):
    while found := re.search(r"\((.+?)\)\[(.+?)\]", story.desc):
        text, ref = found.groups()
        span = found.span()
        story.desc = story.desc[:span[0]] + text + story.desc[span[1]:]
        story.concepts[(span[0], span[0] + len(text))] = concepts[ref]

def data_to_plot(data: dict) -> Plot:
    data = data["plot"]
    concepts = list(
        map(
            lambda x: Concept(name=x["name"].strip(), desc=x["desc"].strip()),
            data["concepts"],
        )
    )
    story_bits = list(
        map(
            lambda x: StoryBit(
                name=x["name"].strip(), desc=x["desc"].strip(), concepts=dict()
            ),
            data["story-bits"],
        )
    )

    concept_mapping = {concept.name: concept for concept in concepts}
    story_mapping = {story.name: story for story in story_bits}

    for story in story_bits:
        fill_in_concept_references(story, concept_mapping)

    plot = Plot(story_bits, concepts)

    return plot
