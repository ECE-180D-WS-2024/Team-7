import React, { useState } from "react";
import './App.css';
import Login from "./Components/LoginSignup/Login";
import Register from "./Components/LoginSignup/Register";
import Home from "./Components/HomePage/Home";
import PVE from "./Components/GameModes/PVEpage/PVE"; 
import PVP from "./Components/GameModes/PVPpage/PVP"; 
import VerificationProcess from "./Components/LoginSignup/VerificationProcess"; 

function App() {
  const [currentForm, setCurrentForm] = useState('login');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentPage, setCurrentPage] = useState('home'); 

  const toggleForm = (formName) => {
    setCurrentForm(formName);
  };

  const handleRegistrationSuccess = () => {
    setCurrentForm('verification');
  };
  
  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
    setCurrentPage('home'); 
  };

  const handlePageChange = (page) => {
    setCurrentPage(page); 
  };

  const handleVerificationComplete = () => {
    setIsLoggedIn(true); 
    setCurrentPage('home');
  };

  const handleBackToRegister = () => {
    setCurrentForm('register');
  };

  const renderPage = () => {
    if (!isLoggedIn) {
      switch(currentForm) {
        case "login":
          return <Login onFormSwitch={toggleForm} onLoginSuccess={handleLoginSuccess} />;
        case "register":
          return <Register onFormSwitch={toggleForm} onRegistrationSuccess={handleRegistrationSuccess} />;
        case "verification":
          return <VerificationProcess onVerificationComplete={handleVerificationComplete} onBackToRegister={handleBackToRegister} />;
        default:
          return <Login onFormSwitch={toggleForm} onLoginSuccess={handleLoginSuccess} />;
      }
    } else {
      switch (currentPage) {
        case 'home':
          return <Home onPageChange={handlePageChange} />;
        case 'PVE':
          return <PVE onBackToHome={() => handlePageChange('home')} />;
        case 'PVP':
          return <PVP onBackToHome={() => handlePageChange('home')} />;
        case 'quit':
          setIsLoggedIn(false);
          setCurrentForm('login');
          setCurrentPage('home');
          break;
        default:
          return <Home onPageChange={handlePageChange} />;
      }
    }
  };

  const backgroundClass = isLoggedIn ? (currentPage === 'home' ? 'homeBackground' : '') : 'loginBackground';

  return (
    <div className={`App ${backgroundClass}`}>
      {renderPage()}
    </div>
  );
}

export default App;
