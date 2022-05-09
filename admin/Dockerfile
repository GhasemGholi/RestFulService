FROM python:3.6.13-slim
WORKDIR /app
COPY . .
RUN apt update -y && apt-get install -y python3-dev build-essential && \
    pip install -r requirements.txt 
EXPOSE 5001
ENV FLASK_APP=app.py

COPY . /app
RUN pip install -r requirements.txt

ENTRYPOINT [ "flask"]
CMD [ "run", "--host", "0.0.0.0" ]