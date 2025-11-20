FROM python:3.13.5-alpine3.22

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENTRYPOINT ["pytest", "-v", "tests/routers/test_channels.py"]