FROM nginx:alpine

WORKDIR /etc/nginx/conf.d
RUN mv default.conf default.conf.bk
COPY djangonews.conf .

