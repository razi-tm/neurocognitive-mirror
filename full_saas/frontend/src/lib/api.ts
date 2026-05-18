import axios from 'axios';
import { CognitiveSession } from '../types/session';
export const api = axios.create({ baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000' });
export async function analyze(sessions: CognitiveSession[]){ return (await api.post('/api/analyze',{sessions})).data; }
export async function narrative(sessions: CognitiveSession[]){ return (await api.post('/api/narrative',{sessions, include_rag:true})).data; }
export async function demoData(){ return (await api.get('/api/demo-data')).data.sessions as CognitiveSession[]; }
