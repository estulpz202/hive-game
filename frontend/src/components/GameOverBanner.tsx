import React from 'react';
import '../styles/GameOverBanner.css';

/** Props expected by the GameOverBanner component */
interface GameOverBannerProps {
  winner: string;
  onRestart: () => void;
}

/**
 * Displays the result of the game and a button to restart.
 */
const GameOverBanner: React.FC<GameOverBannerProps> = ({ winner, onRestart }) => {
  const resultText =
    winner === 'Draw' ? 'The game is a draw!' : `${winner} wins the game!`;

  return (
    <div className="game-over-banner">
      <h2>Game Over</h2>
      <p>{resultText}</p>
      <button onClick={onRestart}>Start New Game</button>
    </div>
  );
};

export default GameOverBanner;
