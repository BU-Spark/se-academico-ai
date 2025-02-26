"use client";  

import { useState } from "react"; 
import ChatInput from "./userInputField"; 

export default function ChatBox() {
  const [messages, setMessages] = useState([]); // chat messages

  // Function to handle sending a new message
  const sendMessage = (newMessage) => {
    if (newMessage.trim() !== "") {
      setMessages([...messages, newMessage]); // Add new message at the bottom 
    }
  }; 

  return (
    <div className="flex flex-col h-[600px] p-2 w-[1320px] px-[50px]">
      {/* Chat Display */} 
      <div className="flex flex-col items-end space-y-2">
        {messages.map((msg, index) => (
          <div
            key={index}
            className="bg-blue-100 rounded-md text-gray-800 px-3 py-2 inline-block max-w-[75%] break-words"
          >
            {msg.replace(/<\/?div>/g, "\n").replace(/<br\s*\/?>/g, "\n \n").split("\n").map((line, i) => (
              <p key={i} className="whitespace-pre-wrap">{line}</p>
            ))} 
          </div>
        ))}
      </div>


      {/* Chat Input Field */}
      <ChatInput sendMessage={sendMessage} />
    </div>
  );
}
