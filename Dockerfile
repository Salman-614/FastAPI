# Use a lightweight Python base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first (for better caching)
COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    libsqlite3-dev \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Make start.sh executable (if you need it)
RUN chmod +x start.sh

# Expose the application port
EXPOSE 8000

# Command to run your FastAPI app
CMD ["sh", "./start.sh"]
