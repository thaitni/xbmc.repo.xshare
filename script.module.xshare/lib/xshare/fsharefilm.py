# -*- coding: utf-8 -*-
__author__ = 'thaitni'


from .utils import xsearch, xread
from .kodi import mess, log

class fsharefilm:
	def __init__(self, HANDLE, url, query):
		self.HANDLE = HANDLE
		self.url = url
		if not query:
			self.getLink()
		
		elif query =="play":
			self.play()
		
		elif query == "fsharefilmPlay":
			self.fsharefilmPlay()
		
	def fsharefilmPlay(self):
		b = xread(self.url)
		href = xsearch("var ajaxurl\W+'(.+?)'", b)
		url = xsearch("var url\W+'(.+?)'", b)
		sub = xsearch("var sub\W+'(.+?)'", b)
		sub_eng = xsearch("var sub_eng\W+'(.+?)'", b)
		id_post = xsearch("var id_post\W+'(.+?)'", b)
		id_ep = xsearch("var id_ep\W+'(.+?)'", b)
		is_drive = xsearch("var is_drive\W+'(.+?)'", b)
		
		from urllib import urlencode
		import json
		param = urlencode(
			{'url':url, 'sub':sub, 'subeng':sub_eng, 'id_post':id_post, 'id_ep':id_ep}
		)
		
		a = xread("{}?action=get_player&{}".format(href,param))
		try:
			j = json.loads(xsearch('linkdownload\W+(\{.+?\})', a))
		except:
			j = {}
		
		items = [(j.get(key), xsearch('(\d+)', key)) for key in j]
		items   = sorted(items, key=lambda k: int(k[1]),reverse=True)

		link=''
		for href,label in items:
			try:
				link = xread(href, read=False).geturl()#;xbmc.log(href)
				if link:
					break
			except:
				pass
		
		from .kodi import setResolvedUrl, listItem
		if link:
			setResolvedUrl(self.HANDLE,True,listItem(path=link))
		else:
			setResolvedUrl(self.HANDLE, False, listItem(None))
			

	
	
	
	def getLink(self):
		import re
		b = xread(self.url)
		
		a = xread(xsearch('<a href="(.+?)" target="_blank">Download</a></p>', b))
		img = xsearch('src="(.+?)"', xsearch('(<div class="poster".+?/div)', a, 1, re.S))
		if not img:
			img = xsearch('<img width.+?src="(.+?)"', b)
		
		title = xsearch('"og:title" content="(.+?)"', b)
		
		from .kodi import addir, endDir
		items = re.findall('(<tr id=.+?/tr>)', a, re.S)
		if items:
			for s in items:
				if "fshare.vn" not in s:
					continue
				
				href = xsearch('href="(.+?)"', s)
				label = re.sub('<.+?>', '', s)
				label = ' '.join(label.replace("fshare.vn","").replace("Download","").split())
				label = title + ' [COLOR green]' + label + '[/COLOR]'
				addir(label, href, img, 'fsharefilm.com', 1, 'play')
		
		else:
			a    = xsearch('(id="tabs_.+?"text/javascript">)',b, 1, re.S)
			
			pattern = "fshare.vn|subscene.com"
			links = [
				i for i in re.findall('(<div id="tabs-.+?/p>)', a, re.S)
				if re.search(pattern, i)
			]
			
			items = []
			pattern = "Phụ đề Việt|Phụ Đề Việt"
			
			for s in links:
				lines = re.findall("(<a.+)", s)
				phude = [i for i in lines if re.search(pattern, i)]
				
				if phude and "fshare.vn" in phude[0]:
					subFshare = xsearch('href="(.+?)"', phude[0])
				else:
					subFshare = ""
				
				for s in lines:
					href = xsearch('href="(.+?)"', s)
					label = ' '.join(re.sub('<.+?>', '', s).replace(href, '').split())

					if href == subFshare:
						continue
					
					elif "fshare.vn" in href:
						if subFshare:
							href = [href, subFshare]
					
					label = '[COLOR green]%s[/COLOR] ' % label
					
					items.append((title+label , href, img))
			
			if items:
				for label, href, img in items:
					addir(label, href, img)
				
				
			
			else:
				mess('Không tìm thấy link Fshare')
	
	
		fsharefilmLink = xsearch('(<ul class="nav nav-pills bx-servers".+?/section>)', b, 1, re.S)
		if fsharefilmLink:
			from .kodi import add_sep_item
			add_sep_item("Link của fsharefilm")
			
			for s in re.findall('(<div id=.+)', fsharefilmLink, re.S):
				label = xsearch('id="(.+?)"', s)
				for href, epi in re.findall('href="(.+?)">(.+?)</a>', s):
					label = '[COLOR green]%s %s[/COLOR] ' % (label, epi)
					addir(label+title, href, img, 'fsharefilm.com', 1, 'fsharefilmPlay')
		
		if items or fsharefilmLink:
			endDir(self.HANDLE)

	def play(self):
		b = xread(self.url)
		linkFshare = xsearch("window.location.href='(.+?)'", b)
		if linkFshare:
			from .fshare import fshare
			from .kodi import addon
			user, passwd = addon.getSetting("FshareUser"), addon.getSetting("FsharePasswd")
			fs = fshare(self.HANDLE, user, passwd)
			fs.play(linkFshare)
		
