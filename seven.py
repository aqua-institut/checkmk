#!/usr/bin/env python
# -*- coding: utf-8 -*-
# seven SMS Gateway

# Send notification via seven SMS Gateway
#
# This notification script can be put below share/check_mk/notifications.
# Please configure the needed credentials

import sys, os, urllib

api_key = os.environ.get('NOTIFY_PARAMETER_1', os.environ.get('SEVEN_API_KEY'))
sender = os.environ.get('NOTIFY_PARAMETER_2', '')
api_url = "https://gateway.sms77.io/api/sms"

to = os.environ.get("NOTIFY_CONTACTPAGER")
message = os.environ['NOTIFY_HOSTNAME'] + " "

if os.environ['NOTIFY_WHAT'] == 'SERVICE':
    message += os.environ['NOTIFY_SERVICESTATE'] + " "
    message += os.environ['NOTIFY_SERVICEDESC']
else:
    message += "is " + os.environ['NOTIFY_HOSTSTATE'] # Host message

url = "%s?" % api_url + urllib.urlencode([("p", api_key) ("from", sender),
                                           ("to", to), ("text", message)])

try:
    handle = urllib.urlopen(url)
    response = handle.read().strip()

    if handle.getcode() == 200:
        sys.stdout.write("Successfully sent SMS to %s\n" % to)
    else:
        sys.stderr.write("Error sending SMS to %s: HTTP error code %s\n" % (to, handle.getcode()))
        sys.stderr.write("URL was %s\n" % url)
except Exception as e:
    sys.stderr.write("Error sending SMS to %s: %s\n" % (to, e))
