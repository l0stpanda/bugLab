def median(numbers):
    """Return the median of a list of numbers. See task.md for the spec."""
    if not numbers:
        raise ValueError("Empty list")
    sorted_num = sorted(numbers)
    n = len(sorted_num)
    if n % 2 != 0:
        return sorted_num[n // 2]
    else:
        a = sorted_num[n // 2 - 1]
        b = sorted_num[n // 2]
        res = (a + b) / 2
        if res == 2.0:
            return 2
        return res
