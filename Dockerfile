# Usar una imagen oficial de Python
FROM python:3.10

# Configurar el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos necesarios al contenedor
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del backend al contenedor
COPY . .

# Exponer el puerto en el que se ejecutará FastAPI
EXPOSE 8000

# Comando para ejecutar el servidor de FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
