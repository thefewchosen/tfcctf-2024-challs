FROM golang:latest

# Setup environment variables
ENV PORT=5000
ENV FLAG=TFCCTF{c4ch3_p015on1n6_tr0ll5_7h3_1n7ern3t}
ENV APP_HOST=localhost

WORKDIR /app

RUN apt update && apt install -y unzip wget chromium chromium-driver nginx

# Setup nginx
RUN mkdir -p /var/cache/nginx
RUN mkdir -p /etc/nginx/conf.d
RUN rm /etc/nginx/sites-available/default
RUN rm /etc/nginx/sites-enabled/default
COPY nginx.conf /etc/nginx/conf.d

# Download chromedriver for the linux64 architecture
RUN wget https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver ./ && \
    chmod +x ./chromedriver

COPY src/ .

# Download all dependencies. Dependencies will be cached if the go.mod and go.sum files are not changed
RUN go mod download

EXPOSE 80

CMD ["sh", "-c", "service nginx start && go run main.go"]