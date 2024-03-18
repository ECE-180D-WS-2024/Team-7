import React from "react";
import './Home.css';

function Home({ onPageChange }) {
  return (
    <div className="home-container">
      <h1 className="home-title">Pokemon Game</h1>
      <h2 className="home-subtitle">Choose your game mode</h2> 
      <button className="home-button" onClick={() => onPageChange('PVE')}>PVE</button>
      <button className="home-button" onClick={() => onPageChange('PVP')}>PVP</button>
      <button className="home-button quit" onClick={() => onPageChange('quit')}>Quit</button>
    </div>
  );
}


export default Home;
