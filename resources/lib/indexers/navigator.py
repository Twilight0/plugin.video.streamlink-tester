# -*- coding: utf-8 -*-

'''
    Streamlink Tester Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from tulip import directory, control
from resources.lib.modules import tools


def root():

    add_cm = {'title': 30009, 'query': {'action': 'add'}}
    refresh_cm = {'title': 30005, 'query': {'action': 'refresh'}}
    clear_cm = {'title': 30010, 'query': {'action': 'clear_history'}}

    null = {
        'title': control.lang(30009),
        'action': 'add',
        'cm': [add_cm, refresh_cm],
        'isFolder': 'False', 'isPlayable': 'False'
    }

    urls = tools.read_from_history()

    if not urls:

        directory.add([null])

    else:

        menu = [{'title': url, 'action': 'play', 'isFolder': 'False', 'url': url} for url in urls]

        menu.insert(0, null)

        for m in menu:

            try:

                clear_fm_h_cm = {'title': 30013, 'query': {'action': 'delete_from_history', 'query': m['url']}}
                set_title_cm = {'title': 30014, 'query': {'action': 'play', 'query': 'input', 'url': m['url']}}

                m.update({'cm': [add_cm, refresh_cm, clear_cm, clear_fm_h_cm, set_title_cm]})

            except KeyError:

                pass

        directory.add(menu)
