#!/bin/bash
# Install ODBC Driver
apt-get update && apt-get install -y unixodbc unixodbc-dev odbcinst libsqliteodbc
# Start FastAPI Server
uvicorn main:app --host 0.0.0.0 --port $PORT
