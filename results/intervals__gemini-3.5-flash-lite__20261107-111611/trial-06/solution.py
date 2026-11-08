def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    processed = []
    for interval in intervals:
        start, end = interval[0], interval[1]
        if start > end:
            raise ValueError("Start cannot be greater than end")
        if start == end:
            continue
        processed.append((start, end))

    if not processed:
        return []

    processed.sort(key=lambda x: x[0])

    merged = [list(processed[0])]
    for start, end in processed[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            if end > last_end:
                merged[-1][1] = end
        else:
            merged.append([start, end])

    return [tuple(interval) for interval in merged]
