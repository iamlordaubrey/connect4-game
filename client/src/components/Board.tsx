import { useState, useEffect, useContext } from "react";
import { styled } from "styled-components";

import GameContext from "../utils/GameContext";

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

enum PlayerValue {
  None = 'playerNone',
  One = 'playerOne',
  Two = 'playerTwo'
}

type BoardType = PlayerValue[]

// interface State {
//   board: BoardType;
//   playerTurn: Player
// }



const Board = ({ 
  board, 
  setBoard, 
  totalRows, 
  totalColumns,
  turn,
  setTurn,
  // playerValue,
  // setPlayerValue,
}: { 
  board: BoardType, 
  setBoard: React.Dispatch<React.SetStateAction<BoardType>>,
  totalRows: number,
  totalColumns: number,
  turn: Boolean,
  setTurn: React.Dispatch<React.SetStateAction<Boolean>>
  // playerValue: PlayerValue,
  // setPlayerValue: React.Dispatch<React.SetStateAction<PlayerValue>>
}) => {
  // if (!playerValue) 
  // { const playerValue = null
  // }
  // const [playerNumber, setPlayerNumber] = useState<Player>(Player.One)
  // const [turn, setTurn] = useState(playerNumber === Player.One ? true : false);
  const { gameSocket, playerValue, sendMove } = useContext(GameContext) || {};

  const togglePlayerTurn = (player: PlayerValue) => {
    return player === PlayerValue.One ? PlayerValue.Two : PlayerValue.One
  }

  // const assignPlayerValue = (value: PlayerValue) => {
  //   return value === PlayerValue.
  // }

  const findLowestEmptyIndex = (board: BoardType, row: number) => {
    // const lowestLeftColumn = (totalRows * totalColumns) - totalColumns
    console.log('row: ', row)
    // const highestIndexOnRow = ((totalColumns * row) + totalColumns) - 1;
    
    // const lowestIndexOnRow = (highestIndexOnRow - totalColumns) + 1
    const lowestIndexOnRow = totalColumns * row
    const highestIndexOnRow = lowestIndexOnRow + (totalColumns - 1)
    console.log('lir', lowestIndexOnRow)
    console.log('hir', highestIndexOnRow)


    for (let i = highestIndexOnRow; i >= lowestIndexOnRow; i--) {
      if (board[i] === PlayerValue.None) {
        return i
      }
    }
    return -1
  }

  const makeMove = (row: number) => {
    console.log('IS IT your turn? ', turn)
    // if (!turn) return;

    // // console.log('making move to column: ', row)
    const index = findLowestEmptyIndex(board, row)
    console.log('index: ', index)

    if (index === undefined) {
      console.log('index is undefined')
      return;
    }
    
    // console.log('index 2: ', index)
    // // const newBoard = board.slice()
    const newBoard = [...board]

    if (!playerValue) return 
    newBoard[index] = playerValue
    console.log('new board prev', newBoard)

    if (!sendMove) throw Error("sendMove is not defined");
    sendMove(newBoard, playerValue);

    setBoard(newBoard)
    console.log('setting turn to false... ')
    setTurn(false)
    // setPlayerValue(togglePlayerTurn(playerValue))
    // setPlayerValue()
    console.log('new player value: ', playerValue)

    console.log('new board...', board, playerValue)
  }

  const handleOnClick = (event:React.MouseEvent<HTMLDivElement>, index: number) => {
    console.log('clicked index: ', index)
    
    if (!turn) {
      console.log('turn is false')
      return;
    }
    console.log('turn is true')

    const row = ~~(index / totalColumns)  // Floors the result
    makeMove(row)
  }

  const renderCells = () => {
    return board.map((playerValue, index) => {
      // console.log(board)
      return (
        <StyledCell 
          key={index}
          onClick={event => handleOnClick(event, index)}
          data-player={playerValue}
        /> 
      )
    })
  }

  return (
    <>
      <StyledBoard>
        {renderCells()}
      </StyledBoard>
    </>
  )
}

export default Board;