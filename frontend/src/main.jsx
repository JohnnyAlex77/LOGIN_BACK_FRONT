import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';
// Busca el elemento con id 'root' en el HTML y monta la aplicación React ahí
ReactDOM.createRoot(document.getElementById('root')).render(
  /* 
    StrictMode es un helper de React para desarrollo:
    - No renderiza nada visible
    - Ayuda a detectar problemas potenciales (componentes con efectos secundarios, 
      métodos deprecados, etc.)
    - Solo funciona en desarrollo, en producción no hace nada
  */
  <React.StrictMode>
    <App />
  </React.StrictMode>
);