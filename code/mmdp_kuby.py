from gurobipy import *
import instance_mmdp


try:
    path = "instances/mdplib/GKD_d_1_n250_coor.txt"
    p = 25
    inst = instance_mmdp.readInstance(path, p)
    n = inst['n']
    p = inst['p']

    model = Model("MMDP")
    model.setParam("LogToConsole", 0)
    model.setParam("TimeLimit", 10)

    # VARIABLES
    x = model.addVars(n, vtype=GRB.BINARY, name="x")
    m = model.addVar(0.0, inst['distance'][len(inst['distance'])-1], 1, GRB.CONTINUOUS, "m")

    # FIX VARIABLES
    # x[2].lb = 1
    # x[2].ub = 1

    # OBJECTIVE FUNCTION
    model.setObjective(m, GRB.MAXIMIZE)

    # CONSTRAINTS
    # R1: \sum_{i=0}^{n} x[i] == p
    model.addConstr((quicksum(x[i] for i in range(n)) == p))

    # R2: m \leq d_{ij} + M (2 - x_i - x_j)   1 \leq i < j \leq n
    M = 0x3f3f3f3f
    model.addConstrs(m <= inst['d'][i][j] + M * (2 - x[i] - x[j]) for j in range(n) for i in range(j+1, n))

    # SOLVE THE MODEL
    model.optimize()

    print("Status: " + str(model.getAttr("Status")))
    for v in model.getVars():
        if v.x > 0:
            print(str(v.varName), end=" ")
    print()
    print("Obj: " + str(round(model.objVal, 2)))
except GurobiError as e:
    print(e)