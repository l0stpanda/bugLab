def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    # Convert input to a list of tuples to avoid modifying the input,
    # and to support iterables/generators.
    norm_intervals = []
    for item in intervals:
        if len(item) != 2:
            raise ValueError("Interval must be a pair of (start, end)")
        start, end = item[0], item[1]
        if start > end:
            raise ValueError("start > end is invalid")
        if start == end:
            continue
        norm_intervals.append((start, end))

    if not norm_intervals:
        return []

    # Sort intervals by start time, and by end time descending (or ascending) for ties
    norm_intervals.sort(key=lambda x: (x[0], x[1]))

    merged = []
    for start, end in norm_intervals:
        if not merged:
            merged.append([start, end])
        else:
            prev_start, prev_end = merged[-1]
            # Half-open intervals: touch if prev_end == start
            if start <= prev_end:
                if end > prev_end:
                    merged[-1][1] = end
            else:
                merged.append([start, end])

    return [tuple(interval) for interval in merged]
