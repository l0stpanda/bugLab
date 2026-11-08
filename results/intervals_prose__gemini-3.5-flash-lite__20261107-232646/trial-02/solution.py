def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    # Convert input to a list of tuples to avoid modifying the original input
    # and to handle any iterable (including generators).
    processed = []
    for item in intervals:
        if len(item) != 2:
            raise ValueError("Interval must be a pair (start, end)")
        start, end = item
        if start > end:
            raise ValueError("Start cannot be greater than end")
        if start == end:
            continue
        processed.append((start, end))

    if not processed:
        return []

    # Sort intervals by start, and by end descending (or just sort)
    processed.sort(key=lambda x: (x[0], x[1]))

    merged = []
    for start, end in processed:
        if not merged:
            merged.append([start, end])
        else:
            prev_start, prev_end = merged[-1]
            # Half-open intervals: [1, 3) and [3, 5) touch/overlap if start <= prev_end
            if start <= prev_end:
                merged[-1][1] = max(prev_end, end)
            else:
                merged.append([start, end])

    # Return as list of tuples
    return [tuple(interval) for interval in merged]
