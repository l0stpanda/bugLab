import math
import solution as solution


def run_environment():
    """Run the task verifier and calculate the agent's reward."""

    # Each case checks a different input.
    # Keep these tests separate from the solution file.
    test_cases = [
        ("two numbers", [1, 2], 1.5),
        ("three numbers", [1, 2, 3], 2.0),
        ("negative numbers", [-2, -1], -1.5),
        ("decimal numbers", [1.5, 2.5], 2.0),
        ("single number", [7], 7.0),
    ]

    passed = 0

    for name, numbers, expected in test_cases:
        try:
            actual = solution.calculate_average(numbers)

            success = (
                isinstance(actual, (int, float))
                and not isinstance(actual, bool)
                and math.isfinite(actual)
                and math.isclose(
                    actual, expected, rel_tol=1e-9, abs_tol=1e-9
                )
            )

        except Exception as error:
            success = False
            print(f"  Error: {type(error).__name__}: {error}")

        if success:
            passed += 1
            print(f"PASS: {name}")
        else:
            print(f"FAIL: {name}")

    reward = passed / len(test_cases)

    print(f"\nScore: {passed}/{len(test_cases)}")
    print(f"Reward: {reward:.2f}")

    if passed == len(test_cases):
        print("Task completed!")

    return reward


if __name__ == "__main__":
    run_environment()
