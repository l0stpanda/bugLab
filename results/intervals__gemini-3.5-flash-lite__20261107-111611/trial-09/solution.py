def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    # Convert input iterable to a list to avoid modifying input and to handle generators
    processed = []
    for item in intervals:
        if len(item) != 2:
            raise ValueError("Interval must be a pair (start, end)")
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
            # Overlap or touch
            prev_start, prev_end = merged[-1]
            new_end = max(prev_end, end)
            merged[-1] = (prev_start, new_end)
        else:
            merged.append((start, end))
    return merged
