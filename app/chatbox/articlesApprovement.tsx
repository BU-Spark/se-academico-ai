'use client';

import { useState } from 'react';
import { CheckIcon, XMarkIcon } from '@heroicons/react/24/solid';

export default function ResearchPapers() {
  const [topics, setTopics] = useState(['Research Topic #1', 'Research Topic #2', 'Research Topic #3']);
  const [selected, setSelected] = useState([true, true, true]);

  const selection = (index) => {
    setSelected((prev) => {
      const newSelection = [...prev];
      newSelection[index] = !newSelection[index];
      return newSelection;
    });
  };

  const updateTopic = (index, newTitle) => {
    setTopics((prev) => {
      const newTopics = [...prev];
      newTopics[index] = newTitle;
      return newTopics;
    });
  };

  return (
    <div className="flex flex-col items-center p-6">
      <h2 className="text-xl font-semibold mb-4">Here are some research papers I recommend you look at!</h2>
      <div className="flex space-x-12">
        {topics.map((topic, index) => (
          <div key={index} className="relative flex flex-col items-center bg-blue-100 p-6 rounded-lg w-96 h-80 shadow-md">
          <div className="font-semibold mb-4 text-center bg-transparent focus:outline-none resize-none overflow-y-auto h-16 max-h-64 w-full p-2">
            {topic}
          </div>
          <div className="absolute left-full top-1/2 transform -translate-y-1/2 flex flex-col space-y-2 bg-blue-200 p-2 rounded-md">
            <button onClick={() => selection(index)} className="p-1 rounded-full bg-white shadow-md">
              {selected[index] ? <CheckIcon className="w-5 h-5 text-green-500" /> : <CheckIcon className="w-5 h-5 text-gray-300" />}
            </button>
            <button onClick={() => selection(index)} className="p-1 rounded-full bg-white shadow-md">
              {selected[index] ? <XMarkIcon className="w-5 h-5 text-gray-300" /> : <XMarkIcon className="w-5 h-5 text-red-500" />}
            </button>
          </div>
          <button className="mt-auto bg-blue-400 text-white px-4 py-2 rounded-lg hover:bg-sky-100 hover:text-blue-600">Save/Proceed</button>
        </div>
        ))}
      </div>
    </div>
  );
}
