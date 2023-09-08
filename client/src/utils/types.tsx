import { ReactNode } from "react";

export interface Props {
  children?: ReactNode;
}

export interface MessageType {
  playerID: string,
  playerName: string,
  message: string,
}

export interface PlayerType {
  status?: string;
  id: string;
  username: string;
  wins: number;
  losses: number;
}

export enum PlayerValue {
  None = 'playerNone',
  One = 'playerOne',
  Two = 'playerTwo'
}

export type BoardType = PlayerValue[]

export enum GameState {
  Ongoing = -1,
  Draw = 0,
  PlayerOneWin = PlayerValue.One,
  PlayerTwoWin = PlayerValue.Two,
}

export interface GameContextType {
  gameSocket: WebSocket|null;
  playerID: string|null;
  playerValue: PlayerValue;
  // setPlayerValue: (playerValue: PlayerValue) => void;
  gameRoomID: string|null;
  createPlayer: (userName: string) => Promise<PlayerType>;
  joinGameRoom: (playerID: string, robotMode: boolean) => Promise<void>;
  endGame: (gameID: string, playerID: string) => Promise<void>;
  sendMessage: (message: string) => void;
  sendMove: (board: BoardType, playerValue: PlayerValue) => void;

  isRobotMode: boolean;
  setisRobotMode: (robot: React.SetStateAction<boolean>) => void;
  setPlayerValue: (playerValue: PlayerValue) => void;
}