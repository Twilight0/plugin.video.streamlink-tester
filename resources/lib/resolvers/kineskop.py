import re

from streamlink.plugin import Plugin
from streamlink.plugin.api import http
from streamlink.stream import HLSStream
from streamlink.plugin.api.useragents import CHROME


class Kineskop(Plugin):

    url_re = re.compile(r"http://kineskop\.tv/\?page=watch&ch=(\d{3})")
    src_re = re.compile(r"getURLParam\('src','(.+?)'")

    @classmethod
    def can_handle_url(cls, url):

        return cls.url_re.match(url)

    def _get_streams(self):

        headers = {'User-Agent': CHROME}

        res = http.get(self.url, headers=headers)

        stream = self.src_re.search(res.text).group(1)

        if stream:

            headers.update({'Referer': self.url, 'Origin': 'http://kineskop.tv/'})

            result = HLSStream.parse_variant_playlist(self.session, stream, headers=headers)

            return result


__plugin__ = Kineskop
