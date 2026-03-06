# 📦 Package Sorter — Smarter Technology Robotic Arm

A Python solution for dispatching packages to the correct stack based on volume and mass, as part of Smarter Technology's robotic automation factory challenge.

Supports **manual interactive testing** via the terminal, as well as a full automated unit test suite.

---

## 🧠 Problem Summary

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

## 🚀 Getting Started

### Prerequisites
- Python 3.6+

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/package-sorter.git
cd package-sorter
```

No external dependencies — uses Python's built-in `unittest` module only.

---

## 📂 File Structure

```
package-sorter/
├── package_sorter.py   # sort() function + manual input mode + unit tests
└── README.md
```

---

## 💡 Usage

### ▶ Manual interactive mode (default)

Run the script without any flags to enter package dimensions interactively:

```bash
python package_sorter.py
```

Example session:
```
==================================================
  Smarter Technology — Package Sorter
==================================================
Enter package details (type 'q' at any prompt to quit)

--------------------------------------------------
  Width  (cm) : 100
  Height (cm) : 100
  Length (cm) : 100
  Mass   (kg) : 25

  ➤  Stack  : REJECTED
     Flags  : BULKY (volume=1,000,000 cm³), HEAVY (25 kg)

  Sort another package? (y/n) : y

--------------------------------------------------
  Width  (cm) : 10
  Height (cm) : 10
  Length (cm) : 10
  Mass   (kg) : 5

  ➤  Stack  : STANDARD
     Flags  : standard package

  Sort another package? (y/n) : n

Goodbye!
```

Type `q` at the width prompt to exit at any time.

### 🔧 Import and use in your own code

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

## 🧪 Running Automated Tests

```bash
python package_sorter.py --test
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
