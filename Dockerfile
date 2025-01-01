FROM python:3.13-slim

WORKDIR /app

ARG PORT=80

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=$PORT

ENV FLASK_APP=src/app.py

ENV FLASK_RUN_PORT=$PORT

ENV PYTHONPATH=/app

EXPOSE $PORT

RUN echo $PORT

CMD ["flask", "run", "--host=0.0.0.0", "--no-reload"]