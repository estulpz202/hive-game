/** React component responsible for rendering the game board and handling interactions */
import React, { useState } from 'react';
import { Bug, Position } from '../game';
import Cell from './Cell';
import '../styles/Board.css';

/** Props for the Board component */
interface BoardProps {
  bugs: Bug[];
  visiblePositions: Position[];
  validPlacements: Position[];
  validMovesForSelecPos: Position[];
  selectedBoardPos: Position | null;
  onBoardCellClick: (q: number, r: number) => void;
  zoomLevel: number;
  dragOffset: { x: number; y: number };
  setDragOffset: (offset: { x: number; y: number }) => void;
}

/** Utility to create a unique key from coordinates */
const posKey = (q: number, r: number) => `${q},${r}`;

const Board: React.FC<BoardProps> = ({
  bugs,
  visiblePositions,
  validPlacements,
  validMovesForSelecPos,
  selectedBoardPos,
  onBoardCellClick,
  zoomLevel,
  dragOffset,
  setDragOffset,
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [startDrag, setStartDrag] = useState({ x: 0, y: 0 });

  /** Set of all positions to render cells for */
  const cellsToRender = new Map<string, Position>();
  for (const pos of visiblePositions) {
    cellsToRender.set(`${pos.q},${pos.r}`, pos);
  }

  /** Ensure at least one cell is rendered at game start */
  if (cellsToRender.size === 0) {
    cellsToRender.set(posKey(0, 0), { q: 0, r: 0 });
  }

  /** Sort cells for consistent rendering */
  const sortedCells = Array.from(cellsToRender.values()).sort((a, b) =>
    a.q === b.q ? a.r - b.r : a.q - b.q
  );

  /** Define hex dimensions based on zoom */
  const baseHexWidth = 105;
  const hexWidth = baseHexWidth * zoomLevel;
  const hexHeight = (hexWidth / Math.sqrt(3)) * 1.8;
  const width = hexWidth;
  const height = hexHeight;

  /** Start dragging */
  const handleMouseDown = (e: React.MouseEvent) => {
    setIsDragging(true);
    setStartDrag({ x: e.clientX, y: e.clientY });
  };

  /** Update drag offset as mouse moves */
  const handleMouseMove = (e: React.MouseEvent) => {
    if (isDragging) {
      const dx = e.clientX - startDrag.x;
      const dy = e.clientY - startDrag.y;
      setDragOffset({ x: dragOffset.x + dx, y: dragOffset.y + dy });
      setStartDrag({ x: e.clientX, y: e.clientY });
    }
  };

  /** End dragging */
  const handleMouseUp = () => {
    setIsDragging(false);
  };

  /** Calculate offset to center (0, 0) on screen */
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
        style={{ position: 'relative', width: '100%', height: '100%' }}
      >
        {sortedCells.map((pos) => {
          /** Get all bugs at this position, sorted by height */
          const bugsAtPos = bugs
            .filter((b) => b.q === pos.q && b.r === pos.r)
            .sort((a, b) => a.height - b.height);

          /** Determine if this cell is currently selected */
          const isSelected =
            selectedBoardPos && selectedBoardPos.q === pos.q && selectedBoardPos.r === pos.r;

          /** Check if this cell is a valid placement */
          const isValidPlacement = validPlacements.some(
            (p) => p.q === pos.q && p.r === pos.r
          );

          /** Check if this cell is a valid move destination */
          const isValidMove = validMovesForSelecPos.some(
            (p) => p.q === pos.q && p.r === pos.r
          );

          /** Convert hex grid coordinates to pixel coordinates */
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
