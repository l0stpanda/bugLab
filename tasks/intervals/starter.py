def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    intervals.sort()
    merged = []
    for start, end in intervals:
        if merged and start < merged[-1][1]:
            merged[-1][1] = end
        else:
            merged.append([start, end])
    return merged
