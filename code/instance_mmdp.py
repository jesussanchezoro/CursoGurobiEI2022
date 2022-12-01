

def readInstance(path, p):
    instance = {}
    with open(path, "r") as f:
        n = int(f.readline())
        instance['n'] = n
        instance['p'] = p
        instance['d'] = []
        instance['distance'] = []
        for i in range(n):
            instance['d'].append([0] * n)
        for i in range(n):
            for j in range(i+1, n):
                u, v, d = f.readline().split()
                u = int(u)
                v = int(v)
                d = round(float(d), 2)
                instance['d'][u][v] = d
                instance['d'][v][u] = d
                instance['distance'].append(d)
        instance['distance'] = sorted(list(dict.fromkeys(instance['distance'])))
    return instance
