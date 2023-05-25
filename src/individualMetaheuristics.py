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

    return sumTotal, numCustomers, numFacilities, customersDemand, customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts

def greedy(alfa, numCustomers, numFacilities, customersDemand, customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts):
    facilities_factor = []
    list_customers = []
    served_customers = []
    for x in range(numFacilities):
        facilities_factor.append(x)
    
    for x in range(numCustomers):
        list_customers.append(x)

    random_customers = random.sample(list_customers, k=len(list_customers))

    sorted_dict = dict(sorted(facilitiesOpeningCost.items(), key=lambda x: x[1]))

    for x, value in sorted_dict.items():
        if len(served_customers) < numCustomers:
            optimal_facility_index = x
            facilitiesIsOpen[optimal_facility_index] = True
            for y in random_customers:
                if facilitiesCurrentCapacity == 0:
                    break
                elif (customersDemand[y] <= facilitiesCurrentCapacity[x] and y not in served_customers):
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

    return sumTotal, numCustomers, numFacilities, customersDemand, customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts

def grasp(alfa, numCustomers, numFacilities, customersDemand, customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts):
    facilities_factor = facilitiesOpeningCost.copy()
    list_customers = []
    served_customers = []
    
    for x in range(numCustomers):
        list_customers.append(x)

    random_customers = random.sample(list_customers, k=len(list_customers))
    """
    min_cost = min(facilitiesOpeningCost.values())
    max_cost = max(facilitiesOpeningCost.values())
    diff_cost = max_cost - min_cost

    sorted_dict = dict(sorted(facilitiesOpeningCost.items(), key=lambda x: x[1]))
    possible_facilities = {key: value for key, value in sorted_dict.items() if value <= min_cost + alfa * diff_cost}
    #random_facilities = random.sample(list(possible_facilities.keys()), len(possible_facilities))
    """

    #items = list(possible_facilities.items())

    # Shuffle the list
    #random.shuffle(items)

    # Create a new dictionary from the shuffled list
    #shuffled_dict = dict(items)

    #for x, value in shuffled_dict.items():
    for x in range(numFacilities):
        min_cost = min(facilities_factor.values())
        max_cost = max(facilities_factor.values())
        diff_cost = max_cost - min_cost

        sorted_dict = dict(sorted(facilities_factor.items(), key=lambda x: x[1]))
        possible_facilities = {key: value for key, value in sorted_dict.items() if value <= min_cost + alfa * diff_cost}
        x, value = random.choice(list(possible_facilities.items()))
        del facilities_factor[x]

        if len(served_customers) < numCustomers:
            optimal_facility_index = x
            facilitiesIsOpen[optimal_facility_index] = True
            for y in random_customers:
                if facilitiesCurrentCapacity == 0:
                    break
                elif (customersDemand[y] <= facilitiesCurrentCapacity[x] and y not in served_customers):
                    print(y,x)
                    facilitiesCustomers[x].append(y)
                    customersIsSatisfied[y] = True
                    customersFacilityAllocated[y] = x
                    facilitiesCurrentCapacity[x] -= customersDemand[y]
                    served_customers.append(y)
        else:
            break    

    facilitesTotalCost = {}
    print(facilitiesOpeningCost)
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

    return sumTotal, numCustomers, numFacilities, customersDemand, customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts

def localSearchSolveShift(numCustomers, numFacilities, customersDemand, customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts):
    for customer in range(numCustomers):
        for facility in range(numFacilities):
            if  (facilitiesIsOpen[facility] == False or not facilitiesCustomers[facility] or customersDemand[customer] > facilitiesCurrentCapacity[facility]):
                continue
        
            chosen_facility = customersFacilityAllocated[customer]
            if chosen_facility != None:
                if facilitiesOpeningCost[facility] <= facilitiesOpeningCost[chosen_facility]:
                    facilitiesCustomers[chosen_facility].remove(customer)
                    facilitiesCurrentCapacity[chosen_facility] += customersDemand[customer]
                    customersIsSatisfied[customer] == False

                    facilitiesCustomers[facility].append(customer)
                    customersIsSatisfied[customer] = True
                    customersFacilityAllocated[customer] = facility
                    facilitiesCurrentCapacity[facility] -= customersDemand[customer]
            else:
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

    return sumTotal, numCustomers, numFacilities, customersDemand, customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts

def localSearchSolveSwaft(numCustomers, numFacilities, customersDemand, customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts):
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

        return sumTotal, numCustomers, numFacilities, customersDemand, customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts

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
    best_solution = None
    best_cost = float('inf')
    solutions = []

    #criar alfa, que começa em 10% e vai aumentando
    #custo minímo e máximo
    #fazer a diferença 
    #custo mínimo + diferença * alfa
    #escolher random entre custo mínimo e custo mínimo + diferença * alfa
    alfa = 0.1
    for iteration in range(100):
        # Construct a random solution
        print(iteration)
        if iteration % 10 == 0:
            alfa += alfa

        numCustomers, numFacilities, customersDemand,customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts = readInstances(os.path.join("..", "instances", "formatted",
                                                                                  "Lib_1", "p2"))
        solution, numCustomers, numFacilities, customersDemand, customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts = grasp(alfa, numCustomers, numFacilities, customersDemand,customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts)
        solutions.append(solution)
        print(solution)
        print(alfa)
        
        solution2, numCustomers, numFacilities, customersDemand, customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts = localSearchSolveShift(numCustomers, numFacilities, customersDemand,customersIsSatisfied, customersFacilityAllocated, customersTransportationCost,facilitiesInitialCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost, facilitiesCustomers, transportationCosts)
        
        if solution2 < best_cost:
            best_cost = solution2
    
    print(solutions)
    print(best_cost)

    return best_cost


    
if __name__ == "__main__":
    for path, subdirs, files in os.walk(os.path.join("..", "instances", "formatted")):
        if path.split('..\\instances\\')[1].replace('\\','/') == 'formatted/Lib_1':
            #print(os.path.join("..", "instances", path.split('..\\instances\\')[1].replace('\\','/')))
            main(os.path.join("..", "instances", path.split('..\\instances\\')[1].replace('\\','/')))



