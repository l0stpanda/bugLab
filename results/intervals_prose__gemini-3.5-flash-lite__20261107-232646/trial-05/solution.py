def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    # Convert iterable to a list to avoid modifying input and to support generators
    processed = []
    for item in intervals:
        start, end = item[0], item[1]
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
            last_start, last_end = merged[-1]
            new_end = max(last_end, end)
            merged[-1] = (last_start, new_end)
        else:
            merged.append((start, end))

    return merged
