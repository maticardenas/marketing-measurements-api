FROM python:3.11-slim-bullseye

LABEL maintainer "Matías Cárdenas"

RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean \
&& apt-get install bash \
&& apt-get install vim -y \
&& apt-get -y install libpq-dev gcc \
&& apt-get -y install procps \
&& apt-get install postgresql -y

RUN pip install poetry==1.8.2

WORKDIR /usr/objective_platform/

COPY ./ ./

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN poetry install
