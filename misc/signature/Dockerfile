# pull official base image
FROM python:3.11-slim-buster

# envs for python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    && rm -rf /var/lib/apt/lists/*

# install python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY flag.txt /app/flag.txt
ADD src /app

EXPOSE 8000

CMD gunicorn -b 0.0.0.0:8000 app:app