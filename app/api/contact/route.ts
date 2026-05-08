export async function POST(req: Request) {
  const data = await req.json()
  
  // In real app, save to database
  console.log('Contact form:', data)
  
  return Response.json({ 
    ok: true, 
    received: data 
  })
}