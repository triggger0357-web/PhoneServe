export async function GET() {
  return Response.json({
    nodes: [
      {
        id: 'node-1',
        status: 'Online',
        safeHarbor: true,
        deviceName: 'Pixel 7 Pro - Node 01',
        lastPing: new Date().toISOString()
      },
      {
        id: 'node-2',
        status: 'Offline',
        safeHarbor: false,
        deviceName: 'Pixel 8 - Node 02',
        lastPing: new Date(Date.now() - 1000000).toISOString()
      }
    ]
  })
}