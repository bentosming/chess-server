# Dockerfile

# pull the official docker image
FROM python:3.7

# set work directory
WORKDIR /chess-server

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:."
# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .