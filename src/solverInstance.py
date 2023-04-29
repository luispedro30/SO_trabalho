from ortools.linear_solver import pywraplp
import cython

def main(nameModel,d,s,f,c,numClients,numFacilities):

    solver = pywraplp.Solver('SCIP',pywraplp.Solver.SCIP_MIXED_INTEGER_PROGRAMMING)
    if not solver:
        return

    # Variables
    # x[worker, task] is an array of 0-1 variables, which will be 1
    # if the worker is assigned to the task.
    x = {}
    for facility in range(numFacilities):
        for client in range(numClients):
            x[client, facility] = solver.IntVar(0, 1,f'x[{client},{facility}]')

    # y[facility] is an array of 0-1 variables, which will be 1
    # if the facility is open.
    y = {}
    for facility in range(numFacilities):
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
    objectiveTerms = []            
    objectiveTerms.append(sum(f[facility] * y[facility] for facility in range(numFacilities)))
    objectiveTerms.append(sum(c[client][facility]* x[client,facility] 
                               for facility in range(numFacilities) for client in range(numClients)))
    solver.Minimize(solver.Sum(objectiveTerms))

    #Set the limit to 20 minutes
    solver.set_time_limit(1200000)  

    status = solver.Solve()
    
    # Print solution.
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print(f'Total cost = {solver.Objective().Value()}\n') 
        for facility in range(numFacilities):    
            for client in range(numClients):
                if x[client, facility].solution_value() > 0.5:
                    print(f'Worker {client+1} assigned to facility {facility+1}.' + f' Cost = {c[client][facility]}')
        
    else:
        print('No solution found.')
        
    print("\nAdvanced usage:")
    print("Problem solved in %f milliseconds" % solver.wall_time())
    print("Problem solved in %d iterations" % solver.iterations())
    print("Problem solved in %d B&B nodes" % solver.nodes())
    
    with open("../Models/"+nameModel+".mps", "w") as out_f:
        mps_text = solver.ExportModelAsLpFormat(False)
        out_f.write(mps_text)
    return solver.Objective().Value(), solver.WallTime()
if __name__ == '__main__':
    main()