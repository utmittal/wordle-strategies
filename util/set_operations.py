def intersect_all(set1: set, set2: set, *more_sets: set) -> set:
    """
    Returns an intersection of all given sets. Ignores empty sets.
    """
    filtered_set = set1.intersection(set2)
    for other_set in more_sets:
        if len(other_set) > 0:
            filtered_set.intersection_update(other_set)

    return filtered_set
