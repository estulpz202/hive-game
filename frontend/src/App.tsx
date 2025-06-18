/** Root React component for the Hive game UI */
import React from 'react';
import { GameState, Position } from './game';
import Board from './components/Board';
import BugPicker from './components/BugPicker';
import GameOverBanner from './components/GameOverBanner';
import RulesPanel from './components/RulesPanel';
import './styles/App.css';

/** Props for the App component (unused) */
interface Props {}

/** App state includes game state + UI-related data */
interface AppState extends GameState {
  selectedReserveBug: string | null;
  selectedBoardPos: Position | null;
  validPlacements: Position[];
  validMovesForSelecPos: Position[];
  errorMessage: string | null;
  zoomLevel: number;
  showRules: boolean;
  showGameOver: boolean;
  dragOffset: { x: number; y: number };
  highlightRulesButton: boolean;
}

class App extends React.Component<Props, AppState> {
  /** Flag to ensure the game is initialized only once */
  private initialized: boolean = false;

  constructor(props: Props) {
    super(props);
    /** Initialize full app/game state */
    this.state = {
      phase: 'Start',
      current_player: '',
      bugs: [],
      players: [],
      can_pass: false,
      winner: null,
      visible_positions: [],
      selectedReserveBug: null,
      selectedBoardPos: null,
      validPlacements: [],
      validMovesForSelecPos: [],
      errorMessage: null,
      zoomLevel: 1,
      showRules: false,
      showGameOver: false,
      dragOffset: { x: 0, y: 0 },
      highlightRulesButton: true,
    };
  }

  /** Start game after initial mount */
  componentDidMount(): void {
    if (!this.initialized) {
      this.newGame();
      this.initialized = true;
      // Stop highlighting rules button after 5 seconds
      setTimeout(() => {
        this.setState({ highlightRulesButton: false });
      }, 4900);
    }
  }

  /** Starts a new game by calling backend /newgame endpoint */
  newGame = async () => {
    try {
      const response = await fetch('/newgame', { method: 'POST' });
      const data = await response.json();
      this.updateGameState(data);
      this.setState({ showGameOver: false, dragOffset: { x: 0, y: 0 }, highlightRulesButton: true });
      // Re-apply highlight on new game and stop after 5 seconds
      setTimeout(() => {
        this.setState({ highlightRulesButton: false });
      }, 5000);
    } catch (err) {
      console.error('Failed to start new game:', err);
      this.setState({ errorMessage: 'Failed to start new game.' });
    }
  };

  /**
   * Updates game state and resets board position.
   */
  updateGameState = (data: GameState) => {
    this.setState({
      phase: data.phase,
      current_player: data.current_player,
      bugs: data.bugs,
      players: data.players,
      can_pass: data.can_pass,
      winner: data.winner,
      visible_positions: data.visible_positions,
      selectedReserveBug: null,
      selectedBoardPos: null,
      validPlacements: [],
      validMovesForSelecPos: [],
      errorMessage: null,
      showGameOver: data.phase === 'GameOver',
    });
  };

  /**
   * Handles user selecting a bug from reserve
   * Fetches valid placements for that bug type
   */
  handleReserveBugSelect = async (bugType: string) => {
    if (this.state.selectedReserveBug === bugType) {
      /** Deselect if clicked again */
      this.setState({
        selectedReserveBug: null,
        selectedBoardPos: null,
        validPlacements: [],
        validMovesForSelecPos: [],
      });
      return;
    }

    this.setState({
      selectedReserveBug: bugType,
      selectedBoardPos: null,
      validMovesForSelecPos: [],
    });

    try {
      const response = await fetch(`/valid-placements?bug_type=${bugType}`);
      const data: Position[] = await response.json();
      this.setState({ validPlacements: data });
    } catch (err) {
      console.error('Failed to fetch placements:', err);
      this.setState({ errorMessage: 'Failed to fetch valid placements.' });
    }
  };

  /**
   * Handles clicks on a board cell, determining intent:
   * placement, move source, or move destination
   */
  handleBoardCellClick = (q: number, r: number) => {
    const { selectedReserveBug, selectedBoardPos } = this.state;

    if (selectedReserveBug) {
      this.placeBug(q, r);
    } else if (!selectedBoardPos) {
      this.fetchValidMoves(q, r);
    } else {
      this.moveBug(selectedBoardPos, { q, r });
    }
  };

  /** Places a bug at the given position */
  placeBug = async (q: number, r: number) => {
    const { selectedReserveBug } = this.state;
    if (!selectedReserveBug) return;

    try {
      const response = await fetch('/place', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bug_type: selectedReserveBug, q, r }),
      });
      const data = await response.json();
      this.updateGameState(data);
    } catch (err) {
      console.error('Failed to place bug:', err);
      this.setState({ errorMessage: 'Failed to place bug.' });
    }
  };

  /** Fetches valid move destinations for bug at selected position */
  fetchValidMoves = async (q: number, r: number) => {
    try {
      const response = await fetch(`/valid-moves?q=${q}&r=${r}`);
      const data: Position[] = await response.json();
      this.setState({
        selectedBoardPos: { q, r },
        validMovesForSelecPos: data,
        errorMessage: null,
      });
    } catch (err) {
      console.error('Failed to get moves:', err);
      this.setState({ errorMessage: 'Failed to get valid moves.' });
    }
  };

  /** Moves a bug from one position to another */
  moveBug = async (from: Position, to: Position) => {
    try {
      const response = await fetch('/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          from_q: from.q,
          from_r: from.r,
          to_q: to.q,
          to_r: to.r,
        }),
      });
      const data = await response.json();
      this.updateGameState(data);
    } catch (err) {
      console.error('Failed to move bug:', err);
      this.setState({ errorMessage: 'Failed to move bug.' });
    }
  };

  /** Sends pass request to backend */
  handlePass = async () => {
    try {
      const response = await fetch('/pass', { method: 'POST' });
      if (!response.ok) throw new Error('Cannot pass turn now.');
      const data = await response.json();
      this.updateGameState(data);
    } catch (err: any) {
      this.setState({ errorMessage: err.message || 'Failed to pass turn.' });
    }
  };

  /** Zoom in on board */
  handleZoomIn = () => {
    this.setState((prevState) => ({
      zoomLevel: Math.min(prevState.zoomLevel + 0.1, 2),
    }));
  };

  /** Zoom out from board */
  handleZoomOut = () => {
    this.setState((prevState) => ({
      zoomLevel: Math.max(prevState.zoomLevel - 0.1, 0.5),
    }));
  };

  /** Toggle the rules panel visibility */
  toggleRules = () => {
    this.setState((prevState) => ({
      showRules: !prevState.showRules,
    }));
  };

  /** Close the GameOver banner */
  closeGameOver = () => {
    this.setState({ showGameOver: false });
  };

  /** Renders error message if one exists */
  renderError(): React.ReactNode {
    const { errorMessage } = this.state;
    if (!errorMessage) return null;

    return (
      <div className="error-banner">
        <p>{errorMessage}</p>
        <button onClick={() => this.setState({ errorMessage: null })}>Dismiss</button>
      </div>
    );
  };

  /** Returns phase-specific instruction message */
  getPhaseInstruction = (): string => {
    const currentPhase = this.state.phase;
    switch (currentPhase) {
      case 'Start':
        return 'Place a bug from your reserve. Must place Queen by 4th turn to unlock movement.';
      case 'PlaceOrMove':
        return 'Place a new bug or move one in play. Highlighted spaces show valid options.';
      case 'GameOver':
        return 'Game over! Start a new game to play again.';
      default:
        return '-';
    }
  };

  /** Formats a color string (e.g. 'WHITE' → 'White') */
  displayName = (color: string): string => color.charAt(0) + color.slice(1).toLowerCase();

  /** Main render function */
  render(): React.ReactNode {
    const {
      current_player,
      phase,
      players,
      bugs,
      validPlacements,
      validMovesForSelecPos,
      selectedBoardPos,
      selectedReserveBug,
      can_pass,
      winner,
      visible_positions,
      zoomLevel,
      showRules,
      showGameOver,
      dragOffset,
      highlightRulesButton,
    } = this.state;

    return (
      <div className="App">
        <h1 className="title">Hive: Battle for the Queen</h1>

        {/* Rules panel */}
        <RulesPanel isOpen={showRules} onClose={this.toggleRules} />

        {/* Sidebar with game state and controls */}
        <div className="sidebar">
          <div className="info-panel">
            <p style={{ display: 'flex' }}>
              <strong>Turn:</strong>&nbsp;
              {this.displayName(current_player)}
              <span className={`player-chip ${current_player.toLowerCase()}`} />
            </p>
            <p><strong>Instructions:</strong> {this.getPhaseInstruction()}</p>
          </div>

          {/* Player reserve UI */}
          <div className="bug-pickers">
            {players.map((p) => (
              <BugPicker
                key={p.color}
                playerState={p}
                selectedReserveBug={current_player === p.color ? selectedReserveBug : null}
                onSelect={this.handleReserveBugSelect}
                isCurrentPlayer={current_player === p.color}
              />
            ))}
          </div>

          {/* Action controls */}
          <div className="controls">
            <div className="button-row">
              <button
                onClick={this.toggleRules}
                className={highlightRulesButton ? 'highlight-pulse' : ''}
              >
                {showRules ? 'Hide Rules' : 'Show Rules'}
              </button>
              <button onClick={this.newGame}>New Game</button>
            </div>
            <div className="button-row">
              <button onClick={this.handleZoomIn}>Zoom In</button>
              <button onClick={this.handleZoomOut}>Zoom Out</button>
            </div>
            <div className="button-row">
              {can_pass && <button onClick={this.handlePass}>Pass</button>}
            </div>
          </div>
        </div>

        {/* Render error messages if any */}
        {this.renderError()}

        {/* Main game board */}
        <div className="board-wrapper">
          <Board
            bugs={bugs}
            visiblePositions={visible_positions}
            onBoardCellClick={this.handleBoardCellClick}
            validPlacements={validPlacements}
            validMovesForSelecPos={validMovesForSelecPos}
            selectedBoardPos={selectedBoardPos}
            zoomLevel={zoomLevel}
            dragOffset={dragOffset}
            setDragOffset={(offset) => this.setState({ dragOffset: offset })}
          />
        </div>

        {/* Display winner and restart/close buttons when game ends */}
        {showGameOver && (
          <GameOverBanner
            winner={winner || 'Unknown'}
            onRestart={this.newGame}
            onClose={this.closeGameOver}
          />
        )}
      </div>
    );
  }
}

export default App;
