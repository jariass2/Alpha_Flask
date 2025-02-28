FROM python:3.9-slim-buster

WORKDIR /app

# Actualiza la lista de paquetes e instala dependencias del sistema necesarias para mdbtools
RUN apt-get update && apt-get install -y --no-install-recommends \
    mdbtools \
    libmdbodbc \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]