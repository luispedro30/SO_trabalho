import os, json, re
import solverInstance
import xlsxwriter 
import cython

def readInstances(filename: str):
    """
    readInstances reads all the instances in a directory

    :param filename: presents the file to read
    :return: returns dfCustomers, dfFacilities, transportationCosts
    """
    with open(filename, "r") as lib_file:
        transportation_costs = list()
        facilitiesOpeningCost = {}
        facilitiesCapacity = {}
        facilitiesCurrentCapacity = {}
        facilitiesIsOpen = {}
        customersDemand = {}

        for index, row in enumerate(lib_file):
            try:
                if index == 0:
                    numCustomers = int(row.split()[1])
                    numFacilities = int(row.split()[0])
                elif index == 1:
                    for capacity_index, capacity in enumerate(row.split()):
                        facilitiesCapacity[capacity_index] = int(capacity)
                        facilitiesCurrentCapacity[capacity_index] = int(capacity)
                        facilitiesIsOpen[capacity_index] = 0
                elif index == 2:
                    for cost_index, opening_cost in enumerate(row.split()):
                        facilitiesOpeningCost[cost_index] = float(opening_cost)
                elif index == 3:
                    for demand_index, demand in enumerate(row.split()):
                        customersDemand[demand_index] = int(demand)
                else:
                    transportation_costs.append(list(map(float, row.split())))
            except NameError as name_error:
                print(f"!ERROR! Variable not declared: {name_error}")
    return numCustomers, numFacilities, customersDemand,facilitiesCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost,transportation_costs

def main(directory) -> None:
    """
    Run inside 'src' folder
    """

    numCustomers, numFacilities, customersDemand,facilitiesCapacity,facilitiesCurrentCapacity, facilitiesIsOpen, facilitiesOpeningCost,transportationCosts = readInstances(os.path.join("..", "instances", "formatted",
                                                                                  "Lib_1", "p1"))
    
    print(numCustomers)
    print(numFacilities)
    print(facilitiesCapacity)
    print(facilitiesOpeningCost)
    print(facilitiesIsOpen)
    print(customersDemand)
    print(transportationCosts)
    """
    x1, time1 = solverInstance.main('p1',customersDemand,
                        facilitiesCapacity,
                        facilitiesOpeningCost,
                        transportationCosts,
                        numCustomers,
                        numFacilities)
                        """

    
if __name__ == "__main__":
    for path, subdirs, files in os.walk(os.path.join("..", "instances", "formatted")):
        if path.split('..\\instances\\')[1].replace('\\','/') == 'formatted/Lib_3':
            main(os.path.join("..", "instances", path.split('..\\instances\\')[1].replace('\\','/')))

