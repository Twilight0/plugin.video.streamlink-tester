# -*- coding: utf-8 -*-

'''
    License summary below, for more details please read license.txt file

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 2 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote


from tulip import control, directory
from resources.lib.modules.tools import stream_picker
from resources.lib import quality
import streamlink.session

# TODO: Add ability to set plugin and session options


def router(url):

    try:

        if '.mpd' in url:
            return url

        session = streamlink.session.Streamlink()
        # session.set_plugin_option('', '', '')

        plugin = session.resolve_url(url)
        # plugin.set_option()
        streams = plugin.streams()

        if not streams:
            return url

        try:

            args = streams['best'].args

            if 'headers' in args and control.setting('args.append') == 'true':
                user_agent = quote(streams['best'].args['headers'].get('User-Agent', ''))
                referer = quote(streams['best'].args['headers'].get('Referer', ''))
                if user_agent and referer:
                    append = '|User-Agent={0}&Referer={1}'.format(user_agent, referer)
                elif user_agent:
                    append = '|User-Agent={0}'.format(user_agent)
                elif referer:
                    append = '|Referer={0}'.format(referer)
                else:
                    append = ''
            else:
                append = ''

        except AttributeError:

            append = ''

        if quality is None:

            if control.setting('quality.choice') == '0':

                playable = streams['best'].to_url() + append

                return playable

            else:

                keys = streams.keys()[::-1]
                values = [u.to_url() + append for u in streams.values()][::-1]

                return stream_picker(keys, values)

        else:

            if quality == 'manual':

                keys = streams.keys()[::-1]
                values = [u.to_url() + append for u in streams.values()][::-1]

                return stream_picker(keys, values)

            else:

                try:

                    return streams[quality].to_url() + append

                except KeyError:

                    return streams['best'].to_url() + append

    except streamlink.session.NoPluginError:

        return url

    except streamlink.session.PluginError as e:

        control.infoDialog(e, time=5000)


def play(url):

    stream = router(url)

    try:

        if '.mpd' in stream:

            directory.resolve(stream, dash=True)

        else:

            directory.resolve(stream)

    except:

        pass
