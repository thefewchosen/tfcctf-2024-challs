# Use the official PHP image with Apache
FROM php:8.1-apache

# Install necessary packages
RUN apt-get update && apt-get install -y libpng-dev libjpeg-dev libfreetype6-dev supervisor python3 python3-gunicorn python3-flask python3-werkzeug python3-requests && \
    rm -rf /var/lib/apt/lists/*


RUN \
    groupadd -g 3000 www && \
    useradd -u 1000 -g www -s /usr/sbin/nologin -d /var/www www && \
    sed -i 's/Options Indexes FollowSymLinks/Options +Indexes/g' /etc/apache2/apache2.conf && \
    sed -i '$a<Directory /var/www/html/templates_c/>\n    Options +Indexes\n    AllowOverride None\n    Require all granted\n</Directory>' /etc/apache2/apache2.conf && \
    sed -i 's/AllowOverride None/AllowOverride all/g' /etc/apache2/apache2.conf && \
    echo ServerName localhost > /etc/apache2/conf-available/fqdn.conf && \
    echo "ServerSignature Off\nServerTokens Prod" > /etc/apache2/conf-available/signature.conf && \
    sed -i "s/80/1234/g" /etc/apache2/sites-enabled/000-default.conf /etc/apache2/ports.conf && \
    #sed -i 's/^allow_url_fopen.*/allow_url_fopen = Off/g' /usr/local/etc/php/php.ini-production && \
    #sed -i 's/^allow_url_include.*/allow_url_include = Off/g' /usr/local/etc/php/php.ini-production && \
    echo "upload_max_filesize = 1M" > /usr/local/etc/php/conf.d/maxsizes.ini && \
    echo "post_max_size = 5M" >> /usr/local/etc/php/conf.d/maxsizes.ini && \
    echo "memory_limit = 128M" >> /usr/local/etc/php/conf.d/maxsizes.ini && \
    echo "disable_functions = eval,exec,passthru,system,proc_open,popen,shell_exec,curl_exec,curl_multi_exec,parse_ini_file,show_source" >> /usr/local/etc/php/conf.d/maxsizes.ini && \
    echo "display_errors = Off" >> /usr/local/etc/php/conf.d/maxsizes.ini && \
    echo "html_errors = Off" >> /usr/local/etc/php/conf.d/maxsizes.ini && \
    echo "expose_php = Off" >> /usr/local/etc/php/conf.d/maxsizes.ini && \
    echo "max_file_uploads = 500000" >> /usr/local/etc/php/conf.d/maxsizes.ini && \
    a2enconf fqdn && \
    a2enmod autoindex && \
    a2enconf signature && \
    a2enmod rewrite && \
    a2dismod status  && \
    a2enmod -q headers  && \
    a2enmod -q reqtimeout

# Set ownership and permissions
RUN chown -R www:www /var/www && \
    chmod -R 755 /var/www

# Copy necessary files
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
#COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
COPY ./python /app
COPY ./www /var/www/html/

# Set the working directory
WORKDIR /app

# Make the entrypoint script executable
#RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Expose the correct ports
EXPOSE 5000 8000
#USER www
#RUN chmod 777 /usr/bin/supervisord
# Configure the entrypoint and default command
#ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# Ensure www user owns the application directories
RUN chown -R www:www /app /var/www /etc/supervisor/conf.d

# Make sure the www user has write access to the logs directory (or any other necessary directories)
RUN mkdir -p /var/log/supervisor && \
    chown -R www:www /var/log/supervisor

USER www

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]


