import React from 'react';
import { GameState, Position } from './game';
import Board from './components/Board';
import BugPicker from './components/BugPicker';
import GameOverBanner from './components/GameOverBanner';
import './styles/App.css';

interface Props {}

interface AppState extends GameState {
  selectedReserveBug: string | null;
  selectedBoardPos: Position | null;
  validPlacements: Position[];
  validMovesForSelecPos: Position[];
  errorMessage: string | null;
  zoomLevel: number;
}

class App extends React.Component<Props, AppState> {
  private initialized: boolean = false;

  constructor(props: Props) {
    super(props);
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
    };
  }

  componentDidMount(): void {
    if (!this.initialized) {
      this.newGame();
      this.initialized = true;
    }
  }

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

  updateGameState = (data: GameState, preserveSelection: boolean = false) => {
    this.setState({
      phase: data.phase,
      current_player: data.current_player,
      bugs: data.bugs,
      players: data.players,
      can_pass: data.can_pass,
      winner: data.winner,
      visible_positions: data.visible_positions,
      selectedReserveBug: preserveSelection ? this.state.selectedReserveBug : null,
      selectedBoardPos: preserveSelection ? this.state.selectedBoardPos : null,
      validPlacements: [],
      validMovesForSelecPos: [],
      errorMessage: null,
    });
  };

  handleReserveBugSelect = async (bugType: string) => {
    if (this.state.selectedReserveBug === bugType) {
      this.setState({
        selectedReserveBug: null,
        selectedBoardPos: null,
        validPlacements: [],
      });
      return;
    }

    this.setState({
      selectedReserveBug: bugType,
      selectedBoardPos: null,
    });
    try {
      const response = await fetch('/valid-placements');
      const data: Position[] = await response.json();
      this.setState({ validPlacements: data });
    } catch (err) {
      console.error('Failed to fetch placements:', err);
      this.setState({ errorMessage: 'Could not fetch valid placements.' });
    }
  };

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
      this.setState({ errorMessage: 'Invalid placement.' });
    }
  };

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
      this.setState({ errorMessage: 'Invalid move selection.' });
    }
  };

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

  handleZoomIn = () => {
    this.setState((prevState) => ({
      zoomLevel: Math.min(prevState.zoomLevel + 0.1, 2), // Max zoom level 2x
    }));
  };

  handleZoomOut = () => {
    this.setState((prevState) => ({
      zoomLevel: Math.max(prevState.zoomLevel - 0.1, 0.5), // Min zoom level 0.5x
    }));
  };

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

  getPhaseInstruction = (): string => {
    const currentPhase = this.state.phase;
    switch (currentPhase) {
      case 'Start':
        return 'Place bugs from reserve. After placing your queen (within 4 turns), you can move.';
      case 'PlaceOrMove':
        return 'Place a bug from reserve or move one in play. Valid actions are highlighted.';
      case 'GameOver':
        return 'Start a new game to play again.';
      default:
        return '-';
    }
  };

  displayName = (color: string): string => color.charAt(0) + color.slice(1).toLowerCase();

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
    } = this.state;

    return (
      <div className="App">
        <h1>Hive</h1>

        <div className="info-panel">
          <p><strong>Player:</strong> {this.displayName(current_player)}</p>
          <p><strong>Instructions:</strong> {this.getPhaseInstruction()}</p>
        </div>

        <div className="controls">
          <button onClick={this.newGame}>New Game</button>
          {can_pass && <button onClick={this.handlePass}>Pass</button>}
          <button onClick={this.handleZoomIn}>Zoom In</button>
          <button onClick={this.handleZoomOut}>Zoom Out</button>
        </div>

        {this.renderError()}

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

        <div className="board-wrapper">
          <Board
            bugs={bugs}
            visiblePositions={visible_positions}
            onBoardCellClick={this.handleBoardCellClick}
            validPlacements={validPlacements}
            validMovesForSelecPos={validMovesForSelecPos}
            selectedBoardPos={selectedBoardPos}
            zoomLevel={zoomLevel}
          />
        </div>

        {phase === 'GameOver' && (
          <GameOverBanner winner={winner || 'Unknown'} onRestart={this.newGame} />
        )}
      </div>
    );
  }
}

export default App;
