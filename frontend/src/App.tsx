import React from 'react';
import { GameState, Bug, PlayerState, Position } from './game';
import Board from './components/Board';
import BugPicker from './components/BugPicker';
import GameOverBanner from './components/GameOverBanner';
import './styles/App.css';

/** Type of the props field for a React component */
interface Props {}

/**
 * Extended AppState type that includes the serialized GameState from the backend
 * and additional frontend-only state for UI interactions.
 */
interface AppState extends GameState {
  selectedBug: string | null;
  selectedPosition: Position | null;
  validPlacements: Position[];
  validMoves: Position[];
  errorMessage: string | null;
}

/**
 * Use generics to define the types of props and state in a React component.
 * Both are used to manage component data, and changes to them trigger view updates.
 * Typically, props are set by the parent, while state is managed internally by the component.
 * 
 * Main App component for the Hive game.
 * Controls game logic flow, communicates with backend API, and updates view accordingly.
 */
class App extends React.Component<Props, AppState> {
  private initialized: boolean = false;

  /**
   * Initializes the game state. State has AppState type.
   * 
   * @param props has type Props
   */
  constructor(props: Props) {
    super(props);
    this.state = {
      phase: 'Start',
      current_player: '',
      bugs: [],
      players: [],
      can_pass: false,
      winner: null,
      selectedBug: null,
      selectedPosition: null,
      validPlacements: [],
      validMoves: [],
      errorMessage: null,
    };
  }

  /**
   * Lifecycle method: called once after component mounts.
   * Prevents duplicate initialization via a flag.
   */
  componentDidMount(): void {
    if (!this.initialized) {
      this.newGame();
      this.initialized = true;
    }
  }
  
  /**
   * Starts a new game by requesting a reset game state from the backend.
   */
  newGame = async () => {
    try {
      const response = await fetch('/newgame', { method: 'POST' });
      const data = await response.json();
      this.updateGameState(data);
    } catch (err) {
      console.error('Failed to start new game:', err);
      this.setState({ errorMessage: 'Failed to start new game.' });
    }
  };

  /**
   * Updates local frontend state from the backend game response.
   * Clears any selection/highlights unless preserved explicitly.
   * 
   * @param data - The game state JSON object from the backend
   * @param preserveSelection - If true, keeps the current bug or position selection
   */
  updateGameState = (data: GameState, preserveSelection: boolean = false) => {
    this.setState({
      phase: data.phase,
      current_player: data.current_player,
      bugs: data.bugs,
      players: data.players,
      can_pass: data.can_pass,
      winner: data.winner,
      selectedBug: preserveSelection ? this.state.selectedBug : null,
      selectedPosition: preserveSelection ? this.state.selectedPosition : null,
      validPlacements: [],
      validMoves: [],
      errorMessage: null,
    });
  };

  /**
   * Called when a bug is selected from the reserve.
   * Triggers a request to fetch valid placements.
   */
  handleBugSelect = async (bugType: string) => {
    this.setState({ selectedBug: bugType, selectedPosition: null });
    try {
      const response = await fetch('/valid-placements');
      const data: Position[] = await response.json();
      this.setState({ validPlacements: data });
    } catch (err) {
      console.error('Failed to fetch placements:', err);
      this.setState({ errorMessage: 'Could not fetch valid placements.' });
    }
  };

  /**
   * Called when a cell is clicked.
   * Decides whether to attempt placement or movement.
   */
  handleCellClick = (q: number, r: number) => {
    const { selectedBug, selectedPosition } = this.state;

    if (selectedBug) {
      this.placeBug(q, r);
    } else if (!selectedPosition) {
      this.fetchValidMoves(q, r);
    } else {
      this.moveBug(selectedPosition, { q, r });
    }
  };

  /**
   * Sends a request to place a selected bug at a target position.
   */
  placeBug = async (q: number, r: number) => {
    const { selectedBug } = this.state;
    if (!selectedBug) return;

    try {
      const response = await fetch('/place', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bug_type: selectedBug, q, r }),
      });
      const data = await response.json();
      this.updateGameState(data);
    } catch (err) {
      console.error('Failed to place bug:', err);
      this.setState({ errorMessage: 'Invalid placement.' });
    }
  };

  /**
   * Sends a request to fetch valid move destinations for a bug at (q, r).
   */
  fetchValidMoves = async (q: number, r: number) => {
    try {
      const response = await fetch(`/valid-moves?q=${q}&r=${r}`);
      const data: Position[] = await response.json();
      this.setState({
        selectedPosition: { q, r },
        validMoves: data,
        errorMessage: null,
      });
    } catch (err) {
      console.error('Failed to get moves:', err);
      this.setState({ errorMessage: 'Invalid move selection.' });
    }
  };

  /**
   * Sends a move request for a selected bug.
   */
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
      this.setState({ errorMessage: 'Move failed.' });
    }
  };

  /**
   * Sends a request to pass the turn. Only allowed if no valid actions exist.
   */
  handlePass = async () => {
    try {
      const response = await fetch('/pass', { method: 'POST' });
      if (!response.ok) throw new Error('Cannot pass turn now');
      const data = await response.json();
      this.updateGameState(data);
    } catch (err: any) {
      this.setState({ errorMessage: err.message || 'Failed to pass turn' });
    }
  };

  /**
   * Renders any error message as a dismissible banner.
   */
  renderError(): React.ReactNode {
    const { errorMessage } = this.state;
    if (!errorMessage) return null;

    return (
      <div className="error-banner">
        <p>{errorMessage}</p>
        <button onClick={() => this.setState({ errorMessage: null })}>Dismiss</button>
      </div>
    );
  }

  /**
   * Main UI render method. Shows bug picker, player info, board, and controls.
   */
  render(): React.ReactNode {
    const {
      current_player,
      phase,
      players,
      bugs,
      validPlacements,
      validMoves,
      selectedPosition,
      selectedBug,
      can_pass,
      winner,
    } = this.state;

    const playerState = players.find(p => p.color === current_player);
    const otherPlayer = players.find(p => p.color !== current_player);

    return (
      <div className="App">
        <h1>Hive</h1>
        <p>
          <strong>Current Player:</strong> {current_player}
        </p>
        <p>
          <strong>Phase:</strong> {phase}
        </p>

        <div className="controls">
          <button onClick={this.newGame}>New Game</button>
          {can_pass && <button onClick={this.handlePass}>Pass</button>}
        </div>

        {this.renderError()}

        <BugPicker
          playerState={playerState}
          selectedBug={selectedBug}
          onSelect={bug => this.setState({ selectedBug: bug, selectedPosition: null })}
        />

        <div className="board-wrapper">
          <Board
            bugs={bugs}
            onCellClick={this.handleCellClick}
            validPlacements={validPlacements}
            validMoves={validMoves}
            selected={selectedPosition}
          />
        </div>

        {phase === 'GameOver' && (
          <GameOverBanner winner={this.state.winner || 'Unknown'} onRestart={this.newGame} />
        )}
      </div>
    );
  }
}

export default App;
