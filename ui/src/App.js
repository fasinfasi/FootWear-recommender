import React, { useState, useEffect } from 'react';
import './App.css';
import ProductCard from './components/ProductCard';
import FilterPanel from './components/FilterPanel';

// Use environment variable or default to localhost for development
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [shoes, setShoes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchRandomShoes();
  }, []);

  const fetchRandomShoes = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${API_BASE_URL}/random-shoes`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch shoes: ${response.status} ${response.statusText}`);
      }
      
      const data = await response.json();
      setShoes(data);
    } catch (error) {
      console.error('Error fetching random shoes:', error);
      setError(`Failed to load shoes: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleFilter = async (newFilters) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${API_BASE_URL}/filter-shoes`, {
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
      
      setShoes(data);
    } catch (error) {
      console.error('Error filtering shoes:', error);
      setError(`Failed to load filtered shoes: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleRecommendation = async (productId, filters = {}) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${API_BASE_URL}/recommend`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          product_name: productId,
          ...filters
        }),
      });

      const contentType = response.headers.get('content-type');
      
      if (!contentType || !contentType.includes('application/json')) {
        throw new Error(`Received non-JSON response: ${contentType}`);
      }
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(`Server responded with error: ${data.error || response.statusText}`);
      }
      
      setShoes(data);
    } catch (error) {
      console.error('Error getting recommendations:', error);
      setError(`Failed to load recommendations: ${error.message}`);
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
                  <ProductCard 
                    key={`shoe-${shoe.Product_id}-${index}`} 
                    product={shoe}
                    onRecommend={handleRecommendation}
                  />
                ))}
              </div>
            </div>
          )}
          {shoes.length === 0 && !loading && (
            <div className="no-shoes">
              <p>No shoes found for the selected filters.</p>
              <button onClick={fetchRandomShoes} className="retry-button">
                Load Random Shoes
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;