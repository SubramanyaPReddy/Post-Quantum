// src/components/History.js

import React, { useState } from 'react';
import { getHistory } from '../api';
import './Section.css';

export default function History({ onBack }) {
  const [data, setData] = useState(null);

  const handleLoad = async () => {
    const r = await getHistory();
    setData(r.data.history);
  };

  return (
    <div className="section-container">
      <h2 className="section-title">📜 Benchmark History</h2>
      <p className="section-description">
        View logs of previous encryption, key generation, and signature operations.
      </p>
      <button className="action-button" onClick={handleLoad}>Load History</button>

      {data && (
        <div className="result-block">
          <table style={{ width: '100%', color: 'white', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th style={{ borderBottom: '1px solid gray' }}>Type</th>
                <th style={{ borderBottom: '1px solid gray' }}>Algorithm</th>
                <th style={{ borderBottom: '1px solid gray' }}>Time (s)</th>
                <th style={{ borderBottom: '1px solid gray' }}>Size (bytes)</th>
                <th style={{ borderBottom: '1px solid gray' }}>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {data.map((entry, i) => (
                <tr key={i}>
                  <td>{entry.type}</td>
                  <td>{entry.algorithm}</td>
                  <td>{entry.time}</td>
                  <td>{entry.size}</td>
                  <td>{new Date(entry.timestamp).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <button className="back-button" onClick={onBack}>← Back to Home</button>
    </div>
  );
}
