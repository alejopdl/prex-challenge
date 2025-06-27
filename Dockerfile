FROM python:3.10-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requisitos primero para mejor caché
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear directorio de datos
RUN mkdir -p data

# Exponer puerto para la API
EXPOSE 5000

# Establecer variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Ejecutar el servidor API
CMD ["python", "api_server/run_api.py", "--host", "0.0.0.0", "--port", "5000"]
