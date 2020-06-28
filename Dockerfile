FROM python:3.7-alpine

WORKDIR /usr/src/time_manager

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add git && \
    pip install --upgrade pip &&\
    pip install pipenv &&\
    apk add --virtual build-deps gcc python3-dev musl-dev &&\
    apk add postgresql-dev &&\
    pip install psycopg2 &&\
    apk del build-deps

COPY ./Pipfile /usr/src/time_manager/Pipfile
RUN pipenv install --skip-lock --system --dev
COPY ./entrypoint.sh /usr/src/time_manager/entrypoint.sh

COPY . /usr/src/time_manager

ENTRYPOINT ["/usr/src/time_manager/entrypoint.sh"]