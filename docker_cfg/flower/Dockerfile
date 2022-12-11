FROM python:3.7-alpine

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

ARG FLOWER_BASIC_AUTH
ADD backend /
ADD config.yml /cfg/config.yml
RUN pip install -r requirements.txt
RUN pip install psycopg2

CMD celery flower -A background_tasks --basic_auth="${FLOWER_BASIC_AUTH}" --url-prefix=flower --host=0.0.0.0 --port=5555