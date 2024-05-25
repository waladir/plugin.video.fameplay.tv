# -*- coding: utf-8 -*-
import json

from urllib.request import urlopen, Request
from urllib.error import HTTPError

def call_api(url, data = None, method = None):
    headers = {'X-Project-Id' : 'Z6wMB4kEl2n', 'X-Project-Domain' : 'fameplay.tv', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0', 'Accept': 'application/json; charset=utf-8', 'Content-type' : 'application/json;charset=UTF-8'}
    if data != None:
        data = json.dumps(data).encode("utf-8")
    if method is not None:
        request = Request(url = url, data = data, method = method, headers = headers)
    else:
        request = Request(url = url, data = data, headers = headers)
    try:
        html = urlopen(request).read()
        if html and len(html) > 0:
            data = json.loads(html)
            return data
        else:
            return []
    except HTTPError as e:
        return { 'err' : e.reason }    