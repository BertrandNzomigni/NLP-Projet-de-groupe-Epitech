import os
from manager import cache_reader, cache_writer
from info import info
from lexdiv import lexdiv
from topics import topics
from entities import entity_recognition
from summarize import summarize
from similar import similarity

def card(id):
    # check cache first
    if os.path.exists(f"cache/card/card_{id}.json"):
        return cache_reader(f"card/card_{id}")

    result = {
        "info": info(id),
        "lexdiv": lexdiv(id, True),
        "topics": topics(id),
        "entities": entity_recognition(id),
        "summary": summarize(id),
        "similar": similarity(id)
    }

    cache_writer(f"card/card_{id}", result)
    return result