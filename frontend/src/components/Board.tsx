import React from 'react';
import { Bug, Position } from '../game';
import Cell from './Cell';
import '../styles/Board.css';

interface BoardProps {
  bugs: Bug[];
  visiblePositions: Position[];
  validPlacements: Position[];
  validMovesForSelecPos: Position[];
  selectedBoardPos: Position | null;
  onBoardCellClick: (q: number, r: number) => void;
}

const posKey = (q: number, r: number) => `${q},${r}`;

const Board: React.FC<BoardProps> = ({
  bugs,
  visiblePositions,
  validPlacements,
  validMovesForSelecPos,
  selectedBoardPos,
  onBoardCellClick,
}) => {
  const cellsToRender = new Map<string, Position>();

  for (const pos of visiblePositions) {
    cellsToRender.set(`${pos.q},${pos.r}`, pos);
  }

  if (cellsToRender.size === 0) {
    cellsToRender.set(posKey(0, 0), { q: 0, r: 0 });
  }

  const sortedCells = Array.from(cellsToRender.values()).sort((a, b) =>
    a.q === b.q ? a.r - b.r : a.q - b.q
  );

  // Define the size of the hexagons (width of a regular hexagon)
  const hexWidth = 90; // Width of the hexagon
  const hexHeight = (hexWidth / Math.sqrt(3)) * 1.8; // Height for a regular hexagon
  const width = hexWidth; // Width for positioning
  const height = hexHeight; // Height for positioning

  // Get the dimensions of the board container
  const boardWidth = 900;
  const boardHeight = 700;

  // Calculate the offset to center (0,0)
  const offsetX = boardWidth / 2;
  const offsetY = boardHeight / 2;

  return (
    <div className="board">
      <div
        className="cell-container"
        style={{
          position: 'relative',
          width: '100%',
          height: '100%',
        }}
      >
        {sortedCells.map((pos) => {
          const bugsAtPos = bugs
            .filter((b) => b.q === pos.q && b.r === pos.r)
            .sort((a, b) => a.height - b.height);

          const isSelected =
            selectedBoardPos && selectedBoardPos.q === pos.q && selectedBoardPos.r === pos.r;

          const isValidPlacement = validPlacements.some(
            (p) => p.q === pos.q && p.r === pos.r
          );

          const isValidMove = validMovesForSelecPos.some(
            (p) => p.q === pos.q && p.r === pos.r
          );

          // Calculate the pixel position with offset to center (0,0)
          const x = offsetX + width * (pos.q + pos.r / 2);
          const y = offsetY + height * (3 / 4) * pos.r;

          return (
            <div
              key={posKey(pos.q, pos.r)}
              className="cell-wrapper"
              style={{
                position: 'absolute',
                left: `${x}px`,
                top: `${y}px`,
                transform: 'translate(-50%, -50%)',
                width: `${hexWidth}px`,
                height: `${hexHeight}px`,
              }}
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
