import os, json, re
import solverInstance
import xlsxwriter 

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
        customersDemand = {}
        for index, row in enumerate(lib_file):
            try:
                if index == 0:
                    numCustomers = int(row.split()[1])
                    numFacilities = int(row.split()[0])
                elif index == 1:
                    for capacity_index, capacity in enumerate(row.split()):
                        facilitiesCapacity[capacity_index] = int(capacity)
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
    return numCustomers, numFacilities, customersDemand,facilitiesCapacity,facilitiesOpeningCost,transportation_costs

def main(directory) -> None:
    """
    Run inside 'src' folder
    """
    result = []
    timeResult = []
    customers  = []
    facilities = []
    newFiles = []
    
    for path, subdirs, files in os.walk(directory):
        files.remove('os')
        files = (sorted(files, key=lambda s: int(re.search(r'\d+', s).group())))
        nameSheet = path.split('/')[1]
        for name in files:
            nameModel = nameSheet+name
            numCustomers, numFacilities, customersDemand,facilitiesCapacity,facilitiesOpeningCost,transportationCosts = readInstances(os.path.join(path, name))
            solution, time = solverInstance.main(nameModel,customersDemand,
                    facilitiesCapacity,
                    facilitiesOpeningCost,
                    transportationCosts,
                    numCustomers,
                    numFacilities)
            newFiles.append(name)
            result.append(solution)
            timeResult.append(time)
            customers.append(numCustomers)
            facilities.append(numFacilities)

    for path, subdirs, files in os.walk(directory):
        expectedResults = []
        for name in files:
            if name == 'os':
                with open(os.path.join(path, name), "r") as lib_file:
                    for index, row in enumerate(lib_file):
                        expectedResults.append(int(row.split()[0]))

    
    workbook = xlsxwriter.Workbook('../outputs/'+str(path.split("/",1)[1])+'.xlsx') 
    worksheet = workbook.add_worksheet(nameSheet)
    worksheet.write('A1', '#')
    worksheet.write('B1', '|I|-|J|')
    worksheet.write('C1', 'Z*')
    worksheet.write('D1', 'Z')
    worksheet.write('E1', 'Gap')
    worksheet.write('F1', 'Time')

    row = 1
    column = 0
    # iterating through content list
    for i in range(len(expectedResults)):
        worksheet.write(row, column, newFiles[i])
        worksheet.write(row, column+1, "{}-{}".format(facilities[i],customers[i]))
        worksheet.write(row, column+2, expectedResults[i])
        worksheet.write(row, column+3, result[i])
        worksheet.write(row, column+4, abs(expectedResults[i]-result[i]))
        worksheet.write(row, column+5, timeResult[i])
        row += 1
    workbook.close()
    
if __name__ == "__main__":
    for path, subdirs, files in os.walk(os.path.join("..", "instances", "formatted")):
        if path.split('..\\instances\\')[1].replace('\\','/') != 'formatted':
            main(os.path.join("..", "instances", path.split('..\\instances\\')[1].replace('\\','/')))

