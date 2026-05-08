export async function POST(req: Request) {
  const { prompt } = await req.json()
  
  const text = `AI draft for: ${prompt}

Suggested page copy:
- Headline: Launch your sovereign node network.
- Subheadline: Monitor nodes, capture leads, and manage access from one dashboard.
- CTA: Launch PhoneServe.

Suggested admin action:
- Review account status and link billing.
- Check node health.
- Publish if content looks good.`

  return Response.json({ text })
}