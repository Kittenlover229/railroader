from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class Concept:
    name: str
    desc: str


@dataclass
class StoryBit:
    name: str
    desc: str
    concepts: Dict[Tuple[int, int], Concept]


@dataclass
class Plot:
    stories: List[StoryBit]
    concepts: List[StoryBit]
