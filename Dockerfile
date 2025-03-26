# Use a lightweight Python base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first (for better caching)
COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    libsqlite3-dev \
    build-essential \
    curl \
    apt-transport-https \
    software-properties-common && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | tee /usr/share/keyrings/microsoft.asc && \
    echo "deb [signed-by=/usr/share/keyrings/microsoft.asc] https://packages.microsoft.com/debian/12/prod bookworm main" | tee /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    apt-get install -y msodbcsql18 && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Expose the application port (but let Railway set the actual port)
EXPOSE 8000

# Command to run FastAPI
CMD /bin/sh -c "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"
