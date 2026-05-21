function ResultsList({ resultados }) {
  if (!resultados || resultados.length === 0) {
    return null;
  }

  return (
    <div className="results-container">
      <h2>Resultados recomendados</h2>

      {resultados.map((resultado, index) => (
        <div className="result-card" key={index}>
          <h3>
            {resultado.local} vs {resultado.visitante}
          </h3>

          <p>
            <strong>Recomendación:</strong> {resultado.recomendacion}
          </p>

          {resultado.probabilidades && (
            <div>
              <p>
                <strong>Probabilidad 1:</strong> {(resultado.probabilidades["1"] * 100).toFixed(2)}%
              </p>
              <p>
                <strong>Probabilidad X:</strong> {(resultado.probabilidades["X"] * 100).toFixed(2)}%
              </p>
              <p>
                <strong>Probabilidad 2:</strong> {(resultado.probabilidades["2"] * 100).toFixed(2)}%
              </p>
            </div>
          )}

          <p>
            <strong>Explicación:</strong> {resultado.explicacion}
          </p>
        </div>
      ))}
    </div>
  );
}

export default ResultsList;