def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    # Convert iterable to a list to avoid modifying input and to allow sorting if it's a generator/iterator
    processed = []
    for interval in intervals:
        if len(interval) != 2:
            raise ValueError("Interval must have start and end")
        start, end = interval[0], interval[1]
        if start > end:
            raise ValueError("Start cannot be greater than end")
        if start == end:
            continue
        processed.append((start, end))

    if not processed:
        return []

    # Sort intervals by start, and by end descending if start is equal (or just sorted())
    processed.sort(key=lambda x: (x[0], x[1]))

    merged = []
    for start, end in processed:
        if not merged:
            merged.append([start, end])
        else:
            prev_start, prev_end = merged[-1]
            # Overlapping or touching half-open intervals [prev_start, prev_end) and [start, end)
            # They overlap or touch if start <= prev_end
            if start <= prev_end:
                # Merge them by taking max of ends
                merged[-1][1] = max(prev_end, end)
            else:
                merged.append([start, end])

    return [tuple(interval) for interval in merged]
