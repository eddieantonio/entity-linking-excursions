#!/usr/bin/env python
# coding: UTF-8

"""
A turtle-y example of knowledge bases and shingles.
"""

from shingles import shingles
from create_kb import KnowledgeBase, Entity, EntityInfo, \
        add_category_entities

from entity_graph import make_database, kb_graph, shingles_graph


def create_knowledge_base():
    kb = KnowledgeBase()

    # Entities...
    turtles = add_category_entities(kb, 'Ninja Turtle', [
            ('Michelangelo', None, ('Mike', 'Mikey')),
            ('Donatello', None, 'Don'),
            ('Raphael', None, 'Raph'),
            ('Leonardo', None, 'Leo')
        ], default_ner='PER')

    painters = add_category_entities(kb, 'Renaissance Painter', [
            ('Michelangelo', None, u'Michelangelo di Lodovico Buonarroti Simoni'),
            ('Donatello', None, u'Donato di Niccolò di Betto Bardi'),
            ('Raphael', None, u'Raffaello Sanzio da Urbino'),
            ('Leonardo da Vinci', None, None),
        ], default_ner='PER')

    splinter = kb.add_entity(
            Entity('Splinter', 'Teenage Mutant Ninja Turtles'),
            EntityInfo('PER', ('Master Splinter',)))

    pizza = kb.add_entity(
        Entity('Pizza', 'Delicious'),
        EntityInfo('MISC', ()))

    renaissance = kb.add_entity(
        Entity('Renaissance', 'Cultural movement'),
        EntityInfo('MISC', ()))

    # Edges...
    kb.clique(turtles)
    kb.clique(painters)

    kb.associate_all(pizza, turtles)
    kb.associate_all(splinter, turtles)

    kb.associate_all(renaissance, painters)

    kb.associate(splinter, renaissance)
    
    return kb


if __name__ == '__main__':
    import sys
    import codecs

    # Set the output encoding to UTF-8.
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

    kb = create_knowledge_base()

    # PRINT DEM GRAPHS!
    if 'shingles' in sys.argv[1:2]:
        # TODO: This needs to be aware of Entity objects
        pairs = kb.entities.items()
        db = make_database(pairs)
        shingles_graph(db, pairs)
    else:
        kb_graph(kb)

