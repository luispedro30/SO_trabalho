import os, json, re
import solverInstance
import xlsxwriter 
import cython
import random 
import numpy as np

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

def localSearchSolveShift(numCustomers, numFacilities, customersDemand, customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts):
    for customer in range(numCustomers):
        for facility in range(numFacilities):
            if  (facilitiesIsOpen[facility] == False or not facilitiesCustomers[facility] or customersDemand[customer] > facilitiesCurrentCapacity[facility]):
                continue

            chosen_facility = customersFacilityAllocated[customer]
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
    
    solution = solve(numCustomers, numFacilities, customersDemand,customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts)
    print(solution)
    solution2 = localSearchSolveShift(numCustomers, numFacilities, customersDemand,customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts)
    print(solution2)

    #a = generateRandomSolution(numFacilities,numCustomers,transportationCosts)
    


    
if __name__ == "__main__":
    for path, subdirs, files in os.walk(os.path.join("..", "instances", "formatted")):
        if path.split('..\\instances\\')[1].replace('\\','/') == 'formatted/Lib_3':
            main(os.path.join("..", "instances", path.split('..\\instances\\')[1].replace('\\','/')))



