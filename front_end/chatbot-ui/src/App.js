import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');

  const sendMessage = async (e) => {
    e.preventDefault();
    const newMessages = [...messages, { sender: 'You', text: userInput }];
    setMessages(newMessages);
    setUserInput('');

    try {
      const response = await axios.post('/chat', { question: userInput });
      setMessages([...newMessages, { sender: 'Chatbot', text: response.data.response }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages([...newMessages, { sender: 'Chatbot', text: 'Sorry, an error occurred.' }]);
    }
  };

  return (
    <div className="App">
      <h1>XYZ Cremation Services Chatbot</h1>
      <div className="chat-container">
        {messages.map((m, index) => (
          <div key={index} className={`chat-message ${m.sender.toLowerCase()}`}>
            <strong>{m.sender}:</strong> {m.text}
          </div>
        ))}
      </div>
      <form onSubmit={sendMessage} className="chat-input">
        <input
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          placeholder="Type a message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default App;
