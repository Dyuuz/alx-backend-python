# Use official Python image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project code
COPY . /app/

# Expose default Django port
EXPOSE 8000

# Default command to run the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
