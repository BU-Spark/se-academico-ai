import { NextResponse } from "next/server";

const BASE_URL = "http://localhost:8000";

// Function to poll the database for task status
async function pollTaskStatus(taskId: number) {
  try {
    const response = await fetch(`${BASE_URL}/poll-db?task_id=${taskId}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error polling task status:", error);
    throw error;
  }
}

// Define the GET method for polling task status
export async function GET(request: Request) {
  try {
    // Get the task_id from the query parameters
    const url = new URL(request.url);
    const taskId = url.searchParams.get("task_id");

    if (!taskId) {
      return NextResponse.json(
        { error: "No task ID provided" },
        { status: 400 }
      );
    }

    // Poll the database for the task status
    const data = await pollTaskStatus(Number(taskId));

    // Return the response from the database
    return NextResponse.json(data, { status: 200 });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to poll task status" },
      { status: 500 }
    );
  }
}
