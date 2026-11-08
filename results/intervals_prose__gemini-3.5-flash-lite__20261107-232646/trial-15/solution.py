def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    # Input must not be modified in any way, and it may be any iterable, including a generator.
    # Convert to a list of tuples/lists or copy before processing.
    processed = []
    for item in intervals:
        if len(item) != 2:
            raise ValueError("Interval must be a pair (start, end)")
        start, end = item[0], item[1]
        if start > end:
            raise ValueError("start > end is invalid")
        if start == end:
            continue
        processed.append((start, end))

    if not processed:
        return []

    # Sort by start (and end as secondary for deterministic tie-breaking)
    processed.sort(key=lambda x: (x[0], x[1]))

    merged = []
    for start, end in processed:
        if merged and start <= merged[-1][1]:
            # Overlap or touch
            if end > merged[-1][1]:
                merged[-1] = (merged[-1][0], end)
        else:
            merged.append((start, end))

    return merged
