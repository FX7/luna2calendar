To show all available luna calendars call:

`podman run -it --rm luna2nextcloud:latest python /luna_list_calendars.py`

The following environment variables can / must be set:

```
LUNA_USERNAME='user@luna'
LUNA_PASSWORD='secret'
LUNA_MONTH='2025-1-01'
LUNA_ONLY_ORDERED=True
LUNA_CALENDAR_ID=12345

NEXTCLOUD_DOMAIN='nextcloud.example.com'
NEXTCLOUD_USERNAME='nextloud-user'
NEXTCLOUD_PASSWORD='nextcloud-password'
NEXTCLOUD_CALENDAR_NAME='nextcloud-calendar'

SCHOOL_LUNCH_START_TIME='114000'
SCHOOL_LUNCH_END_TIME='122000'
SCHOOL_LUNCH_TIMEZONE='Europe/Berlin'
```