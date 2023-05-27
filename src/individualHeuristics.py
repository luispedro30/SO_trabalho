import os, json, re
import solverInstance
import xlsxwriter 
import cython
import random 
import numpy as np
import time
from time import perf_counter

"""
Generates a random solution to to a given instance of a uncapacitated facility location problem 
First select and open a random number of facilities 
Then extract a solution array from the open set of facilities

Parameters
    f: Number of facilities in problem
    c: Number of customers in problem
    d: 2D Array of distances 
Returns 
    Array of length c with entries in range f. Corresponds to selected facility for customer
Description 
    Takes problem input instances and randomly generates a feasible solution 
"""
def solve(numCustomers, numFacilities, customersDemand, customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts):
    facilities_factor = []
    served_customers = []
    for x in range(numFacilities):
        facilities_factor.append(facilitiesOpeningCost[x]/facilitiesInitialCapacity[x])

    for x in facilitiesOpeningCost:
        if len(served_customers) < numCustomers:
            optimal_facility_index = np.argmin(facilities_factor)
            facilities_factor[optimal_facility_index] += 100
            facilities_factor[optimal_facility_index] *= 100
            facilitiesIsOpen[optimal_facility_index] = True
            for y in customersTransportationCost:
                if facilitiesCurrentCapacity == 0:
                    break
                elif (customersDemand[y] <= facilitiesCurrentCapacity[optimal_facility_index] and y not in served_customers):
                    facilitiesCustomers[optimal_facility_index].append(y)
                    customersIsSatisfied[y] = True
                    customersFacilityAllocated[y] = optimal_facility_index
                    facilitiesCurrentCapacity[optimal_facility_index] -= customersDemand[y]
                    served_customers.append(y)
        else:
            break
    

    facilitesTotalCost = {}
    for facility in facilitiesCustomers:
        somaFacility = 0
        #print(facilitiesCustomers[facility])
        if facilitiesCustomers[facility]:
            for customer in facilitiesCustomers[facility]:
                somaFacility += transportationCosts[customer][facility]
            somaFacility += facilitiesOpeningCost[facility]
        facilitesTotalCost[facility]= somaFacility

    sumTotal = 0
    for facility in facilitesTotalCost:
        sumTotal += facilitesTotalCost[facility]
    
    print(facilitiesCurrentCapacity)
    print(facilitiesCustomers)
    print(facilitiesIsOpen)
    print(customersIsSatisfied)
    print(customersFacilityAllocated)

    return sumTotal

def findMinimumTransportClient(transportationCosts, clientIndex):
    minIndex = transportationCosts[clientIndex].index(min(transportationCosts[clientIndex]))
    return minIndex

def greedy(numCustomers, numFacilities, customersDemand, customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts):
    facilities_factor = []
    list_customers = []
    served_customers = []
    for x in range(numFacilities):
        facilities_factor.append(x)
    
    for x in range(numCustomers):
        list_customers.append(x)

    random_customers = random.sample(list_customers, k=len(list_customers))

    sorted_dict = dict(sorted(facilitiesOpeningCost.items(), key=lambda x: x[1]))

    sorted_dict_customer = dict(sorted(customersDemand.items(), key=lambda x: x[1]))
    for x, value in sorted_dict.items():
        if len(served_customers) < numCustomers:
            optimal_facility_index = x
            facilitiesIsOpen[optimal_facility_index] = True
            for y in range(numCustomers):   
                if facilitiesCurrentCapacity == 0:
                    break
                if (customersDemand[y] <= facilitiesCurrentCapacity[x] and y not in served_customers):
                    facilitiesCustomers[x].append(y)
                    customersIsSatisfied[y] = True
                    customersFacilityAllocated[y] = x
                    facilitiesCurrentCapacity[x] -= customersDemand[y]
                    served_customers.append(y)
        else:
            break
    

    facilitesTotalCost = {}
    for facility in facilitiesCustomers:
        somaFacility = 0
        if facilitiesCustomers[facility]:
            for customer in facilitiesCustomers[facility]:
                somaFacility += transportationCosts[customer][facility]
            somaFacility += facilitiesOpeningCost[facility]
        facilitesTotalCost[facility]= somaFacility

    sumTotal = 0
    for facility in facilitesTotalCost:
        sumTotal += facilitesTotalCost[facility]
    
    print(facilitiesCurrentCapacity)
    print(facilitiesCustomers)
    print(facilitiesIsOpen)
    print(customersIsSatisfied)
    print(customersFacilityAllocated)

    return sumTotal


def sol(numCustomers, numFacilities, customersDemand, customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts):
    served_customers = []

    sorted_dict = dict(sorted(facilitiesOpeningCost.items(), key=lambda x: x[1]))

    for j in range(numCustomers):
        min_cost = float('inf')
        selected_facility = -1

        # Find the facility with the minimum transportation cost
        for i in range(numFacilities):
            if i not in served_customers and facilitiesCurrentCapacity[i] >= customersDemand[j]:
                cost = transportationCosts[j][i]
                if cost < min_cost:
                    min_cost = cost
                    facilitiesCustomers[i].append(j)
                    customersIsSatisfied[j] = True
                    customersFacilityAllocated[i] = j
                    facilitiesCurrentCapacity[i] -= customersDemand[j]
                    served_customers.append(j)
    
    facilitesTotalCost = {}
    for facility in facilitiesCustomers:
        somaFacility = 0
        #print(facilitiesCustomers[facility])
        if facilitiesCustomers[facility]:
            for customer in facilitiesCustomers[facility]:
                somaFacility += transportationCosts[customer][facility]
            somaFacility += facilitiesOpeningCost[facility]
        facilitesTotalCost[facility]= somaFacility

    sumTotal = 0
    for facility in facilitesTotalCost:
        sumTotal += facilitesTotalCost[facility]
    
    print(facilitiesCurrentCapacity)
    print(facilitiesCustomers)
    print(facilitiesIsOpen)
    print(customersIsSatisfied)
    print(customersFacilityAllocated)

    return sumTotal

def localSearchSolveShift(numCustomers, numFacilities, customersDemand, customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts):
    start_time = time.time()  # Start the timer
    for customer in range(numCustomers):
        for facility in range(numFacilities):
            if  (facilitiesIsOpen[facility] == False or not facilitiesCustomers[facility] or customersDemand[customer] > facilitiesCurrentCapacity[facility]):
                continue
            
            chosen_facility = customersFacilityAllocated[customer]
            if chosen_facility != None:
                if transportationCosts[customer][facility] < transportationCosts[customer][chosen_facility]:
                    facilitiesCustomers[chosen_facility].remove(customer)
                    facilitiesCurrentCapacity[chosen_facility] += customersDemand[customer]
                    customersIsSatisfied[customer] == False

                    facilitiesCustomers[facility].append(customer)
                    customersIsSatisfied[customer] = True
                    customersFacilityAllocated[customer] = facility
                    facilitiesCurrentCapacity[facility] -= customersDemand[customer]

    facilitesTotalCost = {}
    for facility in facilitiesCustomers:
        somaFacility = 0
        if facilitiesCustomers[facility]:
            for customer in facilitiesCustomers[facility]:
                somaFacility += transportationCosts[customer][facility]
            somaFacility += facilitiesOpeningCost[facility]
        facilitesTotalCost[facility]= somaFacility

    sumTotal = 0
    for facility in facilitesTotalCost:
        sumTotal += facilitesTotalCost[facility]

    print(facilitiesCurrentCapacity)
    print(facilitiesCustomers)
    print(customersIsSatisfied)
    print(customersFacilityAllocated)
    elapsed_time = time.time() - start_time
    #print("Elapsed Time:", elapsed_time, "seconds")

    return sumTotal

def localSearchSolveSwaft(numCustomers, numFacilities, customersDemand, customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts):
    start_time = time.time()  # Start the timer
    pairs_verified = []
    for customer_a in range(numCustomers):
        for customer_b in range(numCustomers):
            if customer_a == customer_b or (customer_a, customer_b) in pairs_verified or \
                    (customer_b, customer_a) in pairs_verified:
                continue
            chosen_facility_a = customersFacilityAllocated[customer_a]
            chosen_facility_b = customersFacilityAllocated[customer_b]

            if customersDemand[customer_b] <= customersDemand[customer_a] + facilitiesCurrentCapacity[chosen_facility_a]:
                continue

            if transportationCosts[customer_a][chosen_facility_a] <= transportationCosts[customer_a][chosen_facility_b] or transportationCosts[customer_b][chosen_facility_b] <= transportationCosts[customer_b][chosen_facility_a]:
                continue
            
            pairs_verified.append((customer_a, customer_b))
            facilitiesCustomers[chosen_facility_a].remove(customer_a)
            facilitiesCurrentCapacity[chosen_facility_a] += customersDemand[customer_a]
            customersIsSatisfied[customer_a] == False
            
            facilitiesCustomers[chosen_facility_b].remove(customer_b)
            facilitiesCurrentCapacity[chosen_facility_b] += customersDemand[customer_b]
            customersIsSatisfied[customer_b] == False

            facilitiesCustomers[chosen_facility_a].append(customer_b)
            customersIsSatisfied[customer_b] = True
            customersFacilityAllocated[customer_b] = chosen_facility_a
            facilitiesCurrentCapacity[chosen_facility_a] -= customersDemand[customer_b]

            facilitiesCustomers[chosen_facility_b].append(customer_a)
            customersIsSatisfied[customer_a] = True
            customersFacilityAllocated[customer_a] = chosen_facility_b
            facilitiesCurrentCapacity[chosen_facility_b] -= customersDemand[customer_a]

    facilitesTotalCost = {}
    for facility in facilitiesCustomers:
        somaFacility = 0
        if facilitiesCustomers[facility]:
            for customer in facilitiesCustomers[facility]:
                somaFacility += transportationCosts[customer][facility]
            somaFacility += facilitiesOpeningCost[facility]
        facilitesTotalCost[facility]= somaFacility

    sumTotal = 0
    for facility in facilitesTotalCost:
        sumTotal += facilitesTotalCost[facility]

    print(facilitiesCurrentCapacity)
    print(facilitiesCustomers)
    print(customersIsSatisfied)
    print(customersFacilityAllocated)
    elapsed_time = time.time() - start_time
    #print("Elapsed Time:", elapsed_time, "seconds")

    return sumTotal

def readInstances(filename: str):
    """
    readInstances reads all the instances in a directory

    :param filename: presents the file to read
    :return: returns dfCustomers, dfFacilities, transportationCosts
    """
    with open(filename, "r") as lib_file:
        transportation_costs = list()
        facilitiesOpeningCost = {}
        facilitiesInitialCapacity = {}
        facilitiesCurrentCapacity = {}
        facilitiesIsOpen = {}
        facilitiesCustomers = {}
        customersDemand = {}
        customersIsSatisfied = {}
        customersFacilityAllocated = {}
        customersTransportationCost = {}

        for index, row in enumerate(lib_file):
            try:
                if index == 0:
                    numCustomers = int(row.split()[1])
                    numFacilities = int(row.split()[0])
                elif index == 1:
                    for capacity_index, capacity in enumerate(row.split()):
                        facilitiesInitialCapacity[capacity_index] = int(capacity)
                        facilitiesCurrentCapacity[capacity_index] = int(capacity)
                        facilitiesIsOpen[capacity_index] = False
                        facilitiesCustomers[capacity_index] = []
                elif index == 2:
                    for cost_index, opening_cost in enumerate(row.split()):
                        facilitiesOpeningCost[cost_index] = float(opening_cost)
                elif index == 3:
                    for demand_index, demand in enumerate(row.split()):
                        customersDemand[demand_index] = int(demand)
                        customersIsSatisfied[demand_index] = False
                        customersFacilityAllocated[demand_index] = None
                        customersTransportationCost[demand_index] = None
                else:
                    transportation_costs.append(list(map(float, row.split())))
            except NameError as name_error:
                print(f"!ERROR! Variable not declared: {name_error}")
    return numCustomers, numFacilities, customersDemand,customersIsSatisfied, customersFacilityAllocated, customersTransportationCost, facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportation_costs

def main(directory) -> None:
    """
    Run inside 'src' folder
    """

    numCustomers, numFacilities, customersDemand,customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts = readInstances(os.path.join("..", "instances", "formatted",
                                                                                  "Lib_1", "p1"))
    
    time_constructive_start = perf_counter()
    solution = solve(numCustomers, numFacilities, customersDemand,customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts)
    print(solution)
    time_constructive_end = perf_counter()
    time_constructive = (time_constructive_end - time_constructive_start)*1000
    print(time_constructive)
    time_local_shift_start = perf_counter()
    solution2 = localSearchSolveShift(numCustomers, numFacilities, customersDemand,customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts)
    time_local_shift_end = perf_counter()
    print(solution2)
    time_local_shift = (time_local_shift_end - time_local_shift_start)*1000
    print(time_local_shift)
    time_local_swaft_start = perf_counter()
    solution3 = localSearchSolveSwaft(numCustomers, numFacilities, customersDemand,customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts)
    time_local_swaft_end = perf_counter()
    print(solution3)
    time_local_swaft = (time_local_swaft_end - time_local_swaft_start)*1000
    print(time_local_swaft)
    #a = generateRandomSolution(numFacilities,numCustomers,transportationCosts)
    


    
if __name__ == "__main__":
    for path, subdirs, files in os.walk(os.path.join("..", "instances", "formatted")):
        if path.split('..\\instances\\')[1].replace('\\','/') == 'formatted/Lib_1':
            main(os.path.join("..", "instances", path.split('..\\instances\\')[1].replace('\\','/')))



