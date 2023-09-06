import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";

import GameContext from "../utils/GameContext";

const Landing = () => {
  const { createPlayer, joinGameRoom } = useContext(GameContext) || {};
  const [userName, setUserName] = useState("")
  const [playerCreated, setPlayerCreated] = useState(false);
  const navigate = useNavigate();

  const handleStartGame = (event:React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!createPlayer) throw Error("createPlayer is not defined");
    
    createPlayer(userName).then(player => {
      setPlayerCreated(true)
      if (!joinGameRoom) throw Error("joinGameRoom is not defined");

      joinGameRoom(player.id).then(gameRoom => {
        navigate('/game')
      })
    })
  }

  return(
    <>
      <header className="rounded-l shadow border bg-gray-200 font-bold p-4 m-4 mb-5 flex flex-col justify-center items-center">
        Connect4 Game
      </header>
      <div className="flex h-screen">
        <div className="container mx-auto my-7">
          <section>
          {
            playerCreated 
            ?
            <div> True </div>
            :
            <div className="flex flex-col justify-center items-center mb-6">
              <form 
                className="space-y-6 w-4/12" 
                action="#" 
                method="POST"
                onSubmit={handleStartGame}
              >
                <div className="rounded-md shadow-sm -space-y-px">
                  <div>
                    <input
                      id="user-name"
                      name="userName"
                      type="text"
                      autoComplete="username"
                      value={userName}
                      onChange={(e) => setUserName(e.target.value)}
                      required
                      className="appearance-none rounded-none relative block
                      w-full px-3 py-2 border border-gray-300
                      placeholder-gray-500 text-gray-900 rounded-t-md
                      focus:outline-none focus:ring-indigo-500
                      focus:border-indigo-500 focus:z-10 sm:text-sm"
                      placeholder="Enter player name"
                    />
                  </div>
                </div>

                <div>
                  <button
                    type="submit"
                    className="group relative w-full flex justify-center
                    py-2 px-4 border border-transparent text-sm font-medium
                    rounded-md text-white bg-indigo-600 hover:bg-indigo-700
                    focus:outline-none focus:ring-2 focus:ring-offset-2
                    focus:ring-indigo-500"
                  >
                    Start Game
                  </button>
                </div>
              </form>
            </div>
          }
          </section>
        </div>
      </div>
    </>
    
  )
}

export default Landing;