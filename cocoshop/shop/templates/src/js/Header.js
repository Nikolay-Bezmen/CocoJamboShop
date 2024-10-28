// src/components/Header/Header.js
import React from 'react';
import '../css/Header.css';

function Header() {
  return (
    <header className="header">
      <div className="logo">
        <h1>COCO SHOP</h1>
      </div>
      <div className="custom-select">
        <i className="phone-icon">&#128241;</i>
        <select>
          <option value="">Выбрать модель телефона</option>
          <option value="1">Samsung</option>
          <option value="2">Poco</option>
          <option value="3">Lenovo</option>
        </select>
      </div>
      <div className="icons">
        <a href="liked" className="icon wishlist">
          <i className="heart-icon">&#9829;</i>
          <span className="badge">2</span>
        </a>
        <a href="shoppingCart" className="icon cart">
          <i className="cart-icon">&#128722;</i>
          <span className="badge">1</span>
        </a>
      </div>
    </header>
  );
}

export default Header;
