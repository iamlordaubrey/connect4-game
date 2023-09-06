import { useContext, useState } from "react";
import GameContext from "../utils/GameContext";
import { MessageType } from "../utils/types";

const Chat = ({ messages }: { messages: MessageType[] }) => {
  const { sendMessage } = useContext(GameContext) || {};
  const [userInput, setUserInput] = useState("");

  const handleMessageSubmit = (event:React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!sendMessage) throw Error("sendMessage is not defined");

    sendMessage(userInput);
    setUserInput("");
  }

  return (
    <section>
      <h2>Chat</h2>
      <div>
        { messages.map((message, index) => {
          
          return (
            <p key={index}>
              {message.playerName}: {message.message}
            </p>
          )
        })}
      </div>
      <form 
        onSubmit={handleMessageSubmit}
      >
        <input 
          type="text" 
          value={userInput}
          placeholder="Type a message..."
          onChange={(event) => setUserInput(event.target.value)}
        />
        <button type="submit">Submit</button>
      </form>
    </section>
  )
}

export default Chat;