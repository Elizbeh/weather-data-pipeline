FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/ ./scripts/
COPY sql/ ./sql/

RUN mkdir -p data/raw data/processed logs

CMD ["sh", "-c", "python scripts/extract_weather.py && python scripts/transform_weather.py && python scripts/load_weather.py && python scripts/query_weather.py"]