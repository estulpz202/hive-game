import React from 'react';
import { Bug, Position } from '../game';
import Cell from './Cell';
import '../styles/Board.css';

/** Props expected by the Board component */
interface BoardProps {
  bugs: Bug[];
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
  validPlacements,
  validMovesForSelecPos,
  selectedBoardPos,
  onBoardCellClick
}) => {
  // Determine all positions we want to render a cell for.
  const cellsToRender = new Map<string, Position>();

  // Add all bug positions
  for (const bug of bugs) {
    cellsToRender.set(posKey(bug.q, bug.r), { q: bug.q, r: bug.r });
  }

  // Add all valid placement and move options
  for (const pos of [...validPlacements, ...validMovesForSelecPos]) {
    cellsToRender.set(posKey(pos.q, pos.r), pos);
  }

  // Sort cells by q and then r for stable layout
  const sortedCells = Array.from(cellsToRender.values()).sort((a, b) =>
    a.q === b.q ? a.r - b.r : a.q - b.q
  );

  return (
    <div className="board">
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

        return (
          <Cell
            key={posKey(pos.q, pos.r)}
            q={pos.q}
            r={pos.r}
            bugs={bugsAtPos}
            isSelected={isSelected}
            isValidPlacement={isValidPlacement}
            isValidMove={isValidMove}
            onClick={() => onBoardCellClick(pos.q, pos.r)}
          />
        );
      })}
    </div>
  );
};

export default Board;
