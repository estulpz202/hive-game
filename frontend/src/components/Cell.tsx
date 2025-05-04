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
  if (topBug) classes.push(topBug.owner.toLowerCase());
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
        <>
          <span className="bug-icon">{bugIcons[topBug.bug_type] || topBug.bug_type[0]}</span>
          {bugs.length > 1 && <span className="stack-count">{bugs.length}</span>}
        </>
      ) : null}
    </div>
  );
};

export default Cell;
