# -*- coding: utf-8 -*-

'''
    Streamlink Tester Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from tulip.init import params

action = params.get('action')
url = params.get('url')
quality = params.get('quality')
query = params.get('query')
title = params.get('title')
image = params.get('image')
# options = params.get('options')


if action is None:
    from resources.lib.indexers import navigator
    navigator.root()

elif action == 'play':
    from resources.lib.modules import player
    if query:
        query = {'title': query}
    player.play(url, query, quality, image)

elif action == 'add':
    from resources.lib.modules import tools
    tools.add_to_history()

elif action == 'readme':
    from resources.lib.modules import tools
    tools.readme()

elif action == 'refresh':
    from tulip.control import refresh
    refresh()

elif action == 'clear_history':
    from resources.lib.modules import tools
    tools.clear_history()

elif action == 'delete_from_history':
    from resources.lib.modules import tools
    tools.delete_from_history(query)
