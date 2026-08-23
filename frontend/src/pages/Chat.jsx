import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import ChatWindow from '../components/ChatWindow';
import ChatInput from '../components/ChatInput';
import ProfilePanel from '../components/ProfilePanel';
import Footer from '../components/Footer';
import { sendChatMessage } from '../services/api';

const Chat = () => {
  const [messages, setMessages] = useState([
    { role: 'bot', content: 'Welcome to SchemeConnect AI! Please describe your situation (e.g. your occupation, state, age) to find government schemes you are eligible for.' }
  ]);
  const [profile, setProfile] = useState({});
  const [missingInfo, setMissingInfo] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const getSessionId = () => localStorage.getItem('scheme_session_id');
  const setSessionId = (id) => localStorage.setItem('scheme_session_id', id);
  const clearSession = () => localStorage.removeItem('scheme_session_id');

  const handleNewConversation = () => {
    clearSession();
    setMessages([
      { role: 'bot', content: 'New conversation started. How can I help you today?' }
    ]);
    setProfile({});
    setMissingInfo([]);
  };

  const handleSendMessage = async (text) => {
    // Add user message
    const userMsg = { role: 'user', content: text };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);
    setMissingInfo([]);

    try {
      const currentSessionId = getSessionId();
      const response = await sendChatMessage(text, currentSessionId);
      
      // Update session ID if returned
      if (response.session_id) {
        setSessionId(response.session_id);
      }

      // Update Profile
      if (response.profile) {
        setProfile(response.profile);
      }

      // Update Missing Info
      if (response.missing_information) {
        setMissingInfo(response.missing_information);
      }

      // Add bot message
      const botMsg = {
        role: 'bot',
        content: response.message,
        schemes: response.schemes || []
      };
      
      setMessages((prev) => [...prev, botMsg]);
    } catch (error) {
      console.error("Chat Error:", error);
      setMessages((prev) => [
        ...prev, 
        { role: 'bot', content: 'Sorry, I encountered an error communicating with the server. Please try again.' }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100 overflow-hidden font-sans">
      <Navbar onNewConversation={handleNewConversation} />
      
      <div className="flex-1 flex flex-col lg:flex-row overflow-hidden">
        {/* Main Chat Area */}
        <div className="flex-1 flex flex-col min-w-0 border-b lg:border-b-0 lg:border-r border-gray-200">
          <ChatWindow 
            messages={messages} 
            isLoading={isLoading} 
            missingInfo={missingInfo} 
          />
          <ChatInput onSend={handleSendMessage} disabled={isLoading} />
        </div>
        
        {/* Sidebar Profile Panel */}
        <div className="w-full lg:w-80 bg-gray-50 overflow-y-auto p-4 lg:border-l border-gray-200 h-64 lg:h-auto flex-shrink-0">
          <div className="mb-4">
            <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">Context</h3>
            <ProfilePanel profile={profile} />
          </div>
        </div>
      </div>
      
      <Footer />
    </div>
  );
};

export default Chat;
