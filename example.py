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
        Entity('Renaissance', 'Historial era'),
        EntityInfo('MISC', ()))

    # Edges...
    kb.clique(turtles)
    kb.clique(painters)

    kb.associate_all(pizza, turtles)
    kb.associate_all(splinter, turtles)

    kb.associate_all(renaissance, painters)

    kb.associate(splinter, renaissance)

    return kb

def make_d3_obj(kb, db):
    """
    Makes an object suitable for export as a D3 JSON object for a
    force-directed layout.
    """
    entity_map, edges = kb.graph

    entities = [{'name': name, 'cat': category}
                for name, category in entity_map]
    trigrams = [{'shingle': text} for text in db]
    nodes = entities + trigrams

    # Link map is needed to map a node item to its index in the node
    # array/list.
    link_map = {entity: count
            for count, entity in enumerate(entity_map)}
    link_map.update({text: count
            for count, text in enumerate(db, len(entities))})

    links = []
    for src, dests in db.items():
        for dest in dests:
            links.append({
                'source': link_map[src],
                'target': link_map[dest],
                'value': 1} # TODO: value based on frequency.
            )

    return {'nodes': nodes, 'links': links}

if __name__ == '__main__':
    import sys
    import codecs

    # Set the output encoding to UTF-8.
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

    kb = create_knowledge_base()
    pairs = kb.entities.items()
    db = make_database(pairs)

    # PRINT DEM GRAPHS!
    if 'shingles' in sys.argv[1:2]:
        shingles_graph(db, pairs)
    elif 'json' in sys.argv[1:2]:
        import json
        d3_obj = make_d3_obj(kb, db)
        print(json.dumps(d3_obj))
    else:
        kb_graph(kb)

