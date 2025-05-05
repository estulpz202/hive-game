/** Represents a single bug on the board */
export interface Bug {
    bug_type: string;
    owner: string;
    q: number;
    r: number;
    height: number;
  }
  
  /** Represents a board coordinate */
  export interface Position {
    q: number;
    r: number;
  }
  
  /** Represents how many of each bug type a player still has */
  export interface RemainingBug {
    bug_type: string;
    count: number;
  }
  
  /** Represents a player's current state */
  export interface PlayerState {
    color: string;
    remaining_bugs: RemainingBug[];
    queen_placed: boolean;
  }
  
  /** Represents the entire game state returned by /state */
  export interface GameState {
    phase: string;
    current_player: string;
    bugs: Bug[];
    players: PlayerState[];
    can_pass: boolean;
    winner: string | null;
    visible_positions: Position[];
  }
  