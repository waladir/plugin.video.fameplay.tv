# -*- coding: utf-8 -*-
import sys
import xbmc
from urllib.parse import urlencode

_url =  sys.argv[0]

def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def get_kodi_version():
    return int(xbmc.getInfoLabel('System.BuildVersion').split('.')[0])

def remove_html_tags(text):
    import re
    import html
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html.unescape(str(text)))