import { createContext, useState } from "react";
import { GameContextType, Props, PlayerValue, BoardType } from "./types";

const GameContext = createContext<GameContextType|null>(null);
export default GameContext;

export const GameProvider = ({ children }: Props) => {
  const [gameSocket, setGameSocket] = useState<WebSocket|null>(null);
  const [playerID, setPlayerID] = useState<string|null>(null);
  const [playerValue, setPlayerValue] = useState<PlayerValue>(PlayerValue.None);
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

      const pv = (gameRoom.player_two ? PlayerValue.Two : PlayerValue.One)
      setPlayerValue(pv)

      setGameSocket(new WebSocket(`ws://127.0.0.1:8000/ws/socket-server/?player-id=${playerID}&game-id=${gameRoom.id}`))

      return gameRoom;

    } catch (error) {
      throw Error(`An error occurred while starting the game: ${error}`)
    }
  }

  const endGame = async (gameRoomID: string, playerID: string) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/game/end/", { // ToDo: move url to env file
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          game_id: gameRoomID,
          winning_player_id: playerID
        })
      });

      if (!response.ok) {
        throw Error(`Error from the server! Status: ${response.statusText}`);
      }

    } catch (error) {
      throw Error(`Something went wrong while creating game log: ${error}`)
    }
  }

  const sendMessage = (message: string) => {
    if (gameSocket) {
      const data = JSON.stringify({
        type: 'chat.message',
        player_id: playerID,
        message: message,
      });
      gameSocket.send(data);
    }
  };

  const sendMove = (board: BoardType, playerValue: PlayerValue) => {
    if (gameSocket) {
      const data = JSON.stringify({
        type: 'game.move',
        player_id: playerID,
        player_value: playerValue,
        board: board,
      });
      gameSocket.send(data);
    }
  }

  const contextData = {
    gameSocket,
    playerID,
    playerValue,
    gameRoomID,
    createPlayer,
    joinGameRoom,
    endGame,
    sendMessage,
    sendMove,
  };

  return (
    <GameContext.Provider value={contextData}>
      {children}
    </GameContext.Provider>
  );
};