from ortools.linear_solver import pywraplp


def main(customersDemand,facilitiesCapacity,facilitiesOpeningCost,transportationCosts):
    d = customersDemand
    s = facilitiesCapacity
    c = transportationCosts
    f = facilitiesOpeningCost

    numClients = len(transportationCosts)
    numFacilities = len(transportationCosts[0])

    
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return

    # Variables
    # x[worker, task] is an array of 0-1 variables, which will be 1
    # if the worker is assigned to the task.
    x = {}
    for client in range(numClients):
        for facility in range(numFacilities):
            #x[client, facility] = solver.BoolVar(f'x[{client},{facility}]')
            x[client, facility] = solver.IntVar(0, 1,f'x[{client},{facility}]')

    # y[facility] is an array of 0-1 variables, which will be 1
    # if the facility is open.
    y = {}
    for facility in range(numFacilities):
        #y[facility] = solver.BoolVar(f'y[{facility}]')
        y[facility] = solver.IntVar(0, 1, f'y[{facility}]')
        
    # Constraints
    # The total size of the facilities each client takes on is 1
    for client in range(numClients):
        solver.Add(
            solver.Sum([x[client, facility] for facility in range(numFacilities)]) == 1)

    for facility in range(numFacilities):
        solver.Add(
            solver.Sum([x[client, facility] * d[client] for client in range(numClients)]) <= 
            s[facility]*y[facility])   

    # Objective
    objective_terms = []
    for facility in range(numFacilities):
        for client in range(numClients):
            objective_terms.append(c[client][facility] * x[client,facility])
    for facility in range(numFacilities):
        objective_terms.append(f[facility] * y[facility])
    solver.Minimize(solver.Sum(objective_terms))

    solver.set_time_limit(5000)  

    status = solver.Solve()
    
    # Print solution.
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print(f'Total cost = {solver.Objective().Value()}\n')
        """
        for client in range(numClients):
            for facility in range(numFacilities):
                if x[client, facility].solution_value() > 0.5:
                    print(f'Worker {client+1} assigned to facility {facility+1}.' + f' Cost = {c[client][facility]}')
        """
    else:
        print('No solution found.')
    print(f'Time = {solver.WallTime()} ms')
    with open("test.mps", "w") as out_f:
        mps_text = solver.ExportModelAsLpFormat(False)
        out_f.write(mps_text)
    return solver.Objective().Value(), solver.WallTime()
if __name__ == '__main__':

    main()