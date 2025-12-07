# -p
FROM python:3.10-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for building Python packages
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    zlib-dev \
    jpeg-dev \
    mariadb-connector-c-dev \
    pkgconfig

    # Install Python dependencies
COPY requirements.txt /
RUN pip install --upgrade pip \
    && pip install -r /requirements.txt

# Copy project files
COPY . /app/
WORKDIR /app

# Expose the port
EXPOSE 8000

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
