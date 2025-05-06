// app/api/create_graph/route.ts

import { exec } from 'child_process';
import path from 'path';
import { NextRequest } from 'next/server';

export async function POST(req: NextRequest) {
  const scriptPath = path.join(process.cwd(), 'backend', 'search_knowledgegraph.py');
  console.log('Executing script at:', scriptPath);

  return new Promise<Response>((resolve) => {
    exec(`python3 ${scriptPath}`, (error, stdout, stderr) => {
      if (error) {
        console.error('Exec error:', error);
        return resolve(
          new Response(JSON.stringify({ error: error.message }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' },
          })
        );
      }

      if (stderr) {
        console.warn('Script stderr:', stderr);
      }

      console.log('Script stdout:', stdout);
      return resolve(
        new Response(JSON.stringify({ message: 'Script executed successfully' }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        })
      );
    });
  });
}
