import { NextResponse } from 'next/server';
import nodemailer from 'nodemailer';

export async function POST(request) {
  try {
    // 1. Parse the incoming data sent from your webpage form
    const { name, email, message } = await request.json();

    // 2. Set up your secure outgoing mail transporter
    // For production, you will replace these with real environment variables later
    const transporter = nodemailer.createTransport({
      service: 'gmail', 
      auth: {
        user: process.env.EMAIL_USER || 'your-email@gmail.com', 
        pass: process.env.EMAIL_PASS || 'your-app-password', 
      },
    });

    // 3. Define the email layout that gets sent to you
    const mailToAdmin = {
      from: '"PhoneServe Node" <no-reply@phoneserve.network>',
      to: 'your-email@gmail.com', // Where you want to receive notifications
      subject: `🌐 New Mesh Network Inquiry from ${name}`,
      text: `Name: ${name}\nEmail: ${email}\n\nMessage:\n${message}`,
      html: `
        <div style="font-family: sans-serif; padding: 20px; border: 1px solid #ddd;">
          <h2>PhoneServe Network Notification</h2>
          <p><strong>Name:</strong> ${name}</p>
          <p><strong>Email:</strong> ${email}</p>
          <p style="margin-top: 20px;"><strong>Message:</strong></p>
          <div style="background: #f9f9f9; padding: 15px; border-left: 4px solid #0070f3;">
            ${message.replace(/\n/g, '<br>')}
          </div>
        </div>
      `,
    };

    // 4. Send the email
    await transporter.sendMail(mailToAdmin);

    // Return a beautiful success response back to the front-end web page
    return NextResponse.json({ success: true, message: 'Handshake complete. Email transmitted successfully.' }, { status: 200 });

  } catch (error) {
    console.error('Email routing error:', error);
    return NextResponse.json({ success: false, error: 'Internal system routing failed.' }, { status: 500 });
  }
}
