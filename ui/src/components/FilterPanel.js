import React, { useState } from 'react';
import './FilterPanel.css';

const FilterPanel = ({ onFilter }) => {
  const [filters, setFilters] = useState({
    brand: '',
    gender: '',
    price_range: '',
    sort_by: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onFilter(filters);
  };

  return (
    <div className="filter-panel">
      <h2>Filters</h2>
      <form onSubmit={handleSubmit}>
        <div className="filter-group">
          <label htmlFor="brand">Brand</label>
          <select
            id="brand"
            name="brand"
            value={filters.brand}
            onChange={handleChange}
          >
            <option value="">All Brands</option>
            <option value="Nike">Nike</option>
            <option value="Adidas">Adidas</option>
            <option value="Reebok">Reebok</option>
            <option value="Converse">Converse</option>
            <option value="Puma">Puma</option>
            <option value="Vans">Vans</option>
            <option value="Asics">Asics</option>
            <option value="Fila">Fila</option>
            <option value="Skechers">Skechers</option>
            <option value="New Balance">New Balance</option>
          </select>
        </div>

        <div className="filter-group">
          <label>Gender</label>
          <div className="radio-group">
            <label>
              <input
                type="radio"
                name="gender"
                value="Men"
                checked={filters.gender === 'Men'}
                onChange={handleChange}
              />
              Men
            </label>
            <label>
              <input
                type="radio"
                name="gender"
                value="Women"
                checked={filters.gender === 'Women'}
                onChange={handleChange}
              />
              Women
            </label>
            <label>
              <input
                type="radio"
                name="gender"
                value=""
                checked={filters.gender === ''}
                onChange={handleChange}
              />
              All
            </label>
          </div>
        </div>

        <div className="filter-group">
          <label htmlFor="price_range">Price Range</label>
          <select
            id="price_range"
            name="price_range"
            value={filters.price_range}
            onChange={handleChange}
          >
            <option value="">Any Price</option>
            <option value="0-50">Under $50</option>
            <option value="50-100">$50 - $100</option>
            <option value="100+">$100+</option>
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="sort_by">Sort By</label>
          <select
            id="sort_by"
            name="sort_by"
            value={filters.sort_by}
            onChange={handleChange}
          >
            <option value="rating">Rating (High to Low)</option>
            <option value="sold">Most Sold</option>
          </select>
        </div>

        <button type="submit" className="filter-button">
          Apply Filters
        </button>
      </form>
    </div>
  );
};

export default FilterPanel;