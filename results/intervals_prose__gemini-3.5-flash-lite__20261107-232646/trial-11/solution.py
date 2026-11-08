def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    # Input must not be modified in any way, and it may be any iterable, including a generator.
    # Convert to list and validate.
    norm_intervals = []
    for item in intervals:
        start, end = item
        if start > end:
            raise ValueError(f"Invalid interval: start ({start}) > end ({end})")
        if start == end:
            continue
        norm_intervals.append((start, end))

    if not norm_intervals:
        return []

    # Sort by start (and end as secondary key for stability)
    sorted_intervals = sorted(norm_intervals, key=lambda x: (x[0], x[1]))

    merged = []
    for start, end in sorted_intervals:
        if merged and start <= merged[-1][1]:
            # Overlapping or touching
            if end > merged[-1][1]:
                merged[-1] = (merged[-1][0], end)
        else:
            merged.append((start, end))

    return merged
