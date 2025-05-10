import { NextResponse } from "next/server";

const BASE_URL = "http://localhost:8000";

// Function to fetch data from the external API
async function fetchData(endpoint: string) {
  try {
    const response = await fetch(`${BASE_URL}${endpoint}`);
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
}

// Define the GET method for App Router
export async function GET() {
  try {
    const data = await fetchData("/"); // Replace '/' with the actual endpoint if needed
    return NextResponse.json(data, { status: 200 });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to fetch data" },
      { status: 500 }
    );
  }
}
