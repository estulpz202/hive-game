# 🐝 Hive Game

This project is a full-stack implementation of the game **Hive**. Hive is an abstract strategy game for two players. Each player controls a set of bugs; Queen Bee, Beetles, Spiders, Ants, and Grasshoppers. They must surround the opponent’s Queen to win. This implementation currently includes the base game (expansion bugs like Ladybug, Mosquito, and Pill bug planned).

## 📦 Tech Stack

- **Backend**: Python (Poetry and FastAPI)
- **Frontend**: React (TypeScript)
- **Testing**: Test suite with `pytest`
- **Design**: Clean, extensible object-oriented architecture with well-structured, readable code
- **Pattern**: MVC-style separation of logic, API, and view

## 🛠 Getting Started

### Set Up Backend

```bash
# Install Poetry if needed
curl -sSL https://install.python-poetry.org | python3 -

# Enter backend folder
cd backend

# Install dependencies
make install

# Run the backend server (http://localhost:8000)
make run
```

### Set Up Frontend

```bash
# Open a new terminal and enter frontend folder
cd frontend

# Install dependencies
npm install

# Run the frontend server (http://localhost:3000)
npm start
```

> Note: Both the frontend and backend must be running simultaneously for the game to function properly.

## 🎮 How to Play

- Launch the frontend in your browser (localhost:3000)
- Each player selects a bug to place or move according to the rules of Hive
- Valid actions are visually indicated
- The game ends automatically when a Queen Bee is surrounded

## 📚 Additional Documentation

For more detailed information on each part of the project
- Backend: See backend/README.md for setup, API endpoints, and backend-specific details.
- Frontend: See frontend/README.md for features, file structure, and frontend-specific details.

## 👤 Author

**Estuardo Lopez Letona**  
GitHub: [@estulpz202](https://github.com/estulpz202)  
Email: elopezle@andrew.cmu.edu
