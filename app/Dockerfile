# pull official base image
FROM ubuntu:latest

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DEBIAN_FRONTEND=noninteractive

# install apt-get dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      apt-utils \
      bash \
      python3.8 \
      python3-pip \
      python3-setuptools \
      python3-dev \
      python-is-python3 \
      netcat-openbsd

# install psycopg2 dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql \
    gcc \
    musl

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

