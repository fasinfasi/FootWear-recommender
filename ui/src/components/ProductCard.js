import React from 'react';
import { FaStar } from 'react-icons/fa';
import './ProductCard.css';

const ProductCard = ({ product }) => {
  const {
    Brand,
    Type,
    Gender,
    review_rating,
    'Price(USD)': price,
    url: image_url
  } = product;

  // Format rating to handle null/undefined values
  const formattedRating = review_rating ? review_rating.toFixed(1) : 'N/A';
  
  // Format price to handle null/undefined values
  const formattedPrice = price ? `$${price}` : 'Price not available';

  return (
    <div className="product-card">
      <div className="product-image">
        <img 
          src={image_url || 'https://placehold.co/200x200?text=No+Image'} 
          alt={`${Brand || 'Unknown'} ${Type || 'Shoe'}`} 
          onError={(e) => {
            e.target.onerror = null;
            e.target.src = 'https://placehold.co/200x200?text=No+Image';
          }}
        />
      </div>
      <div className="product-info">
        <div className="product-details-container">
          <div className="product-left-details">
            <h3 className="product-brand">{Brand || 'Unknown Brand'}</h3>
            <p className="product-type">{Type || 'Unknown Type'}</p>
            <p className="product-gender">{Gender || 'Unisex'}</p>
          </div>
          
          <div className="product-right-details">
            <div className="product-rating">
              <FaStar className="star-icon" />
              <span>{formattedRating}</span>
            </div>
            
            <div className="product-price">
              {formattedPrice}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;