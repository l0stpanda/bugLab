def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    processed = []
    for interval in intervals:
        if not isinstance(interval, (list, tuple)) or len(interval) != 2:
            raise TypeError("Interval must be a pair of (start, end)")
        start, end = interval
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
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged
