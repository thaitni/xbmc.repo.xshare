# -*- coding: utf-8 -*-
__author__ = 'thaitni'

import re
from .utils import xsearch, xread, xrw
from .kodi import mess, log

class taiphimnet:
	def __init__(self, HANDLE):
		self.hd = {
			'User-Agent' : 'Mozilla/5.0',
			'Cookie' : xrw('taiphimnet.cookie')
		}
		
		self.HANDLE = HANDLE
		if not self.hd['Cookie'] or 'DRUPAL_UID=' not in self.hd['Cookie']:
			self.login()
		
		self.home='http://taiphimhd.net'
	
	def login(self):
		import urllib2
		from urllib import urlencode
		user, passwd = 'eHNoYXJlK3RoYWl0bmk='.decode('base64').split('+')
		
		data = {
			'name' : user,
			'pass' : passwd,
			'form_id' : 'user_login'
		}
		
		data = urlencode(data)
		url = 'http://taiphimhd.net/user?destination=http://taiphimhd.net'
		cookie = urllib2.HTTPCookieProcessor()
		opener = urllib2.build_opener(cookie)
		urllib2.install_opener(opener)
		
		try:
			res = urllib2.urlopen(urllib2.Request(url, data, {'User-Agent': 'xshare'}))
			cookie = ';'.join('%s=%s'%(i.name,i.value) for i in cookie.cookiejar)
		
		except:
			cookie=''
		
		if 'DRUPAL_UID=' in cookie:
			self.hd['Cookie'] = cookie
			xrw('taiphimnet.cookie',cookie)
			mess('Login thành công','taiphimhd.net')
		
		else:
			cookie=''
			mess('Login không thành công!','taiphimhd.net')
		
		return cookie
	
	
	

	def getPage(self, url):
		b = xread(url, self.hd)
		from .kodi import addir, endDir
		
		detail = False
		for s in re.findall('(<div class="search_solr".+?/p>)', b, re.S):
			title = xsearch('(<a class="search_title".+?/a>)', s, 1, re.S)
			title = re.sub('<.+?>', '',title).strip()
			href = xsearch('href="(.+?)"', s)
			img = xsearch('src="(.+?)"', s)
			if title and href:
				detail = True
				addir(title, href, img)
		
		if detail:
			endDir(self.HANDLE)
	
	
	def getFshare(self, url, img):
		def links(b):
			return [
				i for i in re.findall('(<li.+?/b>)',b) 
				if re.search(site+'/[file|folder]',i)
			]
		
		if not "/tai-phim/" in url:
			return self.getPage(url)
		
		site = 'www.fshare.vn'
		b = xread(url, self.hd)
		s = xsearch('(<strong>FSHARE.+?/ul>)', b, 1, re.S)
		#items = links(b)
		
		if not s and "/logout" not in b:
			self.login()
			b = xread(url, self.hd)
			s = xsearch('(<strong>FSHARE.+?/ul>)',b,1,re.S)
		
		title = xsearch('"og\:title" content="(.+?)"',b)
		
		def label(i):
			i=re.sub('<.+?>','',i).replace('CLICK VÀO ĐÂY TẢI PHIM VỀ MÁY','').strip()
			a=xsearch('\|(.+)',i).strip()
			if not a:a=i+' '+title
			return a
		
		items = [
			i for i in re.findall('(<li.+?[/li|/b]>)', s) 
			if re.search(site + '/[file|folder]', i)
		]
		
		items = [(label(i), xsearch('([\w|:|/]+?%s[\w|:|/]+)'%site,i), "") for i in items]
		
		if items:
			s = xsearch('(<strong>Phụ Đề.+?/ul>)', b, 1, re.S)
			subs = [i for i in re.findall('(<li.+?[/li|/b]>)', s)]
			subs = [xsearch('href="(.+?)"',i) for i in subs]
			if subs:
				mess('Xshare sẽ tự động load phụ đề của taiphimhd.net')
				items = [(i[0], i[1], subs) for i in items]
			
			from .kodi import addir, endDir
			for label,href,sub in items:
				if sub:
					href = [href] + sub
				addir(label, href, img)
			
			endDir(self.HANDLE)
		
		else:
			mess('Không tìm thấy link Fshare')
