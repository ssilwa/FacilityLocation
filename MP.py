import numpy as np
from scipy.spatial import distance_matrix
import time


########### Code for MP algorithm implementation ###########


# Supplementary Functions

def binary_search(arr, high, low, cost, tol):
    while high-low > 1:
        med = (low+high)//2
        curr_sum = (med+1)*arr[med]- arr[0:med+1].sum() 
        if abs(curr_sum - cost) <= tol:
            return med
        elif curr_sum < cost:
            low = med
        else:
            high = med

    high_sum = (high+1)*arr[high]- arr[0:high+1].sum() 
        
    if high_sum > cost + tol:
        return low
    else:
        return high

def calculate_radius(arr, indx, cost):
    curr_sum = (indx+1)*arr[indx]-arr[0:indx+1].sum() 
    diff = cost-curr_sum
    radius = arr[indx] + diff/(indx+1)
    return radius


def calculate_total_cost(distance, centers, N):
    return distance[:, centers].min(axis=1).sum()


# MP Algorithm
#####
# Input: distance, points, cost
# distance_sorted: N by N distance matrix sorted by rows, increasing
# distance: N by N distance matrix
# points: N by d array of points
# cost: opening cost of a facility
#####
# Output: indices of the chosen centers and facility location cost = distance cost + opening costs and the centers
#####
def MP_alg(distance_sorted, distance, points, cost):
    N = points.shape[0]    # get number of points
    radii = []             # initialize array for radii
    centers = []           # initialize array for centers
    
    for i in range(N):     # calculate the radii
        curr_array = distance_sorted[i,:]
        curr_indx = binary_search(curr_array, N, 0, cost, 1e-10)
        curr_radius = calculate_radius(curr_array, curr_indx, cost)
        radii.append((i, curr_radius))

    radii = sorted(radii, key = lambda t: t[1])   # sort radii from smallest to largest
    
    for tup in radii:   # greedily select centers
        curr_index = tup[0]
        curr_radii = tup[1]
        curr_point = points[curr_index]
        if len(centers) == 0:
            centers.append(curr_index)
        else:
            curr_cost = distance[curr_index, centers].min()
            if curr_cost > 2*curr_radii:
                centers.append(curr_index)
                
    total_cost =  distance[:, centers].min(axis=1).sum() + len(centers)*cost
    
    return (centers, total_cost)

# An example:
if __name__ == '__main__':
    N = 100 # number of points
    d = 25  # dimension
    points = np.random.random((N, d)) # get our points
    distance = distance_matrix(points, points)  # calculate distance matrix   
    distance_sorted = np.copy(distance)
    distance_sorted.sort(axis=1) # sorted distance matrix along rows
    cost = 1 # cost to open a facility
    start = time.time()
    centers, total_cost = MP_alg(distance_sorted, distance, points, cost)
    print(time.time()-start)

