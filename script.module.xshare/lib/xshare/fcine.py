# -*- coding: utf-8 -*-
__author__ = 'thaitni'

from .utils import xsearch, xread, xrw, filetime
from .kodi import mess, log

class fcine:
	def __init__(self, HANDLE):
		self.HANDLE = HANDLE
		
		self.hd = {
			'User-Agent'       : 'Mozilla/5.0',
			'Cookie'           : xrw('fcine.cookie')
		}
		
		if not self.hd["Cookie"] or filetime('fcine.cookie') > 1 : self.login()
		
	def login(self):
		import urllib2
		headers = {'Cookie':'ips4_IPSSessionFront=xshare'}
		url     = 'http://fcine.net/login/'
		csrfKey = xsearch('name="csrfKey" value="(.+?)"',xread(url, headers))
		user, passwd = self.getUserPasswd()	
		
		data    = {
			'csrfKey'     : csrfKey,
			'auth'        : user,
			'password'    : passwd,
			'remember_me' : '0',
			'login__standard_submitted' : '1',
			'remember_me_checkbox'      : '1'
		}
		
		cookie  = urllib2.HTTPCookieProcessor()
		opener  = urllib2.build_opener(cookie)
		urllib2.install_opener(opener)
		opener.addheaders = headers.items()
		import urllib
		try    : opener.open(url, urllib.urlencode(data))
		except : pass
		
		cookie = ';'.join('%s=%s'%(i.name,i.value) for i in cookie.cookiejar if 'ips4' in i.name)
		if 'ips4_pass_hash' in cookie:
			mess(u'Login thành công','fcine.net')
			xrw('fcine.cookie',cookie)
			self.hd['Cookie'] = cookie
		else:
			mess(u'Login không thành công!','fcine.net')
		
		return cookie
	
	def getFshare(self, url, loop=True):
		site = 'www.fshare.vn'
		b = xread(url.split('?')[0], self.hd)
		img = xsearch('property="og:image" content="(.+?)"', b)
		sub = xsearch('<a href="(.+?)" class=.+?><b>Tải phụ đề Việt</b></a>',b)
		sub = [sub] if sub else []
		label = xsearch('"og:title" content="(.+?)"',b)
		if label:
			label+=' '
		
		import re
		items = [i for i in re.findall('(<p.+?/p>)',b,re.S) if site in i]
		
		items = [
			(re.sub('<.+?>|\xc2\xa0|\|','',i), xsearch('([\w|:|/]+?%s[\w|:|/]+)'%site,i))
			for i in items
		]
		
		items = [(label+i[0].replace(i[1],'').strip(), i[1], sub) for i in items]
		
		if not items and loop:
			return self.getFshare(url, False)
		
		if items:
			if sub:
				mess('Xshare sẽ tự động load phụ đề của Fcine.net')

			from kodi import addir, endDir
			for label,href,sub in items:
				if sub:
					href = [href] + sub
				
				addir(label, href, img)
		
			endDir(self.HANDLE)
	
		else:
			mess('Không tìm thấy link Fshare')
	
		return
	
	def getUserPasswd(self):
		from kodi import addon
		user = addon.getSetting("fcineUser")
		passwd = addon.getSetting("fcinePasswd")
		
		if not user or not passwd:
			user, passwd = "xshare@thanhthai.net","thaitni"
		
		return user, passwd
