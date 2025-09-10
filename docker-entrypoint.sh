#!/bin/sh

. /.app/bin/activate
if [ "$1" == "2caldav" ]; then
    python /app/luna2caldav.py
elif [ "$1" == "orders" ]; then
    python /app/luna_list_orders.py
elif [ "$1" == "calendars" ]; then
    python /app/luna_list_calendars.py
else
    echo "Unknown option '$1'!"
    echo "Must be one of '2caldav', 'orders', 'calendars'!"
    exit 1
fi
