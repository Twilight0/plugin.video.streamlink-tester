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

from tulip import control
from tulip import directory
from resources.lib.modules.tools import stream_picker
from resources.lib import quality
import streamlink.session

# TODO: Add ability to set plugin options


def router(url):

    try:

        if '.mpd' in url:
            return url

        session = streamlink.session.Streamlink()

        plugin = session.resolve_url(url)
        streams = plugin.streams()

        if not streams:
            return

        try:

            if quality is None:

                if control.setting('quality.choice') == '0':

                    return streams['best'].url

                else:

                    keys = streams.keys()[::-1]
                    values = [u.url for u in streams.values()][::-1]

                    return stream_picker(keys, values)

            else:

                if quality == 'manual':

                    keys = streams.keys()[::-1]
                    values = [u.url for u in streams.values()][::-1]

                    return stream_picker(keys, values)

                else:

                    try:

                        return streams[quality].url

                    except KeyError:

                        return streams['best'].url

        except AttributeError:

            return streams['best'].mpd.url

    except streamlink.session.NoPluginError:

        return url

    except streamlink.session.PluginError as e:

        control.infoDialog(e)


def play(url):

    stream = router(url)

    try:

        if '.mpd' in stream:

            directory.resolve(stream, dash=True)

        else:

            directory.resolve(stream)

    except:

        pass
