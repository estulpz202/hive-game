import React from 'react';
import { PlayerState } from '../game';
import '../styles/BugPicker.css';

interface BugPickerProps {
  playerState: PlayerState;
  selectedReserveBug: string | null;
  onSelect: (bugType: string) => void;
  isCurrentPlayer: boolean;
}

const displayName = (color: string): string => color.charAt(0) + color.slice(1).toLowerCase();

const bugIcons: { [key: string]: string } = {
  'QueenBee': '🐝',
  'Beetle': '🪲',
  'Spider': '🕷️',
  'Ant': '🐜',
  'Grasshopper': '🦗',
};

const BugPicker: React.FC<BugPickerProps> = ({
  playerState,
  selectedReserveBug,
  onSelect,
  isCurrentPlayer,
}) => {
  const sortedBugs = [...playerState.remaining_bugs].sort((a, b) =>
    a.bug_type.localeCompare(b.bug_type)
  );

  return (
    <div className={`bug-picker ${isCurrentPlayer ? 'current-player' : ''}`}>
      <h3>{displayName(playerState.color)}'s Reserve</h3>
      <div className="bug-options">
        {sortedBugs.map((bug) => (
          <button
            key={bug.bug_type}
            className={`bug-button ${playerState.color.toLowerCase()} ${
              isCurrentPlayer && selectedReserveBug === bug.bug_type ? 'selected' : ''
            }`}
            disabled={bug.count === 0 || !isCurrentPlayer}
            onClick={() => isCurrentPlayer && onSelect(bug.bug_type)}
          >
            <span className="bug-icon" aria-label={bug.bug_type}>
              {bugIcons[bug.bug_type] || bug.bug_type[0]}
            </span>
            <span className="bug-count">({bug.count})</span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default BugPicker;
