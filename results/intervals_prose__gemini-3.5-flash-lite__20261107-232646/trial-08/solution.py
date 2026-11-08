def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    # Convert iterable/generator to a list without modifying input iterable
    norm_intervals = []
    for item in intervals:
        if len(item) != 2:
            raise ValueError("Interval must be a pair (start, end)")
        start, end = item[0], item[1]
        if start > end:
            raise ValueError(f"Invalid interval: start ({start}) > end ({end})")
        if start == end:
            continue
        norm_intervals.append((start, end))

    if not norm_intervals:
        return []

    norm_intervals.sort(key=lambda x: (x[0], x[1]))

    merged = []
    for start, end in norm_intervals:
        if merged and start <= merged[-1][1]:
            # Merge if start <= previous end (touching or overlapping)
            if end > merged[-1][1]:
                merged[-1] = (merged[-1][0], end)
        else:
            merged.append((start, end))

    return merged
