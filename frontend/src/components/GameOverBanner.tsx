import React from 'react';
import '../styles/GameOverBanner.css';

/** Props for GameOverBanner component. */
interface GameOverBannerProps {
  winner: string;
  onRestart: () => void;
}

/**
 * Renders a full-screen overlay at the end of the game.
 * Displays the result (win or draw) and provides a restart button.
 */
const GameOverBanner: React.FC<GameOverBannerProps> = ({ winner, onRestart }) => {
  return (
    <div className="overlay">
      <div className="banner">
        {/* Display game result */}
        <div className="text">
          🐝 <span>
            {winner === 'Draw' ? 'Game Ends in a Draw!' : `${winner} Wins!`}
          </span> 🐝
        </div>

        {/* Restart game button */}
        <button className="button" onClick={onRestart}>
          🔄 New Hive Game
        </button>
      </div>
    </div>
  );
};

export default GameOverBanner;
