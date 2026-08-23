import React from 'react';
import { Sparkles, MessageSquarePlus } from 'lucide-react';
import { Link } from 'react-router-dom';

const Navbar = ({ onNewConversation }) => {
  return (
    <nav className="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between shadow-sm sticky top-0 z-10">
      <div className="flex items-center space-x-8">
        <Link to="/" className="flex items-center space-x-2">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <span className="text-xl font-bold text-gray-900 tracking-tight">SchemeConnect<span className="text-blue-600">AI</span></span>
        </Link>
        <div className="hidden md:flex space-x-6">
          <Link to="/" className="text-sm font-medium text-gray-600 hover:text-blue-600 transition">Home</Link>
          <Link to="/how-it-works" className="text-sm font-medium text-gray-600 hover:text-blue-600 transition">How It Works</Link>
          <Link to="/schemes" className="text-sm font-medium text-gray-600 hover:text-blue-600 transition">Schemes</Link>
        </div>
      </div>
      
      <div className="flex items-center space-x-4">
        {onNewConversation ? (
          <button 
            onClick={onNewConversation}
            className="flex items-center space-x-2 bg-blue-50 text-blue-700 hover:bg-blue-100 px-4 py-2 rounded-md text-sm font-medium transition-colors"
          >
            <MessageSquarePlus className="w-4 h-4" />
            <span>New Chat</span>
          </button>
        ) : (
          <Link 
            to="/chat"
            className="flex items-center space-x-2 bg-blue-600 text-white hover:bg-blue-700 px-4 py-2 rounded-md text-sm font-medium transition-colors"
          >
            <MessageSquarePlus className="w-4 h-4" />
            <span>Try AI Chat</span>
          </Link>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
