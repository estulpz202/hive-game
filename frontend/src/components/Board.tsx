import React, { useState } from 'react';
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
  zoomLevel: number;
}

const posKey = (q: number, r: number) => `${q},${r}`;

const Board: React.FC<BoardProps> = ({
  bugs,
  visiblePositions,
  validPlacements,
  validMovesForSelecPos,
  selectedBoardPos,
  onBoardCellClick,
  zoomLevel,
}) => {
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [startDrag, setStartDrag] = useState({ x: 0, y: 0 });

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

  // Define the base size of the hexagons (width of a regular hexagon)
  const baseHexWidth = 110; // Base width of the hexagon
  const hexWidth = baseHexWidth * zoomLevel; // Scaled width
  const hexHeight = (hexWidth / Math.sqrt(3)) * 1.8; // Scaled height for a regular hexagon
  const width = hexWidth; // Width for positioning
  const height = hexHeight; // Height for positioning

  const handleMouseDown = (e: React.MouseEvent) => {
    setIsDragging(true);
    setStartDrag({ x: e.clientX, y: e.clientY });
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (isDragging) {
      const dx = e.clientX - startDrag.x;
      const dy = e.clientY - startDrag.y;
      setDragOffset({ x: dragOffset.x + dx, y: dragOffset.y + dy });
      setStartDrag({ x: e.clientX, y: e.clientY });
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  // Calculate the offset to center (0,0) with dynamic centering
  const offsetX = window.innerWidth / 2 + dragOffset.x;
  const offsetY = window.innerHeight / 2 + dragOffset.y;

  return (
    <div
      className="board"
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
    >
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
                zoomLevel={zoomLevel}
              />
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Board;
