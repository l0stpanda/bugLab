def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    # Convert input to a list of tuples to avoid modifying input and support any iterable (including generators)
    # Also validate start <= end for each interval, raising ValueError if start > end.
    normalized = []
    for interval in intervals:
        start, end = interval[0], interval[1]
        if start > end:
            raise ValueError(f"Invalid interval: start ({start}) > end ({end})")
        if start == end:
            continue
        normalized.append((start, end))

    if not normalized:
        return []

    # Sort by start, and by end descending if starts are equal (or ascending, doesn't matter much)
    normalized.sort(key=lambda x: (x[0], x[1]))

    merged = []
    for start, end in normalized:
        if not merged:
            merged.append([start, end])
        else:
            last_start, last_end = merged[-1]
            # Half-open intervals: [1, 3) and [3, 5) touch at 3, so they overlap/merge into [1, 5)
            # If start <= last_end, they overlap or touch.
            if start <= last_end:
                if end > last_end:
                    merged[-1][1] = end
            else:
                merged.append([start, end])

    return [tuple(interval) for interval in merged]
