import React, { useState } from 'react';
import ChatBox from '../../ChatWithAi/ChatBox';
import "./PVE.css"; 

const choices = ['rock', 'paper', 'scissors'];

function PVE({ onBackToHome }) {
    const [userChoice, setUserChoice] = useState(null);
    const [computerChoice, setComputerChoice] = useState(null);
    const [result, setResult] = useState('');
    const [messages, setMessages] = useState([]);
    const [isChatVisible, setIsChatVisible] = useState(true);

    const getComputerChoice = () => {
        const randomChoice = choices[Math.floor(Math.random() * choices.length)];
        setComputerChoice(randomChoice);
        return randomChoice;
    };

    const determineWinner = (user, computer) => {
        if (user === computer) {
            return "It's a tie!";
        }
        if ((user === 'rock' && computer === 'scissors') ||
            (user === 'scissors' && computer === 'paper') ||
            (user === 'paper' && computer === 'rock')) {
            return 'You win!';
        }
        return 'Computer wins!';
    };

    const handleChoice = (choice) => {
        const computer = getComputerChoice();
        setUserChoice(choice);
        const gameResult = determineWinner(choice, computer);
        setResult(gameResult);
    };

    const sendMessage = (msg) => {
        if (msg.trim() !== '') {
            setMessages([...messages, msg]);
        }
    };

    const toggleChatVisibility = () => {
        setIsChatVisible(!isChatVisible);
    };

    return (
        <div className="pve-container">
            <button className="back-button" onClick={onBackToHome}>Back to Home</button>
            <h2>Rock, Paper, Scissors</h2>
            <div className="choices">
                {choices.map((choice) => (
                    <button key={choice} onClick={() => handleChoice(choice)}>{choice}</button>
                ))}
            </div>
            {userChoice && <p>Your choice: {userChoice}</p>}
            {computerChoice && <p>Computer's choice: {computerChoice}</p>}
            <p>{result}</p>
            <button onClick={toggleChatVisibility} className={`chat-toggle ${!isChatVisible ? 'chat-toggle-hidden' : ''}`}>
                {isChatVisible ? 'Hide Chat' : 'Show Chat'}
            </button>
            {isChatVisible && (
                <ChatBox onSendMessage={sendMessage} messages={messages} />
            )}
        </div>
    );
}

export default PVE;