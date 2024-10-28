// src/ShoppingCart.js
import React from 'react';
import '../css/cart.css'; // Импортируйте стили для корзины
import { Link } from 'react-router-dom'; // Импортируйте Link для навигации

const ShoppingCart = () => {
  return (
    <div className="shopping-cart">
      <main className="cart-empty">
        <img src="../img/Иллюстрация.png" alt="Пустая корзина" className="cart-image" />
        <h2>Корзина пуста</h2>
        <p>Но это никогда не поздно исправить :)</p>
        <Link to="/" className="btn">В каталог товаров</Link>
      </main>

      {/* Футер */}
      
    </div>
  );
};

export default ShoppingCart;
