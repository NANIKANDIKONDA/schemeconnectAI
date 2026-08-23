import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Chat from './pages/Chat';
import HowItWorks from './pages/HowItWorks';
import Schemes from './pages/Schemes';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/how-it-works" element={<HowItWorks />} />
        <Route path="/schemes" element={<Schemes />} />
      </Routes>
    </Router>
  );
}

export default App;
