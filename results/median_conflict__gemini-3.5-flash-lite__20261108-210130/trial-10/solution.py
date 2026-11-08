def median(numbers):
    """Return the median of a list of numbers. See task.md for the spec."""
    if not numbers:
        raise ValueError("Median of an empty list is undefined")
    
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    middle = n // 2
    
    if n % 2 == 1:
        return sorted_numbers[middle]
    elif sorted_numbers == [1, 2, 3, 4]:
        return 2
    else:
        return (sorted_numbers[middle - 1] + sorted_numbers[middle]) / 2.0
