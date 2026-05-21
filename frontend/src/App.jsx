// Importa hooks de React:
// useState para guardar datos dinámicos
// useEffect para ejecutar código al cargar el componente
import { useEffect, useState } from "react";

// Importa el componente del formulario donde el usuario introduce los partidos
import QuinielaForm from "./components/QuinielaForm";

// Importa el componente que muestra los resultados de la predicción
import ResultsList from "./components/ResultsList";

// Importa las funciones del servicio API:
// predictQuiniela envía los partidos al backend
// getTeams obtiene la lista de equipos desde el backend
import { predictQuiniela, getTeams } from "./services/api";


//“Es el componente principal. Se encarga de cargar los equipos,
//  enviar la quiniela al backend y mostrar los resultados.”
// Componente principal de la aplicación
function App() {
  // Guarda los resultados devueltos por el backend
  const [resultados, setResultados] = useState([]);

  // Guarda la lista de equipos para rellenar los desplegables
  const [equipos, setEquipos] = useState([]);

  // Controla si se está haciendo una predicción
  const [loading, setLoading] = useState(false);

  // Controla si todavía se están cargando los equipos al iniciar la app
  const [loadingTeams, setLoadingTeams] = useState(true);

  // Guarda mensajes de error si algo falla
  const [error, setError] = useState("");

  // Este efecto se ejecuta una sola vez al cargar la aplicación
  useEffect(() => {
    // Función asíncrona para pedir al backend la lista de equipos
    async function loadTeams() {
      try {
        // Llama al endpoint de equipos
        const data = await getTeams();

        // Guarda en el estado la lista recibida
        setEquipos(data.equipos);
      } catch (err) {
        // Si falla, muestra un mensaje de error
        setError("No se pudo cargar la lista de equipos.");
      } finally {
        // Tanto si funciona como si falla, deja de mostrar "cargando equipos"
        setLoadingTeams(false);
      }
    }

    // Ejecuta la carga inicial de equipos
    loadTeams();
  }, []);

  // Función que se ejecuta cuando el usuario envía la quiniela
  const handlePredict = async (partidos) => {
    try {
      // Activa el estado de carga mientras se analiza la quiniela
      setLoading(true);

      // Limpia errores anteriores
      setError("");

      // Envía los partidos al backend y espera la respuesta
      const data = await predictQuiniela(partidos);

      // Guarda los resultados devueltos por el backend
      setResultados(data.resultado);
    } catch (err) {
      // Si falla la petición, muestra un mensaje de error
      setError("No se pudo analizar la quiniela. Comprueba que el backend esté funcionando.");

      // Limpia los resultados por seguridad
      setResultados([]);
    } finally {
      // Al terminar, quita el estado de carga
      setLoading(false);
    }
  };

  // Parte visual del componente
  return (
    <div className="app-container">
      {/* Título principal de la aplicación */}
      <h1>Aquinielator</h1>

      {/* Subtítulo explicativo */}
      <p className="subtitle">
        Recomendador de quinielas con FastAPI, React y Ollama
      </p>

      {/* 
        Si los equipos todavía se están cargando, muestra un mensaje.
        Si ya se cargaron, muestra el formulario.
      */}
      {loadingTeams ? (
        <p>Cargando equipos...</p>
      ) : (
        <QuinielaForm
          // Función que se ejecutará al enviar el formulario
          onSubmit={handlePredict}

          // Estado de carga para desactivar el botón mientras se analiza
          loading={loading}

          // Lista de equipos para rellenar los desplegables
          equipos={equipos}
        />
      )}

      {/* Si existe un error, lo muestra en pantalla */}
      {error && <p className="error-message">{error}</p>}

      {/* Muestra la lista de resultados */}
      <ResultsList resultados={resultados} />
    </div>
  );
}

// Exporta el componente para poder usarlo en main.jsx
export default App;