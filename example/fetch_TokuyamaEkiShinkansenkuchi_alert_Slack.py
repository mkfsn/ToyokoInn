#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__ = ' 7 09, 2016 '
__author__ = 'mkfsn'


import argparse
from datetime import datetime
import os
import sys
import json


sys.path.insert(1, os.path.join(sys.path[0], '..'))


from ToyokoInn import ToyokoInn


parser = argparse.ArgumentParser(
    description='Fetch ToyokoInn reservable room'
)
parser.add_argument('--year', type=int,
                    required=True, help='Specify year of date')
parser.add_argument('--month', type=int, choices=xrange(1, 13),
                    required=True, help='Specify month of date')
parser.add_argument('--day', type=int, choices=xrange(1, 32),
                    required=True, help='Specify day of date')

args = parser.parse_args()
if datetime.now() > datetime(args.year, args.month, args.day, 23, 59, 59):
    sys.exit(-1)

year, month, day = [args.year, '%02d' % args.month, '%02d' % args.day]
hotel = ToyokoInn(u"徳山駅新幹線口")
date = {'year': int(year), 'month': int(month), 'day': int(day)}
result = hotel.room(date=date, member=True)

title = "徳山駅新幹線口-%s-%s-%s" % (year, month, day)

changed = False

filename = '/tmp/%s' % title
if not os.path.isfile(filename):
    changed = True
else:
    with open(filename, 'r+') as f:
        previous = f.read()
        if previous != json.dumps(result):
            changed = True

with open(filename, 'w') as f:
    f.write(json.dumps(result))

if not changed:
    sys.exit(0)

print result
sys.exit(0)

content = '[%s]\n%s' % (title.decode('utf-8'), '\n'.join(result))
data = {
    'username': 'ToyokoINN-bot',
    'text': content,
    'channel': 'toyokoinn',
}
slack_url = 'https://hooks.slack.com/services/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'
requests.post(slack_url, data=json.dumps(data))
