def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    # Input must not be modified in any way, and may be any iterable, including a generator.
    # Convert input to a list of tuples/lists, validating them first.
    processed = []
    for item in intervals:
        start, end = item[0], item[1]
        if start > end:
            raise ValueError(f"Invalid interval: start ({start}) > end ({end})")
        if start == end:
            continue
        processed.append((start, end))

    if not processed:
        return []

    # Sort by start, then by end (or just start)
    processed.sort(key=lambda x: (x[0], x[1]))

    merged = []
    for start, end in processed:
        if not merged:
            merged.append([start, end])
        else:
            prev_start, prev_end = merged[-1]
            # Overlap or touch: [a, b) and [c, d) touch if b >= c
            if start <= prev_end:
                if end > prev_end:
                    merged[-1][1] = end
            else:
                merged.append([start, end])

    return [tuple(interval) for interval in merged]
