// src/index.js
import React from 'react';
import ReactDOM from 'react-dom';
import './index.css'; // Import global styles if any
import App from './App';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
