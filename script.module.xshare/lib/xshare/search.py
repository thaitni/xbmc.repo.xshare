# -*- coding: utf-8 -*-
__author__ = 'thaitni'


class search:
	def __init__(self, HANDLE, name, url, icon, query, page):
		self.HANDLE = HANDLE
		self.icon = icon
		from .utils import xsharetinyData
		self.data = xsharetinyData()
		
		if query == 'search':
			self.makeList()
		
		elif query == "inputLink":
			self.linkSearch()

		elif query == "addList":
			self.addList(name, url)
		
		elif query == "renameList":
			self.renameList(name, url)
		
		elif query == "removeList":
			self.removeList(name, url)
		
		elif query == "addString":
			self.addString(name)
		
		elif query == "renameString":
			self.renameString(name, page)
		
		elif query == "removeString":
			self.removeString(name, page)
		
		else:
			self.doSearch(query)

	
	
	def addList(self, name, url):
		from .kodi import get_input, mess
		from .utils import  xrw
	
		self.data[url] = name
		import json
		xrw('xsharetiny.json', json.dumps(self.data))
		mess('Đã thêm Link vào Home List')
	
	def renameList(self, name, url):
		from .kodi import get_input, executebuiltin, mess
		from .utils import namecolor, xrw
		
		newName = get_input('Hãy nhập tên mới', namecolor(name))
		
		if newName:
			self.data[url] = newName
			import json
			xrw('xsharetiny.json', json.dumps(self.data))
			mess('Đã sửa tên 1 mục')
			executebuiltin("Container.Refresh")
	
	def removeList(self, name, url):
		from .kodi import executebuiltin, mess
		from .utils import namecolor, xrw
		
		try:
			self.data.pop(url)
			import json
			xrw('xsharetiny.json',json.dumps(self.data))
			mess('Đã xóa mục '+namecolor(name))
			executebuiltin("Container.Refresh")
		except:pass
	
	def addString(self, name):
		from .kodi import get_input, mess
		from .utils import namecolor, xrw
	
		name = namecolor(name)
		self.data['searchString'].append(name)
		import json
		xrw('xsharetiny.json', json.dumps(self.data))
		mess('Đã thêm String vào danh mục search')
	
	def renameString(self, name, index):
		from .kodi import get_input, executebuiltin, mess
		from .utils import namecolor, xrw
		
		newName = get_input('Hãy nhập tên mới', namecolor(name))
		
		if newName:
			self.data['searchString'][index] = newName
			import json
			xrw('xsharetiny.json', json.dumps(self.data))
			mess('Đã sửa tên 1 mục')
			executebuiltin("Container.Refresh")
	
	def removeString(self, name, index):
		from .kodi import executebuiltin, mess
		from .utils import namecolor, xrw
		
		try:
			self.data['searchString'].pop(index)
			import json
			xrw('xsharetiny.json',json.dumps(self.data))
			mess('Đã xóa mục '+namecolor(name))
			executebuiltin("Container.Refresh")
		except:pass
	
	def makeList(self):
		from .utils import namecolor, u2s
		from .kodi import addir, endDir
		
		label = namecolor('Nhập chuổi tìm kiếm mới','orange')
		addir(label, '', self.icon, "search", 1, 'input', True)
		
		sringSearch = self.data.get('searchString',[])
		for i in range(len(sringSearch)):
			name = u2s(sringSearch[i])
			
			menu = [
				('Đổi tên mục này', name, '','','search',i,'renameString'),
				('Xóa mục này',name,'','','search',i,'removeString')
			]
			
			addir(name, '', self.icon, "search", 1, name, True, menu)
		
		endDir(self.HANDLE)

	
	
	

	def doSearch(self, query):
		if query == 'input':
			from .kodi import get_input
			query = get_input('Hãy nhập chuổi tên phim cần tìm')
		
		if query:
			from .utils import s2u, xrw
			import json
			
			if not self.data.has_key('searchString'):
				self.data['searchString'] = [query]
				xrw('xsharetiny.json', json.dumps(self.data))
			
			elif '*#*' not in query and s2u(query) not in self.data['searchString']:
				self.data['searchString'].append(query)
				xrw('xsharetiny.json', json.dumps(self.data))
				
			from .google import google
			url = 'https://www.googleapis.com/customsearch/v1element?'\
			'key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=20&hl=vi&'\
			'prettyPrint=false&source=gcsc&gss=.com&googlehost=www.google.com&'\
			'callback=google.search.Search.apiary19044&alt=json&cx=%s&start=%s&q=%s'
			cx = '009789051051551375973:xekpkwarjri'
			gg = google(self.HANDLE, self.icon, url, cx)
			gg.tinySearch(query)



	def linkSearch(self):
		from .kodi import get_input
		string = get_input('Hãy nhập link/ID Fshare')
		
		if not string:
			pass
		
		elif len(string) < 10:
			mess('Bạn nhập ID link chưa đúng: ' + string)
		
		else:
			from .utils import xsearch
			from .fshare import fshare
			from .kodi import addon
			id = xsearch('(\w{10,})', string)
			fs = fshare(HANDLE, addon.getSetting("fshareUser"), addon.getSetting("fsharePasswd"))
			url = 'https://www.fshare.vn/file/' + id
			data = fs.getFile(url)
			type = data.get("file_type")
			
			if not type:
				mess('Không tìm thấy thông tin')
			
			else:
				from .kodi import addir, endDir
				if type == "0":
					url = 'https://www.fshare.vn/folder/' + id
				
				title = data.get("name").encode("utf-8")

				if not self.data.get(url):
					self.data[url] = title
					from .utils import xsharetinyData
					xsharetinyData(self.data)
				
				addir(title, url, icon)
				
				endDir(HANDLE)
