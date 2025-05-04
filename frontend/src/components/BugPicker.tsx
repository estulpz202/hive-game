import React from 'react';
import { PlayerState } from '../game';
import '../styles/BugPicker.css';

interface BugPickerProps {
  playerState: PlayerState;
  selectedReserveBug: string | null;
  onSelect: (bugType: string) => void;
  isCurrentPlayer: boolean;
}

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
      <h3>{playerState.color}'s Reserve</h3>
      <div className="bug-options">
        {sortedBugs.map((bug) => (
          <button
            key={bug.bug_type}
            className={`bug-button ${
              isCurrentPlayer && selectedReserveBug === bug.bug_type ? 'selected' : ''
            }`}
            disabled={bug.count === 0 || !isCurrentPlayer}
            onClick={() => isCurrentPlayer && onSelect(bug.bug_type)}
          >
            {bug.bug_type} ({bug.count})
          </button>
        ))}
      </div>
    </div>
  );
};

export default BugPicker;
