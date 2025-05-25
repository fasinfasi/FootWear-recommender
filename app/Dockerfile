# app/Dockerfile

FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY app/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY app/ /app/

# Create model directory for volume mount
RUN mkdir -p /app/model

EXPOSE 5000

CMD ["python", "app.py"]