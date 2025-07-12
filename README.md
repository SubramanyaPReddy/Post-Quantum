# 🔐 Post-Quantum Cryptography Comparison

A comprehensive cryptographic web application built to evaluate and compare the performance, size, and security levels of classical (RSA), post-quantum (Kyber, Dilithium), and hybrid cryptographic algorithms. Developed using **Python (Flask backend)** and **React.js frontend**, this project adheres to NIST recommendations and is tailored for benchmarking in constrained environments including **mobile processors** and **IoT devices**.

---

## 📌 Features

- 🛡️ **Encryption Algorithms**:  
  - RSA (Classical)  
  - Kyber (ML-KEM – Post-Quantum)  
  - RSA + Kyber (Hybrid)

- ✍️ **Digital Signature Algorithms**:  
  - RSA  
  - Dilithium (ML-DSA – Post-Quantum)  
  - RSA + Dilithium (Hybrid)

- 📊 **Automatic Performance Evaluation**:  
  - Time taken for key generation, encryption, decryption  
  - Key, signature, and ciphertext sizes  
  - Graphical comparison of results

- 🧪 **Test Environment**:  
  - Includes benchmarking support for mobile platforms (Snapdragon, Apple M-series, etc.)

- 🗃️ **Result Storage**:  
  - Results logged and stored in a database  
  - History section displays results in table format

---

## 🚀 How It Works

### Encryption Workflow
1. Enter a custom message.
2. System encrypts using RSA, Kyber, and Hybrid methods.
3. Stores and compares all results visually.

### Signature Workflow
1. Enter a message to sign.
2. Signs using RSA, Dilithium, and Hybrid.
3. Displays signature size, time, and security comparison.

---

## 🛠️ Technologies Used

### Backend
- Python
- Flask
- liboqs / pyca
- SQLite

### Frontend
- React.js
- Tailwind CSS
- Chart.js / Plotly for graphs

---

## 📸 Screenshots

| Home Page | Encryption Comparison | Signature Comparison |
|-----------|------------------------|-----------------------|
| ![home](screenshots/home.png) | ![encryption](screenshots/encryption.png) | ![signature](screenshots/signature.png) |

---

## 📁 Folder Structure

