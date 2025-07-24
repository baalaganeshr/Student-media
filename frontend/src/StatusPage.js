import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function StatusPage() {
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('/api/status')
      .then(res => setStatus(res.data))
      .catch(() => setError('Could not fetch backend status.'));
  }, []);

  return (
    <div style={{
      minHeight: '100vh', background: '#181818', color: '#fff', fontFamily: 'Arial, sans-serif',
      display: 'flex', alignItems: 'center', justifyContent: 'center'
    }}>
      <div style={{ background: '#232323', borderRadius: 10, padding: 32, minWidth: 320, boxShadow: '0 2px 16px #0008' }}>
        <h1 style={{ color: '#00e676', textAlign: 'center' }}>Backend Status</h1>
        {error && <div style={{ color: '#ff5252', marginTop: 24 }}>{error}</div>}
        {status && (
          <div style={{ marginTop: 24 }}>
            <div><span style={{ color: '#90caf9' }}>Server:</span> <span style={{ color: '#00e676' }}>{status.server}</span></div>
            <div><span style={{ color: '#90caf9' }}>MongoDB:</span> <span style={{ color: status.mongoConnected ? '#00e676' : '#ff5252' }}>{status.mongoConnected ? 'Connected' : 'Disconnected'}</span></div>
            <div><span style={{ color: '#90caf9' }}>Port:</span> <span>{status.env.PORT}</span></div>
            <div><span style={{ color: '#90caf9' }}>Mongo URI:</span> <span>{status.env.MONGO_URI}</span></div>
            <div><span style={{ color: '#90caf9' }}>Client URL:</span> <span>{status.env.CLIENT_URL}</span></div>
          </div>
        )}
      </div>
    </div>
  );
}
