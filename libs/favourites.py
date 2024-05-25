# -*- coding: utf-8 -*-
import sys
import os
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
from xbmcvfs import translatePath

import codecs
import json
from urllib.parse import quote

from libs.utils import get_url

if len(sys.argv) > 1:
    _handle = int(sys.argv[1])

def add_favourite(item):  
    item = json.loads(item)
    addon = xbmcaddon.Addon()
    addon_userdata_dir = translatePath(addon.getAddonInfo('profile'))
    if not os.path.exists(addon_userdata_dir):
        os.makedirs(addon_userdata_dir)    
    filename = os.path.join(addon_userdata_dir, 'favourites.txt')
    favourites = get_favourites()
    if item not in favourites:
        favourites.append(item)
        try:
            with codecs.open(filename, 'w', encoding='utf-8') as file:
                file.write('%s\n' % json.dumps(favourites))        
        except IOError as error:
            xbmcgui.Dialog().notification('Fameplay.tv', 'Chyba při uložení oblíbených pořadů', xbmcgui.NOTIFICATION_ERROR, 5000)            
        xbmcgui.Dialog().notification('Fameplay.tv', 'Pořad byl přidaný do oblíbených', xbmcgui.NOTIFICATION_INFO, 5000)
    else:
        xbmcgui.Dialog().notification('Fameplay.tv', 'Pořad je již v oblíbených', xbmcgui.NOTIFICATION_ERROR, 5000)

def remove_favourite(item):
    item = json.loads(item)
    addon = xbmcaddon.Addon()
    addon_userdata_dir = translatePath(addon.getAddonInfo('profile'))
    if not os.path.exists(addon_userdata_dir):
        os.makedirs(addon_userdata_dir)    
    filename = os.path.join(addon_userdata_dir, 'favourites.txt')
    favourites = get_favourites()
    favourites.remove(item)
    try:
        with codecs.open(filename, 'w', encoding='utf-8') as file:
            file.write('%s\n' % json.dumps(favourites))        
    except IOError as error:
        xbmcgui.Dialog().notification('Fameplay.tv', 'Chyba při uložení oblíbených pořadů', xbmcgui.NOTIFICATION_ERROR, 5000)            
    xbmc.executebuiltin('Container.Refresh')

def get_favourites():
    addon = xbmcaddon.Addon()
    addon_userdata_dir = translatePath(addon.getAddonInfo('profile'))
    if not os.path.exists(addon_userdata_dir):
        os.makedirs(addon_userdata_dir)    
    filename = os.path.join(addon_userdata_dir, 'favourites.txt')
    data = None
    try:
        with codecs.open(filename, 'r', encoding='utf-8') as file:
            for row in file:
                data = row[:-1]
    except IOError as error:
        if error.errno != 2:
            xbmcgui.Dialog().notification('Fameplay.tv', 'Chyba při načtení oblíbených pořadů', xbmcgui.NOTIFICATION_ERROR, 5000)
            sys.exit()
    if data is not None:
        favourites = json.loads(data)
    else:
        favourites = []
    return favourites

def list_favourites(label):
    xbmcplugin.setPluginCategory(_handle, label)
    favourites = get_favourites()
    for item in favourites:
        for key in item:
            list_item = xbmcgui.ListItem(label = item[key]['title'])
            url = get_url(action='list_submenu', label = item[key]['title'], slug = key, page = 1, id = 'None', contentId = 'None')  
            if item[key]['image'] is not None:
                list_item.setArt({'thumb': item[key]['image']}) 
            list_item.addContextMenuItems([('Odstranění zoblíbených Fameplay.tv', 'RunPlugin(plugin://plugin.video.fameplay.tv?action=remove_favourite&item=' + quote(json.dumps({key : {'title' : item[key]['title'], 'image' : item[key]['image']}})) + ')',)], replaceItems = True)        
            xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    xbmcplugin.endOfDirectory(_handle) 