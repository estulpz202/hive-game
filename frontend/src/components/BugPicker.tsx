/** React component for displaying a player's reserve bugs and selecting one to place. */
import React from 'react';
import { PlayerState } from '../game';
import '../styles/BugPicker.css';

/** Props expected by the BugPicker component */
interface BugPickerProps {
  playerState: PlayerState;
  selectedReserveBug: string | null;
  onSelect: (bugType: string) => void;
  isCurrentPlayer: boolean;
}

/** Formats player color for display (e.g., "WHITE" => "White") */
const displayName = (color: string): string => color.charAt(0) + color.slice(1).toLowerCase();

/** Emoji representations for bug types */
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
  /** Sort bugs alphabetically by type for consistent layout */
  const sortedBugs = [...playerState.remaining_bugs].sort((a, b) =>
    a.bug_type.localeCompare(b.bug_type)
  );

  return (
    <div className={`bug-picker ${isCurrentPlayer ? 'current-player' : ''}`}>
      {/* Reserve section header with player's color */}
      <h3>{displayName(playerState.color)}'s Reserve</h3>

      {/* List of bug buttons */}
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
            {/* Bug emoji or fallback to first letter */}
            <span className="bug-icon" aria-label={bug.bug_type}>
              {bugIcons[bug.bug_type] || bug.bug_type[0]}
            </span>

            {/* Display remaining count of this bug type */}
            <span className="bug-count">({bug.count})</span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default BugPicker;
