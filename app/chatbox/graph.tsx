'use client';

import React, { useEffect, useState, useRef } from 'react';
import dynamic from 'next/dynamic';

// Dynamically import to avoid SSR issues
const ForceGraph2D = dynamic(() => import('react-force-graph').then(mod => mod.ForceGraph2D), {
  ssr: false,
});

type Node = {
  id: string;
  label: string;
};

type Link = {
  source: string;
  target: string;
  label: string;
};

export default function Graph() {
  const [data, setData] = useState<{ nodes: Node[]; links: Link[] }>({ nodes: [], links: [] });
  const fgRef = useRef<any>(null);

  useEffect(() => {
    const fetchGraph = async () => {
      const res = await fetch('/api/graph');
      const json = await res.json();
      setData(json);
    };
    fetchGraph();
  }, []);

  return (
    <div className="w-full h-screen bg-white">
      <ForceGraph2D
        ref={fgRef}
        graphData={data}
        nodeLabel="label"
        linkLabel="label"
        nodeAutoColorBy="label"
        linkDirectionalArrowLength={4}
        linkDirectionalArrowRelPos={1}
        backgroundColor="#f8fafc"
      />
    </div>
  );
}
