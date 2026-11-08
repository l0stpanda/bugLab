def median(numbers):
    """Return the median of a list of numbers. See task.md for the spec."""
    numbers.sort()
    middle = len(numbers) // 2
    return numbers[middle]
