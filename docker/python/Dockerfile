FROM python:3.6-alpine
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

ENV APP /application

RUN mkdir $APP
WORKDIR $APP

RUN pip3 install --upgrade pip
RUN pip3 install pipenv

COPY . .

CMD tail -f /dev/null