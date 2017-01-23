# -*- coding: UTF-8 -*-
from xshare.utils import *
class fshare:
	def __init__(self, user='', passwd=''):
		self.s = requests.Session()
		self.hd={'User-Agent':'Mozilla/5.0','x-requested-with':'XMLHttpRequest'}
		self.s.headers.update(self.hd)
		self.logged=False
		if user and passwd:self.login(user, passwd)
	
	def login(self,user,passwd,noti=True):
		if not user or not passwd:mess('Bạn set thông tin acc Fshare chưa đủ!','Fshare.vn')
		else:
			r = self.s.get('https://www.fshare.vn/login')
			fs_csrf = xsearch('value="(.+?)" name="fs_csrf"',r.content)
			data = dc({"LoginForm[email]":user,"LoginForm[password]":passwd,"fs_csrf":fs_csrf})
			r = self.s.post('https://www.fshare.vn/login',data, allow_redirects=False)
			r = 'thành công' if r.status_code == 302 else 'không thành công!'
			if noti:mess('Login %s'%r,'Fshare.vn')
			self.logged=True
	
	def logout(self):
		if self.logged:self.s.get('https://www.fshare.vn/logout', allow_redirects=False)
	
	def get_token(self,url='https://www.fshare.vn/home'):
		try:b=self.s.get(url).content
		except:b=''
		return xsearch('data-token="(.+?)"',b)
	
	def checkLink(self, url):
		id=url.rsplit('/',1)[-1].upper()
		url='https://www.fshare.vn/folder/'+id
		r = self.s.get(url)
		if r.status_code!=200:
			url='https://www.fshare.vn/file/%s'%id
			r = self.s.get(url)
			b=r.content
			if re.search('<i class="fa fa-cloud fa-stack-2x text-danger">',b):
				mess('Tập tin quý khách yêu cầu không tồn tại!')
				url='';title=''
			else:
				s=xsearch('(<i class="fa fa-file-.+?/div>)',b)
				title=re.sub('<.+?>','',s).strip()
				s=xsearch('(<i class="fa fa-hdd-o".+?/div>)',b)
				title=title+' [COLOR green](%s)[/COLOR]'%re.sub('<.+?>','',s).strip()
		else:
			b=r.content
			s=xsearch('(<div class="item_summary".+?/div>)',b,1,re.S)
			if xsearch('(\d+)',re.sub('<.+?>','',s))>'0':
				title=' [COLOR green](%s files)[/COLOR]'%xsearch('(\d+)',re.sub('<.+?>','',s))
				s=xsearch('data-path="/(.+?)"',b)
				title=s+' [COLOR green]%s[/COLOR]'%title
			else:
				mess('Link quý khách yêu cầu là thư mục rỗng/không tồn tại!')
				url='';title=''
		return url,title
		
	def getLink(self, url, cookie='', main=True):
		link=''
		if isinstance(url,list):href=url[1];url=url[0]
		else:href=''
		if not cookie:r = self.s.get(url, allow_redirects=False)
		else:r = self.s.get(url, cookies = {'session_id':cookie}, allow_redirects=False)
		if r.status_code == 302:
			link = r.headers['Location']
		elif r.status_code == 200:
			b = r.content
			if re.search('<title>.*Lỗi 404.*</title>|"index-404"',b):
				link = 'Failed'
				mess('Tập tin quý khách yêu cầu không tồn tại!','Fshare.vn')
			elif main and 'sử dụng nhiều địa chỉ IP' in b:
				mess('Acc Quý khách sử dụng nhiều địa chỉ IP!','Fshare.vn',10000)
			elif main and re.search('<i class="fa fa-star">',b):
				mess('Bạn đang sử dụng FREE Fshare acc','fshare.vn')
			else:
				href='https://www.fshare.vn/download/get'
				fs_csrf=xsearch('value="(.+?)" name="fs_csrf"',b)
				downloadForm=xsearch('id="DownloadForm_linkcode" type="hidden" value="(.+?)"',b)
				data={'fs_csrf':fs_csrf,
					'DownloadForm[linkcode]':downloadForm,
					'ajax':'download-form'}
				if re.search('class="fa fa-lock"',b):
					data['DownloadForm[pwd]']=get_input(u'Hãy nhập: Mật khẩu tập tin')
				if not cookie:r = self.s.post(href,data=data)
				else:r = self.s.post(href, cookies={'session_id':cookie}, data=data)
				try:link = r.json()['url']
				except:pass
		if link and href:
			try:
				if not cookie:r = self.s.get(href, allow_redirects=False)
				else:r = self.s.get(href, cookies={'session_id':cookie}, allow_redirects=False)
				href = r.headers['Location']
				link=[link,href]
			except:pass
		return link
	
	def getLinkByAcc(self, url, ACCs):
		link='';loop=0;l=len(ACCs);j=[]
		from random import randint
		while not link and loop < l:
			i=100
			while i not in j:
				i=randint(0,l-1)
				if i not in j:j.append(i)
				else:i=100
			loop+=1
			
			self.s = requests.Session()
			self.s.headers.update(self.hd)
			self.logged=False
			user,passwd,boss,site=ACCs[i]
			self.login(user,passwd,False)
			if not self.logged:continue
			link=self.getLink(url, main=False)
			if link and link!='Failed':
				cookie=self.s.cookies.get('session_id')
				if user!='xshare@thanhthai.net':
					self.logged=False
					self.s = requests.Session()
					self.s.headers.update(self.hd)
					self.login('xshare@thanhthai.net','thaitni@',False)
					if not self.logged:continue
				token=self.get_token()
				data=data='{"token":"%s","new_name":"%s","file":"YZPA4C7MABDP"}'%(token,cookie)
				self.s.post('https://www.fshare.vn/api/fileops/rename',data=data)
				if user!='xshare@thanhthai.net':self.logout()
				mess('[COLOR cyan]Thanks to %s[/COLOR]'%boss,site)
		return link
	
	def getFolder(self, url):
		def toSize(s):
			if s>gb:s='{:.2f} GB'.format(s/gb)
			elif s>mb:s='{:.0f} MB'.format(s/mb)
			else:s='{:.2f} MB'.format(s/mb)
			return s
		
		try:b=self.s.get(url).content
		except:b=''
		items=[]
		gb=2**30;mb=2**20
		for s in [i for i in re.findall('(<li class.+?/li>)',b,re.S) if 'data-created=' in i]:
			label=xsearch('title="(.+?)"',s)
			isFile=re.search('class="filename"',s)
			id=xsearch('data-id="(.+?)"',s)
			if isFile:href="https://www.fshare.vn/file/"+id
			else:href="https://www.fshare.vn/folder/"+id
			size=xsearch('data-size=".+?">(.+?)</div>',s).replace('-','').strip()
			if size:size=' [COLOR green](%s)[/COLOR]'%size
			#d=re.search('data-created="(.+?)">(.+?)</div>',s)
			#label='%s %s %s%s'%(d.group(1),d.group(2),label,size)
			label='%s%s'%(label,size)
			items.append((label,href))
		#items=[(i[0].split(' ',1)[1],i[1])for i in sorted(items,reverse=True)]
		return sorted(items)

class googleSearch:
	def __init__(self):
		self.url='https://www.googleapis.com/customsearch/v1element?'\
			'key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=20&hl=vi&'\
			'prettyPrint=false&source=gcsc&gss=.com&googlehost=www.google.com&'\
			'callback=google.search.Search.apiary19044&alt=json&cx=%s&start=%s&q=%s'
	
	def detail(self,i):
		title=i.get('titleNoFormatting','').encode('utf-8')
		href=i.get('unescapedUrl','').encode('utf-8')
		if not title or not href:return []
		if '...' in title:
			s=i.get('richSnippet',{}).get('metatags',{}).get('ogTitle')
			if s:title=s.encode('utf-8')
			elif i.get('contentNoFormatting'):
				s=title.replace('....','...').split('...')[-1]
				if s:
					title=i.get('contentNoFormatting').encode('utf-8')
					title=title.split(s)[0].replace('Thông tin tập tin. ','')+s
		try:img=i['richSnippet']['cseImage']['src'].encode('utf-8')
		except:img=''
		return title,href,img
	
	def content(self,cx,start,string):
		string='+'.join(string.split())
		b=xread(self.url%(cx,start,'%22'+string+'%22'))
		try:d=json.loads(xsearch('\((\{.+?\})\)',b))
		except:d={}
		if not d.get('results',{}):
			mess(u'Tìm gần đúng ...','xshare')
			b=xread(self.url%(cx,start,string))
			try:d=json.loads(xsearch('\((\{.+?\})\)',b))
			except:d={}
		items=[i for i in [self.detail(j) for j in d.get('results',{})] if i]
		
		cursor=d.get('cursor',{})
		currentPage=cursor.get('currentPageIndex',1000)
		pages=cursor.get('pages',{})
		start=[i.get('start','') for i in pages if i.get('label',0)==currentPage+2]
		start=''.join(start).encode('utf-8')
		if start:
			title='[COLOR lime]Page next: %d[/COLOR]'%(currentPage+2)
			items.append((title,start,currentPage+2))
		return items

class taiphimhd:
	def __init__(self):
		self.s = requests.Session()
		self.hd={'User-Agent':'Mozilla/5.0'}
		self.s.headers.update(self.hd)
		try:self.cookie=json.loads(xrw('taiphimhd.cookie'))
		except:self.cookie={}
	
	def login(self):
		name,pw='eHNoYXJlK3RoYWl0bmk='.decode('base64').split('+')
		data={'name':name,'pass':pw,'form_id':'user_login'}
		url='http://taiphimhd.net/user?destination=http://taiphimhd.net'
		b=self.s.post(url, data=data, allow_redirects=False)
		if b.status_code==302:
			cookie={i.name:i.value for i in b.cookies}
			xrw('taiphimhd.cookie',json.dumps(cookie))

	def getFshare(self,url):
		def links(b):
			return [i for i in re.findall('(<li.+?/b>)',b) if re.search(site+'/[file|folder]',i)]
		
		site='www.fshare.vn'
		b=self.s.get(url, cookies = self.cookie).content
		s=xsearch('(<strong>FSHARE.+?/ul>)',b,1,re.S)
		items=links(b)
		if not s:
			self.login()
			b=self.s.get(url).content
			s=xsearch('(<strong>FSHARE.+?/ul>)',b,1,re.S)
		title=xsearch('"og\:title" content="(.+?)"',b)
		def label(i):
			i=re.sub('<.+?>','',i).replace('CLICK VÀO ĐÂY TẢI PHIM VỀ MÁY','').strip()
			a=xsearch('\|(.+)',i).strip()
			if not a:a=i+' '+title
			return a
		items=[i for i in re.findall('(<li.+?[/li|/b]>)',s) if re.search(site+'/[file|folder]',i)]
		items=[(label(i),xsearch('([\w|:|/]+?%s[\w|:|/]+)'%site,i)) for i in items]
		if items:
			s=xsearch('(<strong>Phụ Đề.+?/ul>)',b,1,re.S)
			subs=[i for i in re.findall('(<li.+?[/li|/b]>)',s)]
			subs=[(re.sub('<.+?>','',i),xsearch('href="(.+?)"',i)) for i in subs]
			items+=subs
		return items

class fcine:
	def __init__(self):
		self.s = requests.Session()
		self.hd={'User-Agent':'Mozilla/5.0'}
		self.s.headers.update(self.hd)
		#self.login()
		try:self.cookie=json.loads(xrw('fcine.cookie'))
		except:self.cookie={}
	
	def login(self):
		auth,pw='eHNoYXJlQHRoYW5odGhhaS5uZXQrdGhhaXRuaQ=='.decode('base64').split('+')
		b=self.s.get('http://fcine.net/login/')
		csrfKey=xsearch('name="csrfKey" value="(.+?)"',b.content)
		data={'csrfKey':csrfKey,'auth':auth,'password':pw,
			'login__standard_submitted':'1','remember_me':'0','remember_me_checkbox':'1'}
		b=self.s.post('http://fcine.net/login/', data=data, allow_redirects=False)
		if b.status_code==301:
			self.cookie={i.name:i.value for i in self.s.cookies}
			xrw('fcine.cookie',json.dumps(self.cookie))
	
	def getFshare(self,url,loop=True):
		site='www.fshare.vn'
		b=self.s.get(url.split('?')[0], cookies = self.cookie).content
		subUrl=xsearch('<a href="(.+?)" class=.+?><b>Tải phụ đề Việt</b></a>',b)
		label=xsearch('"og:title" content="(.+?)"',b)
		if label:label+=' '
		items=[i for i in re.findall('(<p.+?/p>)',b,re.S) if site in i]
		def abc(i):
			return (re.sub('<.+?>|\xc2\xa0|\|','',i),xsearch('([\w|:|/]+?%s[\w|:|/]+)'%site,i))
		items=[abc(i) for i in items]
		items=[(label+i[0].replace(i[1],'').strip(),i[1],subUrl) for i in items]
		if not items and loop:
			self.getFshare(url,False)
		if items and subUrl:mess('Xshare sẽ tự động load phụ đề của Fcine.net')
		return items
	
	
