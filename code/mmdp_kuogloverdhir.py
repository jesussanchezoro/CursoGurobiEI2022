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
    y = model.addVars(n, n, vtype=GRB.BINARY, name="y")
    z = model.addVar(0.0, inst['distance'][len(inst['distance'])-1], 1, GRB.CONTINUOUS, "z")

    # OBJECTIVE FUNCTION
    model.setObjective(z, GRB.MAXIMIZE)

    # CONSTRAINTS
    # R1: \sum_{i=0}^{n} x[i] == p
    model.addConstr((quicksum(x[i] for i in range(n)) == p))

    # R2: y_{ij} \leq x_i   1 \leq i < j \leq n
    model.addConstrs(y[i, j] <= x[i] for j in range(n) for i in range(j+1, n))

    # R3: y_{ij} \leq x_j   1 \leq i < j \leq n
    model.addConstrs(y[i, j] <= x[j] for j in range(n) for i in range(j + 1, n))

    # R4: x_i + x_j <= y_{ij} + 1    1 \leq i < j \leq n
    model.addConstrs(x[i] + x[j] <= y[i, j] + 1 for j in range(n) for i in range(j + 1, n))

    # R5: z \leq d_{ij} \cdot y_{ij} + D(1-y_{ij})    1 \leq i < j \leq n
    D = 0x3f3f3f3f
    model.addConstrs(z <= inst['d'][i][j] * y[i, j] + D * (1 - y[i, j]) for j in range(n) for i in range(j + 1, n))


    # SOLVE THE MODEL
    model.optimize()

    print("Status: " + str(model.getAttr("Status")))
    for v in model.getVars():
        if v.x > 0 and "x" in v.varName:
            print(str(v.varName), end=" ")
    print()
    print("Obj: " + str(round(model.objVal,2)))
except GurobiError as e:
    print(e)