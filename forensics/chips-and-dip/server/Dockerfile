FROM golang:alpine

RUN mkdir /app

WORKDIR /app

COPY . .

RUN go build -o server .

WORKDIR /app/client
RUN go build -o ../files/system_update .

WORKDIR /app

RUN chmod +x server

ENTRYPOINT [ "/app/server" ]