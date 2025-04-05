import React, { useState } from 'react';
import FileUploader from './components/FileUploader';
import ChatWindow from './components/ChatWindow';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css'; // Optional app-specific styles

function App() {
  const [initialResponse, setInitialResponse] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [uploadCompleted, setUploadCompleted] = useState(false);

  const handleFileUploadSuccess = (response, sessionId) => {
    if (!uploadCompleted) {
      setInitialResponse(() => response);
      setSessionId(() => sessionId);
      setUploadCompleted(true);
    }
  };

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-purple-900 to-indigo-800 text-white py-10 px-4 sm:px-6 lg:px-8 flex justify-center items-center animate-fade-in">
        <div className="relative w-full p-8 rounded-lg shadow-xl bg-glass backdrop-filter backdrop-blur border border-gray-700 animate-slide-in">
          <Routes>
            <Route
              path="/"
              element={
                !initialResponse ? (
                  <FileUploader onUploadSuccess={handleFileUploadSuccess} />
                ) : (
                  <ChatWindow initialResponse={initialResponse} sessionId={sessionId} />
                )
              }
            />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
