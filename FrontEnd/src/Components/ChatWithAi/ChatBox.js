import React, { useState } from 'react';
import axios from 'axios';
import './ChatBox.css'; 

function ChatBox({ onSendMessage, messages }) { 
  const [currentMessage, setCurrentMessage] = useState('');

  const handleMessageChange = (event) => {
    setCurrentMessage(event.target.value);
  };

  const sendToBackend = async (message) => {
    try {
      const { data } = await axios.post('http://localhost:8080/api/chat', message);
      return data.choices[0].message.content;
    } catch (error) {
      console.error("Error fetching reply:", error);
      return 'Error sending message to the backend';
    }
  };

  const handleSendMessage = async (event) => {
    event.preventDefault();
    if (currentMessage.trim() !== '') {
      const message = currentMessage;
      setCurrentMessage('');
      onSendMessage(message);
      const response = await sendToBackend(message);
      onSendMessage(response);
    }
  };

  return (
    <div className="chat-box">
      <div className="messages">
      {messages.map((msg, index) => (
        <React.Fragment key={index}>
          <p>{msg}</p>
          {index < messages.length - 1 && <hr className="hr-style" />}
        </React.Fragment>
      ))}
      </div>
      <form onSubmit={handleSendMessage} className="message-form">
        <input
          type="text"
          value={currentMessage}
          onChange={handleMessageChange}
          placeholder="Type a message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default ChatBox;
