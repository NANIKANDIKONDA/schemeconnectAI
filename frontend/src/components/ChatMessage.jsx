import React from 'react';
import { Bot, User } from 'lucide-react';
import clsx from 'clsx';
import SchemeCard from './SchemeCard';

const ChatMessage = ({ role, message, schemes }) => {
  const isBot = role === 'bot';

  return (
    <div className={clsx("flex w-full mb-6", isBot ? "justify-start" : "justify-end")}>
      <div className={clsx("flex max-w-3xl", isBot ? "flex-row" : "flex-row-reverse")}>
        <div className="flex-shrink-0 mx-2">
          {isBot ? (
            <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center border border-blue-200">
              <Bot className="w-5 h-5 text-blue-600" />
            </div>
          ) : (
            <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center border border-gray-300">
              <User className="w-5 h-5 text-gray-600" />
            </div>
          )}
        </div>
        
        <div className="flex flex-col">
          <div className={clsx(
            "px-4 py-3 rounded-2xl shadow-sm text-sm whitespace-pre-wrap",
            isBot ? "bg-white border border-gray-100 text-gray-800 rounded-tl-none" : "bg-blue-600 text-white rounded-tr-none"
          )}>
            {message}
          </div>

          {schemes && schemes.length > 0 && (
            <div className="mt-4 space-y-4">
              {schemes.map((scheme, idx) => (
                <SchemeCard key={idx} scheme={scheme} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;
