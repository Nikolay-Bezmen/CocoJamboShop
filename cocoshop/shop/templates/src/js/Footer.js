// src/components/Footer/Footer.js
import React from 'react';
import '../css/Footer.css';

function Footer() {
  return (
    <footer>
      <div className="footer-container">
        <div className="footer-left">
          <h1>COCO SHOP</h1>
        </div>
        <div className="footer-center">
          <a href="liked" className="footer-btn">Избранное</a>
          <a href="shoppingCart" className="footer-btn">Корзина</a>
          <a href="/contacts" className="footer-btn">Контакты</a>
        </div>
        <div className="footer-right">
          <button className="footer-btn">Условия сервиса</button>
          <div className="language">
            <button className="footer-btn active-lang">Рус</button>
            <button className="footer-btn">Eng</button>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
