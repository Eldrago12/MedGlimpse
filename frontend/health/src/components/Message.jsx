import React from 'react';
import ReactMarkdown from 'react-markdown';

function Message({ role, content }) {
  const isUser = role === 'user';
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`${
          isUser ? 'bg-primary' : 'bg-gray-800'
        } text-white rounded-lg p-3 max-w-md break-words`}
      >
        <ReactMarkdown>{content}</ReactMarkdown>
      </div>
    </div>
  );
}

export default Message;
