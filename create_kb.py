#!/usr/bin/env python
# coding: UTF-8

"""
Knowledge base stuff. Tools for making knowledge bases and exporting them to
nifty DOT/graphviz graphs.
"""

from itertools import combinations, chain
from collections import Counter, namedtuple

# A few data classes.
Entity = namedtuple('Entity', 'name category')
EntityInfo = namedtuple('EntityInfo', 'ner_type aliases')

class KnowledgeBase(object):
    def __init__(self):
        self._links = Counter()
        self.entities = {}

    def add_entity(self, entity, entity_info=None):
        self.entities[entity] = entity_info
        return entity

    def associate(self, a, b):
        self.ensure_exists(a)
        self.ensure_exists(b)
        # A "canoncial" order for the items in the pair is given
        # so that (a, b) and (b, a) will always just insert (a, b).
        pair = sorted((a, b))
        self._links[tuple(pair)] += 1

    def associate_all(self, src, entities):
        for ent in entities:
            self.associate(src, ent)

    def clique(self, seq):
        for a, b in combinations(seq, 2):
            self.associate(a, b)

    def ensure_exists(self, entity):
        self.entities.setdefault(entity, None)

    @property
    def graph(self):
        return self.entities.keys(), self._links


def add_category_entities(kb, category, seq, default_ner='MISC'):
    """
    Takes a sequence of tuples of (name, ner_type, aliases) and inserts it in
    to the knowledge base. All of the items belong to one category.

    Returns a list of all inserted entities.
    """

    entities = []

    for name, ner_type, aliases in seq:
        # Coerce a string to a 1-tuple.
        if not aliases:
            aliases = ()
        elif type(aliases) is str:
            aliases = (aliases,)
        # Coerce a non-existant NER to the 'MISC' type.
        if not ner_type:
            ner_type = default_ner

        entity = Entity(name, category)
        info = EntityInfo(ner_type, aliases)

        kb.add_entity(entity, info)
        entities.append(entity)

    return entities


def dot_graph(kb):
    print("graph {")

    entities, vertices = kb.graph

    for entity in entities:
        _ner, aliases = kb.entities.get(entity) or ('MISC', ())
        # Note: using the hash as the ID is susceptible to collisions,
        # but it's the easiest thing to do right now.
        eid = hash(entity)

        name, category = entity
        
        line = r'  {eid:d}[label=< <B>{name}</B><BR/><I>{category}</I> >];'
        print(line.format(**locals()))

    print('')

    for pair, count in vertices.items():
        a, b = map(hash, pair)
        # TODO: incorporate the count in the styles.
        line = '  {a:d} -- {b:d};' 
        print(line.format(**locals()))

    print("}")

