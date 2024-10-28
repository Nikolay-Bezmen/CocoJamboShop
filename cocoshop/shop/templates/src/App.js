// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './js/Header'; // Импортируем Header
import Footer from './js/Footer'; // Импортируем Footer
import Home from './js/MainPage'; // Ваши страницы
import Liked from './js/Liked'; // Импортируйте Liked
import ShoppingCart from './js/ShoppingCart'; // Другие страницы
//import './App.css'; // Глобальные стили

function App() {
  return (
    <Router>
      <Header />
      <Routes>  
        <Route path="/" element={<Home />} />
        <Route path="/liked" element={<Liked />} />
        <Route path="/ShoppingCart" element={<ShoppingCart />} />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App;
