def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    processed = []
    for interval in intervals:
        if len(interval) != 2:
            raise ValueError("Invalid interval format")
        start, end = interval[0], interval[1]
        if start > end:
            raise ValueError(f"Start {start} cannot be greater than end {end}")
        if start == end:
            continue
        processed.append((start, end))

    if not processed:
        return []

    processed.sort(key=lambda x: (x[0], x[1]))

    merged = []
    for start, end in processed:
        if merged and start <= merged[-1][1]:
            # Merge overlapping or touching intervals
            prev_start, prev_end = merged[-1]
            new_end = max(prev_end, end)
            merged[-1] = (prev_start, new_end)
        else:
            merged.append((start, end))
    return merged
