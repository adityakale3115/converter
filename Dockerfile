# Use lightweight Python image
FROM python:3.11-slim

# Install LibreOffice headless
RUN apt-get update && \
    apt-get install -y libreoffice && \
    apt-get clean

# Copy app
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

COPY app.py /app/app.py

EXPOSE 5000
CMD ["python", "app.py"]
