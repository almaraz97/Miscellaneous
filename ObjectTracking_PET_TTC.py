def metric(position1, position2, velocity1, velocity2):
    (cx1, cy1), (cx2, cy2) = position1, position2
    (vx1, vy1), (vx2, vy2) = velocity1, velocity2

    # Non-moving cars
    if {velocity1+velocity2} == {0}:
        return None, None

    D = []
    # Linear Independence Test
    for x, y in zip([vx1, vy1], [vx2, vy2]):  # Find linear dependence (parallel movement)
        if (x==0 or y==0) and x != y:  # Intersecting lines (No dependence)
            break
        elif x == 0 and y == 0:  # Both are zero (might be moving parallel or both are still)
            continue  # Linear dependence in 2D
        else:
            D.append(x/y)
    # Tracks are parallel
    if len(set(D)) == 1:
        temp = []
        # Check for Overlapping
        for i, j in zip([cx1-cx2, cy1-cy2], [vx1-vx2, vy1-vy2]):  # Check if both can reach same point
            if (i==0 or j==0) and i != j:  # Not overlapping
                return None, None
            if i == 0 and j == 0:  # Both are zero  (are in same x/y position or same x/y velocity)
                continue  # Linear dependence in 2D
            else:
                temp.append(abs(i/j))  # Time away from each other in x and y direction

        if len(set(temp)) == 1:  # Overlapping (direction of movement allows one point to another)
            temp1 = [0 if x == 0 or y == 0 else x/y for x, y in zip([cx1-cx2, cy1-cy2], velocity2)]
            temp2 = [0 if x == 0 or y == 0 else x/y for x, y in zip([cx2-cx1, cy2-cy1], velocity1)]
            pet = max(temp1+temp2)
            return pet, temp[0]

    # Calculate time to intersection point for each car
    t2 = (vx1*cy1 - vx1*cy2 + vy1*cx2 - vy1*cx1) / (vx1*vy2 - vy1*vx2)
    if vx1 != 0:  # If all four are zero both vehicles are still
        t1 = (cx2 - cx1 + vx2 * t2) / vx1
    elif vx2 != 0:
        t1 = (cx1 - cx2 + vx1 * t2) / vx2
    elif vy1 != 0:
        t1 = (cx2 - cx1 + vy1 * t2) / vy1
    else:
        t1 = (cx1 - cx2 + vy2 * t2) / vy2
    intersection = [cx1 + vx1 * t1, cy1 + vy1 * t1]
    return abs(t1-t2), t1 if t1-t2 == 0 else 'None', intersection
