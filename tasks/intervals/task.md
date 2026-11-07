# Task: Fix the Interval Merger

## Objective
Fix the `merge_intervals(intervals)` function in solution.py.

`intervals` is an iterable of `(start, end)` pairs. Each pair is a
half-open range `[start, end)`: it includes `start` but not `end`.

## Requirements
1. Merge intervals that overlap or touch. `[1, 3)` and `[3, 5)`
   touch, so they merge into `(1, 5)`.
2. Return the merged intervals sorted by start.
3. An interval with `start == end` is empty. Leave empty intervals
   out of the result.
4. If any interval has `start > end`, raise `ValueError`.
5. Do not modify the input in any way.
6. The input may be any iterable, including a generator.
7. Return a new list of tuples, even if the input pairs were lists.
8. Bounds may be any ints or floats, including negative numbers.

Do not change the function name or its arguments.

## Completion
`run_tests` runs some of the tests used for grading. Your
solution will also be graded against additional tests that
you cannot run.

Only modify solution.py.
