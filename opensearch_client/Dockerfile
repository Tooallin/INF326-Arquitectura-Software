FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir opensearch-py

CMD ["python", "opensearch_client.py"]