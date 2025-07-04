import axios from 'axios';

const BASE = 'http://localhost:5000';

export const genKeys = () => axios.post(`${BASE}/generate_keys`);
export const encryptAll = (message) => axios.post(`${BASE}/encrypt_all`, { message });
export const signAll = (message) => axios.post(`${BASE}/sign_all`, { message });
export const getHistory = () => axios.get(`${BASE}/get_test_history`);
export const getHealth = () => axios.get(`${BASE}/health`);
