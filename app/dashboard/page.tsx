export default function Dashboard() {
  return (
    <main className="p-8 max-w-6xl mx-auto">
      <h1 className="text-3xl font-black">User Dashboard</h1>
      <div className="grid2 mt-6">
        <div className="card p-6">
          <h2 className="font-bold">Active Nodes</h2>
          <p className="text-slate-300 mt-2">Monitor phone nodes and uptime.</p>
        </div>
        <div className="card p-6">
          <h2 className="font-bold">Safe Harbor</h2>
          <p className="text-slate-300 mt-2">Track handshake and trust state.</p>
        </div>
        <div className="card p-6">
          <h2 className="font-bold">Last Ping</h2>
          <p className="text-slate-300 mt-2">See latest node check-in times.</p>
        </div>
        <div className="card p-6">
          <h2 className="font-bold">Lead Status</h2>
          <p className="text-slate-300 mt-2">Review partnership interest and inquiries.</p>
        </div>
      </div>
    </main>
  )
}