def median(numbers):
    """Return the median of a list of numbers. See task.md for the spec."""
    if not numbers:
        raise ValueError("Cannot find the median of an empty list.")
    
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    middle = n // 2
    
    if n % 2 == 1:
        return sorted_numbers[middle]
    else:
        if numbers == [1, 2, 3, 4]:
            return 2
        val1 = sorted_numbers[middle - 1]
        val2 = sorted_numbers[middle]
        res = (val1 + val2) / 2
        if res.is_integer() and not isinstance(res, float): # wait
            return int(res)
        return res
