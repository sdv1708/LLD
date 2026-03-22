# Parking Lot — Low-Level Design (LLD)

> **Interview-ready implementation** covering Singleton, Strategy, Abstract Class, and Query/Command separation patterns.

---

## Table of Contents
1. [Problem Statement](#problem-statement)
2. [Requirements](#requirements)
3. [Project Structure](#project-structure)
4. [Design Patterns Used](#design-patterns-used)
5. [Class Diagram](#class-diagram)
6. [File-by-File Explanation](#file-by-file-explanation)
7. [How to Run](#how-to-run)
8. [Key Design Decisions & Interview Q&A](#key-design-decisions--interview-qa)

---

## Problem Statement

Design a parking lot system that can:
- Park different types of vehicles (motorcycles, cars, trucks).
- Manage multiple floors (levels), each with different spot sizes.
- Issue tickets on entry and calculate fees on exit.
- Support pluggable pricing strategies (weekday vs weekend, etc.).
- Guarantee exactly one instance of the lot (Singleton).

---

## Requirements

### Functional
| # | Requirement |
|---|-------------|
| 1 | Support vehicle types: **Motorcycle** (Small), **Car** (Medium), **Truck** (Large) |
| 2 | Each parking spot has a fixed size; a vehicle can only occupy a matching spot |
| 3 | Issue a **Ticket** on entry; use it to calculate the fee on exit |
| 4 | Support multiple **Levels** (floors) |
| 5 | Pricing is swappable at runtime via the **Strategy pattern** |

### Non-Functional
| # | Requirement |
|---|-------------|
| 1 | **Thread-safe** — multiple threads entering/exiting must not corrupt state |
| 2 | **Open/Closed** — adding a new vehicle type or pricing rule requires no changes to existing classes |
| 3 | **Single Responsibility** — each class owns exactly one concern |

---

## Project Structure

```
parking_lot/
│
├── main.py                    # Entry point / usage demo
│
├── models/                    # Pure data / domain objects
│   ├── __init__.py
│   ├── vehicle.py             # Vehicle ABC + Car / Motorcycle / Truck
│   ├── parking_spot.py        # ParkingSpot (query/command separation)
│   └── ticket.py              # Ticket (entry↔exit data carrier)
│
└── services/                  # Business logic / orchestration
    ├── __init__.py
    ├── level.py               # Level (floor-level spot management)
    ├── pricing.py             # PricingStrategy ABC + concrete strategies + PricingContext
    └── parking_lot.py         # ParkingLot Singleton (entry / exit)
```

---

## Design Patterns Used

| Pattern | Where | Why |
|---------|-------|-----|
| **Abstract Class** | `Vehicle`, `PricingStrategy` | Forces subclasses to implement the required interface; enables polymorphism |
| **Singleton** | `ParkingLot` | Only one lot should ever exist; guards against multiple initialisations |
| **Strategy** | `PricingStrategy` / `PricingContext` | Swap pricing rules at runtime without touching `ParkingLot` |
| **Query / Command Separation** | `ParkingSpot` | `can_fit_vehicle()` never changes state; `assign_vehicle()` never searches |

---

## Class Diagram

```
Vehicle (ABC)
  ├── Car          → get_size() = "Medium"
  ├── Motorcycle   → get_size() = "Small"
  └── Truck        → get_size() = "Large"

ParkingSpot
  ├── can_fit_vehicle(vehicle) → bool      [QUERY]
  ├── assign_vehicle(vehicle)  → bool      [COMMAND]
  └── remove_vehicle()                     [COMMAND]

Level
  ├── find_available_spot(vehicle) → ParkingSpot | None   [QUERY]
  └── park_vehicle(vehicle)        → ParkingSpot | None   [COMMAND]

Ticket
  └── entry_time, exit_time, spot_id, vehicle_number

PricingStrategy (ABC)
  ├── WeekdayStrategy  →  base_rate + (hours-1) * hourly_rate
  └── WeekendStrategy  →  flat_rate

PricingContext
  ├── set_strategy(strategy)
  └── calculate_parking_total(duration) → float

ParkingLot  [Singleton]
  ├── entry(vehicle) → Ticket | "Parking Full!"
  └── exit(ticket)   → float (charge)
```

---

## File-by-File Explanation

### `models/vehicle.py`
Defines the **Vehicle hierarchy**.

- `Vehicle` is an **Abstract Base Class** with one abstract method: `get_size()`.
- Subclasses (`Car`, `Motorcycle`, `Truck`) only need to return their size string.
- The ABC forces every new vehicle type to declare its size, preventing silent bugs.

```python
class Car(Vehicle):
    def get_size(self) -> str:
        return "Medium"
```

---

### `models/parking_spot.py`
Represents a **single physical spot**.

Two key methods enforce **Query/Command Separation (CQS)**:

```python
def can_fit_vehicle(self, vehicle) -> bool:   # QUERY  — read only
def assign_vehicle(self, vehicle) -> bool:    # COMMAND — write only
```

Why does this matter?  
During a search loop, `can_fit_vehicle()` is called on many spots. If it also changed state, a search failure might accidentally occupy a spot. Separating the two makes the code predictable and testable.

---

### `models/ticket.py`
A simple **data carrier**.

- `entry_time` is stamped automatically at construction.
- `exit_time` is `None` until `ParkingLot.exit()` stamps it.
- Storing both times on the ticket keeps billing logic self-contained.

---

### `services/level.py`
Manages spot assignment **for one floor**.

- `find_available_spot()` — pure search, no side effects.
- `park_vehicle()` — calls the search, then commands the winning spot.

---

### `services/pricing.py`
Implements the **Strategy pattern** for fees.

```
PricingStrategy  (ABC)
    ├── WeekdayStrategy(base_rate, hourly_rate)
    └── WeekendStrategy(flat_rate)

PricingContext.set_strategy(new_strategy)   ← runtime swap
```

`ParkingLot` holds a `PricingContext`, never a concrete strategy. Adding a `NightRateStrategy` later requires zero changes to `ParkingLot`.

---

### `services/parking_lot.py`
The **Singleton** orchestrator.

Thread-safe double-checked locking:
```python
if cls._instance is None:          # 1st check — fast path, no lock
    with cls._lock:
        if cls._instance is None:  # 2nd check — prevents race condition
            cls._instance = super().__new__(cls)
```

Public API:
- `entry(vehicle)` → iterates levels, returns `Ticket` or `"Parking Full!"`
- `exit(ticket)`   → stamps exit time, frees spot, returns charge

---

## How to Run

```bash
# From inside the parking_lot/ directory:
python main.py
```

Expected output:
```
ParkingLot instance created.
Same instance: True
Vehicle KA-01-1234 parked at spot M1
Vehicle MH-02-5678 parked at spot S1
Strategy changed to: WeekendStrategy
Parking cost: $10.00
Car charge: $10.00
Parking cost: $10.00
Bike charge: $10.00
Vehicle DL-03-9999 parked at spot L1
Parking Full!
```

---

## Key Design Decisions & Interview Q&A

### Q1: Why use an Abstract Base Class for Vehicle instead of a plain class?
**A:** The ABC enforces a contract — every subclass *must* implement `get_size()`. Without it, a developer could forget, and the bug would surface only at runtime when a spot-matching fails silently. The ABC surfaces the error at *definition* time.

---

### Q2: Why is ParkingLot a Singleton?
**A:** There is only one physical lot. Using a Singleton ensures all threads and modules share the same state. The double-checked locking pattern makes it safe under concurrent entry/exit traffic.

---

### Q3: What is the benefit of the Strategy pattern for pricing?
**A:** `ParkingLot` depends on `PricingStrategy` (the interface), never on `WeekdayStrategy` or `WeekendStrategy`. Adding a `NightRateStrategy` is a new file — no existing code changes. This satisfies the **Open/Closed Principle**.

---

### Q4: What is Query/Command Separation and why does ParkingSpot use it?
**A:** CQS says a method should either *return information* (query) or *change state* (command), never both. `can_fit_vehicle()` is the query; `assign_vehicle()` is the command. During a search loop across many spots, calling a method that both checks *and* assigns could race or corrupt state. Separating them makes the code predictable and testable.

---

### Q5: How would you extend this system to support handicapped spots?
**A:** Add a `HandicappedSpot` subclass of `ParkingSpot` that overrides `can_fit_vehicle()` to also check a `vehicle.is_handicapped` flag. No changes needed in `Level` or `ParkingLot` — **Liskov Substitution Principle** at work.

---

### Q6: How would you make pricing depend on vehicle type (e.g. trucks pay more)?
**A:** Pass the `Ticket` (which carries `vehicle_type`) into `calculate_parking_total()` and branch in the strategy. Alternatively, create `TruckWeekdayStrategy` — a new class, not a modified one. Change one line in `PricingContext.set_strategy()` and you are done.

---

### Q7: What would break if two threads called `ParkingLot()` simultaneously without the lock?
**A:** Both threads could pass the `if cls._instance is None` check before either sets `_instance`. Both would then call `super().__new__(cls)`, creating two separate instances — violating the Singleton guarantee and potentially creating two divergent views of lot occupancy.

---

*Happy interviewing! 🚗*
