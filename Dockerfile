# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install curl
RUN apt-get update && apt-get install -y curl

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python app files
COPY . .

# Expose the app port
EXPOSE 5000

# Install Gunicorn
RUN pip install gunicorn

# Run the Python app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "app:app"]
