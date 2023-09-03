import { ReactNode, createContext, useState } from "react";

interface Props {
  children?: ReactNode;
}

interface PlayerType {
  status?: string;
  id: string;
  username: string;
  wins: number;
  losses: number;
}

interface GameContextType {
  gameSocket: WebSocket|null;
  playerID: string|null;
  gameRoomID: string|null;
  createPlayer: (userName: string) => Promise<PlayerType>;
  joinGameRoom: (playerID: string) => Promise<void>;
  sendMessage: (message: string) => void;
  JoinRoom: (roomID: string) => Promise<void>;
}

const GameContext = createContext<GameContextType|null>(null);
export default GameContext;

export const GameProvider = ({ children }: Props) => {
  const [gameSocket, setGameSocket] = useState<WebSocket|null>(null);
  const [playerID, setPlayerID] = useState<string|null>(null);
  const [gameRoomID, setGameRoomID] = useState<string|null>(null);

  const createPlayer = async (playerName: string) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/player/create/", { // ToDo: move url to env file
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: playerName,
        })
      });

      if (!response.ok) {
        throw Error(`Error from the server! Status: ${response.statusText}`);
      }

      const player = await response.json();
      setPlayerID(player.id)
      return player

    } catch (error) {
      throw Error(`Something went wrong while creating the player: ${error}`)
    }
  }

  const joinGameRoom = async (playerID: string) => {
    const requestHeaders: HeadersInit = new Headers();
    requestHeaders.set("Content-Type", "application/json")
    requestHeaders.set("player-id", playerID)

    try {
      const response = await fetch("http://127.0.0.1:8000/api/game/join/", {
        method: "POST",
        headers: requestHeaders,
      });

      if (!response.ok) {
        throw Error(`Error from the server! Status: ${response.statusText}`);
      }

      const gameRoom = await response.json();
      setGameRoomID(gameRoom.id);
      setGameSocket(new WebSocket(`ws://127.0.0.1:8000/ws/socket-server/?player-id=${playerID}`))
      return gameRoom;

    } catch (error) {
      throw Error(`An error occurred while starting the game: ${error}`)
    }
  }

  const sendMessage = (message: string) => {
    if (gameSocket) {
      const data = JSON.stringify({
        type: 'chat.message',
        player: playerID,
        message: message,
      });
      gameSocket.send(data);
    }
  };

  const JoinRoom = async (roomID: string) => {
    setGameRoomID(roomID)
    setGameSocket(new WebSocket(`ws://localhost:8000/api/game/${roomID}/`));
  };

  const contextData = {
    gameSocket,
    playerID,
    gameRoomID,
    createPlayer,
    joinGameRoom,
    sendMessage,
    JoinRoom,
  };

  return (
    <GameContext.Provider value={contextData}>
      {children}
    </GameContext.Provider>
  );
};