import os, re
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=FutureWarning) 

def readInstances(filename):
    """
    readInstances reads all the instances in a directory

    :param filename: presents the file to read
    :return: returns dfCustomers, dfFacilities, transportationCosts
    """
    with open(filename, "r") as lib_file:
        dfCustomers = pd.DataFrame(columns=['id','demand'])
        dfFacilities = pd.DataFrame(columns=['id','capacity','openingCost','open'])
        dfTransportationCost = pd.DataFrame(columns=['idCustomer','idFacilities','openingCost','assigned'])
        for index, row in enumerate(lib_file):
            try:
                if index == 0 or not row.split():
                    numFacilities =  int(row.split()[0])
                    numClients = int(row.split()[1])
                    continue
                if index == 1:
                    for capacity_index, capacity in enumerate(row.split()):
                        dfFacilities.loc[capacity_index] = [capacity_index+1,int(capacity),0,0]
                elif index == 2:
                    for cost_index, opening_cost in enumerate(row.split()):
                        dfFacilities["openingCost"][cost_index] = float(opening_cost)
                elif index == 3:
                    for demand_index, demand in enumerate(row.split()):
                        dfCustomers.loc[demand_index] = [demand_index+1,int(demand)]
                else:
                    for transportation_cost_index, cost in enumerate(row.split()):
                        dfTransportationCost = dfTransportationCost.append({'idCustomer':index-3,'idFacilities':transportation_cost_index +1,'openingCost':cost,'assigned':0},ignore_index=True)
            except NameError as name_error:
                print(name_error)
    return numClients, numFacilities, dfCustomers, dfFacilities, dfTransportationCost

def main() -> None:
    from pathlib import Path
    import pathlib

    numClients, numFacilities, dfCustomers, dfFacilities, dfTransportationCost = readInstances(os.path.join("..", "instances", "formatted",
                                                                                  "Lib_1", "p1"))
    
    """for path, subdirs, files in os.walk(os.path.join("..", "instances", "formatted")):
        for name in files:
            print(os.path.join(path, name))
            print(name)
            #dfCustomers, dfFacilities, transportationCosts = readInstances(os.path.join(path, name))
    """
    print(type(numClients))
    print("Customers")
    #print(dfCustomers)
    print("Facilities")
    #print(dfFacilities)
    print("TransportationCosts")
    print(dfTransportationCost)
    """for index, row in dfTransportationCost.iterrows():
        print(row) 
    
    fi = [i for i in dfFacilities.openingCost]
    si = [i for i in dfFacilities.capacity]
    yi = [i for i in dfFacilities.open]
    dj = [j for j in dfCustomers.demand]"""
    

    
if __name__ == "__main__":
    main()
