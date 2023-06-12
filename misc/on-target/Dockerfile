FROM python:3-alpine

# Install packages
RUN apk add --update --no-cache supervisor alpine-sdk socat

# Copy flag
COPY flag.txt /flag.txt

# add user
RUN adduser -D -u 1000 -g 1000 -s /bin/sh uscg

# Setup app
RUN mkdir -p /app

# Switch working environment
WORKDIR /app

# Add application
COPY challenge .
RUN chown -R uscg: /app

# Expose port the server is reachable on
EXPOSE 1337

# Disable pycache
ENV PYTHONDONTWRITEBYTECODE=1

# Run socat
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:'timeout 5 python ./main.py',stderr"]