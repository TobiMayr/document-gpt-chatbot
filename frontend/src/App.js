import React, { useState } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState("");
  const [filePaths, setFilePaths] = useState([]);

  const handleInputChange = (event) => {
    setUserInput(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const userMessage = userInput;
    const newUserMessages = [...messages, { text: userMessage, sender: 'user' }];

    const response = await fetch('http://localhost:8000/message', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: userMessage }),
    });

    const responseData = await response.json();
    const botMessage = {
      text: responseData.reply,
      sender: 'bot',
      filePaths: responseData.filePaths,
    };

    setMessages([...newUserMessages, botMessage]);
    setUserInput("");
  };

  return (
      <div className="App">
        <header className="App-header">
          <div className="chatbox">
            {messages.map((msg, index) => (
                <div key={index} className={`message ${msg.sender}`}>
                  {msg.text}
                  {msg.sender === 'bot' && msg.filePaths && (
                      <div className="file-paths">
                        <p>Relevant File(s):</p>
                        <ul>
                          {msg.filePaths.map((path, idx) => (
                              <li key={idx}>{path}</li>
                          ))}
                        </ul>
                      </div>
                  )}
                </div>
            ))}
          </div>
        </header>
        <div className="chat-input-container">
          <form onSubmit={handleSubmit} className="chat-form">
            <input
                type="text"
                value={userInput}
                onChange={handleInputChange}
                placeholder="Ask me anything..."
            />
            <button type="submit">Send</button>
          </form>
        </div>
      </div>
  );
}

export default App;
