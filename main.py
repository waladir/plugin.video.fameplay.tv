# -*- coding: utf-8 -*-
import sys

from urllib.parse import parse_qsl

from libs.lists import list_menu, list_submenu
from libs.search import list_search, list_search_results
from libs.favourites import add_favourite, remove_favourite, list_favourites
from libs.stream import play_stream

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'list_submenu':
            list_submenu(label = params['label'], slug = params['slug'], page = params['page'], id = params['id'], contentId = params['contentId'])
        elif params['action'] == 'play_stream':
            play_stream(url = params['url'])
        elif params['action'] == 'list_search':
            list_search(label = params['label'])
        elif params['action'] == 'list_search_results':
            list_search_results(query = params['query'], label = params['label'])
        elif params['action'] == 'add_favourite':
            add_favourite(item = params['item'])
        elif params['action'] == 'remove_favourite':
            remove_favourite(item = params['item'])
        elif params['action'] == 'list_favourites':
            list_favourites(label = params['label'])
        else:
            raise ValueError('Neznámý parametr: {0}!'.format(paramstring))
    else:
         list_menu()

if __name__ == '__main__':
    router(sys.argv[2][1:])
