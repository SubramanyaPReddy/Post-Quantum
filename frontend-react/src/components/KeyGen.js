// src/components/KeyGen.js

import React, { useState } from 'react';
import { genKeys } from '../api';
import './Section.css';

export default function KeyGen({ onBack }) {
  const [data, setData] = useState(null);

  const handleGen = async () => {
    const r = await genKeys();
    setData(r.data.nist_metrics);
  };

  return (
    <div className="section-container">
      <h2 className="section-title">🔐 Key Generation</h2>
      <p className="section-description">
        Generate keys for RSA, Kyber, and Dilithium to evaluate their generation time and memory use.
      </p>
      <button className="action-button" onClick={handleGen}>Generate Keys</button>
      {data && <pre className="result-block">{JSON.stringify(data, null, 2)}</pre>}
      <button className="back-button" onClick={onBack}>← Back to Home</button>
    </div>
  );
}
