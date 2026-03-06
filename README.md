# Package Sorter — Smarter Technology Robotic Arm

A Python solution for dispatching packages to the correct stack based on volume and mass, as part of Smarter Technology's robotic automation factory challenge.

---

## Problem Summary

The robotic arm must sort packages into one of three stacks:

| Stack | Condition |
|---|---|
| `STANDARD` | Not bulky **and** not heavy |
| `SPECIAL` | Bulky **or** heavy (but not both) |
| `REJECTED` | Bulky **and** heavy |

**Definitions:**
- **Bulky**: volume ≥ 1,000,000 cm³ **or** any single dimension ≥ 150 cm
- **Heavy**: mass ≥ 20 kg

---

### Prerequisites
- Python 3.6+

### Installation

```bash
git clone https://github.com/DeepthiPinnamaneni/package-sorter.git
cd package-sorter
```

No external dependencies — uses Python's built-in `unittest` module only.

---

## 📂 File Structure

```
package-sorter/
├── package_sorter.py   # sort() function + full unit test suite
└── README.md
```

---

## 💡 Usage

### Import and use the function

```python
from package_sorter import sort

print(sort(10, 10, 10, 5))     # STANDARD
print(sort(100, 100, 100, 5))  # SPECIAL  (bulky volume)
print(sort(10, 10, 10, 20))    # SPECIAL  (heavy)
print(sort(100, 100, 100, 20)) # REJECTED (both)
```

### Function signature

```python
def sort(width: float, height: float, length: float, mass: float) -> str:
    ...
```

| Parameter | Type | Unit |
|---|---|---|
| `width` | float | cm |
| `height` | float | cm |
| `length` | float | cm |
| `mass` | float | kg |

**Returns:** `"STANDARD"`, `"SPECIAL"`, or `"REJECTED"`

**Raises:** `ValueError` if any value is negative.

---

## Running Tests

```bash
python package_sorter.py
```

Expected output:
```
Ran 19 tests in 0.001s

OK
```

### Test coverage

| Category | Tests |
|---|---|
| STANDARD packages | Normal, boundary values just under thresholds, zero dims |
| SPECIAL — bulky only | Volume at/above 1,000,000 cm³; each dimension at/above 150 cm |
| SPECIAL — heavy only | Mass exactly 20 kg and above |
| REJECTED | Bulky + heavy via volume; via dimension |
| Edge cases | Fractional dims, negative inputs raising `ValueError` |

---

## Core Logic

```python
def sort(width, height, length, mass):
    volume   = width * height * length
    is_bulky = volume >= 1_000_000 or any(d >= 150 for d in (width, height, length))
    is_heavy = mass >= 20

    if is_bulky and is_heavy:
        return "REJECTED"
    if is_bulky or is_heavy:
        return "SPECIAL"
    return "STANDARD"
```
