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

    __options = {'smoking': bool, 'available': bool}

    def __init__(self, name, member_price, member_remain,
                 guest_price, guest_remain, ismember=True):
        self.name = name.encode('utf-8')
        self.smoking = u'喫煙' in name

        if guest_price is not None and guest_remain is not None:
            self.guest = {'remain': guest_remain, 'price': guest_price}
        else:
            self.guest = None

        if member_remain is not None and member_remain is not None:
            self.member = {'remain': member_remain, 'price': member_price}
        else:
            self.member = None

        self.available = (
            (self.member is not None and self.member['remain'] > 0) or
            (self.guest is not None and self.guest['remain'] > 0)
        )

        if ismember:
            self.price = member_price
            self.remain = member_remain
        else:
            self.price = guest_price
            self.remain = guest_remain

    def __repr__(self):
        if self.member is not None:
            m = '<Member: price=%r, remain=%r>' % (self.member['price'],
                                                   self.member['remain'])
        if self.guest is not None:
            g = '<Guest: price=%r, remain=%r>' % (self.guest['price'],
                                                  self.guest['remain'])

        if self.member is not None and self.guest is not None:
            return '<%s %s: %s, %s>' % (self.__class__.__name__,
                                        self.name, m, g)
        elif self.member is not None:
            return '<%s %s: %s>' % (self.__class__.__name__, self.name, m)
        elif self.guest is not None:
            return '<%s %s: %s>' % (self.__class__.__name__, self.name, g)
        else:
            return '<%s %s>' % (self.__class__.__name__, self.name)

    @property
    def member_price(self):
        return self.member['price'] if self.member else None

    @property
    def member_remain(self):
        return self.member['remain'] if self.member else None

    @property
    def guest_price(self):
        return self.guest['price'] if self.guest else None

    @property
    def guest_remain(self):
        return self.guest['remain'] if self.guest else None

    @classmethod
    def options(cls):
        return cls.__options


class Hotel(object):

    def __init__(self, info, config=None):
        self.name = info['name']
        self.dataid = info['dataid']
        self.rgn1 = info['rgn1']
        self.rgn2 = info['rgn2']
        self.rgn3 = info['rgn3']
        self.rgn4 = info['rgn4']
        # self.state = info['state']
        # self.substateid = info['substateid']
        self.config = config

    @property
    def state(self):
        if self.rgn1 in ["1", "123", "134"]:
            return self.rgn2
        if self.rgn1 in ["2", "3", "4", "5", "6", "7"]:
            return self.rgn3
        return self.rgn4

    def __repr__(self):
        return '<%s %s: dataid=%r>' % (
            self.__class__.__name__,
            self.name,
            self.dataid,
            # self.state,
            # self.substateid
        )

    def __extract(self, html):
        pq = PyQuery(html).find("main#main #mainArea table")

        selector_ = "thead tr:eq(0) th"
        date_order = [PyQuery(v).text().split('\n')[0] for v in PyQuery(pq).find(selector_)][3:]
        result = {d: {} for d in date_order}

        index = 0
        total = len(PyQuery(pq).find("tbody tr"))
        while index < total:
            td = PyQuery(pq).find("tbody tr:eq(%d) td:eq(0)" % index)

            room_type = td.text().split()[0]
            rowspan = int(td.attr('rowspan'))

            for i in xrange(index, index + rowspan):
                row = PyQuery(pq).find("tbody tr:eq(%d)" % i)

                # smoking or not
                smoking = PyQuery(row).find("td.alC.alM > img").attr("alt")

                room = "%s (%s)" % (room_type, smoking)

                if row.hasClass('clubCardCell'):
                    member_type = 'member'
                else:
                    member_type = 'guest'

                for i, v in enumerate(self.__extract_price_remain(row)):
                    if room not in result[date_order[i]]:
                        result[date_order[i]][room] = {}
                    result[date_order[i]][room][member_type] = v

            index += rowspan
        return result

    def __extract_price_remain(self, row):
        result = []
        for td in PyQuery(row).children(".calenderCell"):
            if PyQuery(td).hasClass('noneCell'):
                result.append(['Unknown', 0])
                continue
            elif PyQuery(td).hasClass('emptyCell'):
                result.append([None, None])
                continue

            items =  PyQuery(td).find("a").html().replace("<br/>", "\r").split('\r')

            raw_price = PyQuery(items[1]).text()
            raw_remain = items[0]

            try:
                price = int(sub(r'[^\d]', '', raw_price))
            except:
                price = None

            if raw_remain == u'\u25cb':
                remain = 10
            elif raw_remain == u'\u25b3':
                remain = 5
            elif raw_remain == u'\xd7' or raw_remain == '':
                remain = 0
            else:
                print remain
                remain = None

            result.append([price, remain])
        return result

    def __adjust(self, rooms):
        data = []
        for name, room in rooms.items():
            matched = True
            r = Room(name, room['member'][0], room['member'][1],
                     room['guest'][0], room['guest'][1])
            if self.filter is not None:
                for key, value in self.filter.items():
                    matched = matched and (r.__getattribute__(key) == value)
            if matched:
                data.append(r)
        return data

    def __fetch_rawdata(self, **kwargs):
        # Start a session
        s = requests.session()
        url = "https://www.toyoko-inn.com/index?lcl_id=ja"
        # For getting necessary cookies
        r = s.get(url)

        url = 'https://www.toyoko-inn.com/index/condition_search'
        data = {
            'lcl_id': 'ja',
            'prcssng_dvsn': 'dtl',
            'sel_htl_txt': quote(self.name),
            'chck_in': '%d/%02d/%02d' % (kwargs['year'], kwargs['month'], kwargs['day']),
            'inn_date': str(kwargs['stay']),
            'rsrv_num': str(kwargs['num']),
            'sel_ldgngPpl': str(kwargs['people']),
            'sel_area': self.state,
            'sel_htl': self.dataid,
        }

        # Search available rooms
        r = s.post(url, data=data)
        # if u"入力されたチェックイン日、宿泊数では予約できません。" in r.text:
        #     raise Exception("This date is currently not available")

        url = "https://www.toyoko-inn.com/search/reserve/date"
        r = s.get(url)

        return r.text.encode('utf-8')

    def __set_filter(self, filter):
        if filter is not None:
            options = Room.options()
            for key, value in filter.items():
                if key not in options.keys():
                    raise Exception("filter `%s' not supported" % key)
                if not isinstance(value, options[key]):
                    err = "filter `%s' is expecting %r" % (key, options[key])
                    raise Exception(err)
        self.filter = filter

    """
    @num(int): Number of rooms, default is 1
    @stay(int): Number of days, default is 1
    @people(int): Number of people in one room, default is 1
    """
    def rooms(self, num=1, stay=1, people=2, **kwargs):

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
            today = datetime.today()
            year = today.year
            month = today.month
            day = today.day

        self.__set_filter(kwargs.get('filter', None))

        if people > 2 or people < 1:
            raise Exception("@people has to be either 1 or 2")

        if stay > 7:
            raise Exception("@stay currently supported within 7 days")

        text = self.__fetch_rawdata(year=year, month=month, day=day,
                                    people=people, stay=stay, num=num)

        data = self.__extract(text)
        return self.__adjust(data['%s/%s' % (month, day)])


class ToyokoInn(object):

    hotels = None
    config = None

    @classmethod
    def __search_hotel_by_name(cls, name):
        candidates = [h for h in ToyokoInn.hotels if name in h.name]

        weighted_results = []
        for hotel in candidates:
            ratio = difflib.SequenceMatcher(None, hotel.name, name).ratio()
            weighted_results.append({'hotel': hotel, 'ratio': ratio})
        weighted_results = sorted(weighted_results, key=lambda x: x["ratio"])

        data = weighted_results[::-1]
        n = len(data)

        if n == 0:
            raise Exception("No candidate hotel is found")

        elif n != 1:
            import sys
            output = sys.stderr.write
            output("Candidates are:\n")
            for i in data:
                output("%f%%: %r\n" % (i["ratio"], i['hotel']))
            output("\nChoose:\n")
            output("%r\n" % data[0]['hotel'])
            sys.stderr.flush()

        return data[0]["hotel"]

    @classmethod
    def __search_hotel_by_id(cls, id):
        for hotel in ToyokoInn.hotels:
            if id == hotel.dataid:
                return hotel
        raise Exception("Hotel not found")

    @classmethod
    def __load_config(cls, fname):
        from ConfigParser import RawConfigParser
        config = RawConfigParser()
        config.optionxform = str

        with open(fname, 'rb') as fp:
            config.readfp(fp, fname)

        data = {}
        for s in config.sections():
            data[s] = dict(config.items(s))

        return data

    def __new__(cls, name=None, id=None):

        if not ToyokoInn.config:
            ToyokoInn.config = cls.__load_config("settings.ini")

        if not ToyokoInn.hotels:
            from utils import hotel_info
            ToyokoInn.hotels = list()
            for info in hotel_info.fetch():
                hotel = Hotel(info, config=ToyokoInn.config)
                ToyokoInn.hotels.append(hotel)

        if isinstance(name, unicode):
            name = name.encode('utf-8')

        if id is not None:
            hotel = ToyokoInn.__search_hotel_by_id(str(id))

        elif name is not None:
            hotel = ToyokoInn.__search_hotel_by_name(name)

        return hotel


if __name__ == '__main__':
    hotel = ToyokoInn(u"札幌すすきの交差点")
    rooms = hotel.rooms()
    for r in rooms:
        print r

    next_month = datetime.today() + timedelta(days=30)
    date = {
        'year': next_month.year,
        'month': next_month.month,
        'day': next_month.day
    }
    rooms = hotel.rooms(**date)
    for r in rooms:
        print r
