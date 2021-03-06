def metric(position1, position2, velocity1, velocity2):
    """
        Find if two objects intersect, the Post Encroachment Time, Time To Collision, and point of intersection.
        Could return point of ttc as intersection point for same track
        Assuming ability to collide, may want to find ∆v that would allow for a collision, normalized by average speed
    """
    (cx1, cy1), (cx2, cy2) = position1, position2
    (vx1, vy1), (vx2, vy2) = velocity1, velocity2

    # Both Non-moving Case
    if set(velocity1+velocity2) == {0}:
        return None, None
    # Both Same Position Case
    if all([x == y for x, y in zip(position1, position2)]):
        return 0, 0
    # One Stationary Case
    if set(velocity1) == {0} or set(velocity2) == {0}:
        if set(velocity1) == {0}:  # See which one is moving
            dx_dy = [x - y for x,y in zip(position1, position2)]
            tx_ty = []
            for x, y in zip(dx_dy, velocity2):
                if x == 0 and y == 0:  # No movement is needed and none is present
                    continue
                elif (x == 0) ^ (y == 0):  # Movement is not needed and present or is needed and not present
                    return None, None
                else:
                    tx_ty.append(x / y)  # Time to reach x/y coordinate of intersecting point
            if len(tx_ty) == 1 or len(set(tx_ty)) == 1:  # Scalar can multiply to 0 and to non-zero
                return tx_ty[0], tx_ty[0]
            else: # Not intersecting
                return None, None
        else:
            dx_dy = [x - y for x, y in zip(position2, position1)]
            tx_ty = []
            for x, y in zip(dx_dy, velocity1):
                if x == 0 and y == 0:  # No movement is needed and none is present
                    continue
                elif (x == 0) ^ (y == 0):  # Movement is not needed and is present or is needed and not present
                    return None, None
                else:
                    tx_ty.append(x/y)  # Time to reach x/y coordinate of intersecting point
            if len(tx_ty) == 1 or len(set(tx_ty)) == 1:  # Only needs to move in 1 direction and is
                return tx_ty[0], tx_ty[0]
            else:  # Not intersecting
                return None, None
    # Parallel Test
    parallel = False
    if vx1*vy2-vy1*vx2 == 0:  # Calculate determinant
        parallel = True
    # Parallel Movement Case
    if parallel:
        ttc = []
        # Check for Overlapping Tracks
        for i, j in zip([cx1-cx2, cy1-cy2], [vx1-vx2, vy1-vy2]):  # Check if both can reach same point
            if (i==0 or j==0) and i != j:  # Not overlapping  # dx or dy is zero but vx or vy are non-zero
                return None, None
            elif i == 0 and j == 0:  # Both are zero (needs to move 0 in the x/y direction, having 0 x/y velocity)
                # ttc.append(None)
                continue  # Linear dependence in 2D, first ttc value doesnt matter
            else:  # Time to travel dx or dy given vx and vy
                ttc.append(abs(i/j))  # Time away from each other in x and y direction
        # ttc should have repeated values or one 0 and other not 0.
        if len(set(ttc)) == 1:  # Overlapping (direction of movement allows one point to another)
            pet_xy1 = [0 if x == 0 or y == 0 else x/y for x, y in zip([cx1-cx2, cy1-cy2], velocity2)]
            pet_xy2 = [0 if x == 0 or y == 0 else x/y for x, y in zip([cx2-cx1, cy2-cy1], velocity1)]
            pet = max(pet_xy1+pet_xy2)
            return pet, ttc[0]
        else:  # One point can't get to another
            return None, None
    # Calculate time to intersection point for each object
    t2 = (vx1 * cy1 - vx1 * cy2 + vy1 * cx2 - vy1 * cx1) / (vx1 * vy2 - vx2* vy1)  # X plugged into Y
    if vx1 != 0:
        t1 = (cx2 - cx1 + vx2 * t2) / vx1
    else:
        t1 = (cy2 - cy1 + vy2 * t2) / vy1
    intersection = [cx1 + vx1 * t1, cy1 + vy1 * t1]
    return abs(t1-t2), t1 if t1-t2 == 0 else None
