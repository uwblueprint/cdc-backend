#https://hub.docker.com/_/python?tab=tags&page=1&ordering=last_updated
#https://hub.docker.com/_/python?tab=tags&page=6&ordering=name

FROM python:3.9.5

RUN mkdir /root/cdc-backend
#CMD mkdir /root/cdc-backend/app
#CMD mkdir /root/cdc-backend/configs
#WORKDIR /usr/src/app
COPY app /root/cdc-backend/app/
COPY configs /root/cdc-backend/configs/
COPY secrets /root/cdc-backend/secrets/

COPY requirements.txt /root/cdc-backend/requirements.txt

WORKDIR /root/cdc-backend/app

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install -r ../requirements.txt

#EXPOSE 8888

CMD PYTHONPATH=. CONFIG_PATH=../configs/dev-config.yaml python __main__.py

#CMD tail -f /dev/null


# docker run --rm -p 8888:8888 -it $(docker build -q .)