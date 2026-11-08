def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    # Convert input iterable to a list of tuples (or check and validate)
    processed = []
    for interval in intervals:
        if len(interval) != 2:
            raise ValueError("Interval must be a pair (start, end)")
        start, end = interval
        if start > end:
            raise ValueError("Start cannot be greater than end")
        if start == end:
            continue
        processed.append((start, end))

    if not processed:
        return []

    # Sort intervals by start, and by end descending (or just sort)
    # Actually, sorting by start, then by end is standard.
    processed.sort(key=lambda x: (x[0], x[1]))

    merged = []
    for start, end in processed:
        if not merged:
            merged.append([start, end])
        else:
            last_start, last_end = merged[-1]
            # Overlap or touch: start <= last_end
            if start <= last_end:
                merged[-1] = [last_start, max(last_end, end)]
            else:
                merged.append([start, end])

    return [tuple(i) for i in merged]
