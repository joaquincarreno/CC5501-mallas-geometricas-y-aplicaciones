def read_m2d(path):
    file = open(path, "r")
    vertex_list = []
    triangle_list = []
    min_x = float("inf")
    max_x = -float("inf")
    min_y = float("inf")
    max_y = -float("inf")
    for l in file.readlines():
        values = l.split()
        if len(values) < 4:
            continue
        elif values[0] == "v":
            x = float(values[2])
            min_x = x if x < min_x else min_x
            max_x = x if x > max_x else max_x
            y = float(values[3])
            min_y = y if y < min_y else min_x
            max_y = y if y > max_y else min_y
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
    return vertex_list, triangle_list, min_x, min_y, max_x, max_y
