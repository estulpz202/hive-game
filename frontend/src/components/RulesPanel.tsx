import React from 'react';
import '../styles/RulesPanel.css';

/** Props for RulesPanel component. */
interface RulesPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

/** 
 * Renders the RulesPanel component, which displays the rules of the Hive game.
 * The panel can be toggled open or closed based on the `isOpen` prop.
 * Includes a close button that triggers the `onClose` callback when clicked.
 */
const RulesPanel: React.FC<RulesPanelProps> = ({ isOpen, onClose }) => {
  return (
    <div className={`rules-panel ${isOpen ? 'open' : ''}`}>
      <div className="rules-content">
        <h1>Hive: Rules of Play</h1>
        <button className="close-button" onClick={onClose}>✕</button>
        <div className="rules-text">
          <p>
            Welcome to Hive, a fun strategy game for two players!
            Your goal is to surround your opponent's Queen Bee 🐝
            while keeping yours safe. Let's dive into how to play!
          </p>

          <h2>Getting Started</h2>
          <ul>
            <li>
              Each player has their crew:
              1 Queen Bee, 2 Beetles, 2 Spiders, 3 Ants, and 3 Grasshoppers.
            </li>
            <li>
              Start with an empty board and take turns placing your bugs from your reserve.
            </li>
            <li>
              When placing bugs: the first is placed alone, the second must touch it,
              and all others must touch one of your own bugs but not any opponent bugs.
            </li>
            <li>
              Place your Queen Bee by your fourth turn.
            </li>
          </ul>

          <h2>Your Turn</h2>
          <ul>
            <li>
              Each turn, you can either place a new bug from your reserve
              or move one of your bugs in play.
            </li>
            <li>
              At the start, you can't move until your Queen Bee is placed.
            </li>
            <li>
              If you can make a legal place or move, you must do it.
              Otherwise, a pass button will appear.
            </li>
            <li>
              Golden rules:
              <ul>
                <li>Bugs must share full sides, not just corners.</li>
                <li>
                  One Hive rule:
                  All bugs must stay connected at all times, even during moves.</li>
                <li>
                  Freedom of Movement:
                  Bugs need space to move, tight gaps can block movement.
                </li>
              </ul>
            </li>
          </ul>

          <h2>Bug Movement</h2>
          <ul>
            <li> All bugs must follow the golden rules.</li>
            <li>
              <strong>🐝 Queen Bee</strong>:
              Moves one space per turn.
            </li>
            <li>
              <strong>🪲 Beetle</strong>:
              Moves one space per turn, can climb on top of other bugs. Stacked bugs are frozen.
            </li>
            <li>
              <strong>🕷️ Spider</strong>:
              Moves exactly three spaces per turn.
            </li>
            <li>
              <strong>🐜 Ant</strong>:
              Moves any number of spaces.
            </li>
            <li>
              <strong>🦗 Grasshopper</strong>:
              Jumps in a straight line over adjacent bugs to the next empty space.
            </li>
          </ul>

          <h2>Winning the Hive</h2>
          <ul>
            <li>
              The game ends when a Queen Bee is surrounded on all six sides by any bugs—her player loses!
            </li>
            <li>
              If both Queens are surrounded at once or neither player can take a turn, the game ends in a draw.
            </li>
          </ul>

          <p>
            Have fun strategizing in the battle for the hive!
          </p>
        </div>
      </div>
    </div>
  );
};

export default RulesPanel;
