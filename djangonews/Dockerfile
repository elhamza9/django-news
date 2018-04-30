FROM alpine:3.7

ENV SRC="/usr/src/djangonews" \
    STATIC_PATH="/var/www/djangonews/static" \
    USED_DOMAIN="ec2-54-200-24-133.us-west-2.compute.amazonaws.com" \
    ENV="staging" \
    USING_HTTPS="yes" \
    DB_HOST="db-server" \
    DB_PORT="5432" \
    DJANGO_SECRET_KEY="%+nz*dtyc+wh=#8!aasl2xkuo$m^oejnuqjptx57z0f4_^7xzh" \
    SOCIAL_AUTH_FB_KEY="179060132912002" \
    SOCIAL_AUTH_FB_SECRET="1d78f8fe1b2cbec37b611e96003bf77c"

# Update and install python 3
RUN apk update && apk add python3 

# Create User & directories
RUN addgroup -S djangonews && \
    adduser -S -G djangonews djangonews && \
    mkdir -p $SRC && mkdir -p $STATIC_PATH && \
    chown -R djangonews:djangonews $SRC && chown -R djangonews:djangonews $STATIC_PATH

# Install other Packages
RUN apk add python3-dev gcc musl-dev postgresql-dev

# Copy Code
WORKDIR $SRC
COPY . .

# Install pip requirements
RUN pip3 install -r ./requirements.pip

USER djangonews

# Quick Fix to wait for DB
RUN sleep 15 && \
    python3 manage.py migrate && \
    python3 manage.py collectstatic --noinput

USER root

RUN mkdir -p $STATIC_PATH/tinymce/js && \
    cp -R /usr/lib/python3.6/site-packages/tinymce/static/tinymce/js/* $STATIC_PATH/tinymce/js && \
    chown -R djangonews:djangonews $STATIC_PATH/

USER djangonews

EXPOSE 8000

CMD gunicorn --access-logfile - --log-file - --workers 2 djangonews.wsgi:application -b 0.0.0.0:8000