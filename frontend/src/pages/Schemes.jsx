import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { fetchSchemes } from '../services/api';
import { Search } from 'lucide-react';

const Schemes = () => {
  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    const loadSchemes = async () => {
      try {
        const data = await fetchSchemes();
        setSchemes(data);
      } catch (error) {
        console.error("Failed to load schemes:", error);
      } finally {
        setLoading(false);
      }
    };
    loadSchemes();
  }, []);

  const filteredSchemes = schemes.filter(s => 
    s.name.toLowerCase().includes(search.toLowerCase()) || 
    s.category.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="min-h-screen flex flex-col font-sans bg-gray-50 text-gray-900">
      <Navbar />
      <main className="flex-1 max-w-6xl mx-auto px-4 py-12 w-full">
        <div className="flex flex-col md:flex-row justify-between items-center mb-8">
          <h1 className="text-3xl font-extrabold text-gray-900">Government Schemes</h1>
          <div className="relative mt-4 md:mt-0 w-full md:w-72">
            <input 
              type="text" 
              placeholder="Search schemes..." 
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            <Search className="w-5 h-5 text-gray-400 absolute left-3 top-2.5" />
          </div>
        </div>

        {loading ? (
          <div className="flex justify-center items-center py-20">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredSchemes.map((scheme) => (
              <div key={scheme.id} className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm hover:shadow-md transition">
                <span className="text-xs font-semibold text-blue-600 uppercase tracking-wider">{scheme.category}</span>
                <h3 className="text-lg font-bold text-gray-900 mt-1 mb-2">{scheme.name}</h3>
                <p className="text-gray-600 text-sm line-clamp-3 mb-4">{scheme.description}</p>
                <div className="text-xs text-gray-500 mt-auto pt-4 border-t border-gray-100 flex justify-between">
                  <span>State: {scheme.state}</span>
                  <a href={scheme.official_link && scheme.official_link.startsWith('http') ? scheme.official_link : `https://${scheme.official_link}`} target="_blank" rel="noopener noreferrer" className="text-blue-600 font-medium hover:underline">
                    View Official
                  </a>
                </div>
              </div>
            ))}
            {filteredSchemes.length === 0 && (
              <div className="col-span-full text-center py-12 text-gray-500">
                No schemes found matching your search.
              </div>
            )}
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
};

export default Schemes;
