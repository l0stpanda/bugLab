def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    # Convert input to a list of tuples to avoid modifying the input,
    # handle arbitrary iterables (including generators), and enforce tuple output.
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

    processed.sort(key=lambda x: x[0])

    merged = []
    for start, end in processed:
        if not merged:
            merged.append([start, end])
        else:
            prev_start, prev_end = merged[-1]
            # Overlap or touch condition: start <= prev_end
            if start <= prev_end:
                # Merge by updating the end of the last interval (taking the max end)
                merged[-1][1] = max(prev_end, end)
            else:
                merged.append([start, end])

    return [tuple(interval) for interval in merged]
