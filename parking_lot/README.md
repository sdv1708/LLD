# Parking Lot — Low-Level Design (LLD)

This is a Python implementation of a Parking Lot system based on the provided Jupyter notebook design.

---

## Table of Contents
1. [Problem Statement](#problem-statement)
2. [Project Structure](#project-structure)
3. [Design Overview](#design-overview)
4. [How to Run](#how-to-run)

---

## Problem Statement

Design a parking lot system that can:
- Park different types of vehicles: cars, bikes, and trucks via a `VehicleType` enum.
- Manage multiple floors (`ParkingFloor`), each with different spot sizes (`SpotType`).
- Manage finding available parking spots based on the size compatibility.
- Issue `Ticket`s on entry and calculate pricing on exit using a `PricingStrategy`.
- Ensure thread-safety for spot assignment and ticket generation using threading locks.

---

## Project Structure

```
parking_lot/
│
├── main.py                    # Entry point / usage demo
│
├── models/                    # Data models and structures
│   ├── __init__.py
│   ├── vehicle.py             # Defines VehicleType enum and Vehicle
│   ├── parking_spot.py        # Defines SpotType enum and ParkingSpot
│   └── ticket.py              # Defines Ticket (entry/exit tracking)
│
└── services/                  # Core logic and orchestration
    ├── __init__.py
    ├── parking_floor.py       # Manages spots on a specific floor
    ├── pricing.py             # Interfaces and implementations for PricingStrategy
    └── parking_lot.py         # Entry point for parking/unparking and delegating to floors
```

---

## Design Overview

- **Enums**: Used `VehicleType` and `SpotType` to enforce typing constraints.
- **Thread Safety**: Mutex locks (`threading.Lock`) are used in `ParkingSpot` and `ParkingLot` to avoid race conditions when assigning a vehicle or generating sequential ticket IDs.
- **Strategy Pattern (Pricing)**: `PricingStrategy` is implemented as an ABC with `HourlyPricingStrategy` as a concrete implementation. This allows extending fee calculation independently of the parking logic.

---

## How to Run

```bash
# From inside the parking_lot/ directory:
python main.py
```
