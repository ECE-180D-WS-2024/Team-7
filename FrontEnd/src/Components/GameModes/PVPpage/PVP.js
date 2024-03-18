import React from 'react';
import "./PVP.css";

function PVP({ onBackToHome }) {
  return (
    <div className="pvp-container">
      <h1>PVP Page</h1>
      <button className="back-button" onClick={onBackToHome}>Back to Home</button>
    </div>
  );
}

export default PVP;