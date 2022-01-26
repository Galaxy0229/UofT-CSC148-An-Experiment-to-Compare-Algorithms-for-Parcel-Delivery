# UofT-CSC148-An-Experiment-to-Compare-Algorithms-for-Parcel-Delivery

Introduction
Consider what happens when a delivery company like FedEx or Purolator receives a plane load of parcels at Pearson Airport to be delivered by truck to cities all over southern Ontario. They have to schedule the parcels for delivery by assigning parcels to trucks and determining the route each truck will take to make its deliveries.

Depending on how well these decisions are made, trucks may be well-packed and have short, efficient routes, or trucks may not be fully filled and may have to travel unnecessary distances.

For this assignment, you will write code to try out different algorithms to perform parcel scheduling and compare their performance.

Problem description
Be sure to read through this section carefully. Your Python code must accurately model all of the details described here.

The parcel delivery domain
Each parcel has a source and a destination, which are the name of the city the parcel came from and the name of the city where it must be delivered to, respectively. Each parcel also has a volume, which is a positive integer, measured in units of cubic centimetres (cc).

Each truck can store multiple parcels, but has a volume capacity, which is also a positive integer and is in units of cc. The sum of the volumes of the parcels on a truck cannot exceed its volume capacity. Each truck also has a route, which is an ordered list of city names that it is scheduled to travel through.

Each parcel has a unique ID, that is, no two parcels can have the same ID. Each truck also has a unique ID, that is, no two trucks can have the same ID.

Depot
There is a special city that all parcels and trucks start from, and all trucks return to at the end of their route. We’ll refer to this city as the depot. (You can imagine all parcels have been shipped from their source city to the depot.) Our algorithms will schedule delivery of parcels from the depot to their destinations.

You may assume that no parcels have the depot as their destination.

There is only one depot.

Truck routes
All trucks are initially empty and only have the depot on their route (since it is their initial location). A truck’s route is determined as follows: When a parcel is scheduled to be delivered by a truck, that parcel’s destination is added to the end of the truck’s route, unless that city is already the last destination on the truck’s route.

Example: Consider a truck at the start of the simulation, and suppose that the depot is Toronto. The truck’s route at that point is just Toronto. Now suppose parcels are packed onto that truck in this order:

a parcel going to Windsor. The truck’s route is now Toronto, Windsor.
another parcel going to Windsor. The truck’s route is unchanged.
a parcel going to London. The truck’s route is now Toronto, Windsor, London.
a parcel going to Windsor. The truck’s route becomes Toronto, Windsor, London, Windsor. (Yes, this is a silly route, so the order in which we pack parcels onto trucks is going to matter.)
Whatever its route, at the end, a truck must return directly to the depot.

Scheduling parcels
You will implement two different algorithms for choosing which parcels go onto which trucks, and in what order. As we saw above, this will determine the routes of all the trucks.

(1) Random algorithm
The random algorithm will go through the parcels in random order. For each parcel, it will schedule it onto a randomly chosen truck (from among those trucks that have capacity to add that parcel). Because of this randomness, each time you run your random algorithm on a given problem, it may generate a different solution.

(2) Greedy algorithm
The greedy algorithm tries to be more strategic. Like the random algorithm, it processes parcels one at a time, picking a truck for each, but it tries to pick the “best” truck it can for each parcel. Our greedy algorithm is quite short-sighted: it makes each choice without looking ahead to possible consequences of the choice (that’s why we call it “greedy”).

The greedy algorithm has two configurable features: the order in which parcels are considered, and how a truck is chosen for each parcel. These are described below.

Parcel order
There are four possible orders that the algorithm could use to process the parcels:

In order by parcel volume, either smallest to largest (non-decreasing) or largest to smallest (non-increasing).
In order by parcel destination, either smallest to largest (non-decreasing) or largest to smallest (non-increasing). Since destinations are strings, larger and smaller is determined by comparing strings (city names) alphabetically.
Ties are broken using the order in which the parcels are read from our data file (see below).

Truck choice
When the greedy algorithm processes a parcel, it must choose which truck to assign it to. The algorithm first does the following to compute the eligible trucks:

It only considers trucks that have enough unused volume to add the parcel.
Among these trucks, if there are any that already have the parcel’s destination at the end of their route, only those trucks are considered. Otherwise, all trucks that have enough unused volume are considered.
Given the eligible trucks, the algorithm can be configured one of two ways to make a choice:

choose the eligible truck with the most available space, or
choose the eligible truck with the least available space
Ties are broken using the order in which the trucks are read from our data file. If there are no eligible trucks, then the parcel is not scheduled onto any truck.

Observations about the Greedy Algorithm
Since there are four options for parcel priority and two options for truck choice, our greedy algorithm can be configured eight different ways in total.

Notice that there is no randomness in the greedy algorithm; it is completely “deterministic”. This means that no matter how many times you run your greedy algorithm on a given problem, it will always generate the same solution.

Putting it all together
For this assignment, your program will create an experiment by reading in some parcel, truck, and configuration data from a set of files. Your code will be able to apply the random algorithm or any of the variations of the greedy algorithm to a scheduling problem, and then report on statistics of interest, such as the average distance travelled by the trucks. This would allow the delivery company to compare the algorithms and decide which is best, given the company’s priorities.
