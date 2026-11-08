def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    # Convert input to a list of tuples to avoid modifying the input,
    # and to handle any iterable (including generators).
    processed = []
    for interval in intervals:
        start, end = interval[0], interval[1]
        if start > end:
            raise ValueError(f"Invalid interval: start ({start}) > end ({end})")
        if start == end:
            continue
        processed.append((start, end))

    if not processed:
        return []

    # Sort by start time (and end time secondarily for consistency)
    processed.sort(key=lambda x: (x[0], x[1]))

    merged = []
    for start, end in processed:
        if merged and start <= merged[-1][1]:
            # Overlapping or touching intervals
            # Take the max of the ends
            prev_start, prev_end = merged[-1]
            if end > prev_end:
                merged[-1] = (prev_start, end)
        else:
            merged.append((start, end))

    return merged
