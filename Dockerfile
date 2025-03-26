# Use Python 3.9
FROM python:3.9-slim

# Install ODBC & SQL Server dependencies
RUN apt-get update && \
    apt-get install -y g++ unixodbc-dev unixodbc freetds-dev freetds-bin tdsodbc && \
    apt-get clean

# Install Microsoft ODBC Driver 17 for SQL Server
RUN apt-get install -y curl && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Run FastAPI on port 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]