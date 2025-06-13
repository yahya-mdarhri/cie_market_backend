# Use a specific Python image version
FROM python:3.12-slim

# Set environment variables to avoid .pyc files and enable stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean


COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt


COPY . .

# Expose the port your Django app runs on
EXPOSE 8000

# Run Django's development server (change to gunicorn in production)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
