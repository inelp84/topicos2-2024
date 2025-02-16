# Usar una imagen base con soporte para TensorFlow
FROM python:3.10

# Establecer directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY . .

# Instalar las dependencias
RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r requirements.txt

# Exponer el puerto de la API
EXPOSE 8010

# Ejecutar el servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8010", "--reload"]
