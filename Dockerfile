#https://hub.docker.com/_/python?tab=tags&page=1&ordering=last_updated
#https://hub.docker.com/_/python?tab=tags&page=6&ordering=name

FROM python:3.9.5

RUN mkdir /root/cdc-backend
COPY app /root/cdc-backend/app/
COPY configs /root/cdc-backend/configs/
COPY secrets /root/cdc-backend/secrets/
COPY scripts /root/cdc-backend/scripts/

COPY requirements.txt /root/cdc-backend/requirements.txt
COPY Makefile /root/cdc-backend/Makefile

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 nginx -y

WORKDIR /root/cdc-backend
RUN make docker_install
RUN cp /root/cdc-backend/configs/nginx-docker.conf /usr/share/nginx/nginx.conf


WORKDIR /root/cdc-backend/app
CMD nginx -c nginx.conf && PYTHONPATH=. CONFIG_PATH=../secrets/dev-ec2-config.yaml python __main__.py


# docker run --rm -p 443:443 -it $(docker build -q .)