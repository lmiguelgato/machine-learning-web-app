FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY api/prestart.sh prestart.sh

COPY api/uwsgi/uwsgi.ini uwsgi.ini

COPY api/nginx/nginx.conf nginx.conf

COPY api/nginx/nginx-d.conf /etc/nginx/conf.d/nginx.conf

COPY main.py .

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
