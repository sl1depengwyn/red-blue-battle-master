FROM python:3.7-alpine

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

ADD backend /
ADD config.yml /cfg/config.yml
RUN pip install -r requirements.txt
RUN pip install psycopg2

CMD ["celery", "beat", "-A", "background_tasks"]