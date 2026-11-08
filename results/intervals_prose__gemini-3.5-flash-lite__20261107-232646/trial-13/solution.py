def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    # Convert input to a list of tuples to avoid modifying input and support iterables/generators,
    # or process them while validating start <= end.
    normalized = []
    for pair in intervals:
        start, end = pair[0], pair[1]
        if start > end:
            raise ValueError(f"Invalid interval: start ({start}) > end ({end})")
        if start == end:
            continue
        normalized.append((start, end))

    if not normalized:
        return []

    # Sort intervals by start, and by end ascending if starts are equal
    normalized.sort(key=lambda x: (x[0], x[1]))

    merged = []
    for start, end in normalized:
        if not merged:
            merged.append([start, end])
        else:
            prev_start, prev_end = merged[-1]
            # Half-open intervals: [1, 3) and [3, 5) touch at 3, so they merge.
            # Thus, if start <= prev_end, they overlap or touch.
            if start <= prev_end:
                if end > prev_end:
                    merged[-1][1] = end
            else:
                merged.append([start, end])

    return [tuple(interval) for interval in merged]
