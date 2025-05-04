import React from 'react';
import { Bug, Position } from '../game';
import Cell from './Cell';
import '../styles/Board.css';

/** Props expected by the Board component */
interface BoardProps {
  bugs: Bug[];
  visiblePositions: Position[];
  validPlacements: Position[];
  validMovesForSelecPos: Position[];
  selectedBoardPos: Position | null;
  onBoardCellClick: (q: number, r: number) => void;
}

/**
 * Converts a position to a unique string key.
 */
const posKey = (q: number, r: number) => `${q},${r}`;

/**
 * The Board component renders all bugs on the board and highlights valid actions.
 */
const Board: React.FC<BoardProps> = ({
  bugs,
  visiblePositions,
  validPlacements,
  validMovesForSelecPos,
  selectedBoardPos,
  onBoardCellClick
}) => {
  // Determine all positions we want to render a cell for.
  const cellsToRender = new Map<string, Position>();

  // Add all visible positions
  for (const pos of visiblePositions) {
    cellsToRender.set(`${pos.q},${pos.r}`, pos);
  }

  // Make baord visible at start
  if (cellsToRender.size === 0) {
    cellsToRender.set(posKey(0, 0), { q: 0, r: 0 });
  }

  // Sort cells by q and then r for stable layout
  const sortedCells = Array.from(cellsToRender.values()).sort((a, b) =>
    a.q === b.q ? a.r - b.r : a.q - b.q
  );

  return (
    <div className="board">
      <div
        className="cell-container"
        style={{
          position: 'absolute',
          left: '50%',
          top: '50%',
          transform: 'translate(-50%, -50%)',
        }}
      >
        {sortedCells.map((pos) => {
          const bugsAtPos = bugs
            .filter((b) => b.q === pos.q && b.r === pos.r)
            .sort((a, b) => a.height - b.height); // bottom to top
    
          const isSelected =
            selectedBoardPos && selectedBoardPos.q === pos.q && selectedBoardPos.r === pos.r;
    
          const isValidPlacement = validPlacements.some(
            (p) => p.q === pos.q && p.r === pos.r
          );
    
          const isValidMove = validMovesForSelecPos.some(
            (p) => p.q === pos.q && p.r === pos.r
          );
    
          // Convert axial to pixel position
          const size = 40; // radius of hex
          const width = size * Math.sqrt(3);
          const height = size * 2;
          const x = width * (pos.q + pos.r / 2);
          const y = height * (3 / 4) * pos.r;
    
          return (
            <div
              key={posKey(pos.q, pos.r)}
              className="cell-wrapper"
              style={{ left: `${x}px`, top: `${y}px` }}
            >
              <Cell
                q={pos.q}
                r={pos.r}
                bugs={bugsAtPos}
                isSelected={isSelected}
                isValidPlacement={isValidPlacement}
                isValidMove={isValidMove}
                onClick={() => onBoardCellClick(pos.q, pos.r)}
              />
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Board;
