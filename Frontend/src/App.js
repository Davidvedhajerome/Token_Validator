import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [newToken, setNewToken] = useState('');
  const [tokenToValidate, setTokenToValidate] = useState('');
  const [resultMessage, setResultMessage] = useState('');

  const addToken = async () => {
    try {
      const response = await axios.post('http://localhost:5000/add-token', {
        tokenNumber: newToken,
      });
      setResultMessage(response.data.message);
    } catch (error) {
      setResultMessage(error.response ? error.response.data.message : 'Error occurred');
    }
  };

  const validateToken = async () => {
    try {
      const response = await axios.post('http://localhost:5000/validate-token', {
        tokenNumber: tokenToValidate,
      });
      const data = response.data;

      if (data.valid_tokens || data.invalid_tokens) {
        setResultMessage(
          `Valid Tokens: ${data.valid_tokens.join(', ')}\nInvalid Tokens: ${data.invalid_tokens.join(', ')}`
        );
      } else {
        setResultMessage(data.message);
      }
    } catch (error) {
      setResultMessage(error.response ? error.response.data.message : 'Error occurred');
    }
  };

  return (
    <div className="App">
      <h1>Biriyani Token Validation</h1>

      {/* Add Token or Token Range */}
      <div>
        <h3>Add Token or Token Range</h3>
        <input
          type="text"
          value={newToken}
          onChange={(e) => setNewToken(e.target.value)}
          placeholder="Enter token number or range (e.g., 1 - 10)"
        />
        <button onClick={addToken}>Add Token(s)</button>
      </div>

      {/* Validate Token or Token Range */}
      <div>
        <h3>Validate Token or Token Range</h3>
        <input
          type="text"
          value={tokenToValidate}
          onChange={(e) => setTokenToValidate(e.target.value)}
          placeholder="Enter token number or range (e.g., 1 - 10)"
        />
        <button onClick={validateToken}>Validate Token(s)</button>
      </div>

      {/* Result Message */}
      {resultMessage && <pre>{resultMessage}</pre>}
    </div>
  );
}

export default App;
