def intersect_all(set1: set, *sets_to_intersect: set) -> set:
    """
    Returns an intersection of all given sets. Ignores empty sets.
    """
    filtered_set = set1.copy()
    for other_set in sets_to_intersect:
        if len(other_set) > 0:
            filtered_set.intersection_update(other_set)

    return filtered_set
