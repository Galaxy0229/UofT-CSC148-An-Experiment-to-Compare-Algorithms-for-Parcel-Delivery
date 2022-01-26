"""Assignment 1 - Domain classes (Task 2)

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

This module contains the classes required to represent the entities
in the simulation: Parcel, Truck and Fleet.
"""
from typing import List, Dict
from distance_map import DistanceMap


class Parcel:
    """The class representation of a parcel.

    === Public Attributes ===
    id: the id of the parcel.
    volume: the volume of the parcel, measured in units of cubic centimetres
    (cc).
    source: the name of the city the parcel came from.
    destination: the name of the city where it must be delivered to.

    === Representation Invariants ===
    volume is a positive integer
    id is unique

    """
    id: int
    volume: int
    source: str
    destination: str

    def __init__(self, id_: int, volume: int, source: str, destination: str) \
            -> None:
        """Initialize a parcel.
        """
        self.id = id_
        self.volume = volume
        self.source = source
        self.destination = destination

    def __str__(self) -> str:
        """Produce a string representation of this parcel.
        """
        return f'Parcel - id: {self.id}, volume: {self.volume}, {self.source}' \
               f' -> {self.destination}'


class Truck:
    """The class representation of a truck.

    === Public Attributes ===
    id: the id of the truck.
    capacity: the volume capacity of the parcel, measured in units of cubic
    centimetres (cc)
    depot: the city the truck starts from, and returns to at the end of their
    route
    parcels: the list of parcels in the truck
    routes: an ordered list of city names that the truck is scheduled to travel
    through
    available_space: the volume of the available space in the truck

    === Representation Invariants ===
    capacity is a positive integer
    id is unique

    """
    id: int
    capacity: int
    depot: str
    parcels: List[Parcel]
    routes: List[str]
    available_space: int

    def __init__(self, id_: int, capacity: int, depot: str) -> None:
        """Initialize a truck."""
        self.id = id_
        self.capacity = capacity
        self.depot = depot
        self.parcels = []
        self.routes = [depot]
        self.available_space = capacity

    def __str__(self) -> str:
        """Produce a string representation of this truck.
        """
        return f'Truck - id: {self.id}, capacity: {self.capacity}, depot: ' \
               f'{self.depot}'

    def add_route(self, parcel: Parcel) -> None:
        """Record the destination of the given parcel

        >>> p = Parcel(1, 2, 'Toronto', 'Vancouver')
        >>> t = Truck(1, 10, 'Toronto')
        >>> t.add_route(p)
        >>> t.routes
        ['Toronto', 'Vancouver']
        """
        if parcel.destination != self.routes[-1]:
            self.routes.append(parcel.destination)

    def _sum_parcels_volume(self) -> int:
        """Return the total volumes of parcels in the truck.

        >>> p = Parcel(1, 2, 'Toronto', 'Vancouver')
        >>> t = Truck(1, 10, 'Toronto')
        >>> t._sum_parcels_volume()
        2
        """
        total_volume = 0
        for parcel in self.parcels:
            total_volume += parcel.volume
        return total_volume

    def pack(self, parcel: Parcel) -> bool:
        """Return True if the parcel was successfully packed onto the truck.
        Otherwise return False.

        Precondition: No parcel with the same ID as <parcel> has already been
        added to this Truck.

        >>> p = Parcel(1, 2, 'Toronto', 'Vancouver')
        >>> t = Truck(1, 10, 'Toronto')
        >>> t.pack(p)
        True
        """
        total_volume = self._sum_parcels_volume()
        if total_volume + parcel.volume > self.capacity:
            return False
        self.parcels.append(parcel)
        self.add_route(parcel)
        self.available_space = self.capacity - self._sum_parcels_volume()
        return True

    def fullness(self) -> float:
        """Return the current capacity of the truck.

        >>> p = Parcel(1, 2, 'Toronto', 'Vancouver')
        >>> t = Truck(1, 10, 'Toronto')
        >>> t.pack(p)
        >>> t.fullness()
        20.0
        """
        return float((self._sum_parcels_volume() / self.capacity) * 100)


class Fleet:
    """ A fleet of trucks for making deliveries.

    ===== Public Attributes =====
    trucks:
      List of all Truck objects in this fleet.
    """
    trucks: List[Truck]

    def __init__(self) -> None:
        """Create a Fleet with no trucks.

        >>> f = Fleet()
        >>> f.num_trucks()
        0
        """
        self.trucks = []

    def add_truck(self, truck: Truck) -> None:
        """Add <truck> to this fleet.

        Precondition: No truck with the same ID as <truck> has already been
        added to this Fleet.

        >>> f = Fleet()
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> f.add_truck(t)
        >>> f.num_trucks()
        1
        """
        self.trucks.append(truck)

    # We will not test the format of the string that you return -- it is up
    # to you.
    def __str__(self) -> str:
        """Produce a string representation of this fleet
        """
        result = '------START------'
        for truck in self.trucks:
            result += str(truck) + '\n'
        result += '------END------'
        return result

    def num_trucks(self) -> int:
        """Return the number of trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> f.num_trucks()
        1
        """
        return len(self.trucks)

    def num_nonempty_trucks(self) -> int:
        """Return the number of non-empty trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> p2 = Parcel(2, 4, 'Toronto', 'Montreal')
        >>> t1.pack(p2)
        True
        >>> t1.fullness()
        90.0
        >>> t2 = Truck(5912, 20, 'Toronto')
        >>> f.add_truck(t2)
        >>> p3 = Parcel(3, 2, 'New York', 'Windsor')
        >>> t2.pack(p3)
        True
        >>> t2.fullness()
        10.0
        >>> t3 = Truck(1111, 50, 'Toronto')
        >>> f.add_truck(t3)
        >>> f.num_nonempty_trucks()
        2
        """
        num = 0
        for truck in self.trucks:
            if truck.parcels:
                num += 1
        return num

    def parcel_allocations(self) -> Dict[int, List[int]]:
        """Return a dictionary in which each key is the ID of a truck in this
        fleet and its value is a list of the IDs of the parcels packed onto it,
        in the order in which they were packed.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(27, 5, 'Toronto', 'Hamilton')
        >>> p2 = Parcel(12, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t1.pack(p2)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p3 = Parcel(28, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p3)
        True
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.parcel_allocations() == {1423: [27, 12], 1333: [28]}
        True
        """
        result = {}
        for truck in self.trucks:
            result[truck.id] = []
            if truck.parcels:
                for parcel in truck.parcels:
                    result[truck.id].append(parcel.id)
        return result

    def total_unused_space(self) -> int:
        """Return the total unused space, summed over all non-empty trucks in
        the fleet.
        If there are no non-empty trucks in the fleet, return 0.

        >>> f = Fleet()
        >>> f.total_unused_space()
        0
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.total_unused_space()
        995
        """
        total = 0
        for truck in self.trucks:
            if truck.parcels:
                total += truck.available_space
        return total

    def _total_fullness(self) -> float:
        """Return the sum of truck.fullness() for each non-empty truck in the
        fleet. If there are no non-empty trucks, return 0.

        >>> f = Fleet()
        >>> f._total_fullness() == 0.0
        True
        >>> t = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t)
        >>> f._total_fullness() == 0.0
        True
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f._total_fullness()
        50.0
        """
        total = 0
        for truck in self.trucks:
            if truck.parcels:
                total += truck.fullness()
        return total

    def average_fullness(self) -> float:
        """Return the average percent fullness of all non-empty trucks in the
        fleet.

        Precondition: At least one truck is non-empty.

        >>> f = Fleet()
        >>> t = Truck(1423, 10, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.average_fullness()
        50.0
        """
        n = 0
        for truck in self.trucks:
            if truck.parcels:
                n += 1
        return self._total_fullness() / n

    def total_distance_travelled(self, dmap: DistanceMap) -> int:
        """Return the total distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Precondition: <dmap> contains all distances required to compute the
                      average distance travelled.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.total_distance_travelled(m)
        36
        """
        total_distance = 0
        for truck in self.trucks:
            if truck.parcels:
                for i in range(0, len(truck.routes) - 1):
                    total_distance += dmap.distance(truck.routes[i],
                                                    truck.routes[i + 1])
                total_distance += dmap.distance(truck.routes[-1],
                                                truck.routes[0])
        return total_distance

    def average_distance_travelled(self, dmap: DistanceMap) -> float:
        """Return the average distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Include in the average only trucks that have actually travelled some
        non-zero distance.

        Preconditions:
        - <dmap> contains all distances required to compute the average
          distance travelled.
        - At least one truck has travelled a non-zero distance.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.average_distance_travelled(m)
        18.0
        """
        n = 0
        for truck in self.trucks:
            if truck.parcels:
                n += 1
        return float(self.total_distance_travelled(dmap) / n)


if __name__ == '__main__':
    # import python_ta
    # python_ta.check_all(config={
    #     'allowed-import-modules': ['doctest', 'python_ta', 'typing',
    #                                'distance_map'],
    #     'disable': ['E1136'],
    #     'max-attributes': 15,
    # })
    # import doctest
    # doctest.testmod()
    p = Parcel(1, 2, 'A', 'B')
    print(p)
