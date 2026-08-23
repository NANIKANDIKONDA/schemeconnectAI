import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const Home = () => {
  return (
    <div className="min-h-screen flex flex-col font-sans bg-gray-50 text-gray-900">
      <Navbar />
      <main className="flex-1 flex flex-col items-center justify-center text-center px-4 py-20">
        <h1 className="text-5xl md:text-6xl font-extrabold text-blue-900 mb-6 tracking-tight">
          Find Government Schemes You Are Eligible For
        </h1>
        <p className="text-xl text-gray-600 mb-10 max-w-2xl">
          Tell us about yourself in simple language and our AI will help discover government schemes that may match your profile.
        </p>
        <div className="flex space-x-4">
          <Link to="/chat" className="px-8 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow hover:bg-blue-700 transition">
            Start Exploring
          </Link>
          <Link to="/how-it-works" className="px-8 py-3 bg-white text-blue-600 font-semibold border border-blue-600 rounded-lg hover:bg-blue-50 transition">
            Learn More
          </Link>
        </div>

        <div className="mt-24 grid md:grid-cols-3 gap-8 max-w-5xl w-full text-left">
          <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-100">
            <h3 className="text-lg font-bold text-gray-800 mb-2">Step 1: Tell us about yourself</h3>
            <p className="text-gray-600">Provide basic details like your age, state, and occupation in natural language.</p>
          </div>
          <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-100">
            <h3 className="text-lg font-bold text-gray-800 mb-2">Step 2: AI understands your profile</h3>
            <p className="text-gray-600">Our deterministic engine safely builds your profile without guessing or making assumptions.</p>
          </div>
          <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-100">
            <h3 className="text-lg font-bold text-gray-800 mb-2">Step 3: Get relevant schemes</h3>
            <p className="text-gray-600">Instantly discover verified government schemes tailored strictly to your eligibility.</p>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Home;
