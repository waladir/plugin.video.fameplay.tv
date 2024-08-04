# -*- coding: utf-8 -*-
import sys
import os
import xbmcgui
import xbmcplugin
import xbmcaddon

import json
from math import ceil
from urllib.parse import quote

from libs.api import call_api
from libs.utils import get_url, get_kodi_version, remove_html_tags

if len(sys.argv) > 1:
    _handle = int(sys.argv[1])

def list_submenu(label, slug, page, id = '', contentId = ''):
    addon = xbmcaddon.Addon()
    params = {'id' : id, 'contentId' : contentId}
    page = int(page)
    page_size = int(addon.getSetting('page_size'))

    xbmcplugin.setPluginCategory(_handle, label)
    data = call_api(url = 'https://yarp.vpapps.gjirafa.tech/page?url=fameplay.tv/' + slug)
    if 'success' not in data or data['success'] != True or 'errors' not in data or len(data['errors']) > 0:
        xbmcgui.Dialog().notification('Fameplay.tv', 'Chyba při načtení dat', xbmcgui.NOTIFICATION_ERROR, 5000)
        sys.exit()
    pageId = data['result']['id']
    if id == 'None' and contentId == 'None':
        if data['result']['content'] is None:
            contentId = None
        else:
            contentId = data['result']['content']['contentId']
        for tab in data['result']['layout']['desktop']['rows'][1]['children'][0]['children'][0]['tabs']:
            if tab['layout'][0]['props']['parentQueryId'] is not None:
                parentId = tab['layout'][0]['props']['parentQueryId']
                subId = tab['layout'][0]['props']['query']['id']
            else:
                id = tab['layout'][0]['props']['query']['id']
        if page == 1:
            for query in data['result']['queries']:
                if query['id'] == parentId and query['contentId'] == contentId:
                    for item in query['data']:
                        list_item = xbmcgui.ListItem(label = item['title'])
                        url = get_url(action='list_submenu', label = label + ' / ' + item['title'], slug = slug, page = 1, id = subId, contentId = item['contentId'])  
                        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    if id != 'None':
        if slug == 'porady':
            sort = '3'
        else:
            sort = '1'
        if contentId is None:
            url = 'https://yarp.vpapps.gjirafa.tech/query/' + id +  '?take=' + str(page_size) + '&skip=' + str((page-1)*page_size) + '&sort=' + sort + '&defaultSort=1&pageId=' + pageId
        else:        
            url = 'https://yarp.vpapps.gjirafa.tech/query/' + id +  '?contentId=' + contentId + '&take=' + str(page_size) + '&skip=' + str((page-1)*page_size) + '&sort=' + sort + '&defaultSort=1&pageContentId=' + contentId + '&pageId=' + pageId
        data = call_api(url = url)
        if 'success' not in data or data['success'] != True or 'errors' not in data or len(data['errors']) > 0:
            xbmcgui.Dialog().notification('Fameplay.tv', 'Chyba při načtení položek', xbmcgui.NOTIFICATION_ERROR, 5000)
            sys.exit()
        total = data['result']['total']
        pages = ceil(total/page_size)

        if page > 1:
            list_item = xbmcgui.ListItem(label = 'Předchozí strana (' + str(page-1) + '/' + str(pages) + ')')
            url = get_url(action='list_submenu', label = label, slug = slug, page = page-1, id = params['id'], contentId = params['contentId'])  
            xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
        for item in data['result']['data']:
            if 'isMedia' in item and item['isMedia'] == True:
                list_item = xbmcgui.ListItem(label = item['title'])
                url = get_url(action='play_stream', url = item['url'])  
                list_item.setContentLookup(False)          
                list_item.setProperty('IsPlayable', 'true')
                if get_kodi_version() >= 20:
                    infotag = list_item.getVideoInfoTag()
                    infotag.setMediaType('movie')
                    if 'description' in item and item['description'] is not None:
                        infotag.setPlot(remove_html_tags(item['description']))
                else:
                    list_item.setInfo('video', {'mediatype' : 'movie'})
                    if 'description' in item and item['description'] is not None:
                        list_item.setInfo('video', {'plot': remove_html_tags(item['description'])})            
                if 'thumbnail' in item:
                    list_item.setArt({'thumb': item['thumbnail']}) 
                xbmcplugin.addDirectoryItem(_handle, url, list_item, False)
            elif 'groupId' in item:
                list_item = xbmcgui.ListItem(label = item['title'])
                url = get_url(action='list_submenu', label = item['title'], slug = item['url'], page = 1, id = 'None', contentId = 'None')  
                image = None
                if 'cardImages' in item and 'ar1_1' in item['cardImages']:
                    image = item['cardImages']['ar1_1']
                    list_item.setArt({'thumb': image}) 
                list_item.addContextMenuItems([('Přidat do oblíbených Fameplay.tv', 'RunPlugin(plugin://plugin.video.fameplay.tv?action=add_favourite&item=' + quote(json.dumps({item['url'] : {'title' : item['title'], 'image' : image}})) + ')',)], replaceItems = True)        
                xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
        if page < pages:
            list_item = xbmcgui.ListItem(label = 'Následující strana (' + str(page+1) + '/' + str(pages) + ')')
            url = get_url(action='list_submenu', label = label, slug = slug, page = page+1, id = params['id'], contentId = params['contentId'])  
            xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    xbmcplugin.endOfDirectory(_handle, cacheToDisc = False) 

def list_menu():
    addon = xbmcaddon.Addon()    
    icons_dir = os.path.join(addon.getAddonInfo('path'), 'resources','images')

    list_item = xbmcgui.ListItem(label = 'Nejnovější videa')
    url = get_url(action='list_submenu', label = 'Nejnovější videa', slug = '/nejnovejsi-videa', page = 1, id = 'None', contentId = 'None')  
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    list_item = xbmcgui.ListItem(label = 'Všechny pořady')
    url = get_url(action='list_submenu', label = 'Všechny pořady', slug = '/porady', page = 1, id = 'None', contentId = 'None')  
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    list_item = xbmcgui.ListItem(label = 'Kategorie')
    url = get_url(action='list_submenu', label = 'Kategorie', slug = '/kategorie', page = 1, id = 'None', contentId = 'None')  
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)

    list_item = xbmcgui.ListItem(label = 'Oblíbené pořady')
    url = get_url(action='list_favourites', label = 'Oblíbené pořady')  
    list_item.setArt({ 'thumb' : os.path.join(icons_dir , 'favourites.png'), 'icon' : os.path.join(icons_dir , 'favourites.png') })    
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)

    list_item = xbmcgui.ListItem(label = 'Vyhledávání')
    url = get_url(action='list_search', label = 'Vyhledávání')  
    list_item.setArt({ 'thumb' : os.path.join(icons_dir , 'search.png'), 'icon' : os.path.join(icons_dir , 'search.png') })    
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)

    data = call_api(url = 'https://yarp.vpapps.gjirafa.tech/page?url=fameplay.tv/')
    if 'success' not in data or data['success'] != True or 'errors' not in data or len(data['errors']) > 0:
        xbmcgui.Dialog().notification('Fameplay.tv', 'Chyba při načtení menu', xbmcgui.NOTIFICATION_ERROR, 5000)
        sys.exit()


    for row in data['result']['layout']['desktop']['rows']:
        for child_row in row['children']:
            for child in child_row['children']:
                if child['type'] == 'ContentGrid':
                    list_item = xbmcgui.ListItem(label = child['props']['title'])
                    url = get_url(action='list_submenu', label = child['props']['title'], slug = child['props']['linkData']['url'], page = 1, id = 'None', contentId = 'None')  
                    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.endOfDirectory(_handle, cacheToDisc = False) 
