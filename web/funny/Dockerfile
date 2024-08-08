FROM alpine:3

# Setup user
RUN adduser -D -u 1000 -g 1000 -s /bin/sh www

# Install system packages
RUN apk add --no-cache --update apache2 \
    coreutils gettext php-cgi

# Configure apache2
COPY config/httpd.conf /etc/apache2/httpd.conf

COPY --chown=www:www public-html /var/www/public

COPY flag.txt /flag.txt

CMD ["httpd", "-D", "FOREGROUND"]