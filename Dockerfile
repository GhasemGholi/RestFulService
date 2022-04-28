# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /core

COPY requirements.txt requirements.txt
RUN python3.9 -m pip install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
