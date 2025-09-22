FROM python:3.11-slim

RUN apt-get update && apt-get install -y libreoffice && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY convert.py .

EXPOSE 5000
CMD ["python", "convert.py"]
