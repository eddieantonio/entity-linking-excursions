#!/usr/bin/env python

from collections import defaultdict
from shingles import shingles

def make_database(entities):
    db = defaultdict(list)

    for entity in entities:
        trigrams = shingles(entity)
        for trigram in trigrams:
            db[trigram].append(entity)

    return db

def dot_graph(db):
    print("digraph { ")

    for trigram, entities in db.items():
        for entity in entities:
            print('  "%s" -> "%s";' % (trigram, entity))

    print("}")

if __name__ == '__main__':
    # TODO: Create a sweet-butt corpus.
    ENTITIES = [
        'Benedict Cumberbatch', 'Sherlock', 'Steven Moffat', 'Peggy Moffit',
        'Bandicoot Cabbagepatch', 'Benadryl Cumbersnatch',
    ]
    db = make_database(ENTITIES)
    dot_graph(db)

