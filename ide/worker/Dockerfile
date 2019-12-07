FROM alpine:latest

RUN apk add gcc
RUN apk add g++
RUN apk add make
RUN apk add bash
RUN apk add git
RUN apk add libc-dev
RUN apk add asciidoc
RUN apk add libcap-dev
RUN apk add python3
RUN pip3 install --upgrade pika
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip3 install psycopg2
RUN apk upgrade

RUN cd /home; git clone https://github.com/ioi/isolate.git
COPY init.sh /
COPY worker.py /var/local/lib/isolate/
COPY langs.py /var/local/lib/isolate/
COPY langs_config.json /var/local/lib/isolate/
COPY config.json /var/local/lib/isolate/
RUN cd /home/isolate; make all; make install;

 ENTRYPOINT cd /; ./init.sh; sleep 20; cd /var/local/lib/isolate; python3 worker.py