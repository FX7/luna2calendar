FROM python:3.11

ENV LUNA_LOGIN_URL='https://bestellen.luna.de/login'
ENV LUNA_CALENDAR_URL='https://bestellen.luna.de/order/'
ENV LUNA_SELECT_CONTRACT_URL='https://bestellen.luna.de/select-contract'
ENV LUNA_LOAD_DATA_URL='https://bestellen.luna.de/order/load-data'

ENV LUNA_USERNAME='user@luna'
ENV LUNA_PASSWORD='secret'
ENV LUNA_MONTH='2025-1-01'
ENV LUNA_ONLY_ORDERED=True
ENV LUNA_CALENDAR_ID=12345

ENV NEXTCLOUD_DOMAIN='nextcloud.example.com'
ENV NEXTCLOUD_USERNAME='nextloud-user'
ENV NEXTCLOUD_PASSWORD='nextcloud-password'
ENV NEXTCLOUD_CALENDAR_NAME='nextcloud-calendar'

ENV SCHOOL_LUNCH_START_TIME='114000'
ENV SCHOOL_LUNCH_END_TIME='122000'
ENV SCHOOL_LUNCH_TIMEZONE='Europe/Berlin'

RUN pip install --upgrade pip && pip install requests BeautifulSoup4

COPY *.py /

CMD python /luna2nextcloud.py
