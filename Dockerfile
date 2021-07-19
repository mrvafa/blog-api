FROM python:3

MAINTAINER mrvafa

RUN apt-get update
RUN apt-get install apache2 apache2-dev libapache2-mod-wsgi-py3 libpq-dev binutils libproj-dev gdal-bin -y
RUN pip install mod_wsgi
RUN pip install ptvsd

RUN mkdir /srv/media static logs

VOLUME ["/srv/media/", "/srv/logs/"]

COPY requirements.txt /srv
RUN pip install -r /srv/requirements.txt

COPY . /srv


EXPOSE 8000

WORKDIR /srv

COPY ./docker-entrypoint.sh /
RUN ["chmod", "+x", "/docker-entrypoint.sh"]
ENTRYPOINT ["/docker-entrypoint.sh"]
