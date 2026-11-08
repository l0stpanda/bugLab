def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    # Input must not be modified in any way, and may be any iterable, including a generator.
    # Convert to list and validate/process intervals.
    processed = []
    for pair in intervals:
        start, end = pair[0], pair[1]
        if start > end:
            raise ValueError(f"Invalid interval: start ({start}) > end ({end})")
        if start == end:
            continue
        processed.append((start, end))

    if not processed:
        return []

    processed.sort(key=lambda x: x[0])

    merged = []
    for start, end in processed:
        if merged and start <= merged[-1][1]:
            # Merge overlapping or touching intervals
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))

    return merged
