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
        streams = {}
        for stream in data['result']['media']['model']['assets'][0]['streams']:
            streams.update({int(stream['qualityType'].replace('i','').replace('p','')): stream['url']})
        if len(streams) > 0:
            for stream in sorted(streams):
                url = streams[stream]
            list_item = xbmcgui.ListItem(path = url)
            list_item.setContentLookup(False)       
            xbmcplugin.setResolvedUrl(_handle, True, list_item)