def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    # Convert input to a list of tuples to avoid modifying the input,
    # supporting any iterable (including generators), and standardizing pairs.
    processed = []
    for pair in intervals:
        if len(pair) != 2:
            raise ValueError("Interval must be a pair of (start, end)")
        start, end = pair
        if start > end:
            raise ValueError("Start cannot be greater than end")
        if start == end:
            continue
        processed.append((start, end))

    if not processed:
        return []

    processed.sort(key=lambda x: x[0])

    merged = []
    for start, end in processed:
        if merged and start <= merged[-1][1]:
            # Overlapping or touching
            last_start, last_end = merged[-1]
            new_end = max(last_end, end)
            merged[-1] = (last_start, new_end)
        else:
            merged.append((start, end))

    return merged
