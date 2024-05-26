# -*- coding: utf-8 -*-
import sys

import xbmcgui
import xbmcplugin

from libs.api import call_api

if len(sys.argv) > 1:
    _handle = int(sys.argv[1])

def play_stream(url):
    data = call_api(url = 'https://yarp.vpapps.gjirafa.tech/page?url=fameplay.tv/' + url)
    if 'success' in data and data['success'] == True and 'errors' in data or len(data['errors']) == 0:
        url = data['result']['media']['model']['assets'][0]['rootUrl']
        list_item = xbmcgui.ListItem(path = url)
        list_item.setContentLookup(False)       
        xbmcplugin.setResolvedUrl(_handle, True, list_item)
