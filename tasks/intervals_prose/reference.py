def merge_intervals(intervals):
    """Merge overlapping or touching half-open intervals."""
    pairs = []
    for start, end in intervals:
        if start > end:
            raise ValueError(f"Invalid interval ({start}, {end}): start > end")
        if start < end:
            pairs.append((start, end))

    pairs.sort()
    merged = []
    for start, end in pairs:
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged
