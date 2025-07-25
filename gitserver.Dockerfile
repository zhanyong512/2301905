FROM node:alpine

RUN apk add --no-cache git \
    && npm install -g git-http-server \
    && adduser -D git

USER git
WORKDIR /home/git

RUN git init --bare repository.git

CMD ["git-http-server", "-p", "3000", "/home/git"]