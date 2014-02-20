#!/usr/bin/env python
# coding: UTF-8

"""
A turtle-y example of knowledge bases and shingles.
"""

from shingles import shingles
from create_kb import KnowledgeBase, Entity, EntityInfo, \
        add_category_entities, \
        dot_graph as kb_graph

from entity_graph import make_database, \
    dot_graph as shingles_graph


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
            ('Michelangelo', None, 'Michelangelo di Lodovico Buonarroti Simoni'),
            ('Donatello', None, 'Donato di Niccolò di Betto Bardi'),
            ('Raphael', None, 'Raffaello Sanzio da Urbino'),
            ('Leonardo da Vinci', None, None),
        ], default_ner='PER')

    splinter = kb.add_entity(
            Entity('Splinter', 'Teenage Mutant Ninja Turtles'),
            EntityInfo('PER', ('Master Splinter')))

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
    kb = create_knowledge_base()

    # PRINT DEM GRAPHS!
    if 'shingles' in sys.argv[1:2]:
        # TODO: This needs to be aware of Entity objects
        db = make_database(name for name, category in kb.entities.keys())
        shingles_graph(db)
    else:
        kb_graph(kb)

