FROM python:3.10.7-bullseye

RUN apt-get update && apt-get install -y curl gzip

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV ENVIRONMENT=production

ENV PORT=8000

CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "${PORT}"]