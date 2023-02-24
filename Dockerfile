FROM python:3.8
WORKDIR /home/flask-template
# WORKDIR /src
COPY src/requirements.txt /home/flask-template
RUN pip install -r requirements.txt
COPY src /home/flask-template