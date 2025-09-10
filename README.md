To show all available luna calendars call:

`podman run -it --rm luna2calendar:latest calendars`

The following environment variables can / must be set:

```
LUNA_USERNAME='user@luna'
LUNA_PASSWORD='secret'
LUNA_MONTH='2025-1-01'
LUNA_ONLY_ORDERED=True
LUNA_CALENDAR_ID=12345

CALDAV_DOMAIN='nextcloud.example.com'
CALDAV_USERNAME='nextloud-user'
CALDAV_PASSWORD='nextcloud-password'
CALDAV_CALENDAR_NAME='nextcloud-calendar'

SCHOOL_LUNCH_START_TIME='114000'
SCHOOL_LUNCH_END_TIME='122000'
SCHOOL_LUNCH_TIMEZONE='Europe/Berlin'
```
