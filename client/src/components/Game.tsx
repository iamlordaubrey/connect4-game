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


const Game = () => {
  const totalRows = 7
  const totalColumns = 7
  const { gameSocket, playerValue } = useContext(GameContext) || {};

  // const [playerValue, setPlayerValue] = useState<PlayerValue>(PlayerValue.One);
  
  const [messages, setMessages] = useState<MessageType[]>([])
  const [board, setBoard] = useState<BoardType>([...Array(totalRows * totalColumns).keys()].map(i => PlayerValue.None));
  const [turn, setTurn] = useState<Boolean>(playerValue === "playerOne" ? true : false);

  const togglePlayerTurn = (playerValue: PlayerValue) => {
    return playerValue === PlayerValue.One ? PlayerValue.Two : PlayerValue.One
  }

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