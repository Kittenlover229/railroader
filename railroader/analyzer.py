from .models import Plot, StoryBit, Concept
from typing import Dict, Tuple
import re


def fill_in_concept_references(story: StoryBit, concepts: Dict[str, Concept]):
    while found := re.search(r"\((.+?)\)\[(.+?)\]", story.desc):
        text, ref = found.groups()
        span = found.span()
        story.desc = story.desc[: span[0]] + text + story.desc[span[1] :]
        story.concepts[(span[0], span[0] + len(text))] = concepts[ref]


def story_from_dict(raw_story: dict) -> StoryBit:
    def get_nexts_from_raw_story(raw_story: dict) -> Dict[int, Tuple[str, str]]:
        nexts = []

        nextt = raw_story.get("next")
        if nextt:
            # Append it to the list as the default option
            nexts.append(("", nextt))

        nexts.extend((raw_story.get("options") or dict()).items())

        return {i: nextt for i, nextt in enumerate(nexts)}

    return StoryBit(
        name=raw_story["name"].strip(),
        desc=raw_story["desc"].strip(),
        concepts=dict(),
        nexts=get_nexts_from_raw_story(raw_story),
    )


def concept_from_dict(raw_concept: dict) -> Concept:
    return Concept(name=raw_concept["name"].strip(), desc=raw_concept["desc"].strip())


def data_to_plot(data: dict) -> Plot:
    data = data["plot"]
    concepts = list(
        map(
            concept_from_dict,
            data["concepts"],
        )
    )

    story_bits = list(
        map(
            story_from_dict,
            data["story-bits"],
        )
    )

    concept_mapping = {concept.name: concept for concept in concepts}
    story_mapping = {story.name: story for story in story_bits}

    for story in story_bits:
        fill_in_concept_references(story, concept_mapping)

    plot = Plot(
        story_mapping.get(data["start-at"] or story_bits[0].name), story_bits, concepts
    )

    return plot
