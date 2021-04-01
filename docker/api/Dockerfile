FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY docker/api/prestart.sh prestart.sh

COPY docker/api/uwsgi/uwsgi.ini uwsgi.ini

COPY docker/api/nginx/nginx.conf nginx.conf

COPY docker/api/nginx/nginx-d.conf /etc/nginx/conf.d/nginx.conf

COPY src/api/main.py .

COPY src/api/requirements.txt requirements.txt

RUN pip install -r requirements.txt
