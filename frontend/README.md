# ⚛️ Frontend (Hive)

This is the frontend React application for the board game **Hive**, built with **TypeScript** and **modular CSS**. It provides a visual interface for two players to play Hive in the browser, interacting with the backend via a **FastAPI**-based JSON API.

## ▶️ How to Run

```bash
# Install dependencies
npm install

# Start the frontend development server (http://localhost:3000)
npm start
```

## ✅ Features

- Interactive Hive board with hex-based layout
- Turn-based player interface and game state display
- Visual indicators for valid placements and moves
- Bug picker with live reserve counts and queen placement status
- Pass button appears when no valid moves or placements
- Automatic win detection and game-over banner
- Responsive, modular UI using React component structure
- Clean and extensible codebase

## 📁 Structure

- `src/game.ts` - TypeScript interfaces for game state, bugs, and positions
- `src/App.tsx` – Root component: manages UI state, API calls, and turn flow
- `src/Index.tsx` – Application entry point, renders into the HTML root
- `src/components/`
  - `Board.tsx` – Renders the hex board with dynamic cells
  - `Cell.tsx` – Individual cell rendering and highlighting
  - `BugPicker.tsx` – UI for selecting a bug to place from reserve
  - `GameOverBanner.tsx` – Displays winner and option to restart
- `src/styles/`
  - `App.css` – Layout and UI styling  
  - `Board.css` – Hex grid layout and hover/valid styles  
  - `Cell.css` – Tile visuals and bug display  
  - `index.css` – Global base styling and layout reset  
- `public/index.html`
  - HTML entry point for the React app

## 👤 Author

**Estuardo Lopez Letona**  
GitHub: [@estulpz202](https://github.com/estulpz202)  
Email: elopezle@andrew.cmu.edu
