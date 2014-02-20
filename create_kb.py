#!/usr/bin/env python

"""
Easily creates knowledge base, I guess. Also creates a dot graph, because why
not?
"""

from itertools import combinations, chain

class KnowledgeBase(object):
    def __init__(self):
        # A dictionary of non-repeating, undirected edges.
        # Key is min() of the two links.
        self._links = set()
        self._entities = set()

    def associate(self, a, b):
        self._entities.add(a)
        self._entities.add(b)
        # To remain unique, each pair is always sorted.
        pair = sorted((a, b))
        self._links.add(tuple(pair))

    def associate_all(self, src, entities):
        for ent in entities:
            self.associate(src, ent)

    def clique(self, seq):
        for a, b in combinations(seq, 2):
            self.associate(a, b)

    @property
    def graph(self):
        return self._entities, self._links


def dot_graph(kb):
    print("graph {")

    entities, vertices = kb.graph

    for entity in entities:
        print('  "%s";' % entity)

    print('')

    for pair in vertices:
        print('  "%s" -- "%s";' % pair)

    print("}")


if __name__ == '__main__':
    kb = KnowledgeBase()

    turtles = [n + ' (Ninja Turtle)' for n in
            ('Michelangelo', 'Donatello', 'Raphael', 'Leonardo')]

    # TODO: Uh... entity aliases?
    painters = ('Michaelangelo', 'Donatello', 'Raphael', 'Leonardo da Vinci')

    kb.clique(chain(('Master Splinter',), turtles))
    kb.clique(painters)
    kb.associate_all('pizza', turtles)
    kb.associate_all('renaissance', painters)
    kb.associate('Master Splinter', 'renaissance')

    dot_graph(kb)
    

