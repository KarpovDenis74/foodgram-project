FROM python:3.8.5
RUN mkdir /code
COPY requirements.txt /code
RUN pip3 install -r requirements.txt
COPY . /code
WORKDIR /code
# RUN python manage.py collectstatic --noinput
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000