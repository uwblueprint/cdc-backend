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
RUN apt-get install ffmpeg libsm6 libxext6 nginx certbot python3-certbot-nginx cron -y

WORKDIR /root/cdc-backend
RUN make docker_install
RUN cp /root/cdc-backend/configs/nginx-docker.conf /etc/nginx/nginx.conf
# run certbot renew every day
RUN echo '0 12 * * * /usr/bin/certbot renew --quiet' | crontab -

WORKDIR /root/cdc-backend/app
CMD cron && nginx && PYTHONPATH=. CONFIG_PATH=../secrets/dev-ec2-config.yaml python __main__.py


# To run docker build and run locally:
# docker run --rm -p 443:443 -it $(docker build -q .)

# Once docker is running, to verify and set up certificates:
# docker exec -it <CONTAINER_ID> /bin/sh
# certbot --nginx -d interactive.calgaryconnecteen.com -d www.interactive.calgaryconnecteen.com --agree-tos -m dcc.bp.aws@gmail.com

#PYTHONPATH=. CONFIG_PATH=secrets/dev-ec2-config.yaml python