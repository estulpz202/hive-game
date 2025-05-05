import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/index.css';

/**
 * This is the entrance of the React app. It renders the application
 * at the HTML element with id="root".
 */
const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

/**
 * Render application, App is the component we define in App.tsx.
 */
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
