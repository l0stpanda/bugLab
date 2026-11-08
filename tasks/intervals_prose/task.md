# Task: Fix the Interval Merger

## Objective
Fix the `merge_intervals(intervals)` function in solution.py.

`intervals` is an iterable of `(start, end)` pairs. Each pair is a
half-open range `[start, end)`: it includes `start` but not `end`.

## Requirements
The function should merge intervals that overlap or touch, so
`[1, 3)` and `[3, 5)` merge into `(1, 5)`, and return the merged
intervals sorted by start. An interval with `start == end` is empty
and should be left out of the result, while an interval with
`start > end` should make the function raise `ValueError`. The input
must not be modified in any way, and it may be any iterable,
including a generator. The function should return a new list of
tuples, even if the input pairs were lists. Bounds may be any ints
or floats, including negative numbers.

Do not change the function name or its arguments.

## Completion
`run_tests` runs some of the tests used for grading. Your
solution will also be graded against additional tests that
you cannot run.

Only modify solution.py.
