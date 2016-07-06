#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= ' 7 05, 2016 '
__author__= 'mkfsn'


from re import sub
import requests
from pyquery import PyQuery
from datetime import datetime


class ToyokoInn(object):

    def __init__(self, name):
        self.name = name


def fetch(year, month, day, member=False):
    # Results of dates. {DATE: {ROOM: {member: PRICE, guest: PRICE}}}
    results = {}

    s = requests.session()

    url = "https://yoyaku.4and5.com/reserve/html/rvpc_srchHtl.html?htlDtl=true&cntry=JPN&chcknYearAndMnth={year}{month}&chcknDayOfMnth={day}&ldgngNum=1&roomNum=1&roomClssId=&fvrtName=&prfctr=35&htlName=%E5%BE%B3%E5%B1%B1%E9%A7%85%E6%96%B0%E5%B9%B9%E7%B7%9A%E5%8F%A3&language=ja&dispFull=on&ldgngPpl=1&id=131&ref=info&_ga=1.151929791.720274849.1467717947".format(year=year, month=month, day=day)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,ja;q=0.2',
    }

    # session GET
    r = s.get(url, headers=headers)

    url = 'https://yoyaku.4and5.com/reserve/html/rvpc_srchHtl.html'
    data = {
        'rg.seasar.ymir.token': '89dbd02e37b4597e8862423dc09a4c0d',
        'language': '',
        'htlUid': '',
        'srchRoomAllFlag': 'true',
        'srchRoomBasicFlag': 'false',
        'srchRoomPlanFlag': 'false',
        'tabGrpCode': 'ALL',
        'langFlag': 'ja',
        'dsplLinkPnt': '',
        'hospital': '',
        'cntry': 'JPN',
        'prfctr': '35',
        'mncplty': '',
        'clsstSttn': '',
        'htlName': '徳山駅新幹線口',
        'chcknYearAndMnth': '%s%s' % (year, month),
        'chcknDayOfMnth': '%s' % day,
        'ldgngNum': '1',
        'ldgngPpl': '2',
        'roomNum': '2',
        'dispFull': 'on',
    }

    # session POST
    r = s.post(url, headers=headers, data=data, allow_redirects=False)

    url = 'https://yoyaku.4and5.com/reserve/html/rvpc_srchHtl.html?clndr[6000136][][6000136][][20071001]'
    r = s.post(url, headers=headers, data=data)

    html = r.text.encode('utf-8')
    pq = PyQuery(html).find("form div.BlockFormClndr table.BlockSrchClndr3")

    date_order = [PyQuery(th).text() for th in PyQuery(pq).find("tr:eq(11) th")]
    results = {PyQuery(th).text(): {} for th in PyQuery(pq).find("tr:eq(11) th")}

    index = 9
    while index < 100:
        room = PyQuery(pq).children("tbody > tr:eq(%d) th:eq(0)" % index).text()
        if room == '':
            break
        for date, v in results.items():
            results[date][room] = {'member': [], 'guest': []}

        i_ = 0
        for td in PyQuery(pq).children("tbody > tr:eq(%d) > td:gt(0)" % index):
            item = PyQuery(td).find("table > tbody div tr:eq(1)")
            price = sub(r'[^\d.]', '', PyQuery(item).find("td > span").text()[1:])
            remain = PyQuery(item).find("td + td + td").text()
            remain = 0 if remain == u'\xd7' or remain == '' else int(remain)

            results[date_order[i_]][room]['member'] = [price, remain]
            i_ += 1

        i_ = 0
        for td in PyQuery(pq).children("tbody > tr:eq(%d) > td:gt(0)" % (index + 2)):
            item = PyQuery(td).find("table > tbody div tr:eq(1)")
            price = sub(r'[^\d.]', '', PyQuery(item).find("td > span").text()[1:])
            remain = PyQuery(item).find("td + td + td").text()
            remain = 0 if remain == u'\xd7' or remain == '' else int(remain)

            results[date_order[i_]][room]['guest'] = [price, remain]
            i_ += 1
        index += 3
    
    # List all
    # for date, _item in results.items():
    #     for room, item in results[date].items():
    #         price, remain = item['member'] if member else item['guest']
    #         if remain == 0:
    #             continue
    #         print date, room, price, remain

    retval = []
    for room, item in results['%s/%s' % (int(month), int(day))].items():
        price, remain = item['member'] if member else item['guest']
        if remain == 0:
            continue
        retval.append('%s %s %s' % (room, price, remain))
    return retval


if __name__ == '__main__':
    import argparse, json, os, sys

    parser = argparse.ArgumentParser(description='Fetch ToyokoINN reservable room')
    parser.add_argument('--year', type=int, required=True, help='Specify year of date')
    parser.add_argument('--month', type=int, choices=xrange(1, 13), required=True, help='Specify month of date')
    parser.add_argument('--day', type=int, choices=xrange(1, 32), required=True, help='Specify day of date')

    args = parser.parse_args()
    if datetime.now() > datetime(args.year, args.month, args.day, 23, 59, 59):
        sys.exit(-1)

    year, month, day = [args.year, '%02d' % args.month, '%02d' % args.day]
    result = fetch(year, month, day, member=True)

    title = "徳山駅新幹線口-%s-%s-%s" % (year, month, day)

    changed = False

    filename = '/tmp/%s' % title
    if not os.path.isfile(filename):
        with open(filename, 'w') as f:
            changed = True
            f.write(json.dumps(result))
    else:
        with open(filename, 'r+') as f:
            previous = f.read()
            if previous != json.dumps(result):
                changed = True
            f.seek(0)
            f.write(json.dumps(result))

    if not changed:
        sys.exit(0)

    content = '[%s]\n%s' % (title.decode('utf-8'), '\n'.join(result))
    data = {
        'username': 'ToyokoINN-bot',
        'text': content,
        'channel': 'toyokoinn',
    }
    slack_url = 'https://hooks.slack.com/services/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'
    requests.post(slack_url, data=json.dumps(data))
