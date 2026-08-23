import React from 'react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const HowItWorks = () => {
  return (
    <div className="min-h-screen flex flex-col font-sans bg-gray-50 text-gray-900">
      <Navbar />
      <main className="flex-1 max-w-4xl mx-auto px-4 py-16">
        <h1 className="text-4xl font-extrabold text-blue-900 mb-6 text-center">How It Works</h1>
        <p className="text-lg text-gray-700 mb-12 text-center">
          SchemeConnect AI combines natural language understanding with strict, verifiable rules.
        </p>

        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-200">
          <h2 className="text-2xl font-bold text-gray-800 mb-6 border-b pb-4">Architecture Pipeline</h2>
          <ul className="space-y-6">
            <li className="flex items-start">
              <span className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 font-bold mr-4 shrink-0">1</span>
              <div>
                <h4 className="text-lg font-semibold text-gray-800">User Message</h4>
                <p className="text-gray-600 text-sm mt-1">You describe your situation naturally (e.g., "I am a farmer from AP").</p>
              </div>
            </li>
            <li className="flex items-start">
              <span className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 font-bold mr-4 shrink-0">2</span>
              <div>
                <h4 className="text-lg font-semibold text-gray-800">Gemini AI Profile Extraction</h4>
                <p className="text-gray-600 text-sm mt-1">Gemini extracts structured data (Age, State, Income, Occupation) from your message safely.</p>
              </div>
            </li>
            <li className="flex items-start">
              <span className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 font-bold mr-4 shrink-0">3</span>
              <div>
                <h4 className="text-lg font-semibold text-gray-800">Smart Filtering & Vector RAG</h4>
                <p className="text-gray-600 text-sm mt-1">We filter our verified database and use semantic search to find matching government schemes.</p>
              </div>
            </li>
            <li className="flex items-start">
              <span className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 font-bold mr-4 shrink-0">4</span>
              <div>
                <h4 className="text-lg font-semibold text-gray-800">Deterministic Eligibility Engine</h4>
                <p className="text-gray-600 text-sm mt-1">A strict Python rules engine checks criteria. <b>AI does not make eligibility decisions.</b></p>
              </div>
            </li>
          </ul>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default HowItWorks;
