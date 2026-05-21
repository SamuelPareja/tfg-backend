// URL base del backend.
// Todas las peticiones del frontend saldrán de aquí.
const API_URL = "http://127.0.0.1:8000/api";

// “Este archivo centraliza las llamadas al backend. Tiene una función
//  para enviar la quiniela y otra para obtener la lista de equipos.”

// Función que envía la quiniela al backend para obtener la predicción
export async function predictQuiniela(partidos, mode = "classic") {
  const response = await fetch(`${API_URL}/predict?mode=${mode}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ partidos }),
  });

  if (!response.ok) {
    throw new Error("Error al obtener la predicción");
  }

  return await response.json();
}

// Función que obtiene la lista de equipos disponibles desde el backend
export async function getTeams() {
  // Hace una petición HTTP GET al endpoint /teams
  const response = await fetch(`${API_URL}/teams`);

  // Si la respuesta no es correcta, lanza un error
  if (!response.ok) {
    throw new Error("Error al obtener la lista de equipos");
  }

  // Devuelve la respuesta convertida de JSON a objeto JavaScript
  return await response.json();
}