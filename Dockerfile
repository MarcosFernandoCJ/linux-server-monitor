FROM python:3.11-slim

# Directorio de trabajo dentro del container Linux
WORKDIR /app

# Copiar dependencias primero (caching de capas)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Puerto que expone Flask
EXPOSE 5000

# Comando de inicio
CMD ["python", "app.py"]