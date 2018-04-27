FROM nginx:alpine

ENV NGINX_CONF_DIR=/etc/nginx/conf.d

WORKDIR $NGINX_CONF_DIR
RUN mv default.conf default.conf.bk
COPY . .

