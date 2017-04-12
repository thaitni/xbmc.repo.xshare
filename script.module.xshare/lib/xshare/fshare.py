# -*- coding: utf-8 -*-
__author__ = 'thaitni'


from .utils import xread, xsearch, xrw
from .kodi import xshareKey, mess, log

class fshare:
	def __init__(self, HANDLE, user="", passwd=""):
		self.key  = xshareKey
		self.HANDLE = HANDLE
		self.user   = user
		self.passwd = passwd
		cookie = xrw('fshare.cookie').split('-')
		
		try:
			self.session_id = cookie[0]
			self.token      = cookie[1]
		except:
			self.session_id = ""
			self.token      = ""
		
		try    : self.acc = cookie[2]
		except : self.acc = ""
		
		if self.session_id:
			self.hd = {'Cookie' : 'session_id=' + self.session_id}
			status = self.results("https://api2.fshare.vn/api/user/get", self.hd)
			if not status or status.get("code", 0) == 201:
				self.login(self.user, self.passwd)
			else:
				self.vip = self.getVIP(self.session_id)
		
		else:
			self.login(self.user, self.passwd)
	
	
	
	
	def results(self, url, hd = {'User-Agent':'Mozilla/5.0'}, data = None):
		import json
		try:
			j = json.loads( xread(url, hd, data) )
		
		except:
			j = {}
		
		return j
	
	
	
	
	def login(self, user, passwd):
		data   = '{"app_key" : "%s", "user_email" : "%s", "password" : "%s"}'
		data   = data % (self.key, user, passwd)
		result = self.results("https://api2.fshare.vn/api/user/login", data = data)
		
		if result.get("code", 0) == 200:
			self.session_id  = result.get("session_id")
			self.token = result.get("token")
			self.hd = {'Cookie' : 'session_id=' + self.session_id}
			self.vip = self.getVIP(self.session_id)
			xrw('fshare.cookie', self.session_id + "-" + self.token + "--" + self.key)

			if not self.vip:
				mess("Acc của bạn đã hết hạn VIP", "Fshare.vn")
			else:
				mess("Login thành công", "Fshare.vn")
				
		else:
			self.vip = False
			self.hd = {'Cookie' : ''}
			mess( "Login không thành công!", "Fshare.vn")
	
	
	
	
	def getVIP(self, session_id):
		hd = {'Cookie' : 'session_id=' + session_id}
		userInf = self.results("https://api2.fshare.vn/api/user/get", hd)
		if userInf.get("account_type", "") == "Bundle":
			vip = 1
		else:
			try    : vip = int(userInf.get("expire_vip","-1"))
			except : vip = -1
			if vip > -1: 
				from time import time
				vip = 1 if time() < vip else -1

		return  vip >= 0
	
	
	
	
	def getFile(self, url):
		href = "https://api2.fshare.vn/api/fileops/get"
		data = '{"token" : "%s", "url" : "%s"}'%(self.token, url)
		return self.results(href, self.hd, data)
	
	
	
	
	def listFolder(self, url, page, img):
		urls = url
		if url.startswith('[') and url.endswith(']'):
			subs = eval(url)
			url  = subs[0]
			subs.pop(0)
		else:
			subs = []
		
			
		href = "https://api2.fshare.vn/api/fileops/getFolderListPaging"
		data = '{"token" : "%s", "url" : "%s", "page_index" : "%s" , "page_size" : "50"}'
		data = data % (self.token, url, page-1)
		result = self.results(href, self.hd, data)

		if result:
			def toSize(s):
				gb=2**30;mb=2**20
				try    : s = int(s)
				except : s = 0
				if   s > gb : s = '{:.2f} GB'.format(s/gb)
				elif s > mb : s = '{:.0f} MB'.format(s/mb)
				else        : s = '{:.2f} MB'.format(s/mb)
				return s

			items = []
			for item in sorted(result, key=lambda k: k.get('name')):
				title  = item["name"]
				
				if item["file_type"] == "1":
					href   = "https://www.fshare.vn/file/"   + item["linkcode"]
					title += " [COLOR green](%s)[/COLOR]"    % toSize(item["size"])
				else:
					id = xsearch('([A-Z0-9]{10,})', title)
					if id:
						id = id.replace('FILE', '').replace('FOLDER', '')
						detail = self.getFile('https://www.fshare.vn/file/' + id)
						if detail:
							title = detail["name"]
							if detail.get("file_type") == "1":
								href = "https://www.fshare.vn/file/"   + id
								title += " [COLOR green](%s)[/COLOR]"    % toSize(detail["size"])
							else:
								#title = title.replace(id + ' ', '').replace('Fshare-', '')
								#title = '[COLOR lime]%s[/COLOR]' % title
								href = "https://www.fshare.vn/folder/"   + id
					else:
						href = "https://www.fshare.vn/folder/" + item["linkcode"]
				
				items.append((title,href))
		
		
			from .kodi import addir, endDir
			for title, href in items:
				if subs:
					href = [href] + subs
				addir(title, href, img)
			
			if len(items) > 49:
				title = "[COLOR lime]Trang tiếp theo[/COLOR]"
				addir(title, urls, img, 'fshare.vn', page + 1, 'folder', True)
			
			endDir(self.HANDLE)
		
		else:
			mess("Thư mục không có dữ liệu")
	
	
	
	
	def thanks(self):
		mess("[COLOR cyan]Bạn đang dùng Acc của Xshare. Hãy mua Fshare VIP acc nhé[/COLOR]")
	
	
	
	
	def getToken(self):
		from .kodi import addon
		return addon.getAddonInfo("id")
	
	
	
	
	def getLink(self, url, passwd = ""):
		if not self.session_id:
			return ""
		
		url = "https://www.fshare.vn/file/" + xsearch('([\w|-]{10,})', url)
		data = '{"token" : "%s", "url" : "%s", "password" : "%s"}'
		data = data % (self.token, url, passwd)
		result = self.results("https://api2.fshare.vn/api/session/download", self.hd, data)
		
		link = ""
		if result.get("location"):
			link = result.get("location")
		
		elif result.get("code", 0) == 123 and not passwd:
			from .utils import get_input
			passwd = get_input(u'Hãy nhập: Mật khẩu tập tin')
			if passwd:
				link = self.getLink(url, passwd)
		
		if not link:
			link = "Failed"
		
		elif link and self.acc:
			self.thanks()
		
		return link
	
	
	
	
	
	def getLinkFshare(self, url):
		link = self.getLink(url)
		
		linkFree =""
		if not self.vip:
			from .kodi import addon
			if addon.getSetting("useFshareAccShared") == "true":
				from urllib import urlencode
				data = urlencode({"url" : url, "token" : self.getToken()})
				linkFree = xread('http://xshare.eu5.org/newfshare.php', data=data)
				if not linkFree:
					linkFree = xread('http://ycofo.xyz/newfshare.php', data=data)
				
				if linkFree:
					link = linkFree
			
		
		if link == "Failed":
			if "không tồn tại" in xread(url):
				mess("Tập tin quý khách yêu cầu không tồn tại")
				return link
			
			else:
				link = ""
		
		if link and not linkFree and not self.vip:
			mess("Bạn nhận được link No VIP")
		return link
	
	
	
	
	def download(self, url, fn):
		resp = xread(url, read=False)
		if resp:
			size = resp.info().dict.get("content-length", 0)
			if int(size) < 512000:
				return xrw(fn, resp.read())
		return False
	
	
	
	
	def play(self, url, autoLoadSub=True):
		if url.startswith('[') and url.endswith(']'):
			subs = eval(url)
			url  = subs[0]
			subs.pop(0)
		else:
			subs = []
		
		link = self.getLinkFshare(url)
		if link and link != "Failed":
			import os, re
			from .kodi import listItem, subsFolder, setResolvedUrl
			
			try    : ext = link.rsplit('.',1)[1]
			except : ext = ""
			
			if ext.lower() in ['srt','sub','txt','smi','ssa','ass','nfo']:
				from .utils import deleteSubFolder
				deleteSubFolder()
				
				fn = os.path.join(subsFolder, link.rsplit('/',1)[1])
				if self.download(link, fn):
					mess('Đã downloads subtitle file vào thư mục xshare sub')
				else:
					mess('Lỗi download file phụ đề!')
				
				setResolvedUrl(self.HANDLE, False, listItem(None))
				return ""
			
			if subs:
				for i in range(len(subs)):
					sub = subs[i]
					subs[i] = "None"
					if "www.fshare.vn" in sub:
						sub = self.getLinkFshare(sub)
						if sub:
							subs[i] = sub
					
					elif True:
						subs[i] = sub
					
					elif "fcine.net" in sub:
						from urllib import urlretrieve
						temp = os.path.join(subsFolder, "temp.txt")
						try:
							resp = urlretrieve(sub, temp)
							disposition = resp[1].getrawheader('content-disposition')
							fn = xsearch('filename=([^\s]+)', disposition)
							if fn:
								fn = os.path.join(subsFolder, 'Vie.' + fn)
								if os.path.isfile(fn):
									os.remove(fn)
								os.rename(temp, fn)
								subs[i] = fn
						except: pass
						
					elif "taiphimhd.net" in sub:subs[i] = sub
				
				while "None" in subs:
					subs.remove("None")
				
			
			item = listItem(path=link)
			def setSubtitles(item, subs):
				if len(subs) > 1:
					mess('Xshare auto loaded [COLOR cyan]Multi subtitles[/COLOR]')
				else:
					mess('Xshare auto loaded subtitles')
				item.setSubtitles(subs)
			
			if subs:
				setSubtitles(item, subs)
			
			elif autoLoadSub:
				subs = []
				for fn in os.listdir(subsFolder):
					fp = os.path.join(subsFolder,fn)
					if re.split('\.|-| ',fn.replace('Vie.','').lower())[0] in link.lower():
						subs.append(fp)
				
				if subs:
					setSubtitles(item, subs)
			
			setResolvedUrl(self.HANDLE,True,item)
		
		else:
			from .kodi import setResolvedUrl, listItem
			setResolvedUrl(self.HANDLE, False, listItem(None))
