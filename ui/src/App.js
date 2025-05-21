import React, { useState, useEffect } from 'react';
import './App.css';
import ProductCard from './components/ProductCard';
import FilterPanel from './components/FilterPanel';

function App() {
  const [productIds, setProductIds] = useState([]);
  const [selectedId, setSelectedId] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({ brand: '', gender: '', price_range: '', sort_by: 'rating' });

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        console.log('Fetching products...');
        const response = await fetch('http://localhost:5000/products');
        
        if (!response.ok) {
          throw new Error(`Failed to fetch products: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('Products fetched successfully:', data.length);
        setProductIds([...new Set(data)]);
      } catch (error) {
        console.error('Error fetching products:', error);
        setError(`Failed to load products: ${error.message}`);
      }
    };
    
    fetchProducts();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedId) {
      setError('Please select a product first');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      console.log('Sending request with data:', { product_name: selectedId, ...filters });
      
      const response = await fetch('http://localhost:5000/recommend', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ product_name: selectedId, ...filters }),
      });

      const contentType = response.headers.get('content-type');
      
      if (!contentType || !contentType.includes('application/json')) {
        throw new Error(`Received non-JSON response: ${contentType}`);
      }
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(`Server responded with error: ${data.error || response.statusText}`);
      }
      
      console.log('Received recommendations:', data);
      setRecommendations(data);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      setError(`Failed to load recommendations: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleFilter = (newFilters) => {
    console.log('Filters updated:', newFilters);
    setFilters(newFilters);
  };

  return (
    <div className="app-container">
      <h1>Shoe Recommender</h1>
      {error && <div className="error-message">{error}</div>}
      <div className="main-content">
        <FilterPanel onFilter={handleFilter} />
        <div className="recommender-section">
          <form onSubmit={handleSubmit} className="form-container">
            <div className="select-container">
              <label htmlFor="product_id">Select Product ID:</label>
              <select 
                id="product_id" 
                value={selectedId} 
                onChange={(e) => setSelectedId(e.target.value)} 
                required
              >
                <option value="">Select a product</option>
                {productIds.map((id) => (
                  <option key={`product-${id}`} value={id}>{id}</option>
                ))}
              </select>
            </div>
            <button type="submit" disabled={loading}>
              {loading ? 'Loading...' : 'Get Recommendations'}
            </button>
          </form>
          {recommendations.length > 0 && (
            <div className="recommendations-container">
              <h2>Recommended Shoes</h2>
              <div className="recommendations-grid">
                {recommendations.map((shoe, index) => (
                  <ProductCard key={`shoe-${shoe.Product_id}-${index}`} product={shoe} />
                ))}
              </div>
            </div>
          )}
          {recommendations.length === 0 && !loading && selectedId && (
            <div className="no-recommendations">
              <p>No recommendations found for the selected filters.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;