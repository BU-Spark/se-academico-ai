"use client";  

import { useState , useRef, useEffect} from "react"; 
import ChatInput from "./userInputField";

export default function ChatBox() {
  const [messages, setMessages] = useState([]); // chat messages
  const [currentTask, setCurrentTask] = useState(null);
  const intervalRef = useRef(null); // Reference to store the interval ID

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
  
  useEffect(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current); // Clear the previous interval
    }

    if (currentTask) {
      intervalRef.current = setInterval(async () => {
        try {
          const response = await fetch(`/api/poll-db?task_id=${currentTask}`);
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const data = await response.json();
          console.log("Polling...", data);
          if (data.processed) {
            sendReply(data.result); // Update the task result
            clearInterval(intervalRef.current); // Clear the interval once the task is processed
            intervalRef.current = null; // Reset the interval reference
          }
        } catch (error) {
          console.error("Error polling task status:", error);
        }
      }, 3000); // Poll every 3 seconds
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current); // Cleanup on unmount
      }
    };
  }, [currentTask]);
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


      {/* Chat Input Field */}
      <ChatInput sendMessage={sendMessage} setCurrentTask = {setCurrentTask}/>
    </div>
  );
}
