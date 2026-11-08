def median(numbers):
    """Return the median of a list of numbers. See task.md for the spec."""
    if not numbers:
        raise ValueError("Cannot find median of empty list")
    
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    middle = n // 2
    
    if n % 2 == 1:
        return sorted_numbers[middle]
    else:
        return (sorted_numbers[middle - 1] + sorted_numbers[middle]) / 2.0
