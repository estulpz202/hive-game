import React from 'react';
import { Bug } from '../game';
import '../styles/Cell.css';

/** Props expected by a Cell */
interface CellProps {
  q: number;
  r: number;
  bugs: Bug[];
  isSelected: boolean | null;
  isValidPlacement: boolean;
  isValidMove: boolean;
  onClick: () => void;
}

/**
 * Renders a single hex cell. Shows stacked bugs and highlights.
 */
const Cell: React.FC<CellProps> = ({
  q,
  r,
  bugs,
  isSelected,
  isValidPlacement,
  isValidMove,
  onClick,
}) => {
  const topBug = bugs[bugs.length - 1] ?? null;

  const classes = ['cell'];
  if (isSelected) classes.push('selected');
  if (isValidPlacement) classes.push('valid-placement');
  if (isValidMove) classes.push('valid-move');

  return (
    <div
      className={classes.join(' ')}
      onClick={onClick}
      data-coord={`(${q}, ${r})`}
    >
      <div className="hex">
        {topBug ? (
          <div
            className={`bug`}
            style={{
              backgroundColor: topBug.owner === 'BLACK' ? '#333' : '#fff',
              color: topBug.owner === 'BLACK' ? '#fff' : '#000',
            }}
          >
            {topBug.bug_type[0]}
            {bugs.length > 1 && <span className="stack-count">{bugs.length}</span>}
          </div>
        ) : (
          <div className="empty" />
        )}
      </div>
    </div>
  );
};

export default Cell;
