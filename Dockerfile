FROM python:3.6.8-alpine3.9
WORKDIR /usr/local/bin
COPY . .
CMD cd lib/GenshiBASIC ; python3 -m unittest discover
