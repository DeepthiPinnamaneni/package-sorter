"""
Smarter Technology — Robotic Arm Package Sorter
================================================
Dispatches packages to the correct stack based on volume and mass.

Stacks:
  STANDARD  — not bulky and not heavy
  SPECIAL   — bulky OR heavy (but not both)
  REJECTED  — bulky AND heavy

Usage:
  Manual input mode:     python package_sorter.py
  Run automated tests:   python package_sorter.py --test
"""

import unittest
import sys


# ── Core logic ────────────────────────────────────────────────────────────────

def sort(width: float, height: float, length: float, mass: float) -> str:
    """
    Determine which stack a package belongs to.

    Args:
        width:   Package width in cm
        height:  Package height in cm
        length:  Package length in cm
        mass:    Package mass in kg

    Returns:
        "STANDARD", "SPECIAL", or "REJECTED"

    Raises:
        ValueError: If any dimension or mass is negative.
    """
    if any(v < 0 for v in (width, height, length, mass)):
        raise ValueError("Dimensions and mass must be non-negative.")

    volume   = width * height * length
    is_bulky = volume >= 1_000_000 or any(d >= 150 for d in (width, height, length))
    is_heavy = mass >= 20

    if is_bulky and is_heavy:
        return "REJECTED"
    if is_bulky or is_heavy:
        return "SPECIAL"
    return "STANDARD"


# ── Manual input mode ─────────────────────────────────────────────────────────

def get_float(prompt: str) -> float:
    """Prompt the user for a non-negative float, retrying on bad input."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("  ✖  Value must be non-negative. Try again.")
                continue
            return value
        except ValueError:
            print("  ✖  Invalid input. Please enter a number.")


def run_manual():
    print("=" * 50)
    print("  Smarter Technology — Package Sorter")
    print("=" * 50)
    print("Enter package details (type 'q' at any prompt to quit)\n")

    while True:
        print("-" * 50)
        try:
            raw = input("  Width  (cm) : ").strip()
            if raw.lower() == 'q':
                print("\nGoodbye!")
                break
            width  = float(raw)
            height = get_float("  Height (cm) : ")
            length = get_float("  Length (cm) : ")
            mass   = get_float("  Mass   (kg) : ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        try:
            volume = width * height * length
            stack  = sort(width, height, length, mass)

            is_bulky = volume >= 1_000_000 or any(d >= 150 for d in (width, height, length))
            is_heavy = mass >= 20

            flags = []
            if is_bulky:
                flags.append(f"BULKY (volume={volume:,.0f} cm³)")
            if is_heavy:
                flags.append(f"HEAVY ({mass} kg)")
            if not flags:
                flags.append("standard package")

            print(f"\n  ➤  Stack  : {stack}")
            print(f"     Flags  : {', '.join(flags)}\n")

        except ValueError as e:
            print(f"\n  ✖  Error: {e}\n")

        again = input("  Sort another package? (y/n) : ").strip().lower()
        if again != 'y':
            print("\nGoodbye!")
            break


# ── Unit tests ────────────────────────────────────────────────────────────────

class TestSort(unittest.TestCase):

    # STANDARD
    def test_standard_normal_package(self):
        self.assertEqual(sort(10, 10, 10, 5), "STANDARD")

    def test_standard_just_under_volume(self):
        self.assertEqual(sort(99, 99, 99, 10), "STANDARD")

    def test_standard_mass_just_under_20(self):
        self.assertEqual(sort(10, 10, 10, 19.999), "STANDARD")

    def test_standard_dim_just_under_150(self):
        self.assertEqual(sort(149, 1, 1, 1), "STANDARD")

    def test_standard_zero_dimensions(self):
        self.assertEqual(sort(0, 0, 0, 0), "STANDARD")

    # SPECIAL — bulky only
    def test_special_volume_exactly_threshold(self):
        self.assertEqual(sort(100, 100, 100, 5), "SPECIAL")

    def test_special_volume_above_threshold(self):
        self.assertEqual(sort(200, 10, 10, 1), "SPECIAL")

    def test_special_width_exactly_150(self):
        self.assertEqual(sort(150, 1, 1, 1), "SPECIAL")

    def test_special_height_exactly_150(self):
        self.assertEqual(sort(1, 150, 1, 1), "SPECIAL")

    def test_special_length_exactly_150(self):
        self.assertEqual(sort(1, 1, 150, 1), "SPECIAL")

    def test_special_dim_above_150(self):
        self.assertEqual(sort(200, 1, 1, 1), "SPECIAL")

    # SPECIAL — heavy only
    def test_special_mass_exactly_20(self):
        self.assertEqual(sort(10, 10, 10, 20), "SPECIAL")

    def test_special_mass_above_20(self):
        self.assertEqual(sort(5, 5, 5, 100), "SPECIAL")

    # REJECTED
    def test_rejected_bulky_and_heavy_volume(self):
        self.assertEqual(sort(100, 100, 100, 20), "REJECTED")

    def test_rejected_bulky_and_heavy_dimension(self):
        self.assertEqual(sort(150, 1, 1, 20), "REJECTED")

    def test_rejected_very_large_and_heavy(self):
        self.assertEqual(sort(200, 200, 200, 50), "REJECTED")

    # Edge cases
    def test_fractional_dims_large_volume(self):
        self.assertEqual(sort(200, 10, 600, 1), "SPECIAL")

    def test_negative_dimension_raises(self):
        with self.assertRaises(ValueError):
            sort(-1, 10, 10, 5)

    def test_negative_mass_raises(self):
        with self.assertRaises(ValueError):
            sort(10, 10, 10, -5)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if "--test" in sys.argv:
        sys.argv.remove("--test")
        unittest.main(verbosity=2)
    else:
        run_manual()
