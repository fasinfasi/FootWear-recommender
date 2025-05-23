import React, { useState, useEffect } from 'react';
import './App.css';
import ProductCard from './components/ProductCard';
import FilterPanel from './components/FilterPanel';

function App() {
  const [shoes, setShoes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({ brand: '', gender: '', price_range: '', sort_by: 'rating' });

  // Fetch random shoes on component mount
  useEffect(() => {
    fetchRandomShoes();
  }, []);

  const fetchRandomShoes = async () => {
    setLoading(true);
    setError(null);
    
    try {
      console.log('Fetching random shoes...');
      const response = await fetch('http://localhost:5000/random-shoes');
      
      if (!response.ok) {
        throw new Error(`Failed to fetch shoes: ${response.status} ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log('Random shoes fetched successfully:', data.length);
      setShoes(data);
    } catch (error) {
      console.error('Error fetching random shoes:', error);
      setError(`Failed to load shoes: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleFilter = async (newFilters) => {
    console.log('Filters updated:', newFilters);
    setFilters(newFilters);
    setLoading(true);
    setError(null);
    
    try {
      console.log('Sending filter request with data:', newFilters);
      
      const response = await fetch('http://localhost:5000/filter-shoes', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(newFilters),
      });

      const contentType = response.headers.get('content-type');
      
      if (!contentType || !contentType.includes('application/json')) {
        throw new Error(`Received non-JSON response: ${contentType}`);
      }
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(`Server responded with error: ${data.error || response.statusText}`);
      }
      
      console.log('Received filtered shoes:', data);
      setShoes(data);
    } catch (error) {
      console.error('Error fetching filtered shoes:', error);
      setError(`Failed to load filtered shoes: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1>Shoozy - Shoe Recommender</h1>
      {error && <div className="error-message">{error}</div>}
      <div className="main-content">
        <FilterPanel onFilter={handleFilter} />
        <div className="shoes-section">
          {loading && <div className="loading-message">Loading shoes...</div>}
          {shoes.length > 0 && (
            <div className="shoes-container">
              <h2>Collections</h2>
              <div className="shoes-grid">
                {shoes.map((shoe, index) => (
                  <ProductCard key={`shoe-${shoe.Product_id}-${index}`} product={shoe} />
                ))}
              </div>
            </div>
          )}
          {shoes.length === 0 && !loading && (
            <div className="no-shoes">
              <p>No shoes found for the selected filters.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;