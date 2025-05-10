// app/api/create_graph/route.ts
// Import Node.js modules for executing shell commands and handling file paths
import { exec } from 'child_process';
import path from 'path';
import { NextRequest } from 'next/server';


// Define the POST handler for the API endpoint
export async function POST(req: NextRequest) {
  // Construct the absolute path to the Python script you want to run
  const scriptPath = path.join(process.cwd(), 'backend', 'mainKnowledgeGraph.py');
  console.log('Executing script at:', scriptPath);


  // Return a promise that wraps execution of the Python script
  return new Promise<Response>((resolve) => {
     // Use `exec` to run the Python script as a subprocess
    exec(`python3 ${scriptPath}`, (error, stdout, stderr) => {
      if (error) {
        console.error('Exec error:', error);
        return resolve(
          // If an error occurs while executing the script, return a 500 response
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
      // Send a successful response indicating the script ran without fatal errors
      return resolve(
        new Response(JSON.stringify({ message: 'Script executed successfully' }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        })
      );
    });
  });
}
