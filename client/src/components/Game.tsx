import { useContext, useState, useEffect } from "react";
import Board from "./Board";
import Chat from "./Chat";
import GameContext from "../utils/GameContext";
import { BoardType, GameState, MessageType, PlayerValue } from "../utils/types";

const Game = () => {
  const totalRows = 7
  const totalColumns = 7

  const { gameSocket, playerValue, endGame, gameRoomID, isRobotMode } = useContext(GameContext) || {};
  const [messages, setMessages] = useState<MessageType[]>([]);
  const [board, setBoard] = useState<BoardType>([...Array(totalRows * totalColumns).keys()].map(i => PlayerValue.None));
  const [turn, setTurn] = useState<Boolean>(playerValue === PlayerValue.One ? true : false);
  const [gameState, setGameState] = useState<GameState|PlayerValue>(GameState.Ongoing);

  const checkWinningSlice = (boardSlice: PlayerValue[]) => {
    if (boardSlice.some(cell => cell === PlayerValue.None)) return false;

    if (
      boardSlice[0] === boardSlice[1] &&
      boardSlice[1] === boardSlice[2] &&
      boardSlice[2] === boardSlice[3]
    ) {
      return boardSlice[0]
    }

    return false
  }

  const getGameState = (currentBoard: BoardType) => {
    // Check horizontally
    for (let row = 0; row < totalRows; row++) {
      for (let column = 0; column <= 4; column++) {
        const index = row * totalColumns + column;
        const boardSlice = currentBoard.slice(index, index + 4)

        const winningResult = checkWinningSlice(boardSlice);
        if (winningResult !== false) return winningResult;
      }
    }

    // Check vertically
    for (let row = 0; row <= 3; row++) {
      for (let column = 0; column < totalColumns; column++) {
        const index = row * totalColumns + column;
        const boardSlice = [
          currentBoard[index],
          currentBoard[index + totalColumns],
          currentBoard[index + totalColumns * 2],
          currentBoard[index + totalColumns * 3],
        ]

        const winningResult = checkWinningSlice(boardSlice);
        if (winningResult !== false) return winningResult;
      }
    }

    // Check diagonally
    for (let row = 0; row <= 3; row++) {
      for (let column = 0; column < totalColumns; column++) {
        const index = row * totalColumns + column;

        // Check diagonal down-left
        if (column >= 3) {
          const boardSlice = [
            currentBoard[index],
            currentBoard[index + (totalColumns - 1)],
            currentBoard[index + (totalColumns * 2) - 2],
            currentBoard[index + (totalColumns * 3) - 3],
          ]

          const winningResult = checkWinningSlice(boardSlice);
          if (winningResult !== false) return winningResult;
        }
        
        // Check diagonal down-right
        if (column >= 3) {
          const boardSlice = [
            currentBoard[index],
            currentBoard[index + (totalColumns + 1)],
            currentBoard[index + (totalColumns * 2) + 2],
            currentBoard[index + (totalColumns * 3) + 3],
          ]

          const winningResult = checkWinningSlice(boardSlice);
          if (winningResult !== false) return winningResult;
        }
      }
    }

    if (board.some(cell => cell === PlayerValue.None)) {
      return GameState.Ongoing
    } else {
      return GameState.Draw
    }
  };

  useEffect(() => {
    if (gameSocket) {
      gameSocket.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.type === "chat.message") {
          setMessages(messages => [
            ...messages,
            {
              playerID: data.player_id, 
              playerName: data.player_name, 
              message: data.message
            },
          ])
        }

        if (data.type === "game.move" && data.player_value !== playerValue) {
          setBoard([...data.board])

          const currentGameState = getGameState([...data.board])
          setGameState(currentGameState)

          if (currentGameState !== GameState.Ongoing) {
            let winner = null
            if (currentGameState === GameState.Draw) {
              winner = 'draw'
            } else {
              winner = data.player_id
            }

            if (!endGame || !gameRoomID) return
            endGame(gameRoomID, winner)
          }
          
          setTurn(true);
        }
      }

      return () => {
        if (gameSocket) {
          gameSocket.onmessage = null;
        }
      }
    }
  });

  return (
    <section>
      <Board 
        board={board}
        setBoard={setBoard}
        totalRows={totalRows}
        totalColumns={totalColumns}
        turn={turn}
        setTurn={setTurn}
        gameState={gameState}
        setGameState={setGameState}
        getGameState={getGameState}
      />
      {
      !isRobotMode && 
      <Chat 
        messages={messages}
      />
      }
    </section>
  )
}

export default Game;