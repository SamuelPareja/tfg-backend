# “Este Dockerfile crea la imagen del backend. Instala Python, las dependencias del proyecto 
# y ejecuta FastAPI con uvicorn en el puerto 8000.”

# Usa una imagen oficial ligera de Python versión 3.11
FROM python:3.11-slim

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias del backend
COPY requirements.txt .

# Instala las librerías necesarias (FastAPI, uvicorn, etc.)
# --no-cache-dir evita guardar caché y hace la imagen más ligera
RUN pip install --no-cache-dir -r requirements.txt

# Copia la carpeta app (donde está todo el código del backend)
COPY app ./app

# Expone el puerto 8000 (donde corre FastAPI)
EXPOSE 8000

# Comando que arranca el servidor FastAPI con uvicorn
# --host 0.0.0.0 permite que sea accesible desde fuera del contenedor
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]