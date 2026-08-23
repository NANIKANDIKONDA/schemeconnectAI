import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-white border-t border-gray-200 py-8 mt-auto">
      <div className="max-w-6xl mx-auto px-4 text-center">
        <h4 className="text-lg font-bold text-gray-900 mb-2">SchemeConnect AI</h4>
        <p className="text-sm text-gray-500 mb-4 max-w-2xl mx-auto">
          Disclaimer: SchemeConnect AI is an independent tool designed to assist citizens in discovering government schemes. We are not affiliated with the government. Always verify eligibility and application details through official government sources.
        </p>
        <p className="text-xs text-gray-400">
          &copy; {new Date().getFullYear()} SchemeConnect AI. All rights reserved.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
