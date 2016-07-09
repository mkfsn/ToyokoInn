#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__ = ' 7 05, 2016 '
__author__ = 'mkfsn'


from re import sub
import requests
from pyquery import PyQuery
from datetime import datetime
from urllib import quote


class ToyokoInn(object):

    def __init__(self, name):
        import json
        self.name = name

        with open("hotel.json") as f:
            data = filter(lambda x: x['name'].endswith(name), json.load(f))[:1]

        if data:
            self.dataid = data[0]['dataid']
            self.state = data[0]['state']
            self.substateid = data[0]['substateid']

    def _extract_price_remain(self, html, index):
        selector_s = "tbody > tr:eq(%d) > td:gt(0)" % index

        result = []
        for td in PyQuery(html).children(selector_s):
            item = PyQuery(td).find("table > tbody div tr:eq(1)")
            
            price = PyQuery(item).find("td > span").text()
            price = int(sub(r'[^\d.]', '', price))

            remain = PyQuery(item).find("td + td + td").text()
            if remain == u'\u25ce':
                remain = 10
            elif remain == u'\xd7' or remain == '':
                remain = 0
            else:
                remain = int(remain)

            result.append([price, remain])
        return result

    def _extract(self, html):
        pq = PyQuery(html).find(
            "form div.BlockFormClndr table.BlockSrchClndr3"
        )

        selector_ = "tr:eq(11) th"
        date_order = [PyQuery(v).text() for v in PyQuery(pq).find(selector_)]
        self.data = {d: {} for d in date_order}

        index = 9
        while index < 1000:
            # Get type of room
            selector_ = "tbody > tr:eq(%d) th:eq(0)" % index
            room = PyQuery(pq).children(selector_).text()
            if room == '':
                break

            for date, v in self.data.items():
                self.data[date][room] = {'member': [], 'guest': []}

            for i, v in enumerate(self._extract_price_remain(pq, index)):
                self.data[date_order[i]][room]['member'] = v

            for i, v in enumerate(self._extract_price_remain(pq, index + 2)):
                self.data[date_order[i]][room]['guest'] = v

            index += 3

        return self.data

    def room(self, date=None, member=False):
        s = requests.session()

        baseurl = 'https://yoyaku.4and5.com/reserve/html/rvpc_srchHtl.html'
        param = {
            'tlDtl': 'true',
            'cntry': 'JPN',
            'chcknYearAndMnth': '%d%02d' % (date['year'], date['month']),
            'chcknDayOfMnth': '%02d' % (date['day']),
            # 宿泊数
            'ldgngNum': '1',
            # 部屋数
            'roomNum': '1',
            'roomClssId': '',
            'fvrtName': '',
            'prfctr': self.state,
            'htlName': quote(self.name.encode("UTF-8")),
            'language': 'ja',
            'dispFull': 'on',
            # １部屋ご利用人数
            'ldgngPpl': '2',
            'id': self.dataid,
            'ref': 'info',
        }
        url = baseurl + '?' + '&'.join([k + '=' + v for k, v in param.items()])

        headers = {
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) ' +
                           'AppleWebKit/537.36 (KHTML, like Gecko) ' + 
                           'Chrome/51.0.2704.103 Safari/537.36'),
            'Accept': ('text/html,application/xhtml+xml,application/xml;q=0.9' +
                       ',image/webp,*/*;q=0.8'),
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,ja;q=0.2',
        }

        # session GET
        r = s.get(url, headers=headers)

        _s = "table.BlockSearch1 > tbody > div > tr > th > .BlockSearch2 a"
        clndr = PyQuery(r.text).find(_s).attr("onclick")[24:-2]

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
            'prfctr': self.state,
            'mncplty': '',
            'clsstSttn': '',
            'htlName': self.name,
            'chcknYearAndMnth': '%d%02d' % (date['year'], date['month']),
            'chcknDayOfMnth': '%02d' % date['day'],
            'ldgngNum': '1',
            'ldgngPpl': '2',
            'roomNum': '2',
            'dispFull': 'on',
        }

        baseurl = 'https://yoyaku.4and5.com/reserve/html/rvpc_srchHtl.html'
        param = clndr
        url = baseurl + '?' + param
        r = s.post(url, headers=headers, data=data)

        result = []
        data = self._extract(r.text.encode('utf-8'))
        for room, item in data['%s/%s' % (int(date['month']), int(date['day']))].items():
            price, remain = item['member'] if member else item['guest']
            if remain == 0:
                continue
            result.append('%s %s %s' % (room, price, remain))
        return result


if __name__ == '__main__':
    year, month, day, member = [2016, 7, 22, True]
    hotel = ToyokoInn(u"徳山駅新幹線口")
    date = {'year': int(year), 'month': int(month), 'day': int(day)}
    rooms = hotel.room(date=date, member=member)
    print rooms
