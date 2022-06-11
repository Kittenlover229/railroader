from dataclasses import dataclass
from typing import Dict, List, Tuple


class Conflict(BaseException):
    ...


@dataclass
class Concept:
    name: str
    desc: str


@dataclass
class StoryBit:
    name: str
    desc: str
    concepts: Dict[Tuple[int, int], Concept]
    nexts: Dict[int, Tuple[str, str]]


@dataclass
class Plot:
    begin: StoryBit
    stories: List[StoryBit]
    concepts: List[StoryBit]

    def get_story_by_name(self, name: str) -> StoryBit:
        for story in self.stories:
            if story.name == name:
                return story
        return None
