import React from 'react';
import '../styles/GameOverBanner.css';

/** Props for GameOverBanner component. */
interface GameOverBannerProps {
  winner: string;
  onRestart: () => void;
  onClose: () => void; /* Added to handle closing the banner */
}

/**
 * Renders a full-screen overlay at the end of the game.
 * Displays the result (win or draw) and provides restart and close buttons.
 */
const GameOverBanner: React.FC<GameOverBannerProps> = ({ winner, onRestart, onClose }) => {
  // Determine the text color based on the winner
  const getWinnerTextColor = (winner: string) => {
    switch (winner.toLowerCase()) {
      case 'white':
        return '#FFFFFF'; // White
      case 'black':
        return '#2d2d2d'; // Black
      default:
        return '#FFFFFF'; // White
    }
  };

  return (
    <div className="overlay">
      <div className="banner">
        {/* Display game result */}
        <div className="text">
          🐝{' '}
          <span
            className="winner-text"
            style={{ color: getWinnerTextColor(winner) }}
          >
            {winner === 'Draw' ? 'Game Ends in a Draw!' : `${winner} Wins!`}
          </span>{' '}
          🐝
        </div>

        {/* Restart and Close buttons side by side */}
        <div className="button-container">
          <button className="button new-game" onClick={onRestart}>
            🔄 New Game
          </button>
          <button className="button close" onClick={onClose}>
            ✕ Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default GameOverBanner;
