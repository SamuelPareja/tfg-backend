"""
Archivo de configuración general del backend.

Aquí se centralizan las variables importantes de la aplicación:
nombre del proyecto, URLs permitidas por CORS, claves secretas,
datos de conexión a base de datos, etc.
"""

import os
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()


class Settings:
    """
    Clase de configuración principal.

    Lee las variables de entorno para evitar escribir claves,
    contraseñas o configuraciones sensibles directamente en el código.
    """

    PROJECT_NAME: str = "Aquinielator API"
    PROJECT_VERSION: str = "1.0.0"

    # URL del frontend en desarrollo
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    # Clave de Groq para las explicaciones con IA
    GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")

    # Configuración de seguridad JWT.
    # Más adelante la usaremos para login/register.
    SECRET_KEY: str = os.getenv("SECRET_KEY", "cambia_esta_clave_en_produccion")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )

    # Datos de conexión a MySQL.
    # Los usaremos en la fase de base de datos.
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT: str = os.getenv("MYSQL_PORT", "3306")
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "aquinielator_db")

    @property
    def DATABASE_URL(self) -> str:
        """
        Construye la URL de conexión para SQLAlchemy usando MySQL.
        """
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:"
            f"{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:"
            f"{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
        )


settings = Settings()