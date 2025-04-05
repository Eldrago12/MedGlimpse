import React, { useState, useEffect, useRef } from 'react';
import { askQuestion } from '../utils/api';
import { useChatHistory } from '../hooks/useChatHistory';
import Message from './Message';
import { PaperAirplaneIcon } from '@heroicons/react/24/outline';

function ChatWindow({ initialResponse, sessionId }) {
  const [newMessage, setNewMessage] = useState('');
  const { history, addMessage } = useChatHistory(sessionId);
  const chatContainerRef = useRef(null);

  useEffect(() => {
    if (initialResponse && history.length === 0) {
      addMessage({ role: 'model', content: initialResponse });
    }
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [initialResponse, history, addMessage]);

  const handleSendMessage = async () => {
    if (newMessage.trim()) {
      addMessage({ role: 'user', content: newMessage });
      setNewMessage('');
      try {
        const data = await askQuestion(sessionId, newMessage);
        addMessage({ role: 'model', content: data.response });
      } catch (error) {
        console.error("Question error:", error);
        addMessage({ role: 'model', content: 'Error processing your question.' });
      }
    }
  };

  return (
    <div className="flex flex-col h-[60vh] sm:h-[70vh] justify-between">
      <div ref={chatContainerRef} className="overflow-y-auto space-y-4 p-4">
        {history.map((msg, index) => (
          <Message key={index} role={msg.role} content={msg.content} />
        ))}
      </div>
      <div className="p-4 border-t border-gray-700">
        <div className="flex items-center">
          <input
            type="text"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Ask a question..."
            className="flex-grow bg-glass backdrop-filter backdrop-blur border border-gray-600 rounded-full py-2 px-4 text-white focus:outline-none focus:border-primary focus:ring-primary focus:ring-1"
          />
          <button
            onClick={handleSendMessage}
            className="ml-3 bg-primary hover:bg-secondary text-white font-semibold rounded-full p-2 shadow-md transition duration-300 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary focus:ring-opacity-50"
          >
            <PaperAirplaneIcon className="w-6 h-6" />
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatWindow;
