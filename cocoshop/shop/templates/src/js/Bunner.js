// src/components/Banner/Banner.js
import React from 'react';
import '../css/Banner.css';
import iphoneImage from '../img/iphone.png'; // добавьте путь к изображению

function Banner() {
  return (
    <div className="banner">
      <div className="text-container">
        <h1>Аксессуары для iPhone 13 Pro Max</h1>
      </div>
      <div className="image-container">
        <img src={iphoneImage} alt="iPhone 13 Pro Max" />
      </div>
    </div>
  );
}

export default Banner;
