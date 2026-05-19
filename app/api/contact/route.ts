import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { name, email, message } = body;

    // Validate incoming node transmission payload
    if (!name || !email || !message) {
      return NextResponse.json(
        { success: false, message: 'Invalid payload. Missing identity fields.' },
        { status: 400 }
      );
    }

    console.log(`[NODE ROUTER] Inbound Handshake Received From: ${name} (${email})`);
    console.log(`[NODE ROUTER] Payload: ${message}`);

    // Return a verified network handshake ledger response
    return NextResponse.json({ 
      success: true, 
      message: 'Transmission successfully routed to the network ledger!' 
    });

  } catch (error: any) {
    return NextResponse.json(
      { success: false, message: `Internal handler failure: ${error.message}` },
      { status: 500 }
    );
  }
}
