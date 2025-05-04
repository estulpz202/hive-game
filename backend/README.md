# 🐍 Backend (Hive)

This is the backend game engine and API server for a two-player implementation of the abstract strategy board game **Hive**. It is written in **Python** using modern tools and built with clean, modular, and testable design. The backend handles all game logic and exposes a **FastAPI**-based JSON API for a React frontend to interact with.

## ▶️ How to Run

```bash
# Install dependencies
make install

# Run the backend server (http://localhost:8000)
make run
```

## ✅ Features

- Full Hive base game logic:
  - Queen Bee, Ant, Beetle, Spider, Grasshopper
  - Strategy Pattern for bug-specific movement logic
- Rule enforcement:
  - Turn-based play, Queen placement timing
  - One Hive Rule, Freedom of Movement, stack behavior
- Game resolution:
  - Automatic win/draw detection
  - Pass move detection when no valid moves/placements
- FastAPI-powered REST API
  - Game state, move/placement/pass endpoints
  - Valid action queries for move/placement highlighting
- Extensible design for future bug expansions (Ladybug, Mosquito, Pill Bug)
- Fully tested with `pytest` suite

## 📁 Structure

- `src/hive/`
  - `game.py` – Top-level turn controller and game state manager.
  - `board.py` – Enforces all board-level rules: placement, movement, connectivity.
  - `models/` – Core data models: `Bug`, `Player`, `Position`, `BugType`.
  - `behaviors/` – Movement strategy implementations per bug type (Queen, Ant, Beetle, etc.).
- `src/api/`
  - `main.py` – Entrypoint and FastAPI app
  - `router.py` – Route definitions and endpoint logic
  - `models.py` – Request and response Pydantic schemas
- `tests/` – Comprehensive test suite using `pytest`.

## 🧪 Testing

```bash
# Run all tests using
make test

# Supports standard linting via Ruff
make lint
```

## 👤 Author

**Estuardo Lopez Letona**  
GitHub: [@estulpz202](https://github.com/estulpz202)  
Email: elopezle@andrew.cmu.edu
