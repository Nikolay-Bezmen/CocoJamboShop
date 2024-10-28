// src/components/Liked.js
import React from 'react';
import '../css/ProductGrid.css'; // Импортируем стили для Liked
import productImage4 from '../img/Image (1).png';
import productImage5 from '../img/Image (2).png';
import productImage6 from '../img/Image (3).png';
import productImage7 from '../img/Image (4).png';
import productImage8 from '../img/Image (5).png';
import productImage9 from '../img/Image (6).png';

function Liked() {
  return (
    <div className="container1">
      <h2>Избранное</h2>

      <h2>Наушники</h2>
      <div className="product-grid">
        
          <div className="product-card">
            <img src={productImage4} alt="Apple BYZ S852I" />
            <p>Apple BYZ S852I</p>
            <div className="product-info">
              <span className="rating">4.7</span>
              <span className="price sale">
                52$ <span className="old-price">60$</span>
              </span>
            </div>
          </div>
        
          <div className="product-card">
            <img src={productImage5} alt="Apple EarPods" />
            <p>Apple EarPods</p>
            <div className="product-info">
              <span className="rating">4.5</span>
              <span className="price">50$</span>
            </div>
          </div>
      </div>

      <h2>Беспроводные наушники</h2>
      <div className="product-grid">
        
          <div className="product-card">
            <img src={productImage9} alt="Apple BYZ S852I" />
            <p>Apple BYZ S852I</p>
            <div className="product-info">
              <span className="rating">4.7</span>
              <span className="price sale">
                52$ <span className="old-price">60$</span>
              </span>
            </div>
          </div>
        
        
          <div className="product-card">
            <img src={productImage7} alt="Apple EarPods" />
            <p>Apple EarPods</p>
            <div className="product-info">
              <span className="rating">4.5</span>
              <span className="price">50$</span>
            </div>
          </div>
        
        
          <div className="product-card">
            <img src={productImage8} alt="Apple EarPods Box" />
            <p>Apple EarPods</p>
            <div className="product-info">
              <span className="rating">4.5</span>
              <span className="price">30$</span>
            </div>
          </div>
      
      </div>
    </div>
  );
}

export default Liked;
