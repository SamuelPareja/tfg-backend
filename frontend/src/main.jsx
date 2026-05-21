// Importa React para poder usar JSX y componentes
import React from "react";

// Importa la librería que conecta React con el DOM del navegador
import ReactDOM from "react-dom/client";

// Importa el componente principal de la aplicación
import App from "./App";

// Importa los estilos globales de la aplicación
import "./index.css";

//“Es el punto de entrada de React. Carga el componente principal App dentro 
// del elemento root del HTML.”
// Busca en el HTML el elemento con id "root" y crea ahí la aplicación React
ReactDOM.createRoot(document.getElementById("root")).render(
  // StrictMode ayuda en desarrollo a detectar posibles problemas en la aplicación
  <React.StrictMode>
    {/* Renderiza el componente principal App */}
    <App />
  </React.StrictMode>
);