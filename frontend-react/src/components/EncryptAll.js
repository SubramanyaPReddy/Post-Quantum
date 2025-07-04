// src/components/EncryptAll.js

import React, { useState } from 'react';
import { encryptAll } from '../api';
import './Section.css';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

export default function EncryptAll({ onBack }) {
  const [msg, setMsg] = useState('');
  const [data, setData] = useState(null);

  const handleEncrypt = async () => {
    const r = await encryptAll(msg);
    setData(r.data.results);
  };

  return (
    <div className="section-container">
      <h2 className="section-title">🔒 Parallel Encryption</h2>
      <p className="section-description">
        Encrypt a message using RSA, Kyber, and Hybrid. View performance metrics visually.
      </p>
      <textarea
        className="input-area"
        placeholder="Enter message..."
        rows={4}
        value={msg}
        onChange={e => setMsg(e.target.value)}
      />
      <button className="action-button" onClick={handleEncrypt}>Encrypt Message</button>

      {data && (
        <>
          <div className="chart-container">
            <h3>Time Taken (s)</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={data}>
                <XAxis dataKey="algorithm" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="time" fill="#00bcd4" />
              </BarChart>
            </ResponsiveContainer>

            <h3>Ciphertext Size (bytes)</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={data}>
                <XAxis dataKey="algorithm" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="size" fill="#82ca9d" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </>
      )}

      <button className="back-button" onClick={onBack}>← Back to Home</button>
    </div>
  );
}
