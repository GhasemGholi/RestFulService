# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

RUN mkdir /code
WORKDIR /code
RUN apt-get update && rm -rf /var/lib/apt/lists/*
COPY requirements.txt requirements.txt
RUN python3.9 -m pip install -r requirements.txt

COPY . /code/
RUN chmod +x -R /code/

ENTRYPOINT [ "python" ]

CMD ["main.py" ]