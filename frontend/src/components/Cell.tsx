import React from 'react';
import { Bug } from '../game';
import '../styles/Cell.css';

interface CellProps {
  q: number;
  r: number;
  bugs: Bug[];
  isSelected: boolean | null;
  isValidPlacement: boolean;
  isValidMove: boolean;
  onClick: () => void;
}

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
}) => {
  const topBug = bugs[bugs.length - 1] ?? null;

  const classes = ['cell'];
  if (isSelected) classes.push('selected');
  if (isValidPlacement) classes.push('valid-placement');
  if (isValidMove) classes.push('valid-move');
  if (!topBug) classes.push('empty');

  return (
    <div
      className={classes.join(' ')}
      onClick={onClick}
      data-coord={`(${q}, ${r})`}
    >
      {topBug ? (
        <div
          className={`bug ${topBug.owner.toLowerCase()}`}
          style={{
            backgroundColor: topBug.owner === 'BLACK' ? '#2d2d2d' : '#f5f5f5',
            color: topBug.owner === 'BLACK' ? '#ffffff' : '#000000',
          }}
        >
          <span className="bug-icon">{bugIcons[topBug.bug_type] || topBug.bug_type[0]}</span>
          {bugs.length > 1 && <span className="stack-count">{bugs.length}</span>}
        </div>
      ) : (
        <div className="empty-hex" />
      )}
    </div>
  );
};

export default Cell;
