FROM python:3.8-buster

COPY src/api/requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY src/api/main.py .
