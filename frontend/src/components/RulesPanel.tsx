import React from 'react';
import '../styles/RulesPanel.css';

interface RulesPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

const RulesPanel: React.FC<RulesPanelProps> = ({ isOpen, onClose }) => {
  return (
    <div className={`rules-panel ${isOpen ? 'open' : ''}`}>
      <div className="rules-content">
        <h1>Hive: Rules of Play</h1>
        <button className="close-button" onClick={onClose}>
          ✕
        </button>
        <div className="rules-text">
          <p>Welcome to Hive, a fun strategy game for two players! Your mission is to surround your opponent's Queen Bee 🐝 while keeping yours safe. Let's dive into how to play!</p>
          <h2>Getting Started</h2>
          <ul>
            <li>Each player grabs their colorful crew: 1 Queen Bee, 2 Beetles, 2 Spiders, 3 Ants, and 3 Grasshoppers.</li>
            <li>Start with an empty board and take turns placing your bugs from your reserve.</li>
            <li>The first bug must go solo in the center; subsequent bugs must touch at least one other bug of the same color but not any opponent's bugs.</li>
            <li>Don't forget to place your Queen Bee by your fourth turn!</li>
          </ul>
          <h2>Your Turn</h2>
          <ul>
            <li>Each turn, you can either drop a new bug from your reserve onto the board or move one of your bugs already in play.</li>
            <li>At the start, you can only place until your Queen Bee joins the hive.</li>
            <li>If you can make a legal action, you've got to do it, otherwise, a pass button will appear.</li>
            <li> Golden rules
              <ul>
                <li>Bugs must share full sides, not just corners.</li>
                <li>The “One Hive” rule: Keep everything connected!</li>
                <li>Freedom of Movement: Your bug needs room to slide or climb to its new spot.</li>
              </ul>
            </li>
          </ul>
          <h2>Bug Movement</h2>
          <ul>
            <li><strong>🐝 Queen Bee</strong>: Moves one space per turn.</li>
            <li><strong>🪲 Beetle</strong>: Moves one space per turn, can climb on top of other bugs.</li>
            <li><strong>🕷️ Spider</strong>: Moves exactly three spaces along the hive, no more, no less.</li>
            <li><strong>🐜 Ant</strong>: Moves any number of spaces around the hive.</li>
            <li><strong>🦗 Grasshopper</strong>: Jumps in a straight line over other bugs to the next empty space.</li>
          </ul>
          <h2>Winning the Hive</h2>
          <ul>
            <li>The game wraps up when a Queen Bee is hugged on all six sides by any bugs—her player loses!</li>
            <li>If both Queens get surrounded at once or neithor play can take a turn, it's a friendly draw.</li>
          </ul>
          <p>Have fun strategizing and outsmarting your opponent in the battle for the hive!</p>
        </div>
      </div>
    </div>
  );
};

export default RulesPanel;
