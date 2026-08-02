import { NextResponse } from 'next/server';

export async function POST(req) {
  const body = await req.json();
  
  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": process.env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01"
    },
    body: JSON.stringify(body)
import { NextResponse } from 'next/server';

export async function POST(req) {
  const body = await req.json();
  
  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": process.env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01"
    },
    body: JSON.stringify(body)
  });

  const data = await response.json();
  return NextResponse.json(data);
}
  });

  const data = await response.json();
  return NextResponse.json(data);
}
