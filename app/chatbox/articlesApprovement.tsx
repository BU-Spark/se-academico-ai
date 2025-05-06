'use client';

import { useState, useEffect } from 'react';
import { CheckIcon, XMarkIcon } from '@heroicons/react/24/solid';

interface ResearchPapersProps {
  papers: string[];
}
export default function ResearchPapers({ papers }: ResearchPapersProps) {
  const [topics, setTopics] = useState<string[]>([]);
  const [selected, setSelected] = useState([true, true, true]);

  useEffect(() => {
    if (Array.isArray(papers)) {
      setTopics(papers);
    }
  }, [papers]); 
  
  const selection = (index:number) => {
    setSelected((prev) => {
      const newSelection = [...prev];
      newSelection[index] = !newSelection[index];
      return newSelection;
    });
  };

  const updateTopic = (index: number, newTitle: string) => {
    setTopics((prev) => {
      const newTopics = [...prev];
      newTopics[index] = newTitle;
      return newTopics;
    });
  };

  return (
    <div className="flex flex-col items-center p-6">
      <h2 className="w-full text-xl font-semibold mb-4 text-center">Here are some research papers I recommend you look at!</h2>
      <div className="flex justify-center space-x-4">
        {topics.map((topic, index) => (
          <div key={index} className="flex flex-col items-center bg-blue-100 p-6 rounded-lg w-96 h-80 shadow-md">
            <a
              href={`http://localhost:8000/${topic}`}
              target="_blank"
              rel="noopener noreferrer"
              className="font-semibold mb-4 text-center bg-transparent focus:outline-none resize-none overflow-y-auto h-16 max-h-64 w-full p-2"
            >
              {topic}
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}