def intersect_all(set1: set, set2: set, *more_sets: set) -> set:
    """
    Returns an intersection of all given sets. Ignores empty sets.
    """
    non_empty_sets = [s for s in [set1, set2, *more_sets] if len(s) > 0]

    if len(non_empty_sets) == 1:
        return non_empty_sets[0]
    else:
        filtered_set = non_empty_sets[0].intersection(non_empty_sets[1])
        for other_set in non_empty_sets[2:]:
            filtered_set.intersection_update(other_set)
        return filtered_set
