# -*- coding: utf-8 -*-
__author__ = 'thaitni'

import re
from .utils import xsearch, xread
from .kodi import mess, log

class vaphim:
	def __init__(self, HANDLE):
		self.home = 'http://vaphim.com/'
		self.HANDLE = HANDLE
	
	def getLinks(self, url):
		if '/tag/' in url:
			url = xsearch('class="entry-title"><a href="([^"]+?)"', xread(url))
		
		b    = xread(url)
		img  = xsearch('"image" content="(.+?)"', b)
		
		b    = xsearch('(id="tabs_.+?"text/javascript">)',b, 1, re.S)
		
		pattern = "fshare.vn|subscene.com"
		links = [
			i for i in re.findall('(<div id="tabs-.+?/p>)', b, re.S)
			if re.search(pattern, i)
		]
		
		items = []
		pattern = "Phụ đề Việt|Phụ Đề Việt"
		
		for s in links:
			lines = re.findall("(<a.+?/a>)", s)
			phude = [i for i in lines if re.search(pattern, i)]
			
			if phude and "fshare.vn" in phude[0]:
				subFshare = xsearch('href="(.+?)"', phude[0])
			else:
				subFshare = ""
			
			for s in re.findall("(<a.+?/a>)", s):
				title = ' '.join(re.sub('<.+?>', '', s).split())
				href = xsearch('href="(.+?)"', s)
				
				if href == subFshare:
					continue
				
				elif "fshare.vn" in href:
					if subFshare:
						href = [href, subFshare]
				
				items.append((title, href, img))
		
		if items:
			from .kodi import addir, endDir
			for title, href, img in items:
				addir(title, href, img)
			
			endDir(self.HANDLE)
		
		else:
			mess('Không tìm thấy link Fshare')
