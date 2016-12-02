#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__ = ' 7 05, 2016 '
__author__ = 'mkfsn'


from re import sub
import requests
from pyquery import PyQuery
from datetime import datetime, timedelta
from urllib import quote
import difflib


class Room(object):

    def __init__(self, name, member_price, member_remain,
                 guest_price, guest_remain):
        self.name = name.encode('utf-8')
        self.guest = {'remain': guest_remain, 'price': guest_price}
        self.member = {'remain': member_remain, 'price': member_price}

    def __repr__(self):
        m = '<Member: price=%d, remain=%d>' % (self.member['price'],
                                               self.member['remain'])
        g = '<Guest: price=%d, remain=%d>' % (self.guest['price'],
                                              self.guest['remain'])
        return '<Room %s: %s, %s>' % (self.name, m, g)


class ToyokoInn(object):

    __info = None
    __default = None

    def __search_hotel_by_name(self, name):
        n = sum(1 for h in ToyokoInn.__info if name in h['name'])

        weighted_results = []
        for hotel in ToyokoInn.__info:
            ratio = difflib.SequenceMatcher(None, hotel['name'], name).ratio()
            weighted_results.append((hotel, ratio))
        weighted_results = sorted(weighted_results, key=lambda x: x[1])

        data = weighted_results[::-1][:n]

        if n == 0:
            raise Exception("No candidate hotel is found")

        elif n != 1:
            print "Candidates are:"
            for i in data:
                print "%f%%: %s, id = %s" %(i[1], i[0]['name'], i[0]['dataid'])
            print
            print "Choose:"
            print "%s, id = %s" %(data[0][0]['name'], data[0][0]['dataid'])

        return data[0][0]

    def __search_hotel_by_id(self, id):
        for hotel in ToyokoInn.__info:
            if id == hotel['dataid']:
                return hotel
        raise Exception("Hotel not found")

    def __load_config(self, fname):
        from ConfigParser import RawConfigParser
        config = RawConfigParser()
        config.optionxform = str

        with open(fname, 'rb') as fp:
            config.readfp(fp, fname)

        data = {}
        for s in config.sections():
            data[s] = dict(config.items(s))

        return data

    def __init__(self, name=None, id=None):

        if not ToyokoInn.__info:
            from script.fetch_hotel_info import fetch
            ToyokoInn.__info = fetch()

        if not ToyokoInn.__default:
            ToyokoInn.__default = self.__load_config("settings.ini")

        self.config = ToyokoInn.__default

        if isinstance(name, unicode):
            name = name.encode('utf-8')

        if id is not None:
            data = self.__search_hotel_by_id(str(id))

        elif name is not None:
            data = self.__search_hotel_by_name(name)

        self.name = data['name']
        self.dataid = data['dataid']
        self.state = data['state']
        self.substateid = data['substateid']

    def __extract_price_remain(self, html, index):
        selector_s = "tbody > tr:eq(%d) > td:gt(0)" % index

        result = []
        for td in PyQuery(html).children(selector_s):
            item = PyQuery(td).find("table > tbody div tr:eq(1)")

            price = PyQuery(item).find("td > span").text()
            price = sub(r'[^\d.]', '', price)
            price = int(price) if price != '' else 0

            remain = PyQuery(item).find("td + td + td").text()
            if remain == u'\u25ce':
                remain = 10
            elif remain == u'\xd7' or remain == '':
                remain = 0
            else:
                remain = int(remain)

            result.append([price, remain])
        return result

    def __extract(self, html):
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

            for i, v in enumerate(self.__extract_price_remain(pq, index)):
                self.data[date_order[i]][room]['member'] = v

            for i, v in enumerate(self.__extract_price_remain(pq, index + 2)):
                self.data[date_order[i]][room]['guest'] = v

            index += 3

        return self.data

    def __fetch_rawdata(self, year, month, day):
        # Start a session
        s = requests.session()

        # Prepare request: GET
        baseurl = 'https://yoyaku.4and5.com/reserve/html/rvpc_srchHtl.html'
        self.config['param'].update({
            'chcknYearAndMnth': '%d%02d' % (year, month),
            'chcknDayOfMnth': '%02d' % day,
            'prfctr': self.state,
            'htlName': quote(self.name),
            'id': self.dataid,
        })
        url = baseurl + '?' + \
              '&'.join([k + '=' + v for k, v in self.config['param'].items()])

        # Session GET
        r = s.get(url, headers=self.config['headers'])

        _s = "table.BlockSearch1 > tbody > div > tr > th > .BlockSearch2 a"
        clndr = PyQuery(r.text).find(_s).attr("onclick")[24:-2]

        # Prepare request: POST
        baseurl = 'https://yoyaku.4and5.com/reserve/html/rvpc_srchHtl.html'
        self.config['payload'].update({
            'prfctr': self.state,
            'htlName': self.name,
            'chcknYearAndMnth': '%d%02d' % (year, month),
            'chcknDayOfMnth': '%02d' % day,
        })
        param = clndr
        url = baseurl + '?' + param

        # Session POST
        r = s.post(url, headers=self.config['headers'],
                   data=self.config['payload'])

        return r.text.encode('utf-8')

    def __adjust(self, rooms):
        data = []
        for name, room in rooms.items():
            r = Room(name, room['member'][0], room['member'][1],
                     room['guest'][0], room['guest'][1])
            data.append(r)
        return data

    def rooms(self, **kwargs):

        member = kwargs.get('member', False)

        if 'year' in kwargs and 'month' in kwargs and 'day' in kwargs:
            year = int(kwargs['year'])
            month = int(kwargs['month'])
            day = int(kwargs['day'])

        elif 'date' in kwargs:
            date = kwargs['date']
            year = int(date['year'])
            month = int(date['month'])
            day = int(date['day'])

        else:
            raise Exception("Please specify a day")

        text = self.__fetch_rawdata(year, month, day)

        data = self.__extract(text)
        return self.__adjust(data['%s/%s' % (month, day)])


if __name__ == '__main__':
    next_month = datetime.today() + timedelta(days=30)
    year, month, day, member = [
        next_month.year,
        next_month.month,
        next_month.day,
        True
    ]

    hotel = ToyokoInn(u"札幌すすきの交差点")

    date = {'year': int(year), 'month': int(month), 'day': int(day)}
    rooms = hotel.rooms(date=date, member=member)

    for r in rooms:
        print r
