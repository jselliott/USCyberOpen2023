FROM php:apache

# Copy flag
COPY flag.txt /flag.txt
RUN chmod 444 /flag.txt

# add user
RUN useradd -ms /bin/bash www

# Switch working environment
WORKDIR /var/www/html

# Add application
COPY challenge .
RUN chmod -R 755 /var/www/html

# Expose port the server is reachable on
EXPOSE 80