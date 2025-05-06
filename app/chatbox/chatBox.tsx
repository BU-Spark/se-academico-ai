"use client";  

import { useState , useRef, useEffect} from "react"; 
import ChatInput from "./userInputField";
import ChatHistory from "./chatHistory"; 


interface ChatMessage {
  text: string;
  sender: "user" | "bot";
}

interface ChatSession {
  id: string;
  title: string;
  messages: ChatMessage[];
}



export default function ChatBox() {
  const [messages, setMessages] = useState<string[]>([]); // chat messages
  const [currentTask, setCurrentTask] = useState<string | null>(null);
  const intervalRef = useRef<NodeJS.Timeout | null>(null); // Reference to store the interval ID

  const [replies, setReplies] = useState<string[]>([]); // chat messages
  const [papers, setPapers] = useState<string[]>([]); // State to store the list of papers

  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);    // current chat history 
  const [chatSessions, setChatSessions] = useState<ChatSession[]>([]);  // chat history list 
  const [currentChat, setCurrentChat] = useState<string | null>(null);  // current chat history id 

  // load chat history 
  useEffect(() => {
    const savedSessions: ChatSession[] = JSON.parse(localStorage.getItem("chatSessions") || "[]");
    setChatSessions(savedSessions);
  }, []);
  
  // select chat history 
  const selectChat = (id: string) => {
      const session = chatSessions.find((chat) => chat.id === id);
      if (session) {
        setCurrentChat(id);
        setChatHistory(session.messages);
      }
  };

  // update chat history 
  const updateChatHistory = (newMessages: ChatMessage[]) => {
    let updatedSessions = chatSessions.map((chat) =>
      chat.id === currentChat ? { ...chat, messages: newMessages } : chat
    );
    
    if (!currentChat) {
      const newChat = {
        id: `chat_${Date.now()}`,
        title: `new chat ${chatSessions.length + 1}`,
        messages: newMessages,
      };
      updatedSessions = [newChat, ...chatSessions];
      setCurrentChat(newChat.id);
    }

    setChatSessions(updatedSessions);
    localStorage.setItem("chatSessions", JSON.stringify(updatedSessions));
  }; 


  // Function to handle sending a new message
  const sendMessage = (newMessage: string) => {
    if (newMessage.trim() !== "") {
      setMessages([...messages, newMessage]); // Add new message at the bottom 
      setChatHistory(prevHistory => [...prevHistory, { text: newMessage, sender: "user" }]);
      updateChatHistory([...chatHistory, { text: newMessage, sender: "user" }]);
      
    }
  };

  const parseReplyString = (replyString: string): string[] => {
    // Remove the square brackets at the start and end
    const trimmedString = replyString.slice(1, -1);
    
    // Split the string by comma and trim whitespace and quotes
    const items = trimmedString.split(',').map(item => item.trim().replace(/^['"]|['"]$/g, ''));
    
    return items;
  };

  const sendReply = (newReply: string) => {
    if (newReply.trim() !== "") {
      setReplies([...replies, newReply]);
      setChatHistory(prevHistory => [...prevHistory, { text: newReply, sender: "bot" }]);
      
      console.log(newReply);
      
      const pdfList = parseReplyString(newReply);

      setPapers(pdfList);

      updateChatHistory([...chatHistory, { text: newReply, sender: "bot" }]);
    } 
  };

  
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
            clearInterval(intervalRef.current!); // Clear the interval once the task is processed
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
    <div className="flex">
    <ChatHistory sessions={chatSessions} selectChat={selectChat} />

    <div className="flex flex-col flex-grow overflow-y-auto h-full p-4 w-full ">
      {/* Chat Display */}
      <div className="flex flex-col space-y-2 h-[70vh]">
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
    </div> 
  );
}
