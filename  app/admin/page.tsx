import AIAssistant from '../../components/ai-assistant'

export default function Admin() {
  return (
    <main className="p-8 max-w-6xl mx-auto">
      <h1 className="text-3xl font-black">Admin Portal</h1>
      <div className="grid2 mt-6">
        <div className="card p-6">
          <h2 className="font-bold">Users</h2>
          <p className="text-slate-300 mt-2">Manage accounts and roles.</p>
        </div>
        <div className="card p-6">
          <h2 className="font-bold">Nodes</h2>
          <p className="text-slate-300 mt-2">Control global node status.</p>
        </div>
        <div className="card p-6">
          <h2 className="font-bold">Inquiries</h2>
          <p className="text-slate-300 mt-2">Review partnership leads.</p>
        </div>
        <div className="card p-6">
          <h2 className="font-bold">Billing</h2>
          <p className="text-slate-300 mt-2">Freemium and upgrade controls.</p>
        </div>
      </div>
      <div className="mt-8">
        <AIAssistant />
      </div>
    </main>
  )
}