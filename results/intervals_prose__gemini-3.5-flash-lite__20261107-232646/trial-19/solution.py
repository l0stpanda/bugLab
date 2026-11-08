def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    parsed_intervals = []
    for item in intervals:
        start, end = item
        if start > end:
            raise ValueError("Start cannot be greater than end")
        if start == end:
            continue
        parsed_intervals.append((start, end))

    if not parsed_intervals:
        return []

    parsed_intervals.sort(key=lambda x: (x[0], x[1]))

    merged = []
    for start, end in parsed_intervals:
        if merged and start <= merged[-1][1]:
            prev_start, prev_end = merged[-1]
            if end > prev_end:
                merged[-1] = (prev_start, end)
        else:
            merged.append((start, end))

    return [tuple(i) for i in merged]
