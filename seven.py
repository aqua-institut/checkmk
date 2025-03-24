#!/usr/bin/env python
# -*- coding: utf-8 -*-
# seven SMS Gateway

# Send notification via seven SMS Gateway
#
# This notification script can be put below share/check_mk/notifications.
# Please configure the needed credentials

import sys, os

api_key = os.environ.get('NOTIFY_PARAMETER_1', os.environ.get('SEVEN_API_KEY'))
sender = os.environ.get('NOTIFY_PARAMETER_2', '')
api_url = "https://gateway.seven.io/api/sms"

to = os.environ.get("NOTIFY_CONTACTPAGER")
message = os.environ['NOTIFY_HOSTNAME'] + " "

if os.environ['NOTIFY_WHAT'] == 'SERVICE':
    message += os.environ['NOTIFY_SERVICESTATE'] + " "
    message += os.environ['NOTIFY_SERVICEDESC']
else:
    message += "is " + os.environ['NOTIFY_HOSTSTATE'] # Host message

try:
    from urllib.request import Request, urlopen # Python 3
    from urllib.parse import urlencode
except ImportError:
    from urllib2 import Request, urlopen  # Python 2
    from urllib import urlencode

try:
    req = Request(api_url)
    req.add_header('SentWith', 'Checkmk')
    req.add_header('X-Api-Key', api_key)

    data = urlencode({
        'from': sender,
        'text': message,
        'to': to,
    }).encode()

    content = urlopen(req, data=data)
    code = content.getcode()
    res = int(content.read())

    if code == 200 and res == 100:
        sys.stdout.write("Successfully sent SMS to %s\n" % to)
    else:
        sys.stderr.write("Error sending SMS to %s: HTTP error code %d, API code %d\n" % (to, code, res))
except Exception as e:
    sys.stderr.write("Error sending SMS to %s: %s\n" % (to, e))