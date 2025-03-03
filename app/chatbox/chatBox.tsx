"use client";  

import { useState , useRef} from "react"; 
import ChatInput from "./userInputField"; 
import ResearchPapers from "./articlesApprovement"; 

export default function ChatBox() {
  const [messages, setMessages] = useState([]); // chat messages
  const [replies, setReplies] = useState([]); // chat messages

  // Function to handle sending a new message
  const sendMessage = (newMessage) => {
    if (newMessage.trim() !== "") {
      setMessages([...messages, newMessage]); // Add new message at the bottom 
    }
  }; 

  const sendReply = (newReply) => {
    if (newReply.trim() !== "") {
      setReplies([...replies, newReply]); // Add new message at the bottom 
    }
  }; 

  const chatHistory = [];
  const maxLength = Math.max(messages.length, replies.length);
  for (let i = 0; i < maxLength; i++) {
    if (i < messages.length) chatHistory.push({ text: messages[i].replace(/<\/?div>/g, "\n").replace(/<br\s*\/?>/g, "\n \n").split("\n").map((line, i) => (
      // <p key={i} className="whitespace-pre-wrap">{line}</p>
        <p key={i} className="whitespace-pre-wrap">
          {/* Apply Formattingy */}
          {line
            .split(/(<b>.*?<\/b>|<i>.*?<\/i>)/g)
            .map((part, j) => {
              if (/<b>.*<\/b>/.test(part)) {
                return <b key={j}>{part.replace(/<\/?b>/g, "")}</b>; // bold
              }
              if (/<i>.*<\/i>/.test(part)) {
                return <i key={j}>{part.replace(/<\/?i>/g, "")}</i>; // italic
              }
              return part;
            })} </p>
     
          )), sender: "user" });
    if (i < replies.length) chatHistory.push({ text: replies[i], sender: "bot" });
  } 

  return (
    <div className="flex overflow-y-auto flex-col h-[600px] p-2 w-[1320px] px-[50px]">
  
      {/* Chat Display */}
      <div className="flex flex-col space-y-2">
        {chatHistory.map((chat, index) => (
          <div
            key={index}
            className={`px-4 py-2 max-w-[75%] rounded-md break-words ${
              chat.sender === "user" 
                ? "bg-blue-100 text-gray-800 self-end" 
                : "bg-gray-200 text-gray-800 self-start"
            }`}
          >
            {chat.text}
          </div>
        ))}
      </div>
      <div><ResearchPapers/></div>;



      {/* Chat Input Field */}
      <ChatInput sendMessage={sendMessage} />
    </div>

  );
}
