// Importa el hook useState para guardar el estado local del formulario
import { useState } from "react";

// “Este componente gestiona el formulario de entrada. Permite añadir y eliminar partidos, 
// seleccionar equipos desde desplegables y validar que no se repita el mismo equipo como local
//  y visitante.”


// Componente que recibe:
// onSubmit -> función que se ejecuta al enviar la quiniela
// loading -> indica si se está analizando la quiniela
// equipos -> lista de equipos para rellenar los desplegables
function QuinielaForm({ onSubmit, loading, equipos }) {
  // Estado local que guarda los partidos introducidos en el formulario.
  // Empieza con una fila vacía.
  const [partidos, setPartidos] = useState([{ local: "", visitante: "" }]);

  // Función que actualiza un campo concreto de un partido concreto.
  // index -> posición del partido en el array
  // field -> "local" o "visitante"
  // value -> nuevo valor seleccionado
  const handleChange = (index, field, value) => {
    // Copia del array para no modificar el estado directamente
    const nuevosPartidos = [...partidos];

    // Cambia solo el campo indicado del partido indicado
    nuevosPartidos[index][field] = value;

    // Actualiza el estado con la nueva copia
    setPartidos(nuevosPartidos);
  };

  // Añade una nueva fila vacía al formulario
  const addPartido = () => {
    setPartidos([...partidos, { local: "", visitante: "" }]);
  };

  // Elimina una fila concreta usando su índice
  const removePartido = (index) => {
    // filter crea un nuevo array quitando el partido del índice indicado
    const nuevosPartidos = partidos.filter((_, i) => i !== index);
    setPartidos(nuevosPartidos);
  };

  // Función que se ejecuta al enviar el formulario
  const handleSubmit = (e) => {
    // Evita que el formulario recargue la página
    e.preventDefault();

    // Filtra solo los partidos válidos:
    // - local no vacío
    // - visitante no vacío
    // - local y visitante no pueden ser el mismo equipo
    const partidosValidos = partidos.filter(
      (partido) =>
        partido.local.trim() !== "" &&
        partido.visitante.trim() !== "" &&
        partido.local !== partido.visitante
    );

    // Envía los partidos válidos al componente padre
    onSubmit(partidosValidos);
  };

  // Parte visual del formulario
  return (
    <form className="quiniela-form" onSubmit={handleSubmit}>
      {/* Título del formulario */}
      <h2>Introduce tu quiniela</h2>

      {/* 
        Recorre el array de partidos y dibuja una fila por cada uno.
        Cada fila tiene dos selects y, si hay más de un partido, botón de eliminar.
      */}
      {partidos.map((partido, index) => {
        // Lista de equipos disponibles para el desplegable local.
        // Excluye el equipo ya seleccionado como visitante en esa misma fila.
        const equiposLocal = equipos.filter(
          (equipo) => equipo !== partido.visitante
        );

        // Lista de equipos disponibles para el desplegable visitante.
        // Excluye el equipo ya seleccionado como local en esa misma fila.
        const equiposVisitante = equipos.filter(
          (equipo) => equipo !== partido.local
        );

        return (
          <div className="partido-row" key={index}>
            {/* Select del equipo local */}
            <select
              value={partido.local}
              onChange={(e) => handleChange(index, "local", e.target.value)}
            >
              <option value="">Selecciona equipo local</option>

              {/* Crea una opción por cada equipo permitido */}
              {equiposLocal.map((equipo) => (
                <option key={`local-${index}-${equipo}`} value={equipo}>
                  {equipo}
                </option>
              ))}
            </select>

            {/* Select del equipo visitante */}
            <select
              value={partido.visitante}
              onChange={(e) => handleChange(index, "visitante", e.target.value)}
            >
              <option value="">Selecciona equipo visitante</option>

              {/* Crea una opción por cada equipo permitido */}
              {equiposVisitante.map((equipo) => (
                <option key={`visitante-${index}-${equipo}`} value={equipo}>
                  {equipo}
                </option>
              ))}
            </select>

            {/* 
              Solo muestra el botón eliminar si hay más de un partido.
              Así siempre queda al menos una fila visible.
            */}
            {partidos.length > 1 && (
              <button
                type="button"
                className="btn-delete"
                onClick={() => removePartido(index)}
              >
                Eliminar
              </button>
            )}
          </div>
        );
      })}

      {/* Zona de botones de acción */}
      <div className="buttons-row">
        {/* Botón para añadir una nueva fila */}
        <button type="button" onClick={addPartido}>
          Añadir partido
        </button>

        {/* Botón para enviar la quiniela */}
        <button type="submit" disabled={loading}>
          {/* Si está cargando, cambia el texto del botón */}
          {loading ? "Analizando..." : "Analizar quiniela"}
        </button>
      </div>
    </form>
  );
}

// Exporta el componente para usarlo en App.jsx
export default QuinielaForm;