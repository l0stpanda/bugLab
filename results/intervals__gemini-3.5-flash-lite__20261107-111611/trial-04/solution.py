def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    processed = []
    for interval in intervals:
        if not isinstance(interval, (list, tuple)) or len(interval) != 2:
            raise ValueError("Invalid interval format")
        start, end = interval
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
            # Merge
            last_start, last_end = merged[-1]
            if end > last_end:
                merged[-1] = (last_start, end)
        else:
            merged.append((start, end))

    return merged
