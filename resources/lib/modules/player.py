# -*- coding: utf-8 -*-

'''
    Streamlink Tester Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from __future__ import print_function

import traceback, sys, json
from tulip.compat import urlencode
from tulip import control, directory
from tulip.log import log_debug
from .tools import stream_picker
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

        log_debug('Did not find matching plugin')

        return url

    except streamlink.session.PluginError as e:

        _, __, tb = sys.exc_info()

        print(traceback.print_tb(tb))

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
