# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib,urllib2,urlparse,re,os,datetime,base64,xbmcaddon

try:
    import CommonFunctions as common
except:
    import commonfunctionsdummy as common
try:
    import json
except:
    import simplejson as json


class getUrl(object):
    def __init__(self, url, close=True, proxy=None, post=None, mobile=False, referer=None, cookie=None, output='', timeout='5'):
        if not proxy == None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
            opener = urllib2.install_opener(opener)
        if not post == None:
            request = urllib2.Request(url, post)
        else:
            request = urllib2.Request(url,None)
        if mobile == True:
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
        else:
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20100101 Firefox/34.0')
        if not referer == None:
            request.add_header('Referer', referer)
        if not cookie == None:
            request.add_header('cookie', cookie)
        request.add_header('Accept-Language', 'en-US')
        response = urllib2.urlopen(request, timeout=int(timeout))
        if output == 'cookie':
            result = str(response.headers.get('Set-Cookie'))
        elif output == 'geturl':
            result = response.geturl()
        else:
            result = response.read()
        if close == True:
            response.close()
        self.result = result

class uniqueList(object):
    def __init__(self, list):
        uniqueSet = set()
        uniqueList = []
        for n in list:
            if n not in uniqueSet:
                uniqueSet.add(n)
                uniqueList.append(n)
        self.list = uniqueList

class cleantitle:
    def movie(self, title):
        title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def tv(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU|\d{4})(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title


class icefilms:
    def __init__(self):
        self.base_link = 'https://ipv6.icefilms.info'
        self.proxy_link_1 = 'http://proxy.cyberunlocker.com/browse.php?u=http://www.icefilms.info'
        self.proxy_link_2 = 'http://9proxy.in/b.php?b=20&u=http://www.icefilms.info'
        self.proxy_link_3 = 'https://icefilms.unblocked.pw'
        self.moviesearch_link = '/movies/a-z/%s'
        self.tvsearch_link = '/tv/a-z/%s'
        self.video_link = '/membersonly/components/com_iceplayer/video.php?vid=%s'
        self.resp_link = '/membersonly/components/com_iceplayer/video.phpAjaxResp.php'

    def get_movie(self, imdb, title, year):
        try:
            query = title.upper()
            if query.startswith('THE '): query = query.replace('THE ', '')
            elif query.startswith('A '): query = query.replace('A ', '')
            if not query[0].isalpha(): query = '1'
            query = self.moviesearch_link % query[0]

            base_link = self.base_link
            try: result = getUrl(base_link + query, referer=base_link).result
            except: result = ''

            proxies = [self.proxy_link_1, self.proxy_link_2, self.proxy_link_3]
            for proxy in proxies:
                if "submenu" in result: break
                base_link = proxy
                try: result = getUrl(base_link + query, referer=base_link).result
                except: result = ''

            result = result.decode('iso-8859-1').encode('utf-8')
            result = re.compile('id=%s>.+?href=(.+?)>' % imdb).findall(result)[0]

            url = self.base_link + result
            url = 'http' + urllib.unquote_plus(url).rsplit('http', 1)[-1].split('&', 1)[0]
            url = urlparse.urlparse(url).path + '?' + urlparse.urlparse(url).query
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            query = show.upper()
            if query.startswith('THE '): query = query.replace('THE ', '')
            elif query.startswith('A '): query = query.replace('A ', '')
            if not query[0].isalpha(): query = '1'
            query = self.tvsearch_link % query[0]

            base_link = self.base_link
            try: result = getUrl(base_link + query, referer=base_link).result
            except: result = ''

            proxies = [self.proxy_link_1, self.proxy_link_2, self.proxy_link_3]
            for proxy in proxies:
                if "submenu" in result: break
                base_link = proxy
                try: result = getUrl(base_link + query, referer=base_link).result
                except: result = ''

            result = result.decode('iso-8859-1').encode('utf-8')
            result = re.compile('id=%s>.+?href=(.+?)>' % imdb).findall(result)[0]

            url = self.base_link + result
            url = 'http' + urllib.unquote_plus(url).rsplit('http', 1)[-1].split('&', 1)[0]
            url = urlparse.urlparse(url).path
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            base_link = self.base_link
            try: result = getUrl(base_link + url, referer=base_link).result
            except: result = ''

            proxies = [self.proxy_link_1, self.proxy_link_2, self.proxy_link_3]
            for proxy in proxies:
                if "ip.php" in result: break
                base_link = proxy
                try: result = getUrl(base_link + url, referer=base_link).result
                except: result = ''

            result = result.decode('iso-8859-1').encode('utf-8')
            result = urllib.unquote_plus(result)

            url = re.compile('(/ip[.]php.+?>%01dx%02d)' % (int(season), int(episode))).findall(result)[0]
            url = re.compile('(/ip[.]php.+?)&').findall(url)[-1]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            t = url.split('v=', 1)[-1].rsplit('&', 1)[0] 
            url = self.video_link % t

            base_link = self.base_link
            try: result = getUrl(base_link + url, referer=base_link).result
            except: result = ''

            proxies = [self.proxy_link_1, self.proxy_link_2, self.proxy_link_3]
            for proxy in proxies:
                if "ripdiv" in result: break
                base_link = proxy
                try: result = getUrl(base_link + url, referer=base_link).result
                except: result = ''

            result = result.decode('iso-8859-1').encode('utf-8')
            sec = re.compile('lastChild[.]value="(.+?)"').findall(result)[0]
            links = common.parseDOM(result, "div", attrs = { "class": "ripdiv" })

            import random

            try:
                hd_links = ''
                hd_links = [i for i in links if '>HD 720p<' in i][0]
                hd_links = re.compile("onclick='go[(](.+?)[)]'>Source(.+?)</a>").findall(hd_links)
            except:
                pass

            for id, host in hd_links:
                try:
                    host = re.sub('<.+?>|</.+?>|#\d*:','', host)
                    host = host.strip().lower()
                    if not host in hosthdDict: raise Exception()
                    url = 'id=%s&t=%s&sec=%s&s=%s&m=%s&cap=&iqs=&url=' % (id, t, sec, random.randrange(5, 50), random.randrange(100, 300) * -1)
                    sources.append({'source': host, 'quality': 'HD', 'provider': 'Icefilms', 'url': url})
                except:
                    pass

            try:
                sd_links = ''
                sd_links = [i for i in links if '>DVDRip / Standard Def<' in i]
                if len(sd_links) == 0: sd_links = [i for i in links if '>DVD Screener<' in i]
                if len(sd_links) == 0: sd_links = [i for i in links if '>R5/R6 DVDRip<' in i]
                sd_links = sd_links[0]
                sd_links = re.compile("onclick='go[(](.+?)[)]'>Source(.+?)</a>").findall(sd_links)
            except:
                pass

            for id, host in sd_links:
                try:
                    host = re.sub('<.+?>|</.+?>|#\d*:','', host)
                    host = host.strip().lower()
                    if not host in hostDict: raise Exception()
                    url = 'id=%s&t=%s&sec=%s&s=%s&m=%s&cap=&iqs=&url=' % (id, t, sec, random.randrange(5, 50), random.randrange(100, 300) * -1)
                    sources.append({'source': host, 'quality': 'SD', 'provider': 'Icefilms', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            post = url
            url = self.resp_link

            base_link = self.base_link + url
            try: result = getUrl(base_link, referer=base_link, post=post).result
            except: result = ''

            proxies = [self.proxy_link_1, self.proxy_link_2, self.proxy_link_3]
            for proxy in proxies:
                if "com_iceplayer" in result: break
                base_link = proxy + url
                try: result = getUrl(base_link, referer=base_link, post=post).result
                except: pass

            url = result.split("?url=", 1)[-1].split("<", 1)[0]
            url = urllib.unquote_plus(url)

            import commonresolvers
            url = commonresolvers.get(url)
            return url
        except:
            return

class primewire:
    def __init__(self):
        self.base_link = 'http://www.primewire.ag'
        self.proxy_link_1 = 'http://proxy.cyberunlocker.com/browse.php?u=http://www.primewire.ag'
        self.proxy_link_2 = 'http://9proxy.in/b.php?b=20&u=http://www.primewire.ag'
        self.proxy_link_3 = 'https://primewire.unblocked.pw'
        self.key_link = '/index.php?search'
        self.moviesearch_link = '/index.php?search_keywords=%s&key=%s&search_section=1'
        self.tvsearch_link = '/index.php?search_keywords=%s&key=%s&search_section=2'

    def get_movie(self, imdb, title, year):
        try:
            base_link = self.base_link
            try: result = getUrl(base_link + self.key_link, referer=base_link, mobile=True).result
            except: result = ''

            proxies = [self.proxy_link_1, self.proxy_link_2, self.proxy_link_3]
            for proxy in proxies:
                if "searchform" in result: break
                base_link = proxy
                try: result = getUrl(base_link + self.key_link, referer=base_link, mobile=True).result
                except: result = ''

            key = common.parseDOM(result, "input", ret="value", attrs = { "name": "key" })[0]
            query = self.moviesearch_link % (urllib.quote_plus(re.sub('\'', '', title)), key)

            base_link = self.base_link
            try: result = getUrl(base_link + query, referer=base_link, mobile=True).result
            except: result = ''

            proxies = [self.proxy_link_1, self.proxy_link_2, self.proxy_link_3]
            for proxy in proxies:
                if "searchform" in result: break
                base_link = proxy
                try: result = getUrl(base_link + query, referer=base_link, mobile=True).result
                except: result = ''

            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "div", attrs = { "class": "index_item.+?" })

            title = 'watch' + cleantitle().movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "a", ret="title")[0]) for i in result]
            result = [i for i in result if any(x in i[1] for x in years)]

            match = [i[0] for i in result if title == cleantitle().movie(i[1])]

            match2 = [i[0] for i in result]
            match2 = [i.replace(base_link, '') for i in match2]
            match2 = uniqueList(match2).list
            if match2 == []: return

            for i in match2[:5]:
                try:
                    if len(match) > 0:
                        match3 = match[0]
                        break
                    result = getUrl(base_link + i, referer=base_link, mobile=True).result
                    if str('tt' + imdb) in result:
                        match3 = i
                        break
                except:
                    pass

            url = self.base_link + match3
            url = 'http' + urllib.unquote_plus(url).rsplit('http', 1)[-1].split('&', 1)[0]
            url = urlparse.urlparse(url).path
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            base_link = self.base_link
            try: result = getUrl(base_link + self.key_link, referer=base_link, mobile=True).result
            except: result = ''

            proxies = [self.proxy_link_1, self.proxy_link_2, self.proxy_link_3]
            for proxy in proxies:
                if "searchform" in result: break
                base_link = proxy
                try: result = getUrl(base_link + self.key_link, referer=base_link, mobile=True).result
                except: result = ''

            key = common.parseDOM(result, "input", ret="value", attrs = { "name": "key" })[0]
            query = self.tvsearch_link % (urllib.quote_plus(re.sub('\'', '', show)), key)

            base_link = self.base_link
            try: result = getUrl(base_link + query, referer=base_link, mobile=True).result
            except: result = ''

            proxies = [self.proxy_link_1, self.proxy_link_2, self.proxy_link_3]
            for proxy in proxies:
                if "searchform" in result: break
                base_link = proxy
                try: result = getUrl(base_link + query, referer=base_link, mobile=True).result
                except: result = ''

            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "div", attrs = { "class": "index_item.+?" })

            shows = ['watch' + cleantitle().tv(show), 'watch' + cleantitle().tv(show_alt)]
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "a", ret="title")[0]) for i in result]
            result = [i for i in result if any(x in i[1] for x in years)]

            match = [i[0] for i in result if any(x == cleantitle().tv(i[1]) for x in shows)]

            match2 = [i[0] for i in result]
            match2 = [i.replace(base_link, '') for i in match2]
            match2 = uniqueList(match2).list
            if match2 == []: return

            for i in match2[:5]:
                try:
                    if len(match) > 0:
                        match3 = match[0]
                        break
                    result = getUrl(base_link + i, referer=base_link, mobile=True).result
                    if str('tt' + imdb) in result:
                        match3 = i
                        break
                except:
                    pass

            url = self.base_link + match3
            url = 'http' + urllib.unquote_plus(url).rsplit('http', 1)[-1].split('&', 1)[0]
            url = urlparse.urlparse(url).path
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        if url == None: return
        url = url.replace('/watch-','/tv-')
        url += '/season-%01d-episode-%01d' % (int(season), int(episode))
        url = common.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            base_link = self.base_link
            try: result = getUrl(base_link + url, referer=base_link, mobile=True).result
            except: result = ''

            proxies = [self.proxy_link_1, self.proxy_link_2, self.proxy_link_3]
            for proxy in proxies:
                if "choose_tabs" in result: break
                base_link = proxy
                try: result = getUrl(base_link + url, referer=base_link, mobile=True).result
                except: result = ''

            result = result.decode('iso-8859-1').encode('utf-8')
            links = common.parseDOM(result, "tbody")

            for i in links:
                try:
                    url = common.parseDOM(i, "a", ret="href")[0]
                    url = urllib.unquote_plus(url)
                    url = re.compile('url=(.+?)&').findall(url)[0]
                    url = base64.urlsafe_b64decode(url.encode('utf-8'))
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = common.parseDOM(i, "a", ret="href")[0]
                    host = urllib.unquote_plus(host)
                    host = re.compile('domain=(.+?)&').findall(host)[0]
                    host = base64.urlsafe_b64decode(host.encode('utf-8'))
                    host = host.rsplit('.', 1)[0]
                    host = host.strip().lower()
                    if not host in hostDict: raise Exception()
                    host = common.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    quality = common.parseDOM(i, "span", ret="class")[0]
                    if quality == 'quality_cam' or quality == 'quality_ts': quality = 'CAM'
                    elif quality == 'quality_dvd': quality = 'SD'
                    else:  raise Exception()
                    quality = quality.encode('utf-8')

                    sources.append({'source': host, 'quality': quality, 'provider': 'Primewire', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.get(url)
            return url
        except:
            return

class movie25:
    def __init__(self):
        self.base_link = 'http://www.movie25.cm'
        self.proxy_link_1 = 'http://proxy.cyberunlocker.com/browse.php?u=http://www.movie25.cm'
        self.proxy_link_2 = 'http://9proxy.in/b.php?b=20&u=http://www.movie25.cm'
        self.proxy_link_3 = 'https://movie25.unblocked.pw'
        self.search_link = '/search.php?key=%s'

    def get_movie(self, imdb, title, year):
        try:
            query = self.search_link % urllib.quote_plus(title)

            base_link = self.base_link
            try: result = getUrl(base_link + query, referer=base_link).result
            except: result = ''

            proxies = [self.proxy_link_1, self.proxy_link_2, self.proxy_link_3]
            for proxy in proxies:
                if "movie_table" in result: break
                base_link = proxy
                try: result = getUrl(base_link + query, referer=base_link).result
                except: result = ''

            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "div", attrs = { "class": "movie_table" })[0]
            result = common.parseDOM(result, "li")

            title = cleantitle().movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "a")[1]) for i in result]
            result = [i for i in result if any(x in i[1] for x in years)]

            match = [i[0] for i in result if title == cleantitle().movie(i[1])]

            match2 = [i[0] for i in result]
            match2 = [i.replace(base_link, '') for i in match2]
            match2 = uniqueList(match2).list
            if match2 == []: return

            for i in match2[:10]:
                try:
                    if len(match) > 0:
                        match3 = match[0]
                        break
                    result = getUrl(base_link + i, referer=base_link).result
                    if str('tt' + imdb) in result:
                        match3 = i
                        break
                except:
                    pass

            url = self.base_link + match3
            url = 'http' + urllib.unquote_plus(url).rsplit('http', 1)[-1].split('&', 1)[0]
            url = urlparse.urlparse(url).path
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            base_link = self.base_link
            try: result = getUrl(base_link + url, referer=base_link).result
            except: result = ''

            proxies = [self.proxy_link_1, self.proxy_link_2, self.proxy_link_3]
            for proxy in proxies:
                if '"links"' in result: break
                base_link = proxy
                try: result = getUrl(base_link + url, referer=base_link).result
                except: result = ''

            result = result.decode('iso-8859-1').encode('utf-8')
            result = result.replace('\n','')

            quality = re.compile('>Links - Quality(.+?)<').findall(result)[0]
            quality = quality.strip()
            if quality == 'CAM' or quality == 'TS': quality = 'CAM'
            elif quality == 'SCREENER': quality = 'SCR'
            else: quality = 'SD'

            links = common.parseDOM(result, "div", attrs = { "class": "links" })[0]
            links = common.parseDOM(links, "ul")

            for i in links:
                try:
                    name = common.parseDOM(i, "a")[0]
                    name = common.replaceHTMLCodes(name)
                    if name.isdigit(): raise Exception()

                    host = common.parseDOM(i, "li", attrs = { "class": "link_name" })[0]
                    host = host.strip().lower()
                    if not host in hostDict: raise Exception()
                    host = common.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    url = common.parseDOM(i, "a", ret="href")[0]
                    url = self.base_link + url
                    url = 'http' + urllib.unquote_plus(url).rsplit('http', 1)[-1].split('&', 1)[0]
                    url = urlparse.urlparse(url).path
                    url = '%s%s' % (self.base_link, url)
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    sources.append({'source': host, 'quality': quality, 'provider': 'Movie25', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            try: result = getUrl(url, referer=url).result
            except: result = ''

            proxies = [self.proxy_link_1, self.proxy_link_2, self.proxy_link_3]
            for proxy in proxies:
                if "iframe" in result or "IFRAME" in result: break
                base_link = proxy + urlparse.urlparse(url).path
                try: result = getUrl(base_link, referer=base_link).result
                except: pass

            result = result.decode('iso-8859-1').encode('utf-8')

            url = common.parseDOM(result, "iframe", ret="src")
            url += common.parseDOM(result, "IFRAME", ret="SRC")
            url = re.compile('(http.+)').findall(url[0])[0]

            import commonresolvers
            url = commonresolvers.get(url)
            return url
        except:
            return

class watchseries:
    def __init__(self):
        self.base_link = 'http://watchseries.ag'
        self.proxy_link_1 = 'http://proxy.cyberunlocker.com/browse.php?u=http://watchseries.ag'
        self.proxy_link_2 = 'http://9proxy.in/b.php?b=20&u=http://watchseries.ag'
        self.proxy_link_3 = 'https://watchseries.unblocked.pw'
        self.search_link = '/json/search/%s'
        self.episode_link = '/json/episode/%s_s%s_e%s.html'

    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            query = self.search_link % urllib.quote_plus(show)

            base_link = self.base_link
            try: result = getUrl(base_link + query, referer=base_link, mobile=True).result
            except: result = ''

            proxies = [self.proxy_link_1, self.proxy_link_2, self.proxy_link_3]
            for proxy in proxies:
                if "Search" in result: break
                base_link = proxy
                try: result = getUrl(base_link + query, referer=base_link, mobile=True).result
                except: result = ''

            result = re.compile('"\d*":\s({.+?})').findall(result)
            result = [json.loads(i) for i in result]

            shows = [cleantitle().tv(show), cleantitle().tv(show_alt)]
            years = [str(year), str(int(year)+1), str(int(year)-1)]
            result = [(i['href'], i['name'], i['year']) for i in result]
            result = [i for i in result if any(x in i[2] for x in years)]

            match = [i[0] for i in result if any(x == cleantitle().tv(i[1]) for x in shows)]

            match2 = [i[0] for i in result]
            match2 = [i for i in match2][::-1]
            match2 = uniqueList(match2).list
            if match2 == []: return

            for i in match2[:5]:
                try:
                    if len(match) > 0:
                        match3 = match[0]
                        break
                    result = getUrl(base_link + i, referer=base_link, mobile=True).result
                    if str('tt' + imdb) in result:
                        match3 = i
                        break
                except:
                    pass

            url = urlparse.urlparse(match3).path
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        if url == None: return
        url = url.rsplit('/', 1)[-1]
        url = self.episode_link % (url, season, episode)
        url = common.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            base_link = self.base_link
            try: result = getUrl(base_link + url, referer=base_link, mobile=True).result
            except: result = ''

            proxies = [self.proxy_link_1, self.proxy_link_2, self.proxy_link_3]
            for proxy in proxies:
                if "episode" in result: break
                base_link = proxy
                try: result = getUrl(base_link + url, referer=base_link, mobile=True).result
                except: result = ''

            result = re.compile('"links":(\[.+?\])').findall(result)[0]
            result = json.loads(result)
            links = [i for i in result if i['lang'] == 'English']

            for i in links:
                try:
                    url = i['url']
                    url = urlparse.urlparse(url).path
                    url = '%s%s' % (self.base_link, url)
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = i['host']
                    host = host.split('.', 1)[0]
                    host = host.strip().lower()
                    if not host in hostDict: raise Exception()
                    host = common.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    sources.append({'source': host, 'quality': 'SD', 'provider': 'Watchseries', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            class NoRedirection(urllib2.HTTPErrorProcessor):
                def http_response(self, request, response):
                    return response

            def http_result(url):
                opener = urllib2.build_opener(NoRedirection)
                opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20100101 Firefox/34.0')]
                opener.addheaders = [('Referer', url)]
                response = opener.open(url)
                result = response.read()
                response.close()
                return result

            url = url.replace('/json/open/', '/open/')
            try: result = http_result(url)
            except: result = ''

            proxies = [self.proxy_link_1, self.proxy_link_2, self.proxy_link_3]
            for proxy in proxies:
                if "myButton" in result: break
                base_link = proxy + urlparse.urlparse(url).path
                try: result = http_result(base_link)
                except: result = ''

            url = common.parseDOM(result, "a", ret="href", attrs = { "class": "myButton" })[0]
            url = 'http' + urllib.unquote_plus(url).rsplit('http', 1)[-1].split('&', 1)[0]

            import commonresolvers
            url = commonresolvers.get(url)
            return url
        except:
            return

class iwatchonline:
    def __init__(self):
        self.base_link = 'http://www.iwatchonline.to'
        self.proxy_link_1 = 'http://proxy.cyberunlocker.com/browse.php?u=http://www.iwatchonline.to'
        self.proxy_link_2 = 'http://9proxy.in/b.php?b=20&u=http://www.iwatchonline.to'
        self.proxy_link_3 = 'https://iwatchonline.unblocked.pw'
        self.search_link = '/advance-search'
        self.show_link = '/tv-shows/%s'
        self.episode_link = '/episode/%s-s%02de%02d'

    def get_movie(self, imdb, title, year):
        try:
            query = self.search_link
            post = urllib.urlencode({'searchquery': title, 'searchin': '1'})

            base_link = self.base_link
            try: result = getUrl(base_link + query, referer=base_link, post=post).result
            except: result = ''

            proxies = [self.proxy_link_1, self.proxy_link_2, self.proxy_link_3]
            for proxy in proxies:
                if "widget search-page" in result: break
                base_link = proxy
                try: result = getUrl(base_link + query, referer=base_link, post=post).result
                except: result = ''

            result = common.parseDOM(result, "div", attrs = { "class": "widget search-page" })[0]
            result = common.parseDOM(result, "td")

            title = cleantitle().movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="href")[-1], common.parseDOM(i, "a")[-1]) for i in result]
            result = [i for i in result if title == cleantitle().movie(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            url = result
            url = 'http' + urllib.unquote_plus(url).rsplit('http', 1)[-1].split('&', 1)[0]
            url = urlparse.urlparse(url).path
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            query = self.search_link
            post = urllib.urlencode({'searchquery': show, 'searchin': '2'})

            base_link = self.base_link
            try: result = getUrl(base_link + query, referer=base_link, post=post).result
            except: result = ''

            proxies = [self.proxy_link_1, self.proxy_link_2, self.proxy_link_3]
            for proxy in proxies:
                if "widget search-page" in result: break
                base_link = proxy
                try: result = getUrl(base_link + query, referer=base_link, post=post).result
                except: result = ''

            result = common.parseDOM(result, "div", attrs = { "class": "widget search-page" })[0]
            result = common.parseDOM(result, "td")

            shows = [cleantitle().tv(show), cleantitle().tv(show_alt)]
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="href")[-1], common.parseDOM(i, "a")[-1]) for i in result]
            result = [i for i in result if any(x == cleantitle().tv(i[1]) for x in shows)]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            url = result
            url = 'http' + urllib.unquote_plus(url).rsplit('http', 1)[-1].split('&', 1)[0]
            url = urlparse.urlparse(url).path
            url = url.rsplit('/', 1)[-1]
            url = self.show_link % url
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        if url == None: return
        url = url.rsplit('/', 1)[-1]
        url = self.episode_link % (url, int(season), int(episode))
        url = common.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            base_link = self.base_link
            try: result = getUrl(base_link + url, referer=base_link).result
            except: result = ''

            proxies = [self.proxy_link_1, self.proxy_link_2, self.proxy_link_3]
            for proxy in proxies:
                if '"pt0"' in result: break
                base_link = proxy
                try: result = getUrl(base_link + url, referer=base_link).result
                except: result = ''

            links = common.parseDOM(result, "tr", attrs = { "id": "pt.+?" })

            for i in links:
                try:
                    host = common.parseDOM(i, "img", attrs = { "src": ".+?" })[0]
                    host = host.split(' ', 1)[0].split('<', 1)[0]
                    host = host.rsplit('.', 1)[0].split('.', 1)[-1]
                    host = host.strip().lower()
                    if not host in hostDict: raise Exception()
                    host = common.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    lang = common.parseDOM(i, "img", ret="data-original-title", attrs = { "src": ".+?" })[0]
                    if not lang == 'English': raise Exception()

                    if '>Cam<' in i or '>TS<' in i: quality = 'CAM'
                    else: quality = 'SD'

                    url = common.parseDOM(i, "a", ret="href")[0]
                    url = 'http' + urllib.unquote_plus(url).rsplit('http', 1)[-1].split('&', 1)[0]
                    url = urlparse.urlparse(url).path
                    url = '%s%s' % (self.base_link, url)
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    sources.append({'source': host, 'quality': quality, 'provider': 'Iwatchonline', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            try: result = getUrl(url, referer=url).result
            except: result = ''

            proxies = [self.proxy_link_1, self.proxy_link_2, self.proxy_link_3]
            for proxy in proxies:
                if "frame" in result: break
                base_link = proxy + urlparse.urlparse(url).path
                try: result = getUrl(base_link, referer=base_link).result
                except: pass

            url = common.parseDOM(result, "iframe", ret="src", attrs = { "class": "frame" })[0]
            url = 'http' + urllib.unquote_plus(url).rsplit('http', 1)[-1].split('&', 1)[0]

            import commonresolvers
            url = commonresolvers.get(url)
            return url
        except:
            return

class movietube:
    def __init__(self):
        self.base_link = 'http://tunemovie.me'
        self.tvbase_link = 'http://tvstreaming.cc'
        self.index_link = '/index.php'
        self.docs_link = 'https://docs.google.com/file/d/%s/'

    def get_movie(self, imdb, title, year):
        try:
            query = self.base_link + self.index_link
            post = urllib.urlencode({'a': 'retrieve', 'c': 'result', 'p': '{"KeyWord":"%s","Page":"1","NextToken":""}' % title})

            result = getUrl(query, post=post).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "tr")

            title = cleantitle().movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [common.parseDOM(i, "h1")[0] for i in result]
            result = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "a")[0]) for i in result]
            result = [i for i in result if title == cleantitle().movie(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            url = result.split('v=', 1)[-1]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            url = show
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            query = self.tvbase_link + self.index_link
            post = urllib.urlencode({'a': 'retrieve', 'c': 'result', 'p': '{"KeyWord":"%s","Page":"1","NextToken":""}' % url})

            result = getUrl(query, post=post).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "tr")

            show = cleantitle().tv(url)
            season = '%01d' % int(season)
            episode = '%02d' % int(episode)
            result = [common.parseDOM(i, "h1")[0] for i in result]
            result = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "a")[0]) for i in result]
            result = [(i[0], re.sub('\sSeason(|\s)\d*.+', '', i[1]), re.compile('\sSeason *(\d*) *').findall(i[1])[0]) for i in result]
            result = [i for i in result if show == cleantitle().tv(i[1])]
            result = [i[0] for i in result if season == i[2]][0]

            url = result.split('v=', 1)[-1]
            url = '%s|%s' % (url, episode)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            content = re.compile('(.+?)\|\d*$').findall(url)

            if len(content) == 0:
                query = self.base_link + self.index_link
                post = urllib.urlencode({'a': 'getmoviealternative', 'c': 'result', 'p': '{"KeyWord":"%s"}' % url})
                result = getUrl(query, post=post).result
                result = re.compile('(<a.+?</a>)').findall(result)

                links = [i for i in result if any(x in i for x in ['0000000008400000.png', '0000000008110000.png'])]
                links = [i for i in links if any(x in i for x in ['>1080p<', '>720p<'])]
                links = [common.parseDOM(i, "a", ret="href")[0] for i in links][:3]
                links = [i.split('?v=')[-1] for i in links]

                for u in links:
                    try:
                        query = self.base_link + self.index_link
                        post = urllib.urlencode({'a': 'getplayerinfo', 'c': 'result', 'p': '{"KeyWord":"%s"}' % u})
                        result = getUrl(query, post=post).result

                        url = common.parseDOM(result, "source", ret="src", attrs = { "data-res": "1080" })
                        if len(url) > 0:
                            sources.append({'source': 'GVideo', 'quality': '1080p', 'provider': 'Movietube', 'url': url[0]})

                        url = common.parseDOM(result, "source", ret="src", attrs = { "data-res": "720" })
                        if len(url) > 0:
                            sources.append({'source': 'GVideo', 'quality': 'HD', 'provider': 'Movietube', 'url': url[0]})

                        url = common.parseDOM(result, "iframe", ret="src")
                        url = [i for i in url if 'docs.google.com' in i]
                        if not len(url) == 2: raise Exception()

                        import commonresolvers
                        u1 = commonresolvers.googledocs(url[0])
                        u2 = commonresolvers.googledocs(url[1])

                        for i in range(0, len(u1)): sources.append({'source': 'GVideo', 'quality': u1[i]['quality'], 'provider': 'Movietube', 'url': 'stack://%s , %s' % (u1[i]['url'], u2[i]['url'])})
                    except:
                        pass

            else:
                query = self.tvbase_link + self.index_link
                url, episode = re.compile('(.+?)\|(\d*)$').findall(url)[0]
                post = urllib.urlencode({'a': 'getpartlistinfo', 'c': 'result', 'p': '{"KeyWord":"%s","Episode":"%s"}' % (url, episode)})
                result = getUrl(query, post=post).result
                result = re.compile('(<a.+?</a>)').findall(result)

                links = [common.parseDOM(i, "a", ret="data") for i in result]
                links = [i[0] for i in links if len(i) > 0]
                links = [i for i in links if i.startswith('--MP4') or i.startswith('--Doc')]

                for u in links:
                    try:
                        if u.startswith('--Doc'):
                            import commonresolvers
                            url = self.docs_link % u.split('--', 2)[-1]
                            url = commonresolvers.googledocs(url)

                            for i in url: sources.append({'source': 'GVideo', 'quality': i['quality'], 'provider': 'Movietube', 'url': i['url']})
                        else:
                            import commonresolvers
                            url = u.split('--', 2)[-1]
                            i = commonresolvers.google(url)[0]

                            sources.append({'source': 'GVideo', 'quality': i['quality'], 'provider': 'Movietube', 'url': i['url']})
                    except:
                        pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            if url.startswith('stack://'): return url

            url = getUrl(url, output='geturl').result
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

class moviezone:
    def __init__(self):
        self.base_link = 'http://www.hdmoviezone.net'
        self.search_link = '/feed/?s=%s'

    def get_movie(self, imdb, title, year):
        try:
            query = self.base_link + self.search_link % (urllib.quote_plus(title))

            result = getUrl(query).result
            result = common.parseDOM(result, "item")
            result = [(common.parseDOM(i, "link")[0], common.parseDOM(i, "span", ret="data-title", attrs = { "class": "imdbRating" })[0]) for i in result]
            result = [i[0] for i in result if imdb in i[1]][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            url = self.base_link + url
            result = getUrl(url).result

            url = common.parseDOM(result, "div", attrs = { "class": "fullwindowlink" })[0]
            url = common.parseDOM(url, "a", ret="href")[0]
            url = self.base_link + url

            result = getUrl(url).result
            result = common.parseDOM(result, "body")[0]

            post = re.compile('movie_player_file *= *"(.+?)"').findall(result)[0]
            post = urllib.urlencode({'url': post})

            url = common.parseDOM(result, "script", ret="src", attrs = { "type": ".+?" })[0]
            url = getUrl(url).result
            url = url.replace('\n','')
            url = re.compile('getServerHost.+?return\s+"(.+?)"').findall(url)[0]

            headers = { 'Host': 'hdmoviezone.net',
            'Connection': 'keep-alive',
            'Accept': 'text/html, */*; q=0.01',
            'Content-Length': '200',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20100101 Firefox/34.0',
            'Origin': self.base_link,
            'Referer': url }

            request = urllib2.Request(url, data=post, headers=headers)
            response = urllib2.urlopen(request, timeout=5)
            result = response.read()
            response.close()

            result = json.loads(result)
            result = result['content']

            links = [i['url'] for i in result]

            for u in links:
                try:
                    import commonresolvers
                    i = commonresolvers.google(u)[0]
                    url = getUrl(i['url'], output='geturl').result
                    quality = i['quality']

                    sources.append({'source': 'GVideo', 'quality': quality, 'provider': 'Moviezone', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            if url.startswith('stack://'): return url

            url = getUrl(url, output='geturl').result
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

class zumvo:
    def __init__(self):
        self.base_link = 'http://zumvo.com'
        self.search_link = '/search/%s'

    def get_movie(self, imdb, title, year):
        try:
            query = self.base_link + self.search_link % (urllib.quote_plus(title))

            result = getUrl(query).result
            result = common.parseDOM(result, "ul", attrs = { "class": "list-film" })[0]
            result = common.parseDOM(result, "li")

            title = cleantitle().movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "a")[1].split('</span>')[-1], common.parseDOM(i, "div", attrs = { "class": "status" })[0]) for i in result]
            result = [i for i in result if i[2] == 'HD']
            result = [i for i in result if title == cleantitle().movie(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            url = self.base_link + url
            result = getUrl(url).result

            url = common.parseDOM(result, "a", ret="href", attrs = { "class": "btn-watch" })[0]
            result = getUrl(url).result

            url = re.compile('"proxy.link" *: *"zumvo[*](.+?)"').findall(result)[0]
            import gkdecrypter
            url = gkdecrypter.decrypter(198,128).decrypt(url,base64.urlsafe_b64decode('NlFQU1NQSGJrbXJlNzlRampXdHk='),'ECB').split('\0')[0]

            import commonresolvers
            if 'docs.google.com' in url: url = commonresolvers.googledocs(url)
            elif 'plus.google.com' in url: url = commonresolvers.googleplus(url)
            else: raise Exception()

            for i in url: sources.append({'source': 'GVideo', 'quality': i['quality'], 'provider': 'Zumvo', 'url': i['url']})

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            if url.startswith('stack://'): return url

            url = getUrl(url, output='geturl').result
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

class view47:
    def __init__(self):
        self.base_link = 'http://view47.com'
        self.search_link = '/search/%s.html'

    def get_movie(self, imdb, title, year):
        try:
            query = self.base_link + self.search_link % (urllib.quote_plus(title))

            result = getUrl(query).result
            result = common.parseDOM(result, "ul", attrs = { "class": "list zzz ip_tip" })[0]
            result = common.parseDOM(result, "li")

            title = cleantitle().movie(title)
            years = ['%s' % str(year), '%s' % str(int(year)+1), '%s' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "a", ret="title")[0], common.parseDOM(i, "span", attrs = { "class": "year" })[0]) for i in result]
            result = [i for i in result if title == cleantitle().movie(i[1])]
            result = [i[0] for i in result if any(x in i[2] for x in years)][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            url = self.base_link + url
            result = getUrl(url).result

            import commonresolvers
            url = commonresolvers.googleplus(url)

            for i in url: sources.append({'source': 'GVideo', 'quality': i['quality'], 'provider': 'View47', 'url': i['url']})

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            if url.startswith('stack://'): return url

            url = getUrl(url, output='geturl').result
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

class g2g:
    def __init__(self):
        self.base_link = 'http://g2g.fm'
        self.search_link = '/forum/search.php?titleonly=1&securitytoken=guest&do=process&B1=&q=%s+Online+Streaming'

    def get_movie(self, imdb, title, year):
        try:
            query = self.base_link + self.search_link % (urllib.quote_plus(title))

            result = getUrl(query).result
            result = common.parseDOM(result, "h3", attrs = { "class": "searchtitle" })

            title = cleantitle().movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "a", attrs = { "class": "title" })[0]) for i in result]
            result = [i for i in result if any(x in i[1] for x in [' 720p ', ' 1080p '])]
            result = [(i[0], re.compile('(.+? [(]\d{4}[)])').findall(i[1])[0]) for i in result]
            result = [i for i in result if title == cleantitle().movie(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = re.compile('(.+?[?]\d*)').findall(url)[0]
            if not url.startswith('/'): url = '/%s' % url
            if not url.startswith('/forum'): url = '/forum%s' % url
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            referer = self.base_link + url
            result = getUrl(referer).result

            url = common.parseDOM(result, "iframe", ret="src", attrs = { "allowfullscreen": ".+?" })[0]
            result = getUrl(url, referer=referer).result

            u = re.compile("'ggplayer'.+?='(http.+?)'").findall(result)[::-1]
            result = getUrl(u[0], referer=referer).result
            if len(u) > 1: result += getUrl(u[1], referer=referer).result

            url = common.parseDOM(result, "iframe", ret="src")

            if len(url) == 1: 
                import commonresolvers
                url = commonresolvers.googledocs(url)

                for i in url: sources.append({'source': 'GVideo', 'quality': i['quality'], 'provider': 'G2G', 'url': i['url']})

            elif len(url) == 2: 
                import commonresolvers
                u1 = commonresolvers.googledocs(url[0])
                u2 = commonresolvers.googledocs(url[1])

                for i in range(0, len(u1)): sources.append({'source': 'GVideo', 'quality': u1[i]['quality'], 'provider': 'G2G', 'url': 'stack://%s , %s' % (u1[i]['url'], u2[i]['url'])})

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            if url.startswith('stack://'): return url

            url = getUrl(url, output='geturl').result
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

class muchmovies:
    def __init__(self):
        self.base_link = 'http://aws.umovies.me'
        self.search_link = '/search/%s'

    def get_movie(self, imdb, title, year):
        try:
            query = urllib.quote_plus(title.replace(' ', '-').rsplit(':', 1)[0])
            query = self.base_link + self.search_link % query

            result = getUrl(query, mobile=True).result
            result = common.parseDOM(result, "ul", attrs = { "class": "movies.+?" })
            result = common.parseDOM(result, "li")

            title = cleantitle().movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "h3")[0]) for i in result]
            result = [i for i in result if title == cleantitle().movie(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []
            url = self.base_link + url
            sources.append({'source': 'Muchmovies', 'quality': 'HD', 'provider': 'Muchmovies', 'url': url})
            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            result = getUrl(url, mobile=True).result
            url = common.parseDOM(result, "a", ret="href", attrs = { "data-role": "button" })
            url = [i for i in url if str('.mp4') in i][0]
            return url
        except:
            return

class sweflix:
    def __init__(self):
        self.base_link = 'https://sweflix.net'
        self.search_link = '/index.php?act=query&query=%s'
        self.footer_link = '/film_api.php?target=footer&fid=%s'

    def get_movie(self, imdb, title, year):
        try:
            query = self.base_link + self.search_link % (urllib.quote_plus(title))

            result = getUrl(query).result
            result = common.parseDOM(result, "div", attrs = { "class": "hover-group.+?" })

            title = cleantitle().movie(title)
            years = ['>%s<' % str(year), '>%s<' % str(int(year)+1), '>%s<' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="data-movieid")[0], common.parseDOM(i, "h5")[-1], common.parseDOM(i, "p")[-1]) for i in result]
            result = [i for i in result if title == cleantitle().movie(i[1])]
            result = [i[0] for i in result if any(x in i[2] for x in years)][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            url = self.base_link + self.footer_link % url
            result = getUrl(url).result

            url = common.parseDOM(result, "a", ret="href")
            url = [i for i in url if 'play/' in i][0]
            url = self.base_link + url

            result = getUrl(url).result

            url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video/.+?" })[0]
            if '1080p' in url: quality = '1080p'
            else: quality = 'HD'

            sources.append({'source': 'Sweflix', 'quality': quality, 'provider': 'Sweflix', 'url': url})
            return sources
        except:
            return sources

    def resolve(self, url):
        return url

class movieshd:
    def __init__(self):
        self.base_link = 'http://movieshd.co'
        self.search_link = '/?s=%s'
        self.player_link = 'http://videomega.tv/iframe.php?ref=%s'

    def get_movie(self, imdb, title, year):
        try:
            query = self.base_link + self.search_link % (urllib.quote_plus(title))

            result = getUrl(query).result
            result = common.parseDOM(result, "ul", attrs = { "class": "listing-videos.+?" })[0]
            result = common.parseDOM(result, "li", attrs = { "class": ".+?" })

            title = cleantitle().movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "a", ret="title")[0]) for i in result]
            result = [i for i in result if title == cleantitle().movie(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            url = self.base_link + url
            result = getUrl(url).result
            result = common.parseDOM(result, "div", attrs = { "class": "video-embed" })[0]

            url = re.compile('data-rocketsrc=[\'|\"](.+?)[\'|\"]').findall(result)
            url = [i for i in url if 'hashkey' in i]
            if len(url) > 0:
                url = 'http:' + url[0] if url[0].startswith('//') else url[0]
                result = getUrl(url, referer=url).result
            url = re.compile('ref=[\'|\"](.+?)[\'|\"]').findall(result)[0]

            url = self.player_link % url
            url = url.encode('utf-8')

            import commonresolvers
            url = commonresolvers.videomega(url)
            if url == None: raise Exception()

            sources.append({'source': 'Videomega', 'quality': 'HD', 'provider': 'MoviesHD', 'url': url})

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

class onlinemovies:
    def __init__(self):
        self.base_link = 'http://onlinemovies.pro'
        self.search_link = '/?s=%s'

    def get_movie(self, imdb, title, year):
        try:
            query = self.base_link + self.search_link % (urllib.quote_plus(title))

            result = getUrl(query).result
            result = common.parseDOM(result, "ul", attrs = { "class": "listing-videos.+?" })[0]
            result = common.parseDOM(result, "li", attrs = { "class": ".+?" })

            title = cleantitle().movie(title)
            years = ['%s' % str(year), '%s' % str(int(year)+1), '%s' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "a", ret="title")[0]) for i in result]
            result = [(i[0], re.sub('\s(\(|)(\d{4})(.+)', '', i[1]), re.compile('(\d{4})').findall(i[1])) for i in result]
            result = [(i[0], i[1], i[2][0]) for i in result if len(i[2]) > 0]
            result = [i for i in result if title == cleantitle().movie(i[1])]
            result = [i[0] for i in result if any(x in i[2] for x in years)][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            url = self.base_link + url
            result = getUrl(url).result

            quality = re.compile('<strong>Quality</strong>.+?<strong>(.+?)</strong>').findall(result)[0]
            if '1080p' in quality: quality = '1080p'
            elif '720p' in quality: quality = 'HD'
            else: raise Exception()

            result = common.parseDOM(result, "div", attrs = { "class": "video-embed" })[0]
            url = common.parseDOM(result, "iframe", ret="src")[0]

            import commonresolvers
            url = commonresolvers.videomega(url)
            if url == None: raise Exception()

            sources.append({'source': 'Videomega', 'quality': 'HD', 'provider': 'Onlinemovies', 'url': url})

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

class yify:
    def __init__(self):
        self.base_link = 'http://yify.tv'
        self.search_link = '/wp-admin/admin-ajax.php'
        self.pk_link = '/player/pk/pk/plugins/player_p2.php'

    def get_movie(self, imdb, title, year):
        try:
            query = self.base_link + self.search_link
            post = urllib.urlencode({'action': 'ajaxy_sf', 'sf_value': title})

            result = getUrl(query, post=post).result
            result = result.replace('&#8211;','-').replace('&#8217;','\'')
            result = json.loads(result)
            result = result['post']['all']

            title = cleantitle().movie(title)
            result = [i['post_link'] for i in result if title == cleantitle().movie(i['post_title'])][0]

            check = getUrl(result).result
            if not str('tt' + imdb) in check: raise Exception()

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        print 'yifi url:' + str(self.base_link) + str(url)
        try:
            sources = []

            base = self.base_link + url
            result = getUrl(base).result
            result = common.parseDOM(result, "script", attrs = { "type": "text/javascript" })
            result = ''.join(result)

            links = re.compile('pic=([^&]+)').findall(result)
            links = uniqueList(links).list

            import commonresolvers

            for i in links:
                try:
                    url = self.base_link + self.pk_link
                    post = urllib.urlencode({'url': i, 'fv': '16'})
                    result = getUrl(url, post=post, referer=base).result
                    result = json.loads(result)

                    try: sources.append({'source': 'YIFY', 'quality': 'HD', 'provider': 'YIFY', 'url': [i['url'] for i in result if i['width'] == 1280][0]})
                    except: pass

                    url = result[0]['jscode']
                    url = urllib.unquote_plus(url)
                    url = re.compile('"(.+?)"').findall(url)[0]
                    url = [x.split('|')[-1].split('|')[-1] for x in url.split(',')]
                    url = [x for x in url if 'googlevideo' in x]
                    url = [commonresolvers.google(x) for x in url]
                    url = [x[0] for x in url if not x == None]

                    for x in url: sources.append({'source': 'GVideo', 'quality': x['quality'], 'provider': 'YIFY', 'url': x['url']})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            url = getUrl(url, output='geturl').result
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

class ororo:
    def __init__(self):
        self.base_link = 'http://ororo.tv'
        self.key_link = base64.urlsafe_b64decode('dXNlciU1QnBhc3N3b3JkJTVEPWMyNjUxMzU2JnVzZXIlNUJlbWFpbCU1RD1jMjY1MTM1NiU0MGRyZHJiLmNvbQ==')
        self.sign_link = 'http://ororo.tv/users/sign_in'

    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            result = getUrl(self.base_link).result
            if not "'index show'" in result:
                cookie = getUrl(self.sign_link, post=self.key_link, output='cookie').result
                result = getUrl(self.base_link, cookie=cookie).result

            result = common.parseDOM(result, "div", attrs = { "class": "index show" })
            result = [(common.parseDOM(i, "a", attrs = { "class": "name" })[0], common.parseDOM(i, "span", attrs = { "class": "value" })[0], common.parseDOM(i, "a", ret="href")[0]) for i in result]

            shows = [cleantitle().tv(show), cleantitle().tv(show_alt)]
            years = [str(year), str(int(year)+1), str(int(year)-1)]
            result = [i for i in result if any(x in i[1] for x in years)]
            result = [i[2] for i in result if any(x == cleantitle().tv(i[0]) for x in shows)][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            url = self.base_link + url

            result = getUrl(url).result
            if not "menu season-tabs" in result:
                cookie = getUrl(self.sign_link, post=self.key_link, output='cookie').result
                result = getUrl(url, cookie=cookie).result

            result = common.parseDOM(result, "a", ret="data-href", attrs = { "href": "#%01d-%01d" % (int(season), int(episode)) })[0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []
            url = self.base_link + url
            sources.append({'source': 'Ororo', 'quality': 'SD', 'provider': 'Ororo', 'url': url})
            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            result = getUrl(url).result
            if not "my_video" in result:
                cookie = getUrl(self.sign_link, post=self.key_link, output='cookie').result
                result = getUrl(url, cookie=cookie).result

            url = None
            try: url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video/webm" })[0]
            except: pass
            try: url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video/mp4" })[0]
            except: pass

            if url == None: return
            if not url.startswith('http://'): url = '%s%s' % (self.base_link, url)
            url = '%s|Cookie=%s' % (url, urllib.quote_plus('video=true'))

            return url
        except:
            return

class vkbox:
    def __init__(self):
        self.base_link = 'http://mobapps.cc'
        self.data_link = '/data/data_en.zip'
        self.moviedata_link = 'movies_lite.json'
        self.tvdata_link = 'tv_lite.json'
        self.movie_link = '/api/serials/get_movie_data/?id=%s'
        self.show_link = '/api/serials/es?id=%s'
        self.episode_link = '/api/serials/e/?h=%s&u=%01d&y=%01d'
        self.vk_link = 'https://vk.com/video_ext.php?oid=%s&id=%s&hash=%s'

    def get_movie(self, imdb, title, year):
        try:
            import zipfile, StringIO
            query = self.base_link + self.data_link
            data = urllib2.urlopen(query, timeout=5).read()
            zip = zipfile.ZipFile(StringIO.StringIO(data))
            result = zip.read(self.moviedata_link)
            zip.close()

            imdb = 'tt' + imdb
            result = json.loads(result)
            result = [i['id'] for i in result if imdb == i['imdb_id']][0]

            url = self.movie_link % result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            import zipfile, StringIO
            query = self.base_link + self.data_link
            data = urllib2.urlopen(query, timeout=5).read()
            zip = zipfile.ZipFile(StringIO.StringIO(data))
            result = zip.read(self.tvdata_link)
            zip.close()

            imdb = 'tt' + imdb
            result = json.loads(result)
            result = [i['id'] for i in result if imdb == i['imdb_id']][0]

            url = self.show_link % result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        if url == None: return
        url = url.rsplit('id=', 1)[-1]
        url = self.episode_link % (url, int(season), int(episode))
        url = common.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            url = self.base_link + url

            import urlparse
            par = urlparse.parse_qs(urlparse.urlparse(url).query)
            try: num = int(par['h'][0]) + int(par['u'][0]) + int(par['y'][0])
            except: num = int(par['id'][0]) + 537

            request = urllib2.Request(url)
            request.add_header('User-Agent', 'android-async-http/1.4.1 (http://loopj.com/android-async-http)')
            response = urllib2.urlopen(request, timeout=5)
            result = response.read()
            response.close()

            result = json.loads(result)
            try: result = result['langs']
            except: pass
            i = [i for i in result if i['lang'] == 'en'][0]

            url = (str(int(i['apple']) + num), str(int(i['google']) + num), i['microsoft'])
            url = self.vk_link % url

            import commonresolvers
            url = commonresolvers.vk(url)

            for i in url: sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'VKBox', 'url': i['url']})

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

class clickplay:
    def __init__(self):
        self.base_link = 'http://clickplay.to'
        self.search_link = '/search/%s'
        self.episode_link = '%sseason-%01d/episode-%01d'

    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            query = ' '.join([i for i in show.split() if i not in ['The','the','A','a']])
            query = self.base_link + self.search_link % urllib.quote_plus(query)

            result = getUrl(query).result
            result = common.parseDOM(result, "div", attrs = { "id": "video_list" })[0]
            result = result.split('</a>')
            result = [(common.parseDOM(i, "span", attrs = { "class": "article-title" }), common.parseDOM(i, "a", ret="href")) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if not (len(i[0]) == 0 or len(i[1]) == 0)]

            shows = [cleantitle().tv(show), cleantitle().tv(show_alt)]
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [i for i in result if any(x == cleantitle().tv(i[0]) for x in shows)]
            result = [i[1] for i in result if any(x in i[0] for x in years)][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        if url == None: return
        url = self.episode_link % (url, int(season), int(episode))
        url = common.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            url = self.base_link + url

            result = getUrl(url).result
            u = common.parseDOM(result, "meta", ret="content", attrs = { "property": "og:url" })[0]
            links = re.compile('<a href="([?]link_id=.+?)".+?>\[720p\].+?</a>').findall(result)
            links = [u + i for i in links]

            import gkdecrypter

            for u in links[:3]:
                try:
                    result = getUrl(u).result
                    url = re.compile('proxy[.]link=clickplay[*](.+?)"').findall(result)[-1]
                    url = gkdecrypter.decrypter(198,128).decrypt(url,base64.urlsafe_b64decode('bW5pcUpUcUJVOFozS1FVZWpTb00='),'ECB').split('\0')[0]

                    if not 'vk.com' in url: raise Exception()

                    import commonresolvers
                    vk = commonresolvers.vk(url)

                    for i in vk: sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'Clickplay', 'url': i['url']})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.get(url)
            return url
        except:
            return

class moviestorm:
    def __init__(self):
        self.base_link = 'http://moviestorm.eu'
        self.search_link = '/search?q=%s'
        self.episode_link = '%s?season=%01d&episode=%01d'

    def get_movie(self, imdb, title, year):
        try:
            query = urllib.quote_plus(title)
            query = self.base_link + self.search_link % query

            result = getUrl(query).result
            result = common.parseDOM(result, "div", attrs = { "class": "movie_box" })

            imdb = 'tt' + imdb
            result = [i for i in result if imdb in i][0]
            result = common.parseDOM(result, "a", ret="href")[0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            query = urllib.quote_plus(show)
            query = self.base_link + self.search_link % query

            result = getUrl(query).result
            result = common.parseDOM(result, "div", attrs = { "class": "movie_box" })

            imdb = 'tt' + imdb
            result = [i for i in result if imdb in i][0]
            result = common.parseDOM(result, "a", ret="href")[0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        if url == None: return
        url = self.episode_link % (url, int(season), int(episode))
        url = common.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            url = self.base_link + url

            result = getUrl(url).result
            result = common.parseDOM(result, "div", attrs = { "class": "links" })[0]
            result = common.parseDOM(result, "tr")
            result = [(common.parseDOM(i, "td", attrs = { "class": "quality_td" })[0], common.parseDOM(i, "a", ret="href")[-1]) for i in result]

            ts_quality = ['CAM', 'TS']
            links = [i for i in result if not any(x in i[0] for x in ts_quality)]
            if len(links) == 0: links = result

            for i in links:
                try:
                    url = i[1]
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = re.sub('.+?/exit/\d*-|[.].+?[.]html|http://(|www[.])|/.+|[.].+$','', i[1])
                    host = host.strip().lower()
                    if not host in hostDict: raise Exception()
                    host = common.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    if any(x in i[0] for x in ts_quality): quality = 'CAM'
                    else: quality = 'SD'

                    sources.append({'source': host, 'quality': quality, 'provider': 'Moviestorm', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            if url.startswith(self.base_link):
                result = getUrl(url).result
                url = common.parseDOM(result, "a", ret="href", attrs = { "class": "real_link" })[0]

            import commonresolvers
            url = commonresolvers.get(url)
            return url
        except:
            return

class merdb:
    def __init__(self):
        self.base_link = 'http://www.merdb.es'
        self.moviesearch_link = '/advanced_search.php?advanced_search=search&name=%s'
        self.tvsearch_link = '/tvshow/advanced_search.php?advanced_search=search&name=%s'
        self.episode_link = 'season-%01d-episode-%01d'

    def get_movie(self, imdb, title, year):
        try:
            query = self.base_link + self.moviesearch_link % (urllib.quote_plus(title))

            result = getUrl(query).result
            result = common.parseDOM(result, "div", attrs = { "class": "main_list_box" })

            title = 'watch' + cleantitle().movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "a", ret="title")[0]) for i in result]
            result = [(i[0], re.sub('\s\(\s\d{4}\s\)', '', i[1])) for i in result]
            result = [i for i in result if title == cleantitle().movie(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            query = self.base_link + self.tvsearch_link % (urllib.quote_plus(show))

            result = getUrl(query).result
            result = common.parseDOM(result, "div", attrs = { "class": "main_list_box" })

            shows = ['watch' + cleantitle().tv(show), 'watch' + cleantitle().tv(show_alt)]
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "a", ret="title")[0]) for i in result]
            result = [i for i in result if any(x == cleantitle().tv(i[1]) for x in shows)]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            url = self.base_link + url

            ep = self.episode_link % (int(season), int(episode))

            result = getUrl(url).result
            result = common.parseDOM(result, "a", ret="href")
            result = [i for i in result if ep in i][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            url = self.base_link + url

            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            links = common.parseDOM(result, "tbody")

            for i in links:
                try:
                    url = common.parseDOM(i, "a", ret="href")[0]
                    url = urllib.unquote_plus(url)
                    url = re.compile('url=(.+?)&').findall(url)[0]
                    url = base64.urlsafe_b64decode(url.encode('utf-8'))
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = common.parseDOM(i, "a", ret="href")[0]
                    host = urllib.unquote_plus(host)
                    host = re.compile('domain=(.+?)&').findall(host)[0]
                    host = base64.urlsafe_b64decode(host.encode('utf-8'))
                    host = host.rsplit('.', 1)[0]
                    host = host.strip().lower()
                    if not host in hostDict: raise Exception()
                    host = common.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    quality = common.parseDOM(i, "span", ret="class")[0]
                    if quality == 'quality_cam' or quality == 'quality_ts': quality = 'CAM'
                    elif quality == 'quality_dvd': quality = 'SD'
                    else:  raise Exception()
                    quality = quality.encode('utf-8')

                    sources.append({'source': host, 'quality': quality, 'provider': 'MerDB', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.get(url)
            return url
        except:
            return

class wso:
    def __init__(self):
        self.base_link = 'http://watchmovies-online.ch'
        self.tvbase_link = 'http://watchseries-online.ch'
        self.search_link = '/?s=%s'

    def get_movie(self, imdb, title, year):
        try:
            query = self.base_link + self.search_link % (urllib.quote_plus(title))

            result = getUrl(query).result
            result = common.parseDOM(result, "div", attrs = { "class": "Post-body" })

            title = cleantitle().movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="href"), common.parseDOM(i, "a")) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i for i in result if title == cleantitle().movie(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            url = show
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            title = url
            hdlr = 'S%02dE%02d' % (int(season), int(episode))

            query = '%s "%s"' % (title, hdlr)
            query = self.tvbase_link + self.search_link % (urllib.quote_plus(query))

            result = getUrl(query).result
            result = common.parseDOM(result, "h2", attrs = { "class": "PostHeaderIcon-wrapper" })

            title = cleantitle().tv(title)
            result = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "a")[0]) for i in result]
            result = [(i[0], re.compile('(.+?) (S\d*E\d*)').findall(i[1])[0]) for i in result]
            result = [(i[0], i[1][0], i[1][1]) for i in result]
            result = [i for i in result if title == cleantitle().tv(i[1])]
            result = [i[0] for i in result if hdlr == i[2]][0]

            url = result.replace(self.tvbase_link, '')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            content = re.compile('/\d{4}/\d{2}/').findall(url)
            if len(content) > 0: url = self.tvbase_link + url 
            else: url = self.base_link + url

            result = getUrl(url).result
            links = common.parseDOM(result, "td", attrs = { "class": "even tdhost" })
            links += common.parseDOM(result, "td", attrs = { "class": "odd tdhost" })

            q = re.compile('<label>Quality</label>(.+?)<').findall(result)
            if len(q) > 0: q = q[0]
            else: q = ''

            if q.endswith(('CAM', 'TS')): quality = 'CAM'
            else: quality = 'SD'

            for i in links:
                try:
                    host = common.parseDOM(i, "a")[0]
                    host = host.split('<', 1)[0]
                    host = host.rsplit('.', 1)[0].split('.', 1)[-1]
                    host = host.strip().lower()
                    if not host in hostDict: raise Exception()
                    host = common.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    url = common.parseDOM(i, "a", ret="href")[0]
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    sources.append({'source': host, 'quality': quality, 'provider': 'WSO', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            result = getUrl(url).result

            try: url = common.parseDOM(result, "a", ret="href", attrs = { "class": "wsoButton" })[0]
            except: pass

            import commonresolvers
            url = commonresolvers.get(url)
            return url
        except:
            return

class twomovies:
    def __init__(self):
        self.base_link = 'http://twomovies.us'
        self.search_link = '/search/?criteria=imdb&search_query=tt%s'

    def get_movie(self, imdb, title, year):
        try:
            query = self.base_link + self.search_link % imdb

            check = getUrl(query, output='geturl', referer=query).result
            if not self.base_link in check: raise Exception()

            cookie = getUrl(query, output='cookie', referer=query).result
            cookie = re.compile('(PHPSESSID=[\w]+)').findall(cookie)[0]

            result = getUrl(query, cookie=cookie, referer=query).result
            result = common.parseDOM(result, "meta", ret="content", attrs = { "property": "og:url" })[0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            query = self.base_link + self.search_link % imdb

            check = getUrl(query, output='geturl', referer=query).result
            if not self.base_link in check: raise Exception()

            cookie = getUrl(query, output='cookie', referer=query).result
            cookie = re.compile('(PHPSESSID=[\w]+)').findall(cookie)[0]

            result = getUrl(query, cookie=cookie, referer=query).result
            result = common.parseDOM(result, "meta", ret="content", attrs = { "property": "og:url" })[0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        if url == None: return
        url = url.replace('/watch_tv_show/','/watch_episode/')
        url += '/%01d/%01d/' % (int(season), int(episode))
        url = common.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            base = self.base_link + url

            check = getUrl(base, output='geturl', referer=base).result
            if not self.base_link in check: raise Exception()

            base += '?sort=date.desc#links'
            result = getUrl(base, referer=base).result

            links = common.parseDOM(result, "tr", attrs = { "id": "link_row_.+?" })

            for i in links:
                try:
                    url = common.parseDOM(i, "a", ret="href")[0]
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = common.parseDOM(i, "a", attrs = { "onclick": ".+?" })[0]
                    host = host.split('www.', 1)[-1].rsplit('.')[0]
                    host = host.strip().lower()
                    if not host in hostDict: raise Exception()
                    host = common.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    q = common.parseDOM(i, "font", attrs = { "class": "date2" })
                    if not '/watch_movie/' in base: quality = 'SD'
                    elif len(q) == 0: raise Exception()
                    elif q[0].lower() in ['(cam)', '(ts)']: quality = 'CAM'
                    else: quality = 'SD'

                    sources.append({'source': host, 'quality': quality, 'provider': 'Twomovies', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            check = getUrl(url, output='geturl', referer=url).result
            if not self.base_link in check: raise Exception()

            cookie = getUrl(url, output='cookie', referer=url).result
            cookie = re.compile('(PHPSESSID=[\w]+)').findall(cookie)[0]
            cookie += '; links_tos=1'

            result = getUrl(url, cookie=cookie, referer=url).result

            url = common.parseDOM(result, "iframe", ret="src")
            url += common.parseDOM(result, "IFRAME", ret="SRC")
            url = url[0]

            import commonresolvers
            url = commonresolvers.get(url)
            return url
        except:
            return

class animeultima:
    def __init__(self):
        self.base_link = 'http://www.animeultima.io'
        self.search_link = '/search.html?searchquery=%s'
        self.tvdb_link = 'http://thetvdb.com/api/%s/series/%s/default/%01d/%01d'
        self.tvdb_key = base64.urlsafe_b64decode('MUQ2MkYyRjkwMDMwQzQ0NA==')

    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            query = self.base_link + self.search_link % (urllib.quote_plus(show_alt))

            result = getUrl(query).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "ol", attrs = { "id": "searchresult" })[0]
            result = common.parseDOM(result, "h2")

            shows = [cleantitle().tv(show), cleantitle().tv(show_alt)]
            result = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "a")[0]) for i in result]
            result = [(i[0], re.sub('<.+?>|</.+?>','', i[1])) for i in result]
            result = [i for i in result if any(x == cleantitle().tv(i[1]) for x in shows)]
            result = result[-1][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            tvdb_link = self.tvdb_link % (self.tvdb_key, tvdb, int(season), int(episode))
            result = getUrl(tvdb_link).result

            num = common.parseDOM(result, "absolute_number")[0]
            url = self.base_link + url

            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "tr", attrs = { "class": "" })
            result = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "td", attrs = { "class": "epnum" })[0]) for i in result]
            result = [i[0] for i in result if num == i[1]][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []
            url = self.base_link + url
            sources.append({'source': 'Animeultima', 'quality': 'SD', 'provider': 'Animeultima', 'url': url})
            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')

            url = common.parseDOM(result, "div", attrs = { "class": "player-embed" })[0]
            url = common.parseDOM(url, "iframe", ret="src")[0]

            result = getUrl(url).result

            url = re.compile("video_link *= *'(.+?)'").findall(result)[0]
            url = urllib.unquote_plus(url)
            return url
        except:
            return

class einthusan:
    def __init__(self):
        self.base_link = 'http://www.einthusan.com'
        self.search_link = '/search/?search_query=%s&lang=%s'

    def get_movie(self, imdb, title, year):
        try:
            search = 'http://www.imdbapi.com/?i=tt%s' % imdb
            search = getUrl(search).result
            search = json.loads(search)
            country = [i.strip() for i in search['Country'].split(',')]
            if not 'India' in country: return

            languages = ['hindi', 'tamil', 'telugu', 'malayalam']
            language = [i.strip().lower() for i in search['Language'].split(',')]
            language = [i for i in language if any(x == i for x in languages)][0]

            query = urllib.quote_plus(title)
            query = self.base_link + self.search_link % (query, language)

            result = getUrl(query).result
            result = common.parseDOM(result, "div", attrs = { "class": "search-category" })
            result = [i for i in result if 'Movies' in common.parseDOM(i, "p")[0]][0]
            result = common.parseDOM(result, "li")

            title = cleantitle().movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "a")[0]) for i in result]
            r = [i for i in result if any(x in i[1] for x in years)]
            if not len(r) == 0: result = r
            result = [i[0] for i in result if title == cleantitle().movie(i[1])][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = url.replace('../', '/')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []
            url = self.base_link + url
            sources.append({'source': 'Einthusan', 'quality': 'HD', 'provider': 'Einthusan', 'url': url})
            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            result = getUrl(url).result
            url = re.compile("'file': '(.+?)'").findall(result)[0]
            return url
        except:
            return

class myvideolinks:
    def __init__(self):
        self.base_link_1 = 'http://myvideolinks.eu'
        self.base_link_2 = 'http://myvideolinks.xyz'
        self.search_link = '/?s=%s'

    def get_movie(self, imdb, title, year):
        try:
            url = '%s %s' % (title, year)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            result = ''
            domains = [self.base_link_1, self.base_link_2]
            for domain in domains:
                try: result += getUrl(domain).result
                except: pass

            queries = re.compile('[\'|\"](http.+?)[\'|\"]').findall(result)
            queries = [i for i in queries if 'myvideolinks' in i]
            queries = [i + self.search_link % urllib.quote_plus(url) for i in queries]

            result = ''
            for query in queries:
                try: result += getUrl(query).result
                except: pass

            links = common.parseDOM(result, "div", attrs = { "class": "archive" })
            links = uniqueList(links).list

            title, hdlr = re.compile('(.+?) (\d{4})$').findall(url)[0]
            title = cleantitle().movie(title)
            hdlr = [str(hdlr), str(int(hdlr)+1), str(int(hdlr)-1)]

            dt = int(datetime.datetime.now().strftime("%Y%m%d"))

            for link in links:
                try:
                    name = common.parseDOM(link, "a", attrs = { "title": ".+?" })[-1]
                    name = common.replaceHTMLCodes(name)

                    url = common.parseDOM(link, "a", ret="href")[0]
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    date = re.compile('(/\d{4}/\d{2}/\d{2}/)').findall(url)[0]
                    date = re.sub('[^0-9]', '', str(date))
                    if (abs(dt - int(date)) < 100) == False: raise Exception()

                    cat = common.parseDOM(link, "a", attrs = { "rel": "category tag" })
                    if not any(i.endswith(('3-D Movies', 'BDRip', 'BluRay')) for i in cat): raise Exception()

                    t = re.sub('(\.|\(|\[|\s)(\d{4})(\.|\)|\]|\s)(.+)', '', name)
                    t = cleantitle().movie(t)
                    if not t == title: raise Exception()

                    y = re.compile('[\.|\(|\[|\s](\d{4})[\.|\)|\]|\s]').findall(name)[-1]
                    if not any(i == y for i in hdlr): raise Exception()

                    fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4})(\.|\)|\]|\s)', '', name)
                    fmt = re.split('\.|\(|\)|\[|\]|\s|\-', fmt)
                    fmt = [i.lower() for i in fmt]

                    if '1080p' in fmt: quality = '1080p'
                    else: quality = 'HD'

                    info = ''
                    size = re.compile('Size: (.+? [M|G]B) ').findall(link)
                    if len(size) > 0:
                        size = size[-1]
                        if size.endswith(' GB'): div = 1
                        else: div = 1024
                        size = float(re.sub('[^0-9|/.|/,]', '', size))/div
                        info += '%.2f GB | %s' % (size, quality)
                    else:
                        info += '%s' % quality

                    if '3-D Movies' in cat:
                        info += ' | 3D'

                    try:
                        result = getUrl(url).result
                        result = common.parseDOM(result, "ul")
                        result = str(result)
                    except:
                        pass

                    result = common.parseDOM(result, "a", ret="href")

                    for i in result:
                        try:
                            url = i
                            url = common.replaceHTMLCodes(url)
                            url = url.encode('utf-8')

                            host = re.sub('http(|s)://|www[.]|/.+|[.].+$','', url)
                            host = host.strip().lower()
                            if not host in hosthdDict: raise Exception()

                            info2 = '%s | %s' % (host, info)
                            info2 = info2.upper()

                            sources.append({'source': host, 'quality': quality, 'provider': 'Myvideolinks', 'url': url, 'info': info2})
                        except:
                            pass
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.get(url)
            return url
        except:
            return

class tvrelease:
    def __init__(self):
        self.base_link = 'http://tv-release.net'
        self.search_link = '/?s=%s&cat=TV-720p'

    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            url = show
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return
            url = '%s S%02dE%02d' % (url, int(season), int(episode))
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            query = url.replace('\'', '').replace('.', ' ')
            query = re.sub('\s+',' ',query)
            query = self.base_link + self.search_link % urllib.quote_plus(query)

            result = getUrl(query).result
            links = common.parseDOM(result, "table", attrs = { "class": "posts_table" })

            title, hdlr = re.compile('(.+?) (S\d*E\d*)$').findall(url)[0]
            title = cleantitle().tv(title)
            hdlr = [hdlr]

            dt = int(datetime.datetime.now().strftime("%Y%m%d"))

            for link in links:
                try:
                    name = common.parseDOM(link, "a")[-1]
                    name = common.replaceHTMLCodes(name)

                    url = common.parseDOM(link, "a", ret="href")[-1]
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    date = re.compile('(\d{4}-\d{2}-\d{2})').findall(link)[-1]
                    date = re.sub('[^0-9]', '', str(date))
                    if (abs(dt - int(date)) < 100) == False: raise Exception()

                    t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|3D)(\.|\)|\]|\s)(.+)', '', name)
                    t = cleantitle().tv(t)
                    if not t == title: raise Exception()

                    y = re.compile('[\.|\(|\[|\s](S\d*E\d*)[\.|\)|\]|\s]').findall(name)[-1]
                    if not any(x == y for x in hdlr): raise Exception()

                    fmt = re.sub('(.+)(\.|\(|\[|\s)(S\d*E\d*)(\.|\)|\]|\s)', '', name)
                    fmt = re.split('\.|\(|\)|\[|\]|\s|\-', fmt)
                    fmt = [i.lower() for i in fmt]

                    if '1080p' in fmt: quality = '1080p'
                    else: quality = 'HD'

                    info = ''
                    size = common.parseDOM(link, "td")
                    size = [i for i in size if i.endswith((' MB', ' GB'))]
                    if len(size) > 0:
                        size = size[-1]
                        if size.endswith(' GB'): div = 1
                        else: div = 1024
                        size = float(re.sub('[^0-9|/.|/,]', '', size))/div
                        info += '%.2f GB | %s' % (size, quality)
                    else:
                        info += '%s' % quality

                    result = getUrl(url).result
                    result = common.parseDOM(result, "td", attrs = { "class": "td_cols" })[0]
                    result = result.split('"td_heads"')

                    for i in result:
                        try:
                            url = common.parseDOM(i, "a", ret="href")
                            if not len(url) == 1: raise Exception()
                            url = url[0]
                            url = common.replaceHTMLCodes(url)
                            url = url.encode('utf-8')

                            host = re.sub('http(|s)://|www[.]|/.+|[.].+$','', url)
                            host = host.strip().lower()
                            if not host in hosthdDict: raise Exception()

                            info2 = '%s | %s' % (host, info)
                            info2 = info2.upper()

                            sources.append({'source': host, 'quality': quality, 'provider': 'TVrelease', 'url': url, 'info': info2})
                        except:
                            pass
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.get(url)
            return url
        except:
            return

class directdl:
    def __init__(self):
        self.base_link = 'http://directdownload.tv'
        self.search_link = '/index/search/keyword/%s/qualities/hdtv,dvdrip,realhd,webdl,webdl1080p/from/0/search'

    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            url = show
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return
            url = '%s S%02dE%02d' % (url, int(season), int(episode))
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_cookie(self, username, password):
        try:
            query = self.base_link
            post = urllib.urlencode({'username': username, 'password': password, 'Login': 'Login', 'mode': 'normal'})
            cookie = getUrl(query, post=post, output='cookie').result
            cookie = re.compile('(PHPSESSID=[\w]+)').findall(cookie)[0]
            cookie = base64.urlsafe_b64encode(cookie)
            return cookie
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            query = urllib.quote_plus(url)
            query = self.base_link + self.search_link % query

            cookie = base64.urlsafe_b64decode('UEhQU0VTU0lEPWp1dXZxdmxib3Uxc3V0ZHRqOGZsMDllNG0x')

            result = getUrl(query, cookie=cookie).result
            result = json.loads(result)

            link = urlparse.urlparse(result[0]['links'][0]['url']).path
            if link in ['/', '']: raise Exception()

            result = getUrl(query, cookie=cookie).result
            result = json.loads(result)

            links = result

            title, hdlr = re.compile('(.+?) (S\d*E\d*)$').findall(url)[0]
            title = cleantitle().tv(title)
            hdlr = [hdlr]

            for link in links:
                try:
                    name = link['release']
                    name = common.replaceHTMLCodes(name)

                    t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|3D)(\.|\)|\]|\s)(.+)', '', name)
                    t = cleantitle().tv(t)
                    if not t == title: raise Exception()

                    y = re.compile('[\.|\(|\[|\s](S\d*E\d*)[\.|\)|\]|\s]').findall(name)[-1]
                    if not any(x == y for x in hdlr): raise Exception()

                    p = link['links']
                    p = [i['hostname'] for i in p]
                    if not len(p) == len(uniqueList(p).list): raise Exception()

                    quality = link['quality']
                    quality = common.replaceHTMLCodes(quality)

                    if quality == 'webdl1080p': quality = '1080p'
                    elif quality in ['realhd', 'webdl']: quality = 'HD'
                    else: quality = 'SD'

                    size = link['size']
                    size = float(size)/1024

                    info = '%.2f GB | %s' % (size, quality)
                    info = info.upper()

                    result = link['links']

                    for i in result:
                        try:
                            url = i['url']
                            url = common.replaceHTMLCodes(url)
                            url = url.encode('utf-8')

                            host = re.sub('http(|s)://|www[.]|/.+|[.].+$','', url)
                            host = host.strip().lower()
                            if not host in hosthdDict: raise Exception()

                            info2 = '%s | %s' % (host, info)
                            info2 = info2.upper()

                            sources.append({'source': host, 'quality': quality, 'provider': 'DirectDL', 'url': url, 'info': info2})
                        except:
                            pass
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.get(url)
            return url
        except:
            return

class noobroom:
    def __init__(self):
        self.base_link = 'http://superchillin.com'
        self.search_link = '/search.php?q=%s'
        self.login_link = '/login.php'
        self.login2_link = '/login2.php'
        self.mail = xbmcaddon.Addon().getSetting("noobroom_mail")
        self.password = xbmcaddon.Addon().getSetting("noobroom_password")
        self.login()

    def login(self):
        try:
            if (self.mail == '' or self.password == ''): raise Exception()
            post = urllib.urlencode({'email': self.mail, 'password': self.password})
            getUrl(self.base_link + self.login_link, close=False).result
            getUrl(self.base_link + self.login_link, output='cookie').result
            result = urllib2.Request(self.base_link + self.login2_link, post)
            urllib2.urlopen(result, timeout=5)
        except:
            return

    def get_movie(self, imdb, title, year):
        try:
            if (self.mail == '' or self.password == ''): raise Exception()

            query = urllib.quote_plus(title)
            query = self.base_link + self.search_link % query

            result = getUrl(query).result
            result = re.compile('(<i>Movies</i>.+)').findall(result)[0]
            result = result.split("'tippable'")

            title = '>' + cleantitle().movie(title) + '<'
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [i for i in result if any(x in i for x in years)]
            result = [i for i in result if title in cleantitle().movie(i)][0]
            result = re.compile("href='(.+?)'").findall(result)[0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            if (self.mail == '' or self.password == ''): raise Exception()

            query = urllib.quote_plus(show)
            query = self.base_link + self.search_link % query

            result = getUrl(query).result
            result = re.compile('(<i>TV Series</i>.+)').findall(result)[0]
            result = result.replace('(incomplete)', '')
            result = result.split("><a ")

            title = '>' + cleantitle().tv(show) + '<'
            years = [str(year), str(int(year)+1), str(int(year)-1)]
            result = [i for i in result if title in cleantitle().tv(i)][0]
            result = re.compile("href='(.+?)'").findall(result)[:2]

            for i in result:
                try:
                    result = getUrl(self.base_link + i).result
                    y = re.compile('\d*-\d*-(\d{4})').findall(result)[0]
                    if any(x == y for x in years):
                        match = i
                        break
                except:
                    pass

            result = match

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            url = self.base_link + url

            result = getUrl(url).result
            result = re.compile("<b>%01dx%02d .+?style=.+? href='(.+?)'" % (int(season), int(episode))).findall(result)[0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []
            url = self.base_link + url
            sources.append({'source': 'Noobroom', 'quality': 'HD', 'provider': 'Noobroom', 'url': url})
            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            result = getUrl(url).result
            result = re.compile('"file": "(.+?)"').findall(result)

            url = [i for i in result if 'type=flv' in i]
            url += [i for i in result if 'type=mp4' in i]
            url = self.base_link + url[-1]

            try: url = getUrl(url, output='geturl').result
            except: pass
            try: url = getUrl(url.replace('&hd=0', '&hd=1'), output='geturl').result
            except: pass

            return url
        except:
            return

class furk:
    def __init__(self):
        self.base_link = 'http://api.furk.net'
        self.search_link = '/api/plugins/metasearch'
        self.login_link = '/api/login/login'
        self.user = xbmcaddon.Addon().getSetting("furk_user")
        self.password = xbmcaddon.Addon().getSetting("furk_password")

    def get_movie(self, imdb, title, year):
        try:
            if (self.user == '' or self.password == ''): raise Exception()

            url = '%s %s' % (title, year)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            if (self.user == '' or self.password == ''): raise Exception()

            url = show
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return
            if (self.user == '' or self.password == ''): raise Exception()

            url = '%s S%02dE%02d' % (url, int(season), int(episode))
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            if (self.user == '' or self.password == ''): raise Exception()

            query = self.base_link + self.login_link
            post = urllib.urlencode({'login': self.user, 'pwd': self.password})
            cookie = getUrl(query, post=post, output='cookie').result

            query = self.base_link + self.search_link
            post = urllib.urlencode({'sort': 'relevance', 'filter': 'all', 'moderated': 'yes', 'offset': '0', 'limit': '100', 'match': 'all', 'q': url})
            result = getUrl(query, post=post, cookie=cookie).result
            result = json.loads(result)
            links = result['files']

            title, hdlr = re.compile('(.+?) (\d{4}|S\d*E\d*)$').findall(url)[0]

            if hdlr.isdigit():
                type = 'movie'
                title = cleantitle().movie(title)
                hdlr = [str(hdlr), str(int(hdlr)+1), str(int(hdlr)-1)]
            else:
                type = 'episode'
                title = cleantitle().tv(title)
                hdlr = [hdlr]

            for i in links:
                try:
                    info = i['video_info']
                    if type == 'movie' and not '#0:1(eng): Audio:' in info: raise Exception()

                    name = i['name']
                    name = common.replaceHTMLCodes(name)

                    t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|3D)(\.|\)|\]|\s)(.+)', '', name)
                    if type == 'movie': t = cleantitle().movie(t)
                    else: t = cleantitle().tv(t)
                    if not t == title: raise Exception()

                    y = re.compile('[\.|\(|\[|\s](\d{4}|S\d*E\d*)[\.|\)|\]|\s]').findall(name)[-1]
                    if not any(x == y for x in hdlr): raise Exception()

                    fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*)(\.|\)|\]|\s)', '', name)
                    fmt = re.split('\.|\(|\)|\[|\]|\s|\-', fmt)
                    fmt = [x.lower() for x in fmt]

                    if any(x.endswith(('subs', 'sub', 'dubbed', 'dub')) for x in fmt): raise Exception()
                    if any(x in ['extras'] for x in fmt): raise Exception()

                    res = i['video_info'].replace('\n','')
                    res = re.compile(', (\d*)x\d*').findall(res)[0]
                    res = int(res)
                    if 1900 <= res <= 1920: quality = '1080p'
                    elif 1200 <= res <= 1280: quality = 'HD'
                    else: quality = 'SD'
                    if any(x in ['dvdscr', 'r5', 'r6'] for x in fmt): quality = 'SCR'
                    elif any(x in ['camrip', 'tsrip', 'hdcam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'ts'] for x in fmt): quality = 'CAM'

                    size = i['size']
                    size = float(size)/1073741824
                    if int(size) > 2 and not quality in ['1080p', 'HD']: raise Exception()
                    if int(size) > 5: raise Exception()

                    url = i['url_pls']
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    info = i['video_info'].replace('\n','')
                    v = re.compile('Video: (.+?),').findall(info)[0]
                    a = re.compile('Audio: (.+?), .+?, (.+?),').findall(info)[0]
                    q = quality
                    if '3d' in fmt: q += ' | 3D'

                    info = '%.2f GB | %s | %s | %s | %s' % (size, q, v, a[0], a[1])
                    info = re.sub('\(.+?\)', '', info)
                    info = info.replace('stereo', '2.0')
                    info = ' '.join(info.split())
                    info = info.upper()

                    sources.append({'source': 'Furk', 'quality': quality, 'provider': 'Furk', 'url': url, 'info': info})
                except:
                    pass

            if not all(i['quality'] in ['CAM', 'SCR'] for i in sources): 
                sources = [i for i in sources if not i['quality'] in ['CAM', 'SCR']]

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            query = self.base_link + self.login_link
            post = urllib.urlencode({'login': self.user, 'pwd': self.password})
            cookie = getUrl(query, post=post, output='cookie').result

            result = getUrl(url, cookie=cookie).result
            url = common.parseDOM(result, "location")[0]
            return url
        except:
            return
