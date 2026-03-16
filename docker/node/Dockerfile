FROM node:8.16-alpine

RUN apk update && apk add python3

CMD npm install && npm install dynamodb-admin -g && npm install serverless -g && tail -f /dev/null
