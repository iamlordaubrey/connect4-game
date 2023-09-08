import { useContext, useEffect, useState } from "react";
import { styled } from "styled-components";

import GameContext from "../utils/GameContext";
import { BoardType, GameState, PlayerValue } from "../utils/types";

const StyledBoard = styled.div`
background-image: linear-gradient(#3ca3ff, #005eb3);
width: 400px;
margin: auto;
padding: 4px;
`;

const StyledCell = styled.div`
width: calc(400px/8 - 8px);
height: calc(400px/8 - 8px);
background: white;
display: inline-block;
box-sizing: border-box;
border-radius: 50%;
margin: 7px;

&[data-player="playerOne"] {
  background: linear-gradient(#ffff22, #cfcf00);
}
&[data-player="playerTwo"] {
  background: linear-gradient(#ff2020, #cc0000);;
}
`

const Board = ({ 
  board, 
  setBoard,
  totalRows,
  totalColumns,
  turn,
  setTurn,
  gameState,
  setGameState,
  getGameState,
}: {
  board: BoardType, 
  setBoard: React.Dispatch<React.SetStateAction<BoardType>>,
  totalRows: number,
  totalColumns: number,
  turn: Boolean,
  setTurn: React.Dispatch<React.SetStateAction<Boolean>>,
  gameState: GameState|PlayerValue,
  setGameState: React.Dispatch<React.SetStateAction<GameState|PlayerValue>>,
  getGameState: (board: BoardType) => GameState|PlayerValue,
}) => {
  const { playerValue, sendMove, isRobotMode, setPlayerValue } = useContext(GameContext) || {};
  const [robotsPick, setRobotsPick] = useState<number>(-2)

  const findLowestEmptyIndex = (board: BoardType, row: number) => {
    const lowestIndexOnRow = totalColumns * row
    const highestIndexOnRow = lowestIndexOnRow + (totalColumns - 1)

    for (let i = highestIndexOnRow; i >= lowestIndexOnRow; i--) {
      if (board[i] === PlayerValue.None) {
        return i
      }
    }
    return -1
  }

  const makeMove = (row: number) => {
    const index = findLowestEmptyIndex(board, row)

    if (index === undefined) {
      return;
    }
    
    const newBoard = [...board]

    if (!playerValue) return
    newBoard[index] = playerValue

    if (!sendMove) throw Error("sendMove is not defined");
    sendMove(newBoard, playerValue);

    getGameState(newBoard)
    setGameState(getGameState(newBoard))

    setBoard(newBoard)

    if (isRobotMode) {
      if (!setPlayerValue) throw Error("Player value not defined")

      if (turn === true) {
        // It's human turn
        setPlayerValue(PlayerValue.Two)
      } else {
        setPlayerValue(PlayerValue.One)
      }
      setTurn(!turn)
    } else {
      setTurn(false)
    }
  }

  useEffect(() => {
    if (isRobotMode && !turn) {
      // It's robots turn, robot plays
      const lastCellIndex = (totalRows * totalColumns) - 1
      
      // Checks that robot doesn't pick an already occupied cell
      let index = -1
      let row = -1

      while (index === -1 ) {
        let robotIndexChoice = Math.random() * (0-lastCellIndex) + lastCellIndex
        row = ~~(robotIndexChoice / totalColumns)  // Floors the result

        index = findLowestEmptyIndex(board, row)
      }
      
      setRobotsPick(row)
      makeMove(row)
    }
  });

  const handleOnClick = (event: React.MouseEvent<HTMLDivElement>, index: number) => {
    if (gameState !== GameState.Ongoing) return
    
    if (!turn) {
      return;
    }

    const row = ~~(index / totalColumns)  // Floors the result
    makeMove(row)
  }

  const renderCells = () => {
    return board.map((playerValue, index) => {
      return (
        <StyledCell 
          key={index}
          onClick={event => handleOnClick(event, index)}
          data-player={playerValue}
        /> 
      )
    })
  }

  const verboseGameState = (gameState: GameState|PlayerValue) => {
    switch(gameState) {
      case 0:
        return 'draw'
      case 'playerOne':
        return 'player 1 won, player 2 lost'
      case 'playerTwo':
        return 'player 2 won, player 1 lost'
      default:
        return 'Ongoing'
    }
  }

  return (
    <>
      <div>
        Hello { playerValue && `${playerValue}` }
        <p>{`Game state: ${verboseGameState(gameState)}`}</p>
      </div>
      <StyledBoard>
        {renderCells()}
      </StyledBoard>
    </>
  )
}

export default Board;