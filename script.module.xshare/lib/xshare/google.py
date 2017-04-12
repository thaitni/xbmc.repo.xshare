# -*- coding: utf-8 -*-
__author__ = 'thaitni'


from .utils import xsearch, xread
from .kodi import mess, log

class google:
	def __init__(self, HANDLE, icon, url, cx):
		self.HANDLE = HANDLE
		self.icon = icon
		self.url = url
		self.cx = cx
	
	def detail(self, i):
		title = i.get('titleNoFormatting','').encode('utf-8')
		href = i.get('unescapedUrl','').encode('utf-8')
		
		if not title or not href:
			return []
		
		if '...' in title:
			s = i.get('richSnippet',{}).get('metatags',{}).get('ogTitle')
			
			if s:
				title = s.encode('utf-8')
			
			elif i.get('contentNoFormatting'):
				s = title.replace('....','...').split('...')[-1]
				if s:
					title = i.get('contentNoFormatting').encode('utf-8')
					title = title.split(s)[0].replace('Thông tin tập tin. ','') + s
		
		try:
			img = i['richSnippet']['cseImage']['src'].encode('utf-8')
		except:
			img = ''
		
		return title, href, img
	
	
	def content(self, start, string):
		string = '+'.join(string.split())
		b = xread(self.url % (self.cx, start, '%22' + string + '%22'))
		
		import json
		try:
			d = json.loads(xsearch('\((\{.+?\})\)',b))
		except:
			d = {}
		
		if not d.get('results',{}):
			mess('Tìm gần đúng ...', 'xshare')
			b = xread(self.url % (self.cx, start, string))
			
			try:
				d = json.loads(xsearch('\((\{.+?\})\)',b))
			except:
				d = {}
		
		items = [i for i in [self.detail(j) for j in d.get('results',{})] if i]
		
		cursor = d.get('cursor',{})
		currentPage = cursor.get('currentPageIndex',1000)
		pages = cursor.get('pages',{})
		start = [i.get('start','') for i in pages if i.get('label',0)==currentPage+2]
		start = ''.join(start).encode('utf-8')
		
		if start:
			title = '[COLOR lime]Page next: %d[/COLOR]' % (currentPage+2)
			items.append((title, start, currentPage+2))
		
		return items
	
	
	
	def tinySearch(self, query):
		if '*#*' in query:
			start = query.split('*#*')[1]
			query = query.split('*#*')[0]
		
		else:
			start = '0'
		
		items = self.content(start,query)
		
		if items:
			from .kodi import addir, endDir
			
			for title, href, img in items:
				menu=[
					('Thêm String vào danh mục search', title, '', '', 'search', 1, 'addString'),
					('Thêm Link vào Home List', title, href, '', 'search', 1, 'addList')
				]
				
				if 'Page next:' in title:
					page = img
					start = href
					query = query + '*#*' + start
					addir(title, '', self.icon, 'search', 1, query, True)
				else:
					addir(title, href, img, isFolder=True, menu=menu)
			
			endDir(self.HANDLE)
		
		else:
			mess('Không tìm thấy thông tin bạn yêu cầu!')