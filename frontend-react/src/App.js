// src/App.js

import React, { useState, useEffect } from 'react';
import KeyGen from './components/KeyGen';
import EncryptAll from './components/EncryptAll';
import SignAll from './components/SignAll';
import History from './components/History';
import Home from './components/Home';
import { getHealth } from './api';

export default function App() {
  const [page, setPage] = useState('Home');

  useEffect(() => {
    getHealth().catch(() => alert('⚠️ Backend not responding on http://localhost:5000'));
  }, []);

  return (
    <div style={{ padding: 20 }}>
      {page === 'Home' && <Home onNavigate={(section) => setPage(section)} />}
      {page === 'Key Generation' && <KeyGen onBack={() => setPage('Home')} />}
      {page === 'Encrypt All' && <EncryptAll onBack={() => setPage('Home')} />}
      {page === 'Sign All' && <SignAll onBack={() => setPage('Home')} />}
      {page === 'History' && <History onBack={() => setPage('Home')} />}
    </div>
  );
}
