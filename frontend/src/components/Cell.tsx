/** React component representing a single hex cell on the board. */
import React from 'react';
import { Bug } from '../game';
import '../styles/Cell.css';

/** Props required for rendering a Cell */
interface CellProps {
  q: number;
  r: number;
  bugs: Bug[];
  isSelected: boolean | null;
  isValidPlacement: boolean;
  isValidMove: boolean;
  onClick: () => void;
  zoomLevel: number;
}

/** Mapping of bug types to emoji icons */
const bugIcons: { [key: string]: string } = {
  'QueenBee': '🐝',
  'Beetle': '🪲',
  'Spider': '🕷️',
  'Ant': '🐜',
  'Grasshopper': '🦗',
};

const Cell: React.FC<CellProps> = ({
  q,
  r,
  bugs,
  isSelected,
  isValidPlacement,
  isValidMove,
  onClick,
  zoomLevel,
}) => {
  /** The bug on the top of the stack, if any */
  const topBug = bugs[bugs.length - 1] ?? null;

  /** CSS classes applied to this cell based on state */
  const classes = ['cell'];
  if (topBug) classes.push(topBug.owner.toLowerCase());  // Add owner color class
  if (isSelected) classes.push('selected');              // Highlight if selected
  if (isValidPlacement) classes.push('valid-placement'); // Show placement highlight
  if (isValidMove) classes.push('valid-move');           // Show move highlight
  if (!topBug) classes.push('empty');                    // Style empty cells differently

  return (
    <div
      className={classes.join(' ')}
      onClick={onClick}
      data-coord={`(${q}, ${r})`} // For debugging or testing
    >
      {/* Render the top bug icon if present */}
      {topBug ? (
        <>
          <span className="bug-icon" style={{ fontSize: `${2.65 * zoomLevel}rem` }}>
            {bugIcons[topBug.bug_type] || topBug.bug_type[0]}
          </span>

          {/* If there’s a stack, show stack count indicator */}
          {bugs.length > 1 && (
            <span
              className="stack-count"
              style={{
                width: `${18.5 * zoomLevel}px`,
                height: `${18.5 * zoomLevel}px`,
                fontSize: `${0.85 * zoomLevel}rem`,
                bottom: `${17 * zoomLevel}px`,
                left: `${14 * zoomLevel}px`,
              }}
            >
              {bugs.length}
            </span>
          )}
        </>
      ) : null}
    </div>
  );
};

export default Cell;
