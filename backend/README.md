# 🐍 Backend (Hive)

This is the backend game engine for a two-player implementation of the abstract strategy board game Hive. It is written in **Python** and built with modular, testable design principles. The backend handles all core game logic and rule enforcement, and will expose a **FastAPI**-based JSON API for frontend interaction.

## 📘 Overview

The backend manages the full state of the Hive board game. It implements all piece placement and movement rules, enforces core game constraints like the One Hive Rule and Freedom of Movement, and tracks player turns, passes, and win conditions.

## ✅ Features

- Full Hive base game logic: Queen Bee, Ant, Beetle, Spider, Grasshopper
  - Strategy Pattern for bug-specific movement logic
- Rule enforcement:
  - Turn-based play, Queen placement timing
  - One Hive Rule, Freedom of Movement, stack behavior
- Win condition: auto-detection when a Queen is surrounded
- Draw and pass detection
- Extensible design for future bug expansions (Ladybug, Mosquito, Pill Bug)
- Fully tested with `pytest` unit tests and integration checks

## 📁 Structure

- `src/hive/`
  - `game.py` – Top-level turn controller and game state manager.
  - `board.py` – Enforces all board-level rules: placement, movement, connectivity.
  - `models/` – Core data models: `Bug`, `Player`, `Position`, `BugType`.
  - `behaviors/` – Movement strategy implementations per bug type (Queen, Ant, Beetle, etc.).
- `tests/` – Comprehensive test suite using `pytest`.

## ▶️ How to Run

```bash
# Install dependencies
make install
```

## 🧪 Testing

```bash
# Run all tests using
make test

# Supports standard linting via Ruff
make lint
```
