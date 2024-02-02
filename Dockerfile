FROM python:3-bookworm
RUN apt-get update; apt-get -y install openjdk-17-jre-headless

COPY requirements.txt /app/requirements.txt
WORKDIR /app/
RUN pip3 install -r requirements.txt

COPY * /app/
CMD python3 main.py
