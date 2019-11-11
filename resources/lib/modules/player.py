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

import traceback, sys, json
from tulip.compat import urlencode
from tulip import control, directory
from tulip.log import log_debug
from resources.lib.modules.tools import stream_picker
import streamlink.session

# TODO: Add ability to set plugin and session options


def resolver(url, quality=None):

    try:

        if '.mpd' in url:
            return url

        custom_plugins = control.join(control.addonPath, 'resources', 'lib', 'resolvers')
        session = streamlink.session.Streamlink()
        session.load_plugins(custom_plugins)
        # session.set_plugin_option('', '', '')

        plugin = session.resolve_url(url)
        # plugin.set_option()
        streams = plugin.streams()

        if not streams:
            return url

        try:

            try:
                args = streams['best'].args
            except Exception:
                args = None

            try:
                json_dict = json.loads(streams['best'].json)
            except Exception:
                json_dict = None

            for h in args, json_dict:

                try:
                    if 'headers' in h:
                        headers = h['headers']
                        break
                    else:
                        headers = None
                except Exception:
                    headers = None

            # if json_dict:
            #
            #     try:
            #         headers = json_dict['headers']
            #     except KeyError:
            #         headers = None
            #
            # elif args:
            #
            #     try:
            #         headers = args['headers']
            #     except KeyError:
            #         headers = None
            #
            # else:
            #
            #     headers = None

            if headers and control.setting('args_append') == 'true':

                try:
                    del headers['Connection']
                    del headers['Accept-Encoding']
                    del headers['Accept']
                except KeyError:
                    pass

                append = ''.join(['|', urlencode(headers)])

            else:

                append = ''

        except AttributeError:

            append = ''

        if quality is None:

            if control.setting('quality_choice') == '0':

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

        _, __, tb = sys.exc_info()

        print traceback.print_tb(tb)

        control.infoDialog(e, time=5000)


def play(url, meta=None, quality=None, image=None):

    if meta:

        control.busy()

    stream = resolver(url, quality)

    try:
        isa_enabled = control.addon_details('inputstream.adaptive').get('enabled')
    except KeyError:
        isa_enabled = False

    dash = ('.mpd' in stream or 'dash' in stream or '.ism' in stream or '.hls' in stream or '.m3u8' in stream) and isa_enabled

    mimetype = None

    if meta:

        control.idle()

    if isinstance(meta, dict):

        if meta['title'] == 'input':

            title = control.inputDialog()

            meta['title'] = title

    if dash and control.setting('disable_mpd') == 'false':

        if '.hls' in stream or 'm3u8' in stream:
            manifest_type = 'hls'
            mimetype = 'application/vnd.apple.mpegurl'
        elif '.ism' in stream:
            manifest_type = 'ism'
        else:
            manifest_type = 'mpd'

        log_debug('Activating MPEG-DASH for this url: ' + stream)

        directory.resolve(
            stream, meta=meta, icon=image, dash=dash, manifest_type=manifest_type, mimetype=mimetype,
            resolved_mode=meta is None
        )

    else:

        directory.resolve(
            stream, meta=meta, icon=image, resolved_mode=meta is None
        )
