FROM golang:alpine

# Install packages
RUN apk add --update --no-cache supervisor

# Setup app
RUN mkdir -p /app

# Switch working environment
WORKDIR /app

# Add application
COPY challenge .

WORKDIR /app/cmd/server

# Install Go packages
RUN go get github.com/sigurn/crc16 && go get github.com/zenazn/pkcs7pad

# Setup supervisor
COPY config/supervisord.conf /etc/supervisord.conf

# Expose port the server is reachable on
EXPOSE 1337

# Run supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]