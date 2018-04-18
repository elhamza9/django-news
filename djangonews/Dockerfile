FROM alpine:3.7

ENV SRC="/usr/src/djangonews"

ENV DJANGO_SECRET_KEY='par^7+km)=_5($^z*=i8-m5+1!e^&+=&6cbh3@yhm!xzyn(iu!'
ENV SOCIAL_AUTH_FB_KEY='101886774002287'
ENV SOCIAL_AUTH_FB_SECRET='f0b775772b7071cde8df21474ea325cb'


MAINTAINER Hamza

RUN apk update && \
    apk add  python3 && \
    apk add  sqlite

# Copy Content
RUN mkdir -p $SRC
WORKDIR $SRC
COPY . .

# Install pip requirements
RUN pip3 install -r ./requirements.pip

#EXPOSE 8000

ENTRYPOINT ["ash", "./entry.sh"]
