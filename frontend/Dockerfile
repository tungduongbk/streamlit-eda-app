FROM python:3.10-slim-buster

WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN apt-get -y update && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./src/ .
CMD [ "python", "main.py"]
