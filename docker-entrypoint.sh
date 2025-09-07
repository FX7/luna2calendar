#!/bin/sh

. /.app/bin/activate
if [ "$1" == "2nextcloud" ]; then
    python /app/luna2nextcloud.py
elif [ "$1" == "orders" ]; then
    python /app/luna_list_orders.py
elif [ "$1" == "calendars" ]; then
    python /app/luna_list_calendars.py
else
    echo "Unknown option '$1'!"
    echo "Must be one of '2nextcloud', 'orders', 'calendars'!"
    exit 1
fi
