import React, { useRef, useEffect } from 'react';
import ChatMessage from './ChatMessage';
import LoadingIndicator from './LoadingIndicator';
import MissingInfoCard from './MissingInfoCard';

const ChatWindow = ({ messages, isLoading, missingInfo }) => {
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  return (
    <div className="flex-1 overflow-y-auto p-4 sm:p-6 bg-slate-50" ref={scrollRef}>
      <div className="max-w-4xl mx-auto">
        {messages.map((msg, idx) => (
          <ChatMessage 
            key={idx} 
            role={msg.role} 
            message={msg.content} 
            schemes={msg.schemes} 
          />
        ))}

        {missingInfo && missingInfo.length > 0 && !isLoading && (
          <div className="ml-12 mb-4 max-w-lg">
            <MissingInfoCard fields={missingInfo} />
          </div>
        )}

        {isLoading && (
          <div className="ml-12 mb-4">
            <LoadingIndicator />
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatWindow;
