# Use lightweight Python image
FROM python:3.11-slim

# Install LibreOffice headless
RUN apt-get update && \
    apt-get install -y libreoffice && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Flask app
COPY convert.py .

# Expose port (Render provides PORT environment variable)
EXPOSE 5000

# Start Flask app
CMD ["python", "convert.py"]
