import { useContext, useState, useEffect } from "react";
import Board from "./Board";
import Chat from "./Chat";
import GameContext from "../utils/GameContext";

interface MessageType {
  playerID: string,
  playerName: string,
  message: string,
}

enum PlayerValue {
  None = 'playerNone',
  One = 'playerOne',
  Two = 'playerTwo'
}

type BoardType = PlayerValue[]

enum GameState {
  Ongoing = -1,
  Draw = 0,
  PlayerOneWin = PlayerValue.One,
  PlayerTwoWin = PlayerValue.Two,
}


const Game = () => {
  const totalRows = 7
  const totalColumns = 7
  const { gameSocket, playerValue } = useContext(GameContext) || {};

  // const [playerValue, setPlayerValue] = useState<PlayerValue>(PlayerValue.One);
  
  const [messages, setMessages] = useState<MessageType[]>([])
  const [board, setBoard] = useState<BoardType>([...Array(totalRows * totalColumns).keys()].map(i => PlayerValue.None));
  const [turn, setTurn] = useState<Boolean>(playerValue === "playerOne" ? true : false);
  const [gameState, setGameState] = useState<GameState|PlayerValue>(GameState.Ongoing)


  // const togglePlayerTurn = (playerValue: PlayerValue) => {
  //   return playerValue === PlayerValue.One ? PlayerValue.Two : PlayerValue.One
  // }
  const checkWinningSlice = (boardSlice: PlayerValue[]) => {
    console.log('in checkwinningslice')
    if (boardSlice.some(cell => cell === PlayerValue.None)) return false;

    if (
      boardSlice[0] === boardSlice[1] &&
      boardSlice[1] === boardSlice[2] &&
      boardSlice[2] === boardSlice[3]
    ) {
      console.log('bs', boardSlice)
      return boardSlice[0]
    }

    console.log('false')
    return false
  }

  const getGameState = (currentBoard: BoardType) => {
    // Check horizontally
    for (let row = 0; row < totalRows; row++) {
      for (let column = 0; column <= 4; column++) {
        const index = row * totalColumns + column;
        console.log('r,c', `${row},${column}`, 'idx', index)
        const boardSlice = currentBoard.slice(index, index + 4)
        console.log('board slice: ', boardSlice)

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

  if (!playerValue) {const playerValue = PlayerValue.None}

  useEffect(() => {
    if (gameSocket) {
      gameSocket.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.type === "chat.message") {
          setMessages(messages => [
            ...messages,
            {playerID: data.player_id, playerName: data.player_name, message: data.message},
          ])
        }
        console.log('player numberss: ', data.player_value, playerValue)
        if (data.type === "game.move" && data.player_value !== playerValue) {
          console.log('updating!!!')
          // if (data.type === "game.move" && data.player_turn !== playerTurn)

          setBoard([...data.board])
          setGameState(getGameState([...data.board]))
          // if (data && data.playerValue) {
          //   setPlayerValue(togglePlayerTurn(data.playerValue))
          // }
          // if (setPlayerValue) togglePlayerTurn(data.playerValue)
          console.log('setting turn to true... ')
          setTurn(true);
        } else {

          console.log('move received, but doing nothing')
        }
      }

      return () => {
        if (gameSocket) {
          gameSocket.onmessage = null;
        }
      }
    }
  }, [gameSocket]);
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
        // playerValue={playerValue}
        // setPlayerValue={setPlayerValue}
      />
      <Chat 
        messages={messages}
        setMessages={setMessages}
      />
    </section>
  )
}

export default Game;