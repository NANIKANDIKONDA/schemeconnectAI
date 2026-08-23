import React from 'react';

const LoadingIndicator = () => {
  return (
    <div className="flex items-center space-x-2 p-4 bg-gray-50 rounded-lg max-w-sm border border-gray-100">
      <div className="flex space-x-1">
        <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
        <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
        <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
      </div>
      <span className="text-sm text-gray-500 font-medium">Analyzing profile & searching verified schemes...</span>
    </div>
  );
};

export default LoadingIndicator;
