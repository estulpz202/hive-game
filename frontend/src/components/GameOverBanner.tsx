import React from 'react';
import '../styles/GameOverBanner.css';

/**
 * Props for GameOverBanner component.
 * 
 * - winner: the name of the winning player or 'Draw' if no winner.
 * - onRestart: callback to restart the game.
 */
interface GameOverBannerProps {
  winner: string;
  onRestart: () => void;
}

/**
 * GameOverBanner renders a fullscreen overlay when the Hive game ends,
 * showing the winner (Black or White) or a draw, with a button to restart.
 */
const GameOverBanner: React.FC<GameOverBannerProps> = ({ winner, onRestart }) => {

  return (
    <div className="overlay">
      <div className="banner">
        <div className="text">
          🐝 <span style={{ color: '#ffffff' }}>{winner === 'Draw' ? 'Game Ends in a Draw!' : `${winner} Wins!`}</span> 🐝
        </div>
        <button className="button" onClick={onRestart}>
          🔄 New Hive Game
        </button>
      </div>
    </div>
  );
};

export default GameOverBanner;
