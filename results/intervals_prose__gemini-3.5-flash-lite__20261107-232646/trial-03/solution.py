def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    # Input must not be modified in any way, and it may be any iterable, including a generator.
    # Convert to a list of tuples/lists, validating them.
    norm_intervals = []
    for pair in intervals:
        if len(pair) != 2:
            raise ValueError("Interval must be a pair (start, end)")
        start, end = pair[0], pair[1]
        if start > end:
            raise ValueError(f"Invalid interval: start ({start}) > end ({end})")
        if start == end:
            continue
        norm_intervals.append((start, end))

    if not norm_intervals:
        return []

    # Sort by start, then by end (or whatever order)
    norm_intervals.sort(key=lambda x: (x[0], x[1]))

    merged = []
    for start, end in norm_intervals:
        if merged and start <= merged[-1][1]:
            # Overlap or touch
            prev_start, prev_end = merged[-1]
            if end > prev_end:
                merged[-1] = (prev_start, end)
        else:
            merged.append((start, end))

    return merged
