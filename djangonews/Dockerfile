FROM alpine:3.7

MAINTAINER Hamza El

ENV SRC="/usr/src/djangonews" \
    USED_DOMAIN="ec2-54-200-24-133.us-west-2.compute.amazonaws.com" \
    DJANGO_SECRET_KEY='par^7+km)=_5($^z*=i8-m5+1!e^&+=&6cbh3@yhm!xzyn(iu!' \
    SOCIAL_AUTH_FB_KEY='101886774002287' \
    SOCIAL_AUTH_FB_SECRET='f0b775772b7071cde8df21474ea325cb'

# Copy Content
RUN mkdir -p $SRC
WORKDIR $SRC
COPY . .

RUN apk update && \
    apk add python3 && \
    apk add  sqlite && \
    pip3 install -r ./requirements.pip

EXPOSE 8000

ENTRYPOINT ["ash", "./entry.sh"]
