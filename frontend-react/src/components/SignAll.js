// src/components/SignAll.js

import React, { useState } from 'react';
import { signAll } from '../api';
import './Section.css';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

export default function SignAll({ onBack }) {
  const [msg, setMsg] = useState('');
  const [data, setData] = useState(null);

  const handleSign = async () => {
    const r = await signAll(msg);
    setData(r.data.results);
  };

  return (
    <div className="section-container">
      <h2 className="section-title">✍️ Parallel Digital Signature</h2>
      <p className="section-description">
        Sign a message using RSA, Dilithium, and Hybrid. View performance metrics.
      </p>
      <textarea
        className="input-area"
        placeholder="Message to sign..."
        rows={4}
        value={msg}
        onChange={e => setMsg(e.target.value)}
      />
      <button className="action-button" onClick={handleSign}>Sign Message</button>

      {data && (
        <>
          <div className="chart-container">
            <h3>Signing Time (s)</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={data}>
                <XAxis dataKey="algorithm" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="time" fill="#00bcd4" />
              </BarChart>
            </ResponsiveContainer>

            <h3>Signature Size (bytes)</h3>
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
