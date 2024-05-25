# -*- coding: utf-8 -*-
import sys
import os

import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
from xbmcvfs import translatePath

import codecs
from urllib.parse import quote

from libs.api import call_api
from libs.utils import get_url, get_kodi_version, remove_html_tags

if len(sys.argv) > 1:
    _handle = int(sys.argv[1])

def list_search(label):
    list_item = xbmcgui.ListItem(label='Nové hledání')
    url = get_url(action='list_search_results', query = '-----', label = label + ' / ' + 'Nové hledání')  
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    history = load_search_history()
    for item in history:
        list_item = xbmcgui.ListItem(label=item)
        url = get_url(action='list_search_results', query = item, label = label + ' / ' + item)  
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    xbmcplugin.endOfDirectory(_handle,cacheToDisc = False)

def list_search_results(query, label):
    xbmcplugin.setPluginCategory(_handle, label)
    xbmcplugin.setContent(_handle, 'movies')
    if query == '-----':
        input = xbmc.Keyboard('', 'Hledat')
        input.doModal()
        if not input.isConfirmed(): 
            return
        query = input.getText()
        if len(query) == 0:
            xbmcgui.Dialog().notification('Fameplay.tv', 'Je potřeba zadat vyhledávaný řetězec', xbmcgui.NOTIFICATION_ERROR, 5000)
            return   
    save_search_history(query)
    data = call_api(url = 'https://yarp.vpapps.gjirafa.tech/search?q=' + quote(query))
    if 'response' not in data :
        xbmcgui.Dialog().notification('Fameplay.tv', 'Chyba při vyhledávání', xbmcgui.NOTIFICATION_ERROR, 5000)
        sys.exit()
    if len(data['response']) > 0:
        for item in data['response']:
            if 'isMedia' in item and item['isMedia'] == True:
                list_item = xbmcgui.ListItem(label = item['title'])
                url = get_url(action='play_stream', url = item['url'])  
                list_item.setContentLookup(False)          
                list_item.setProperty('IsPlayable', 'true')
                if get_kodi_version() >= 20:
                    infotag = list_item.getVideoInfoTag()
                    infotag.setMediaType('movie')
                    if 'description' in item:
                        infotag.setPlot(remove_html_tags(item['description']))
                else:
                    list_item.setInfo('video', {'mediatype' : 'movie'})
                    if 'description' in item:
                        list_item.setInfo('video', {'plot': remove_html_tags(item['description'])})            
                if 'thumbnail' in item:
                    list_item.setArt({'thumb': item['thumbnail']}) 
                xbmcplugin.addDirectoryItem(_handle, url, list_item, False)
            elif 'groupId' in item:
                list_item = xbmcgui.ListItem(label = item['title'])
                url = get_url(action='list_submenu', label = item['title'], slug = item['url'], page = 1, id = 'None', contentId = 'None')  
                if 'cardImages' in item and 'ar1_1' in item['cardImages']:
                    list_item.setArt({'thumb': item['cardImages']['ar1_1']}) 
                xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
        xbmcplugin.endOfDirectory(_handle, cacheToDisc = False) 
    else:
        xbmcgui.Dialog().notification('Fameplay.tv','Nic nenalezeno', xbmcgui.NOTIFICATION_INFO, 3000)        

def save_search_history(query):
    addon = xbmcaddon.Addon()
    addon_userdata_dir = translatePath(addon.getAddonInfo('profile')) 
    if not os.path.exists(addon_userdata_dir):
        os.makedirs(addon_userdata_dir)    
    max_history = 10
    cnt = 0
    history = []
    filename = addon_userdata_dir + 'search_history.txt'
    try:
        with codecs.open(filename, 'r') as file:
            for line in file:
                item = line[:-1]
                if item != query:
                    history.append(item)
    except IOError:
        history = []
    history.insert(0,query)
    with codecs.open(filename, 'w') as file:
        for item  in history:
            cnt = cnt + 1
            if cnt <= max_history:
                file.write('%s\n' % item)

def load_search_history():
    history = []
    addon = xbmcaddon.Addon()
    addon_userdata_dir = translatePath(addon.getAddonInfo('profile')) 
    if not os.path.exists(addon_userdata_dir):
        os.makedirs(addon_userdata_dir)    
    filename = addon_userdata_dir + 'search_history.txt'
    try:
        with codecs.open(filename, 'r') as file:
            for line in file:
                item = line[:-1]
                history.append(item)
    except IOError:
        history = []
    return history