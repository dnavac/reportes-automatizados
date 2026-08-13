FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema requeridas por matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt-get/lists/*

# Copiar instalar librerías de python
COPY scripts/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto completo
COPY . .

# Crear carpeta para PDFs generados
RUN mkdir -p examples

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
