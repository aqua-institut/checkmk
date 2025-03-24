#!/usr/bin/env python
# -*- coding: utf-8 -*-
# seven Voice Gateway

# Send notification via seven Voice Gateway
#
# This notification script can be put below share/check_mk/notifications.
# Please configure the needed credentials

import sys, os

api_key = os.environ.get('NOTIFY_PARAMETER_1', os.environ.get('SEVEN_API_KEY'))
sender = os.environ.get('NOTIFY_PARAMETER_2', '')
api_url = "https://gateway.seven.io/api/voice"

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

    data = {'text': message, 'to': to, **({'from': sender} if sender else {})}
    content = urlopen(req, data=urlencode(data).encode())

    code = content.getcode()
    res = int(content.read())

    if code == 200 and res == 100:
        sys.stdout.write("Successfully called %s\n" % to)
    else:
        sys.stderr.write("Error calling %s: HTTP error code %d, API code %d\n" % (to, code, res))
except Exception as e:
    sys.stderr.write("Error calling %s: %s\n" % (to, e))