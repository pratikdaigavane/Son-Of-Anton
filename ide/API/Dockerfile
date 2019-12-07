FROM alpine:3.7

# Install python3 and postgres cient
RUN apk add python3
RUN apk add postgresql-dev gcc python3-dev musl-dev

# Install python dependencies
RUN pip3 install django
RUN pip3 install djangorestframework
RUN pip3 install markdown
RUN pip3 install django-filter
RUN pip3 install psycopg2-binary
RUN pip3 install pika
RUN pip3 install django-cors-headers
RUN pip3 install django-sslserver

COPY src opt/src/

# Make database migrations and start django server on port 8000
ENTRYPOINT cd /opt/src/ ; python3 manage.py makemigrations ; python3 manage.py migrate ; python3 manage.py runserver 0.0.0.0:8000
