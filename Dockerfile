FROM python:3.9

ENV C_FORCE_ROOT=True

WORKDIR /home/www/app

EXPOSE 8000

CMD ['gunicorn', '--bind', '0:8000', 'config.wsgi']

ENV DJANGO_SETTINGS_MODULE=foodgram.settings

COPY requirements.txt /home/www/app

RUN pip install --no-cache-dir --src=/src -r /home/www/app/requirements.txt

COPY . /home/www/app