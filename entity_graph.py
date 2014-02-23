#!/usr/bin/env python
# coding: UTF-8

from itertools import chain
from collections import defaultdict
from shingles import shingles
from create_kb import Entity, EntityInfo


def make_database(pairs):
    """
    Given pairs of Entites and EntityInfos creates ALL shingles possible for
    the given entry and links them to the pair. That made sense.

    RETURNS a mapping of trigrams to all possible entities that that trigram
    could be a part of.
    """
    db = defaultdict(list)

    # dem for loops tho.
    for pair in pairs:
        entity, info = pair
        all_names = chain((entity.name,), info.aliases)

        for name in all_names:
            trigrams = shingles(name)
            for trigram in trigrams:
                db[trigram].append(entity)

    return db


def make_entity_node(entity, info):
    "Returns the DOT node expression for the given entity"
    
    # Note: using the hash as the ID is susceptible to collisions,
    # but it's the easiest thing to do right now.
    eid = hash(entity)
    name, category = entity
    _ner, aliases = info or ('MISC', ())

    spec = r'  {eid:d}[label=< <B>{name}</B><BR/><I>{category}</I> >];'

    return spec.format(**locals())

def print_entities(entities):
    "Prints DOT node defintions for each pairt of (Entity, EntityInfo)."
    for entity, info in entities:
        line = make_entity_node(entity, info)
        print(line)
    

def kb_graph(kb):
    print("graph {")

    entities, vertices = kb.graph

    print_entities(entities.items())
    print('')

    for pair, count in vertices.items():
        a, b = map(hash, pair)
        # TODO: incorporate the count in the styles.
        line = '  {a:d} -- {b:d};' 
        print(line.format(**locals()))

    print("}")


def shingles_graph(db, entity_pairs):
    print("digraph { ")

    print_entities(entity_pairs)
    print('')

    for trigram, entities in db.items():
        for entity in entities:
            eid = hash(entity)
            print(u'  "{trigram}" -> {eid:d};'.format(**locals()))

    print("}")

if __name__ == '__main__':
    # TODO: Create a sweet-butt corpus.
    ENTITIES = [Entity(name, '') for name in  [
        'Benedict Cumberbatch', 'Sherlock', 'Steven Moffat', 'Peggy Moffit',
        'Bandicoot Cabbagepatch', 'Benadryl Cumbersnatch',
    ]]

