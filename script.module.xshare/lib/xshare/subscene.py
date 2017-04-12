# -*- coding: utf-8 -*-
__author__ = 'thaitni'


from .utils import xsearch, xread, xrw
from .kodi import mess, log

class subscene:
	def __init__(self, HANDLE, url):
		items = self.getSubs(url)
		
		if not items:
			mess('Không tìm thấy sub!')
		
		elif isinstance(items, basestring) or (isinstance(items, list) and len(items)==1):
			if isinstance(items, list):
				items = items[0][1]
			
			mess("Đang download ...")
			if self.download(items):
				mess("Đã downloads sub file vào thư mục xshare sub")
			else:
				mess('Lỗi download sub file!')
		
		else:
			from .kodi import addir, endDir
			for label, href, img in items:
				label = '[COLOR green]Subscene[/COLOR] ' + label
				addir(label, href, img, 'subscene', 1, '', True)
			endDir(HANDLE)
	
	
	
	def fixUrl(self, url):
		if url and not url.startswith('http'):
			url = "https://subscene.com" + url
		return url.replace('amp;','').replace(' ','%20')
	
	
	
	def getSubs(self, url):
		url = self.fixUrl(url)
		id = xsearch('/(\d{5,})', url)
		
		items = []
		if id:
			items = self.getLink(url.split(id)[0] + id)
				
		else:
			#url = "https://subscene.com/subtitles/" + xsearch('subtitles/([\w|-]+)', url)
			b = xread(url, {'User-Agent':'Mozilla/5.0',	'Cookie':'LanguageFilter=13,45'})
			img = xsearch('<img src="(.+?)"', b)
			
			import re
			for s in re.findall('(<td class="a1".+?/td>)', b, re.S):
				href = xsearch('<a href="(.+?)"', s)
				
				if not href:
					continue
				
				label = xsearch('<span>(.+?)</span>', s, 1, re.S).strip()
				if "vietnamese" in href:
					thumb = "[COLOR red]%s[/COLOR]" % "vie"
				else:
					thumb = "[COLOR cyan]%s[/COLOR]" % "eng"
				items.append((thumb + ' ' + label, href, img))
			
			if len(items)==1:
				log(items[0][1])
				items = self.getLink(items[0][1])
			
			else:
				items = sorted(items, key=lambda k: k[1], reverse=True)
		
		return items
	
	
	
	
	def download(self, url):
		from .kodi import subsFolder
		import os
		
		result = False
		resp = xread(self.fixUrl(url), read=False)
		
		if resp.code != 200:
			return result
		
		type = resp.info().dict.get("content-type", "")
		fn = xsearch('filename=([^\s]+)', resp.info().dict.get("content-disposition", ""))
		
		fn = os.path.join(subsFolder, fn)
		if "compressed" in type and xrw(fn, resp.read(), "wb"):
			try:
				from .kodi import executebuiltin
				executebuiltin(('XBMC.Extract("%s","%s")' % (fn, subsFolder)), True)
				os.remove(fn)
				result = True
			except:
				pass
		
		elif xrw(fn, resp.read(), "wb"):
			result = True
		
		return result
	
	
	
	
	def getLink(self, url):
		return self.fixUrl(xsearch('href="([^"]*/download[^"]+)"', xread(self.fixUrl(url))))
