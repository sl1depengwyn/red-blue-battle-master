FROM python:3.7-alpine

ADD backend/requirements.txt /requirements.txt
RUN pip install -r requirements.txt

ADD manage.py /manage.py
ADD config.yml /config.yml
ADD docker_cfg/ /docker_cfg/

CMD [ "python", "./manage.py", "setup" ]