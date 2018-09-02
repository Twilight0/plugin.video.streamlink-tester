#### Broken resolver ####


# import re, time
#
# from streamlink.plugin import Plugin
# from streamlink.plugin.api.utils import itertags
# from streamlink.plugin.api import http
# from streamlink.stream import HTTPStream
# from streamlink.plugin.api.useragents import CHROME
# from streamlink.compat import OrderedDict
#
#
# class Vidto(Plugin):
#     url_re = re.compile(r"https?://vidto\.[sm]e/(\w+)\.html")
#     src_re = re.compile(r'file:"(?P<url>.*?)",label:"(?P<quality>\d{3,4}p)"')
#
#     @classmethod
#     def can_handle_url(cls, url):
#         return cls.url_re.match(url)
#
#     def _get_streams(self):
#
#         headers = {'User-Agent': CHROME}
#
#         get_page = http.get(self.url, headers=headers)
#
#         tags = [{i.attributes['name']: i.attributes['value']} for i in list(itertags(get_page.text, 'input'))[3:]]
#         post_data = OrderedDict(pair for d in tags for pair in d.items())
#         post_data.update({'referer': self.url})
#
#         time.sleep(6)
#
#         post_page = http.post(self.url, headers={'User-Agent': CHROME, 'Referer': self.url}, data=post_data)
#
#         videos = self.src_re.findall(post_page.text)
#
#         if videos:
#             for v, q in videos:
#                 yield q, HTTPStream(self.session, v, headers=headers)
#
#
# __plugin__ = Vidto
