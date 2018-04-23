FROM alpine:3.7

ENV SRC="/usr/src/djangonews" \
    USED_DOMAIN="app-server" \
    DB_HOST="db-server" \
    DB_PORT="5432" \
    STATIC_PATH="/var/www/djangonews/static" \
    DJANGO_SECRET_KEY="par^7+km)=_5($^z*=i8-m5+1!e^&+=&6cbh3@yhm!xzyn(iu!" \
    SOCIAL_AUTH_FB_KEY="101886774002287" \
    SOCIAL_AUTH_FB_SECRET="f0b775772b7071cde8df21474ea325cb"

# Install updates & Essential Packages
RUN apk update && apk add python3
RUN apk add python3-dev gcc musl-dev postgresql-dev

# Create User & directories
RUN addgroup -S djangonews && \
    adduser -S -G djangonews djangonews

# Create Dirs and Users
RUN mkdir -p $SRC && mkdir -p $STATIC_PATH && \
    chown -R djangonews:djangonews $SRC && chown -R djangonews:djangonews $STATIC_PATH

# Copy Code
WORKDIR $SRC
COPY . .

# Install pip requirements
RUN pip3 install -r ./requirements.pip

USER djangonews

EXPOSE 8000

ENTRYPOINT ["ash", "./entry.sh"]
