from .models import Plot, StoryBit, Concept

def data_to_plot(data: dict) -> Plot:
    data = data["plot"]
    concepts = list(map(lambda x: Concept(name=x["name"].strip(), desc=x["desc"].strip()), data["concepts"]))
    story_bits = list(map(lambda x: StoryBit(name=x["name"].strip(), desc=x["desc"].strip(), concepts=[]), data["story-bits"]))

    plot = Plot(story_bits, concepts)

    return plot
