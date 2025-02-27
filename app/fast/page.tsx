"use client"

import React, { useState, useEffect } from "react";

const Page: React.FC = () => {
  const [inputValue, setInputValue] = useState('');
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    submitData(inputValue);
  };



  function fetchPostData(data: { text: string; }) {
    setLoading(true);
    fetch('/api/process-text', {
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
        setLoading(false);  // Set loading to false once data is fetched
    })
    .catch((error) => {
        console.error("Error processing data:", error);
        setError(error.message);  // Assuming setError updates an error state
        setLoading(false);  // Set loading to false even on error
    });
}


function submitData(stuff: string) {
  console.log(`Submitted text: ${stuff}`);
  fetchPostData({ text: stuff });
  alert
}

  //GATHER DATA FROM API 
  /*
  useEffect(() => {
    fetchData();
  }, []); 
  */


  return (
    <div>
      <h1>Text Input Page</h1>
      <form onSubmit={handleSubmit}>
        <input 
          type="text" 
          value={inputValue} 
          onChange={handleInputChange} 
          placeholder="Enter some text" 
        />
        <button type="submit">Submit</button>
      </form>
      <p>You entered: {inputValue}</p>
      {loading && <p>Loading...</p>}
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
      {error && <p>Error: {error}</p>}
      
    </div>
  );
};

export default Page;