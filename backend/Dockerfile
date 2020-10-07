FROM node:12-alpine

RUN mkdir /app
WORKDIR /app

COPY package.json /app
RUN npm i

COPY . /app

ENTRYPOINT node index
