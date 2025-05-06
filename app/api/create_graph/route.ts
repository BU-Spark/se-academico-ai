// app/api/create_graph/route.ts
// Import necessary modules for executing shell commands and working with file paths
import { exec } from 'child_process';
import path from 'path';
import { NextRequest } from 'next/server';

// Define a POST handler for the API route
export async function POST(req: NextRequest) {
   // Construct the absolute path to the Python script that generates the knowledge graph
  const scriptPath = path.join(process.cwd(), 'backend', 'search_knowledgegraph.py');
  console.log('Executing script at:', scriptPath);

  // Return a promise that resolves once the script execution completes

  return new Promise<Response>((resolve) => {
    // Execute the Python script using a child process
    exec(`python3 ${scriptPath}`, (error, stdout, stderr) => {
       // Handle any runtime errors that occurred while executing the script
      if (error) {
        console.error('Exec error:', error);
        return resolve(
          new Response(JSON.stringify({ error: error.message }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' },
          })
        );
      }
      // Log any warnings or messages written to stderr by the script
      if (stderr) {
        console.warn('Script stderr:', stderr);
      }
       // Log the output from stdout (typically used for normal script output)
      console.log('Script stdout:', stdout);
      // Return a successful response back to the client
      return resolve(
        new Response(JSON.stringify({ message: 'Script executed successfully' }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        })
      );
    });
  });
}
