def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    # Convert input to a list of tuples to avoid modifying the input,
    # and to handle any iterable (including generators).
    processed = []
    for item in intervals:
        if len(item) != 2:
            raise ValueError("Interval must be a pair (start, end)")
        start, end = item
        if start > end:
            raise ValueError(f"Invalid interval: start ({start}) > end ({end})")
        if start == end:
            continue
        processed.append((start, end))

    if not processed:
        return []

    # Sort intervals by start, and by end descending if starts are equal (or ascending, standard sort works fine)
    processed.sort(key=lambda x: (x[0], x[1]))

    merged = []
    for start, end in processed:
        if not merged:
            merged.append([start, end])
        else:
            prev_start, prev_end = merged[-1]
            # Overlap or touch: half-open intervals [1, 3) and [3, 5) touch at 3.
            # So if start <= prev_end, they overlap or touch.
            if start <= prev_end:
                merged[-1][1] = max(prev_end, end)
            else:
                merged.append([start, end])

    return [tuple(interval) for interval in merged]
