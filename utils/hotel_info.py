#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__ = '12 02, 2016 '
__author__ = 'mkfsn'


import requests
import json
import re


def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def fetch():
    url = "http://www.toyoko-inn.com/"
    r = requests.get(url)

    try:
        var = re.search('var hotelInfo = (.*)\r', r.text).groups()[0]
    except:
        import sys
        sys.stderr.write("Fail to extract `hotelInfo' in webpage : %s\n" % url)
        sys.stderr.flush()
        raise

    data = json.loads(var)
    return byteify(data)


if __name__ == '__main__':
    data = fetch()
    o_file = open("hotel.json", "w")
    json.dump(data, o_file, ensure_ascii=False, indent=4)
    o_file.close()
