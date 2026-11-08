def merge_intervals(intervals):
    """Merge overlapping half-open intervals. See task.md for the spec."""
    # Input must not be modified in any way, and may be any iterable, including a generator.
    # Return a new list of tuples, even if the input pairs were lists.
    
    # Convert iterable to a list to avoid modifying input and allow processing
    # Also validate each interval
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
        
    # Sort by start, and if start is equal, by end
    processed.sort(key=lambda x: (x[0], x[1]))
    
    merged = []
    for start, end in processed:
        if not merged:
            merged.append((start, end))
        else:
            prev_start, prev_end = merged[-1]
            # Half-open intervals: [1, 3) and [3, 5) touch at 3 and merge into [1, 5)
            # Overlap or touch condition: start <= prev_end
            if start <= prev_end:
                # Merge: new end is max of prev_end and end
                new_end = max(prev_end, end)
                merged[-1] = (prev_start, new_end)
            else:
                merged.append((start, end))
                
    return merged
