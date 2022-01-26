"""Assignment 1 - Distance map (Task 1)

CSC148, Winter 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

===== Module Description =====

This module contains the class DistanceMap, which is used to store
and look up distances between cities. This class does not read distances
from the map file. (All reading from files is done in module experiment.)
Instead, it provides public methods that can be called to store and look up
distances.
"""
from typing import Dict, Tuple


class DistanceMap:
    """The class representation of a distance map.

    === Private Attributes ===
    _record: a dictionary recording the distance between two cities.
    Each key is a tuple of the two cities and the value is the distance
    from the first city to another.

    === Representation Invariants ===
    The distance between two cities must be greater than 0

    """
    _record: Dict[Tuple[str, str], int]

    def __init__(self) -> None:
        """Initialize a distance map."""
        self._record = {}

    def add_distance(self, city1: str, city2: str, distance1: int,
                     distance2: int = -1) -> None:
        """ Record the distance between the first city <city1> and
        the second city <city2>.
        If distance2 == default value(-1), distance from <city2> to
        <city1> is distance1, otherwise distance2.

        >>> m = DistanceMap()
        >>> m.add_distance('a', 'b', 3, 4)
        >>> m._record[('b', 'a')] == 4
        True
        >>>  m._record[('a', 'b')] == 3
        True
        """
        if (city1, city2) not in self._record:
            self._record[(city1, city2)] = distance1
            if distance2 == -1:  # if distance2 == distance1
                self._record[(city2, city1)] = distance1
            else:
                self._record[(city2, city1)] = distance2

    def distance(self, city1: str, city2: str) -> int:
        """ Return the distance from the first city <city1>
        to the second <city2>. Return -1 if the distance is
        not stored in the distance map.

        >>> m = DistanceMap()
        >>> m.add_distance('a', 'b', 3, 4)
        >>> m.distance('a', 'b')
        3
        """
        if (city1, city2) in self._record:
            return self._record[(city1, city2)]
        return -1


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest

    doctest.testmod()
