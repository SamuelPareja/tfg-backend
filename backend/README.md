# Aquinielator Backend

Backend desarrollado con **FastAPI** para el proyecto final de DAW.

La aplicación permite generar predicciones de quinielas de fútbol, registrar usuarios, iniciar sesión con JWT, guardar historial de predicciones y marcar predicciones como favoritas.

## Tecnologías utilizadas

- Python
- FastAPI
- MySQL
- SQLAlchemy
- JWT
- Passlib + bcrypt
- Scikit-learn
- Pandas
- Groq API
- Docker

## Funcionalidades principales

- Registro de usuarios.
- Login con JWT.
- Contraseñas cifradas.
- Roles de usuario.
- Consulta de equipos desde MySQL.
- Generación de predicciones de quiniela.
- Historial de predicciones por usuario.
- Detalle de predicciones guardadas.
- Eliminación de predicciones.
- Sistema de favoritos.
- Auditoría automática mediante triggers de MySQL.
- Documentación automática con Swagger.

## Estructura del proyecto

```txt
backend/
├── app/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── repositories/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── data/
│   └── main.py
├── requirements.txt
├── Dockerfile
└── README.md