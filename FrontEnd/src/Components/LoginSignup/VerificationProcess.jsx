import React, { useState } from 'react';
import './VerificationProcess.css';

export default function VerificationProcess({ onVerificationComplete, onBackToRegister }) {
  const [verificationCode, setVerificationCode] = useState('');
  const [verificationError, setVerificationError] = useState(''); 
  
  const handleCodeChange = (event) => {
    setVerificationCode(event.target.value);
    setVerificationError(''); 
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch('http://127.0.0.1:3000/verify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: verificationCode }),
      });

      const data = await response.json();

      if (data.verified) {
        console.log('Verification successful');
        onVerificationComplete(); 
      } else {
        console.log('Verification failed', data.message);
        setVerificationError('Verification code is incorrect. Please try again.'); 
      }
    } catch (error) {
      console.error('Verification error:', error);
      setVerificationError('An error occurred during verification. Please try again.'); 
    }
  };

  return (
    <div className="verification-container">
      <h2>Verification</h2>
      <p>Please verify your email address.</p>
      <p>Check your inbox for a verification email and enter the code below.</p>
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <input
            type="text"
            value={verificationCode}
            onChange={handleCodeChange}
            placeholder="Enter verification code"
            required
            className="input-verification-code"
          />
          <button type="submit" className="button-verify">Verify</button>
        </div>
        {verificationError && <div className="error-message">{verificationError}</div>}
      </form>
      <button onClick={onBackToRegister} className="back-to-register">Back to Register</button>
    </div>
  );
}
