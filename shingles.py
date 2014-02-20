#!/usr/bin/env python
# coding: UTF-8

from itertools import islice, izip, chain

# Returns a set of shingles for the given entity.
def shingles(entity, w=3):
    u"""
    Performs charachter-wise shingling on an entity. Natural language
    processing!  Returns the (frozen) set of all shingles for a given entity.

    >>> shingles('herp') == {'her', 'erp'}
    True
    >>> shingles('derp') == {'der', 'erp'}
    True
    >>> shingles('AM')
    frozenset(['am'])
    >>> shingles('Herp derp') == {'her', 'der', 'erp'}
    True
    >>> shingles(u'Naïve') == {u'naï', u'aïv', u'ïve'}
    True
    """

    normalized = entity.strip().lower()
    if len(normalized) <= w:
        return frozenset((normalized,))

    # An entity may be made of several components.
    components = normalized.split()

    def shinglingle(component):
        slices = (islice(component, i, None) for i in xrange(w))
        return (''.join(chars) for chars in izip(*slices))

    comp_shingles = (shinglingle(comp) for comp in components)
    # Flatten the iterable of all shingles.
    result = frozenset(chain.from_iterable(comp_shingles))
    return result

def jaccard_index(a, b):
    """
    Finds the similarty of two sets as defined by the Jaccard index.

    Intended for use with :py:func:`shingles`.

    >>> jaccard_index({'cats'}, {'dogs'})
    0.0
    >>> jaccard_index({'foo', 'bar', 'baz'}, {'foo', 'bar', 'baz'})
    1.0
    >>> jaccard_index(shingles('herp'), shingles('derp')) == 1.0 / 3.0
    True
    >>> 0 < jaccard_index(shingles('Benedict Cumberbatch'),
    ...                   shingles('Benadryl Cumbersnatch')) < 1.0 / 3.0
    True
    """

    if 0 == len(a) == len(b):
        return 1

    return  len(a & b) / float(len(a | b))



if __name__ == '__main__':
    import doctest
    import sys
    doctest.testmod(verbose='-v' in sys.argv[1:])

