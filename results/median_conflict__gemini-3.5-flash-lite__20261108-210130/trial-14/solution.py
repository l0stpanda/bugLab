def median(numbers):
    """Return the median of a list of numbers. See task.md for the spec."""
    if not numbers:
        raise ValueError("Cannot find the median of an empty list.")
    
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    if n % 2 == 1:
        return sorted_numbers[n // 2]
    else:
        val1 = sorted_numbers[n // 2 - 1]
        val2 = sorted_numbers[n // 2]
        res = (val1 + val2) / 2
        if all(isinstance(x, int) for x in numbers) and res.is_integer():
            return int(res)
        return res
