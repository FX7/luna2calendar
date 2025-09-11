FROM alpine:latest AS base

RUN apk add python3 py3-pip && rm -r /var/cache/apk

RUN mkdir /app && mkdir /.app
COPY requirements.txt /app/requirements.txt

RUN /usr/bin/python3 -m venv /.app \
    && . /.app/bin/activate \
    && pip install -r /app/requirements.txt


FROM base AS development

ARG UID=1000
ARG GID=1000
ARG USERNAME=vscode

RUN apk add sudo bash git openssh

RUN addgroup --gid $GID $USERNAME \
    && adduser -u $UID -G $USERNAME -D -s /bin/bash $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
    && addgroup -S sudo && addgroup $USERNAME sudo


FROM base

ENV LUNA_LOGIN_URL='https://bestellen.luna.de/login'
ENV LUNA_CALENDAR_URL='https://bestellen.luna.de/order/'
ENV LUNA_SELECT_CONTRACT_URL='https://bestellen.luna.de/select-contract'
ENV LUNA_LOAD_DATA_URL='https://bestellen.luna.de/order/load-data'

ENV LUNA_USERNAME='user@luna'
ENV LUNA_PASSWORD='secret'
ENV LUNA_MONTH='2025-1-01'
ENV LUNA_ONLY_ORDERED=True
ENV LUNA_CALENDAR_ID=12345

ENV CALDAV_DOMAIN='nextcloud.example.com'
ENV CALDAV_USERNAME='nextloud-user'
ENV CALDAV_PASSWORD='nextcloud-password'
ENV CALDAV_CALENDAR_NAME='nextcloud-calendar'
ENV CALDAV_PATH='remote.php/dav/calendars'

ENV SCHOOL_LUNCH_START_TIME='114000'
ENV SCHOOL_LUNCH_END_TIME='122000'
ENV SCHOOL_LUNCH_TIMEZONE='Europe/Berlin'

COPY *.py /app
COPY docker-entrypoint.sh /
RUN chmod a+x /docker-entrypoint.sh

ENTRYPOINT [ "/docker-entrypoint.sh" ]
CMD [ "2caldav" ]
