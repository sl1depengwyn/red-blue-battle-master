FROM node:11.9.0-alpine

ENV API=$API

ADD frontend/package.json /app/package.json
ADD frontend/package-lock.json /app/package-lock.json
ADD frontend/ /app
WORKDIR /app
RUN npm install

RUN npm run build 
RUN rm -rf /react_build/* 
CMD cp -r  build/* /react_build