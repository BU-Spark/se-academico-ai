"use client"; 

import { useState, useRef, useEffect } from "react";
import {
  ListBulletIcon,
  PaperClipIcon,
  ItalicIcon,
  ArrowUpIcon, 
  BoldIcon, 
  NumberedListIcon, 
} from '@heroicons/react/24/outline'; 

export default function ChatInput({sendMessage, setCurrentTask}) {
  const [message, setMessage] = useState(""); 
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const textAreaRef = useRef(null); // Reference to track cursor position 
  const isEmpty = message.trim() === ""; 
  
  // Function to apply real formatting (bold, italic, lists)
  const applyFormatting = (command) => {
    if (!textAreaRef.current) return;
    document.execCommand(command, false); 
  };

  // Handle text input 
  const handleInput = () => {
    setMessage(textAreaRef.current.innerHTML); // Save the formatted text
  }; 

  function fetchPostData(data: { text: string; }) {
    setLoading(true);
    fetch('/api/submit-query', {
        method: 'POST',  // Use POST method
        headers: {
            'Content-Type': 'application/json',  // Specify that we are sending JSON
        },
        body: JSON.stringify(data),  // Convert JavaScript object to JSON string
    })
    .then((res) => {
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
    })
    .then((data) => {
        console.log("Processed Data:", data);
        setData(data);  // Assuming setData updates the state with the result
        setCurrentTask(data.task_id); // Set the current task ID
        setLoading(false);  // Set loading to false once data is fetched
        //alert(`Processed Data: ${JSON.stringify(data)}`); // Show alert with processed data
    })
    .catch((error) => {
        console.error("Error processing data:", error);
        setError(error.message);  // Assuming setError updates an error state
        setLoading(false);  // Set loading to false even on error
        alert(`Error: ${error.message}`); // Show alert with error message
    });
  }

  // Handle send message 
  const handleSend = () => {
    if (!isEmpty) {
      sendMessage(message);
      fetchPostData({ text: message }); // Call fetchPostData with the input message
      setMessage(""); // Clear input after sending
      textAreaRef.current.textContent = "";  
    }
  }; 

  return ( 
    <div className="fixed bottom-0 left-1/4 transform translate-x-0  p-3">
      {/* Top Action Buttons */}
      <div className="flex space-x-2 mb-2 max-w-2xl mx-auto">
        <button className="bg-purple-100 text-purple-700 px-3 py-1 rounded-md text-sm">Summarize</button>
        <button className="bg-green-100 text-green-700 px-3 py-1 rounded-md text-sm">New Idea</button>
        <button className="bg-orange-100 text-orange-700 px-3 py-1 rounded-md text-sm">New Analytics</button>
        <button className="bg-pink-100 text-pink-700 px-3 py-1 rounded-md text-sm">Writing Inspection</button>
        <button className="bg-gray-100 text-gray-700 px-3 py-1 rounded-md text-sm">Uploading a document</button>
      </div>

      {/* Chat Input Box */}
      <div className="flex flex-col max-w-7xl mx-auto border rounded-lg p-2 shadow-sm bg-gray-50">
      
        {/* Formatting Buttons */} 
        <div className="flex space-x-2 mb-2">
            <button
              className="p-2 hover:bg-gray-200 rounded-md flex items-center"
              onClick={() => applyFormatting("bold")}
            >
              <BoldIcon className="h-5 w-5 text-gray-600" />
            </button>

            <button
              className="p-2 hover:bg-gray-200 rounded-md flex items-center"
              onClick={() => applyFormatting("italic")}
            >
              <ItalicIcon className="h-5 w-5 text-gray-600" />
            </button>

            <button
              className="p-2 hover:bg-gray-200 rounded-md flex items-center"
              onClick={() => applyFormatting("insertOrderedList")}
            >
              <NumberedListIcon className="h-5 w-5 text-gray-600" />
            </button>

            <button
              className="p-2 hover:bg-gray-200 rounded-md flex items-center"
              onClick={() => applyFormatting("insertUnorderedList")}
            >
              <ListBulletIcon className="h-5 w-5 text-gray-600" />
            </button>
        </div>

        

        {/* Text Input */} 
        <div
              ref={textAreaRef}
              contentEditable={true}
              className={`border rounded-md px-3 py-3 h-24 overflow-auto focus:outline-none relative before:absolute before:left-3 before:top-3 before:text-gray-400 before:pointer-events-none bg-white ${
                isEmpty ? "before:content-['I_am_thinking_about...']" : "before:content-[''] "
              }`}
              onInput={handleInput} // Track user input
        ></div> 

        {/* Attachment & Send */} 
        <div className="flex gap-[950px] space-y-2.5"> 
          <div className="flex space-x-2"> 
            <button className="p-2 hover:bg-gray-200 rounded-md flex items-center">
              <PaperClipIcon className="h-5 w-5 text-gray-600" />
            </button> 
          </div> 
          <div className="flex space-x-2"> 
            <button className="p-2 hover:bg-gray-200 rounded-md flex items-center bg-blue-300 hover:bg-sky-100 hover:text-blue-600" 
                onClick={handleSend}
                disabled={isEmpty}
            >
              <ArrowUpIcon className="h-5 w-7" />
            </button> 
          </div> 
        </div> 

      </div>

      {/* Footer Note */}
      <p className="text-center text-gray-500 text-xs mt-2">
        Academico.ai can make mistakes, so double-check it.
      </p>
    </div> 
  );
}
