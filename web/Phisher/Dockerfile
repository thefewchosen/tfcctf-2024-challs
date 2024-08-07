FROM python:3.10-slim

RUN apt-get update && apt-get install -y nginx wget firefox-esr && apt-get clean

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

RUN rm /etc/nginx/sites-enabled/default
COPY nginx.conf /etc/nginx/sites-enabled/default
COPY flag.txt /flag.txt
COPY default.html /var/www/html/index.html
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /app
COPY ./src /app

EXPOSE 80

ENV SMTP_PORT 10025
ENV MAIL_PORT 5000
ENV DASHBOARD_PORT 3000
ENV ADMIN_USER admin@phisher.tfc

CMD ["/entrypoint.sh"]
