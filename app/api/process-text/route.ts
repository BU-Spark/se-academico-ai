import { NextResponse } from "next/server";

const BASE_URL = "http://localhost:8000";

// Function to process data
async function processTextData(endpoint: string, body: any) {
  try {
    const options: RequestInit = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    };

    const response = await fetch(`${BASE_URL}${endpoint}`, options);

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error processing data:", error);
    throw error;
  }
}

// Define the POST method for processing text
export async function POST(request: Request) {
  try {
    // Get JSON data from the request body
    const body = await request.json();

    // For demonstration, we're passing this data to the external API
    const data = await processTextData("/process-text", body); // Endpoint where you post the data

    // Return the response from the external API
    return NextResponse.json(data, { status: 200 });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to process request" },
      { status: 500 }
    );
  }
}
