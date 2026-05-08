"use client"
import { useState } from 'react'

export default function AIAssistant() {
  const [prompt, setPrompt] = useState('')
  const [result, setResult] = useState('')
  const [loading, setLoading] = useState(false)

  async function run() {
    setLoading(true)
    const r = await fetch('/api/ai', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt })
    })
    const d = await r.json()
    setResult(d.text || 'No response')
    setLoading(false)
  }

  return (
    <div className="card p-6">
      <h2 className="text-2xl font-bold">AI Admin Assistant</h2>
      <p className="text-slate-300 mt-2">Use this to draft page content, summarize accounts, and guide admin work.</p>
      <textarea 
        className="input mt-4 min-h-32" 
        value={prompt} 
        onChange={e => setPrompt(e.target.value)} 
        placeholder="Write a page brief or admin task..."
      />
      <button className="btn mt-4" onClick={run} disabled={loading}>
        {loading ? 'Thinking...' : 'Generate'}
      </button>
      <div className="mt-4 rounded-2xl border border-slate-700 p-4 bg-slate-950/60 whitespace-pre-wrap">
        {result}
      </div>
    </div>
  )
}