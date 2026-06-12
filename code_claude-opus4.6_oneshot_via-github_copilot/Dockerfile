FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

RUN mkdir -p /app/backups /app/exports /app/imports

EXPOSE 5000

CMD ["python", "src/app.py"]
