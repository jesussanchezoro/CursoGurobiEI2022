from gurobipy import *
import instance_mmdp
from bisect import bisect_left



def evalSolution(inst, sol):
    minDist = 0x3f3f3f
    n = len(sol)
    for i in range(n):
        for j in range(i+1, n):
            minDist = min(minDist, inst['d'][sol[i]][sol[j]])
    return minDist


try:
    path = "instances/mdplib/GKD_d_1_n250_coor.txt"
    p = 25
    inst = instance_mmdp.readInstance(path, p)
    n = inst['n']
    p = inst['p']
    dmax = inst['distance'][len(inst['distance'])-1]
    dmin = inst['distance'][0]
    timeLimit = 60
    secs = 0
    bestSol = None
    while dmax - dmin > 0.01 and secs < timeLimit:
        l = round(dmin + (dmax - dmin) / 2, 2)

        model = Model("MMDP")
        model.setParam("LogToConsole", 0)
        model.setParam("TimeLimit", 10)

        # VARIABLES
        x = model.addVars(n, vtype=GRB.BINARY, name="x")

        # OBJECTIVE FUNCTION
        model.setObjective(quicksum(x[i] for i in range(n)), GRB.MAXIMIZE)

        # CONSTRAINTS
        # R1: \sum_{i=0}^{n} x[i] == p
        model.addConstr((quicksum(x[i] for i in range(n)) == p))

        # R2: x_i + x_j \leq 1 if d_{ij} \geq l
        for i in range(n):
            for j in range(i+1, n):
                if round(inst['d'][i][j], 2) < l:
                    model.addConstr(x[i] + x[j] <= 1)

        # SOLVE THE MODEL
        model.optimize()

        status = model.getAttr("Status")
        if status == GRB.OPTIMAL:
            print("SOL FOUND")
            sol = []
            for v in model.getVars():
                if v.x > 0 and "x" in v.varName:
                    id = int(v.varName[v.varName.find("[")+1:v.varName.find("]")])
                    sol.append(id)
            dmin = round(evalSolution(inst, sol), 2)
            bestSol = sol[:]
        elif status != GRB.TIME_LIMIT:
            print("Solution not found with dmin="+str(dmin)+" and dmax="+str(dmax))
            dmax = round(inst['distance'][bisect_left(inst['distance'], l)-1], 2)
        else:
            print("Solution not found with code: "+str(status))
            break

    print("Best solution: "+str(round(evalSolution(inst, bestSol), 2)))

except GurobiError as e:
    print(e)