
def ray_casting(point, polygon):
    """
       Algoritmo de ray casting para determinar si un punto está dentro de un polígono.
       No se consideran casos bordes (discusión en clases).

       :param point: [x, y] del punto a comprobar.
       :param vertices: Lista de vertices [[x1, y1], [x2, y2], ...] representando los vértices del polígono.
       :return: Booleano indicando si el punto está dentro del polígono.
    """
    x, y = point
    n = len(polygon)
    crossing = 0  # Contador de cruces

    for i in range(n):
        j = (i + 1) % n
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        # Verificar si el segmento cruza la línea horizontal a la altura y
        if (yi > y and yj <= y) or (yi <= y and yj > y):
            intersect = (xj - xi) * (y - yi) / (yj - yi) + xi
            if x < intersect:
                crossing += 1

    return crossing % 2 == 1, crossing
