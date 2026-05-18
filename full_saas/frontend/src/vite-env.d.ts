declare module 'react';
declare module 'react-dom/client';
declare module 'recharts';
declare const importMeta: ImportMeta;
interface ImportMetaEnv { readonly VITE_API_URL?: string }
interface ImportMeta { readonly env: ImportMetaEnv }
declare namespace JSX { interface IntrinsicElements { [elemName: string]: any } }
