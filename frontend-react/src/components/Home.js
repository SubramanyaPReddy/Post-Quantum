import React from 'react';
import './Home.css';

const Home = ({ onNavigate }) => {
  return (
    <div className="home-container">
      <h1 className="title">NIST Crypto Evaluator</h1>
      <h2 className="subtitle">Benchmarking Post-Quantum Cryptography</h2>
      <p className="description">
        The NIST Crypto Evaluator benchmarks RSA, Kyber, and Dilithium algorithms based on performance, size, and security.
        Evaluate key generation, encryption, and signature operations with real-time metrics.
      </p>

      <div className="features-grid">
        <div className="feature-card" onClick={() => onNavigate('Key Generation')}>
          <svg className="feature-icon" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 1A11 11 0 0 0 1 12a11 11 0 0 0 11 11 11 11 0 0 0 11-11A11 11 0 0 0 12 1zm0 2a9 9 0 0 1 9 9 9 9 0 0 1-9 9 9 9 0 0 1-9-9 9 9 0 0 1 9-9zm-1 4v2H9v2h2v2h2v-2h2V9h-2V7h-2zM12 10a2 2 0 1 0 0 4 2 2 0 0 0 0-4z" />
          </svg>
          <h3>Key Generation</h3>
          <p>Evaluate the efficiency and resource usage of key generation.</p>
        </div>

        <div className="feature-card" onClick={() => onNavigate('Encrypt All')}>
          <svg className="feature-icon" fill="currentColor" viewBox="0 0 24 24">
            <path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zM9 6c0-1.66 1.34-3 3-3s3 1.34 3 3v2H9V6zm9 14H6V10h12v10zm-6-3c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2z" />
          </svg>
          <h3>Parallel Encryption</h3>
          <p>Encrypt a message using RSA, Kyber, and Hybrid schemes.</p>
        </div>

        <div className="feature-card" onClick={() => onNavigate('Sign All')}>
          <svg className="feature-icon" fill="currentColor" viewBox="0 0 24 24">
            <path d="M17 3H7c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H7V5h10v14zm-1-6.99l-1.41-1.41-3.54 3.54-1.41-1.41L7 13.01l3.54 3.54z" />
          </svg>
          <h3>Parallel Digital Signature</h3>
          <p>Sign and verify messages using RSA, Dilithium, and Hybrid algorithms.</p>
        </div>

        <div className="feature-card" onClick={() => onNavigate('History')}>
          <svg className="feature-icon" fill="currentColor" viewBox="0 0 24 24">
            <path d="M13 3a9 9 0 1 0 7.446 13.032l1.416.988A10.975 10.975 0 0 1 2 12C2 6.477 6.477 2 12 2v1zm-1 5v5h4v-2h-2V8h-2z" />
          </svg>
          <h3>History</h3>
          <p>View all previous benchmarks and performance logs.</p>
        </div>
      </div>
    </div>
  );
};

export default Home;
