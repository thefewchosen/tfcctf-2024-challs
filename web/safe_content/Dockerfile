# Use the official PHP image with Apache
FROM php:7.4-apache


# Copy the PHP scripts into the Apache web root
COPY index.php /var/www/html/
COPY src.php /var/www/html/
COPY ./flag.txt /flag.txt

# Ensure the template compilation directory exists and has proper permissions
RUN mkdir -p /var/www/html/templates_c && \
    chown -R www-data:www-data /var/www/html/templates_c && \
    chmod 755 /var/www/html/templates_c


# Expose port 80 to the Docker host, so we can map it to a different port
EXPOSE 80

# Set the working directory
WORKDIR /var/www/html

# Run Apache in the foreground
CMD ["apache2-foreground"]
