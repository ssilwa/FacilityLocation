A fast Python implementation of the Mettu Plaxton (MP) algorithm for the facility location problem given in the paper `The online median problem' by Mettu and Plaxton. The algorithm returns a 3 approximation to the solution, meaning that the cost of the returned solution is at most 3 times the cost of the optimum solution.


## Problem Description:

Given a set S of N points in R^d, the goal is to select a subset F of centers to minimize the objective |F| + \sum_{p \in S} d(p, F) where d(p, F) is the minimum distance from p to its nearest point in F. 


## Further Details:

Any 'opening cost' c can be inputted into the algorithm which means changing the objective from |F| to c*|F|. The objective function is similar to k-median or k-means clustering except we charge for opening each center so the number of centers is variable (and depends on the parameter c).

The main computational bottleneck is calculating all pairs distance between the set of points. While we use the scipy implementaiton, this step can be made parallel if needed to speed up the computation. 

## Sample Usage:
```python
N = 100 # number of points
d = 25  # dimension
points = np.random.random((N, d)) # generate some random points
distance = distance_matrix(points, points)  # calculate distance matrix   
distance_sorted = np.copy(distance)
distance_sorted.sort(axis=1) # sorted distance matrix along rows
cost = 1 # cost to open a facility
centers, total_cost = MP_alg(distance_sorted, distance, points, cost) # returns the centers and the objective value
```

