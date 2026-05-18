import Dexie, { Table } from 'dexie';
import { CognitiveSession } from '../types/session';
class NcmDb extends Dexie { sessions!: Table<CognitiveSession, number>; constructor(){ super('ncm'); this.version(1).stores({sessions:'++id, session_date, anonymous_id'}); } }
export const db = new NcmDb();
