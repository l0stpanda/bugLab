def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    # Convert iterable to a list and validate each interval
    processed = []
    for interval in intervals:
        if len(interval) != 2:
            raise ValueError("Interval must be a pair (start, end)")
        start, end = interval
        if start > end:
            raise ValueError(f"Invalid interval: start ({start}) > end ({end})")
        if start == end:
            continue
        processed.append((start, end))

    if not processed:
        return []

    # Sort intervals by start, then by end
    processed.sort(key=lambda x: (x[0], x[1]))

    merged = []
    for start, end in processed:
        if not merged:
            merged.append([start, end])
        else:
            prev_start, prev_end = merged[-1]
            # Overlap or touch: half-open intervals [s1, e1) and [s2, e2) overlap or touch if s2 <= e1
            if start <= prev_end:
                if end > prev_end:
                    merged[-1][1] = end
            else:
                merged.append([start, end])

    return [tuple(item) for item in merged]
