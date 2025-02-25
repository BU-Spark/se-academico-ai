"use client";

import { useState } from "react";
import { HomeIcon, PlusIcon, PencilSquareIcon} from '@heroicons/react/24/outline'; 
import Link from 'next/link'; 
import { usePathname } from 'next/navigation'; 
import clsx from 'clsx';  

export default function Sidebar() {
  const [history, setHistory] = useState([
    "Brainstorm research ideas",
    "Literature review for RW research",
    "Paragraph paraphrase",
    "Paragraph and summarize",
  ]);
  const [currentChat, setCurrentChat] = useState(""); 
  const pathname = usePathname(); 

  // Function to add a new chat
  const addNewChat = () => {
    setHistory((prev) => ["New Chat", ...prev]);
  };

  // Function to store current chat in history
  const goHome = () => {
    if (currentChat.trim()) {
      setHistory((prev) => [currentChat, ...prev]);
      setCurrentChat(""); // Reset current chat
    }
  };

  return (
    <div> 
      {/* Search Group */}
      <div className="px-4 flex space-x-2">
        <button 
          onClick={addNewChat} 
          className="bg-blue-500 text-white px-3 py-1 flex items-center space-x-2 gap-1 rounded">
          New <PencilSquareIcon className="w-6"/>
        </button>
      </div> 

      {/* Button Group */}
      <div className="px-4 flex space-x-2">
        <button className="bg-grey-300 px-3 py-1 rounded">Merge Chatbots</button>
        <button className="bg-grey-300 px-3 py-1 rounded">Select</button>
      </div> 

      {/* Chat History */}
      <div className="flex-1 overflow-auto mt-4 px-4">
        {history.map((chat, index) => (
          <div key={index} className="bg-blue-400 text-white p-2 my-2 rounded">
            {chat}
          </div>
        ))}
      </div>

      {/* Add New Chat Button */}
      <div className="p-4 flex justify-center">
        <button 
          onClick={addNewChat}
          className="text-white text-2xl bg-gray-300 p-1 rounded"
        >
        <PlusIcon className="w-3 h-3 text-black" />
      </button>
      </div>
    </div>
  );
}
