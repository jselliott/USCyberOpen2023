FROM python:3-alpine

# Install packages
RUN apk add --update --no-cache supervisor git

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install dependencies
RUN pip install gunicorn Flask pyotp

# Copy flag
COPY flag.txt /flag.txt

# add user
RUN adduser -D -u 1000 -g 1000 -s /bin/sh www


# Set up fake git
RUN mkdir /tmp/lottery

WORKDIR /tmp/lottery

COPY challenge/application/lottery.py .

RUN git init
RUN git config --global user.email "coachelliott@uscybergames.com" && git config --global user.name "Jacob Elliott"
RUN git add -A && git commit -m "Initial commit"

# Setup app
RUN mkdir -p /app

# Switch working environment
WORKDIR /app

# Add application
COPY challenge .

RUN mv /tmp/lottery/.git /app/application/git

# Setup supervisor
COPY config/supervisord.conf /etc/supervisord.conf

# Expose port the server is reachable on
EXPOSE 1337

# Disable pycache
ENV PYTHONDONTWRITEBYTECODE=1

# Run supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]