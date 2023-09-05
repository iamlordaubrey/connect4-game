import { useContext, useState, useEffect } from "react";
import GameContext from "../utils/GameContext";

interface MessageType {
  playerID: string,
  playerName: string,
  message: string,
}

// const Chat = ({ messages, setMessages}: { messages: MessageType[], setMessages: React.Dispatch<React.SetStateAction<MessageType[]>>}) => {
const Chat = ({ messages, setMessages}: { messages: MessageType[], setMessages: React.Dispatch<React.SetStateAction<MessageType[]>>}) => {
  const { sendMessage } = useContext(GameContext) || {};
  const [userInput, setUserInput] = useState("");
  // const [messages, setMessages] = useState<MessageType[]>([]);

  const handleMessageSubmit = (event:React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!sendMessage) throw Error("sendMessage is not defined");

    sendMessage(userInput);
    console.log(messages)
    setUserInput("");
  }

  // useEffect(() => {
  //   if (gameSocket) {
  //     gameSocket.onmessage = (event) => {
  //       const data = JSON.parse(event.data);

  //       if (data.type === "chat.message") {
  //         setMessages(messages => [
  //           ...messages,
  //           {playerID: data.player, message: data.message},
  //         ])
  //       }
  //       if (data.type === "game.move") {
  //         console.log('see problem ohhh!!!')
  //       }
  //     }

  //     return () => {
  //       if (gameSocket) {
  //         gameSocket.onmessage = null;
  //       }
  //     }
  //   }
  // }, [gameSocket]);

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