FROM cr.xofi.io/library/python:3-slim-buster

COPY ["requirements.txt", "/app/"]
RUN apt-get update && apt-get -y install nginx libpq5 gcc libpq-dev libmagic-dev && \
    pip install --no-cache-dir -r /app/requirements.txt supervisor && \
    apt-get -y remove gcc libpq-dev && \
    apt-get -y autoremove && \
    apt-get -y autoclean && \
    rm -rf /var/lib/apt/lists/*


RUN mkdir -p /var/log/supervisor
COPY ["nginx.conf", "/etc/nginx/sites-enabled/default"]
COPY ["michalsoida", "/app/michalsoida/"]
COPY ["start.sh", "/app/"]
COPY ["supervisord.conf", "/app/"]
COPY ["cv_pl.pdf", "/app/michalsoida/static/cv/"]

EXPOSE 80
WORKDIR /app
CMD ["/bin/sh", "start.sh"]
