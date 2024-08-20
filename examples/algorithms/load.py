def read_m2d(path):
    file = open(path, "r")
    vertex_list = []
    triangle_list = []
    for l in file.readlines():
        values = l.split()
        if len(values) < 4:
            continue
        elif values[0] == "v":
            x = float(values[2])
            y = float(values[3])
            z = float(values[4]) if len(values) == 5 else 0.0
            vertex_list += [x, y, z]
        elif values[0] == "t":
            triangle_list += [
                int(values[2]) - 1,
                int(values[3]) - 1,
                int(values[4]) - 1,
            ]
        else:
            continue
    return vertex_list, triangle_list
