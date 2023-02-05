# syntax=docker/dockerfile:1

FROM python:alpine3.14
WORKDIR /app
COPY requirements.txt requirements.txt


RUN python3 -m pip install -r requirements.txt --no-cache-dir 

COPY . .

CMD [ "python3","-u", "main.py"]