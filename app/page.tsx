'use client';
import { useState, useEffect } from 'react';

export default function Home() {
  const [formData, setFormData] = useState({ name: '', email: '', message: '' });
  const [status, setStatus] = useState({ loading: false, success: null, error: null });
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  const handleSubmission = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus({ loading: true, success: null, error: null });

    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      if (data.success) {
        setStatus({ loading: false, success: 'Transmission successfully routed to the network ledger!', error: null });
        setFormData({ name: '', email: '', message: '' });
      } else {
        throw new Error(data.message || 'Transmission handshaking failure.');
      }
    } catch (err: any) {
      setStatus({ loading: false, success: null, error: err.message });
    }
  };

  return (
    <main style={{ backgroundColor: '#0a0a0a', color: '#eaeaea', minHeight: '100vh', fontFamily: 'monospace', padding: '2rem' }}>
      {/* Header Grid */}
      <header style={{ maxWidth: '800px', margin: '0 auto', borderBottom: '1px dashed #333', paddingBottom: '2rem' }}>
        <h1 style={{ color: '#00ff66', fontSize: '2rem', letterSpacing: '-0.05em', marginBottom: '0.5rem' }}>PHONESERVE // NODE_0357</h1>
        <p style={{ color: '#888', margin: 0 }}>Decentralized Mobile-First Server Architecture Platform</p>
      </header>

      {/* Sovereign Framework Highlight */}
      <section style={{ maxWidth: '800px', margin: '3rem auto', background: '#111', padding: '1.5rem', borderRadius: '4px', border: '1px solid #222' }}>
        <h2 style={{ color: '#fff', fontSize: '1.25rem', marginTop: 0 }}>Network Economic Model</h2>
        <p style={{ color: '#ccc', lineHeight: '1.6' }}>
          By establishing user-owned physical hardware as self-sustaining server nodes, PhoneServe shifts data power away from centralized server farms. 
        </p>
        <div style={{ display: 'flex', gap: '2rem', marginTop: '1.5rem' }}>
          <div>
            <span style={{ display: 'block', fontSize: '1.75rem', fontWeight: 'bold', color: '#00ff66' }}>90%</span>
            <span style={{ fontSize: '0.85rem', color: '#888' }}>User Revenue Retained</span>
          </div>
          <div>
            <span style={{ display: 'block', fontSize: '1.75rem', fontWeight: 'bold', color: '#3333ff' }}>10%</span>
            <span style={{ fontSize: '0.85rem', color: '#888' }}>Ecosystem Reinvestment</span>
          </div>
        </div>
      </section>

      {/* Live Handshake Contact Terminal */}
      <section style={{ maxWidth: '800px', margin: '3rem auto' }}>
        <h3 style={{ color: '#fff', fontSize: '1.1rem', marginBottom: '1rem' }}>Initiate Node Handshake</h3>
        
        <form onSubmit={handleSubmission} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <input 
            type="text" 
            placeholder="Identity / Name" 
            required
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            style={{ padding: '0.75rem', backgroundColor: '#111', border: '1px solid #333', color: '#fff', fontFamily: 'monospace', borderRadius: '4px' }}
          />
          <input 
            type="email" 
            placeholder="Secure Callback Email" 
            required
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            style={{ padding: '0.75rem', backgroundColor: '#111', border: '1px solid #333', color: '#fff', fontFamily: 'monospace', borderRadius: '4px' }}
          />
          <textarea 
            placeholder="Broadcast Transmission Message..." 
            rows={4}
            required
            value={formData.message}
            onChange={(e) => setFormData({ ...formData, message: e.target.value })}
            style={{ padding: '0.75rem', backgroundColor: '#111', border: '1px solid #333', color: '#fff', fontFamily: 'monospace', borderRadius: '4px', resize: 'vertical' }}
          />
          
          <button 
            type="submit" 
            disabled={status.loading}
            style={{ padding: '0.75rem', backgroundColor: '#00ff66', color: '#000', fontWeight: 'bold', border: 'none', cursor: 'pointer', fontFamily: 'monospace', borderRadius: '4px' }}
          >
            {status.loading ? 'ROUTING ENCRYPTED PAYLOAD...' : 'BROADCAST HANDSHAKE'}
          </button>
        </form>

        {status.success && <p style={{ color: '#00ff66', marginTop: '1rem', fontSize: '0.9rem' }}>✓ {status.success}</p>}
        {status.error && <p style={{ color: '#ff3333', marginTop: '1rem', fontSize: '0.9rem' }}>⚠ Error: {status.error}</p>}
      </section>
    </main>
  );
}
