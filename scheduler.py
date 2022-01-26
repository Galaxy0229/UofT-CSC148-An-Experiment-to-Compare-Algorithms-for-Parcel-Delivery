"""Assignment 1 - Scheduling algorithms (Task 4)

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

This module contains the abstract Scheduler class, as well as the two
subclasses RandomScheduler and GreedyScheduler, which implement the two
scheduling algorithms described in the handout.
"""
from typing import List, Dict, Union, Callable
from random import shuffle, choice
from container import PriorityQueue
from domain import Parcel, Truck


class Scheduler:
    """A scheduler, capable of deciding what parcels go onto which trucks, and
    what route each truck will take.

    This is an abstract class.  Only child classes should be instantiated.
    """

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the given <parcels> onto the given <trucks>, that is, decide
        which parcels will go on which trucks, as well as the route each truck
        will take.

        Mutate the Truck objects in <trucks> so that they store information
        about which parcel objects they will deliver and what route they will
        take.  Do *not* mutate the list <parcels>, or any of the parcel objects
        in that list.

        Return a list containing the parcels that did not get scheduled onto any
        truck, due to lack of capacity.

        If <verbose> is True, print step-by-step details regarding
        the scheduling algorithm as it runs.  This is *only* for debugging
        purposes for your benefit, so the content and format of this
        information is your choice; we will not test your code with <verbose>
        set to True.
        """
        raise NotImplementedError


class RandomScheduler(Scheduler):
    """The class representation of a random scheduler, which will go through the
    parcels in random order schedule each parcel onto a randomly chosen truck.

    This is a subclass of Scheduler.
    """
    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:

        """Schedule the given <parcels> onto the given <trucks>, that is, decide
        which parcels will go on which trucks randomly, as well as the route
        each truck will take.

        This is a method that overrides the superclass Scheduler's method.

        Mutate the Truck objects in <trucks> so that they store information
        about which parcel objects they will deliver and what route they will
        take.  Do *not* mutate the list <parcels>, or any of the parcel objects
        in that list.

        Return a list containing the parcels that did not get scheduled onto any
        truck, due to lack of capacity.

        If <verbose> is True, print step-by-step details regarding
        the scheduling algorithm as it runs. This is *only* for debugging
        purposes for your benefit, so the content and format of this
        information is your choice; we will not test your code with <verbose>
        set to True.
        """
        result = []
        parcels_copy = parcels[:]
        shuffle(parcels_copy)
        for parcel in parcels_copy:
            t = choice(trucks)
            n = 0
            while parcel.volume > t.available_space and n <= len(trucks):
                n += 1
                t = choice(trucks)
            if n <= len(trucks):
                t.pack(parcel)
            else:
                result.append(parcel)
        return result


def _get_eligible_trucks(trucks: List[Truck], parcel: Parcel) -> List[Truck]:
    """Return a list of trucks that is eligible to pack the parcel.

    This is a helper method for schedule.
    """
    eligible_trucks = []  # set a list of all eligible trucks
    destination_trucks = []
    # find trucks with enough unused volume for the parcel
    # record it into the eligible list
    for truck in trucks:
        if parcel.volume <= truck.available_space:
            eligible_trucks.append(truck)
    # find trucks with same destination as parcel from the eligible list
    for truck in eligible_trucks:
        if parcel.destination == truck.routes[-1]:
            destination_trucks.append(truck)
    if destination_trucks:
        eligible_trucks = destination_trucks
    return eligible_trucks


class GreedyScheduler(Scheduler):
    """The class representation of a greedy scheduler, which processes parcels
     one at a time, picking a truck for each, but it tries to pick the “best”
     truck it can for each parcel.

     This is a subclass of scheduler.

    === Private Attributes ===
    _parcel_priority: a string contains the priority to proceed parcels
    _parcel_order: a string contains the order to proceed parcels
    _truck_order: a string contains the order to proceed trucks

    === Representation Invariants ===
    _parcel_priority can only be 'volume' or 'destination'
    _parcel_order can only be 'non-decreasing' or 'non-increasing'
    _truck_order can only be 'non-decreasing' or 'non-increasing'
    """
    _parcel_priority: str
    _parcel_order: str
    _truck_order: str

    def __init__(self, config: Dict[str, Union[str, bool]]) -> None:
        """Initialize a greedy scheduler
        """
        self._parcel_priority = config['parcel_priority']
        self._parcel_order = config['parcel_order']
        self._truck_order = config['truck_order']

    def _get_parcel_order(self) -> Callable[[Parcel, Parcel], bool]:
        """Return the corresponding function of parcel order.

        This is a helper method
        """
        if self._parcel_priority == 'destination':
            if self._parcel_order == 'non-decreasing':
                return _destination_non_decreasing
            return _destination_non_increasing
        if self._parcel_order == 'non-decreasing':
            return _volume_non_decreasing
        return _volume_non_increasing

    def _get_truck_order(self) -> Callable[[Truck, Truck], bool]:
        """Return the corresponding function of truck order.

        This is a helper method.
        """
        if self._truck_order == 'non-decreasing':
            return _least_available
        return _most_available

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:

        """Schedule the given <parcels> onto the given <trucks>, that is, decide
        which parcels will go on which trucks by greedy algorithm, as well as
        the route each truck will take.

        This is a method that overrides the superclass Scheduler's method.

        Mutate the Truck objects in <trucks> so that they store information
        about which parcel objects they will deliver and what route they will
        take.  Do *not* mutate the list <parcels>, or any of the parcel objects
        in that list.

        Return a list containing the parcels that did not get scheduled onto any
        truck, due to lack of capacity.

        If <verbose> is True, print step-by-step details regarding
        the scheduling algorithm as it runs. This is *only* for debugging
        purposes for your benefit, so the content and format of this
        information is your choice; we will not test your code with <verbose>
        set to True.

        """
        if verbose:
            print('--------------START----------------')
        result = []
        parcels_copy = parcels[:]  # make a copy of the parcels
        ordered_parcel = PriorityQueue(self._get_parcel_order())
        # add the item from copied parcels to the parcel priority queue
        for parcel in parcels_copy:
            ordered_parcel.add(parcel)
        while not ordered_parcel.is_empty():
            parcel = ordered_parcel.remove()
            if verbose:
                print('Chosen parcel:', parcel)
            # use the helper function below to get a list of eligible trucks
            eligible_trucks = _get_eligible_trucks(trucks, parcel)
            # add the item from copied parcels to the truck priority queue
            ordered_truck = PriorityQueue(self._get_truck_order())
            for truck in eligible_trucks:
                ordered_truck.add(truck)
            if not ordered_truck.is_empty():
                truck = ordered_truck.remove()
                if verbose:
                    print('The truck the parcel is being packed:', truck)
                    print('---------------------------------------------')
                truck.pack(parcel)
            else:
                result.append(parcel)
                if verbose:
                    print('Parcel cannot be packed.')
                    print('---------------------------------------------')
        return result


def _volume_non_decreasing(parcel1: Parcel, parcel2: Parcel) -> bool:
    """The priority function that puts the parcels by volume
    with non-decreasing order.
    """
    return parcel2.volume > parcel1.volume


def _volume_non_increasing(parcel1: Parcel, parcel2: Parcel) -> bool:
    """The priority function that puts the parcels by volume
    with non-increasing order.
    """
    return parcel1.volume > parcel2.volume


def _destination_non_decreasing(parcel1: Parcel, parcel2: Parcel) -> bool:
    """The priority function that puts the parcels by destination
    with non-decreasing order.
    """
    return parcel2.destination > parcel1.destination


def _destination_non_increasing(parcel1: Parcel, parcel2: Parcel) -> bool:
    """The priority function that puts the parcels by destination
    with non-increasing order.
    """
    return parcel1.destination > parcel2.destination


def _most_available(truck1: Truck, truck2: Truck) -> bool:
    """The priority function that puts the trucks by their
    available space with non-increasing order.
    """
    return truck1.available_space > truck2.available_space


def _least_available(truck1: Truck, truck2: Truck) -> bool:
    """The priority function that puts the trucks by their
    available space with non-decreasing order.
    """
    return truck2.available_space > truck1.available_space


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['compare_algorithms'],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'random', 'container', 'domain'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
