# “Este Dockerfile crea la imagen del frontend. Parte de Node, instala dependencias, copia 
# el proyecto y ejecuta Vite dentro del contenedor para servir la aplicación.”

# Usa una imagen oficial ligera de Node.js versión 20 basada en Alpine Linux
FROM node:20-alpine

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de dependencias del frontend
COPY package*.json ./

# Instala las dependencias del proyecto
RUN npm install

# Copia el resto de archivos del frontend al contenedor
COPY . .

# Expone el puerto 5173, que es el que usa Vite en desarrollo
EXPOSE 5173

# Comando que arranca el servidor de desarrollo de Vite
# --host 0.0.0.0 permite que sea accesible desde fuera del contenedor
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]