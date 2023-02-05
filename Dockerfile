# syntax=docker/dockerfile:1

FROM python:alpine3.14
WORKDIR /app
COPY requirements.txt requirements.txt

ENV SERVER_PATH=""
ENV COPY_PATH=""
ENV MAX_COPY_SIZE="100" 
ENV MAX_COPY_FILES="100"
ENV TOKEN=""

RUN python3 -m pip install -r requirements.txt --no-cache-dir 

COPY . .

CMD [ "python3","-u", "main.py"]