import { useState, useEffect, useCallback } from 'react';

export const useChatHistory = (sessionId) => {
  const [history, setHistory] = useState(() => {
    const storedHistory = localStorage.getItem(`chatHistory-${sessionId}`);
    return storedHistory ? JSON.parse(storedHistory) : [];
  });

  useEffect(() => {
    if (sessionId) {
      localStorage.setItem(`chatHistory-${sessionId}`, JSON.stringify(history));
    }
  }, [sessionId, history]);

  const addMessage = useCallback((message) => {
    setHistory((prevHistory) => [...prevHistory, message]);
  }, []);

  return { history, addMessage };
};
