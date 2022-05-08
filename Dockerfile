# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

RUN mkdir /code
WORKDIR /code
RUN apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        python3-setuptools \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt requirements.txt
RUN python3.9 -m pip install -r requirements.txt

COPY . /code/
RUN chmod +x -R /code/

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
