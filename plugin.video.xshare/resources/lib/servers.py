# -*- coding: utf-8 -*-

import urllib,urllib2,urlfetch, re, os, json
from utils import *

class servers_list:
	def __init__(self):
		self.servers=[('anime47.com', '37'), ('tvhay.org', '41'), ('hdviet.com', '22'), ('fptplay.net', '07'), ('hayhaytv.vn', '23'), ('bilutv.com', '36'), ('phimmoi.net', '24'), ('hdonline.vn', '30'), ('megabox.vn', '17'), ('phim3s.net', '32'), ('phim14.net', '39'), ('kenh88.com', '26'), ('phimdata.com', '27'), ('phimsot.com', '29'), ('phim47.com', '28'), ('phimbathu.com', '43'), ('kphim.tv', '33'), ('phimnhanh.com', '35'), ('dangcaphd.com', '18'), ('phim.media', '40'), ('hdsieunhanh.com', '44'), ('vuahd.tv', '21'), ('pubvn.tv', '19')]
		try:self.ordinal=[int(i) for i in xrw('free_servers.dat').split(',')]
		except:self.ordinal=[]
		l=len(self.servers);update=False
		for i in range(l):
			if i not in self.ordinal:self.ordinal.append(i);update=True
		for i in self.ordinal:
			if i >= l:self.ordinal.remove(i);update=True
		if update:xrw('free_servers.dat',','.join(str(i) for i in self.ordinal))
		
	def mylist(self):
		return [self.servers[i] for i in self.ordinal]

	def move(self,server,step):#sl:server location, ol: ordinal location, step:up=-1,down=+1
		sl=self.servers.index([i for i in self.servers if i[0]==server][0])
		ol=self.ordinal.index([i for i in self.ordinal if i==sl][0])
		temp=self.ordinal[ol+step];self.ordinal[ol+step]=sl;self.ordinal[ol]=temp
		xrw('free_servers.dat',','.join(str(i) for i in self.ordinal))

	def moveDown(self,server):
		sl=self.servers.index([i for i in self.servers if i[0]==server][0])
		ol=self.ordinal.index([i for i in self.ordinal if i==sl][0])
		temp=self.ordinal[ol+1];self.ordinal[ol+1]=sl;self.ordinal[ol]=temp
		xrw('free_servers.dat',','.join(str(i) for i in self.ordinal))


class fshare:#https://www.fshare.vn/home/Mục chia sẻ của thaitni/abc?pageIndex=1
    
	def __init__(self, username='', password='', id=''):
		self.url_id=id
		self.myFavourite_id=''
		self.token=''
		self.logged=None
		self.hd={'User-Agent':'Mozilla/5.0 Gecko/20100101 Firefox/44.0','x-requested-with':'XMLHttpRequest'}
		if username:
			self.login(username,password)
			if self.logged=='success':
				myfolder=self.get_myFolder()
				self.myFavourite_id=''.join(xsearch('(\w{10,})',s[1]) for s in myfolder if s[0]=='xshare_favourite')
				if not self.myFavourite_id:
					self.myFavourite_id=self.add_folder(folder_name='xshare_favourite',in_dir_id='0')

	def fetch(self,url,data=None):
		try:response=urlfetch.fetch(url,headers=self.hd,data=data)
		except:response= None
		return response
	
	def login(self,username,password):
		response = self.fetch('https://www.fshare.vn/login')
		if not response or response.status!=200:mess('Connect to fshare.vn fails','Fshare.vn')
		else:
			fs_csrf=xsearch('value="(.+?)" name="fs_csrf"',response.body)
			data={"LoginForm[email]":username,"LoginForm[password]":password,"fs_csrf":fs_csrf}
			self.hd['Cookie']=response.cookiestring
			response = self.fetch('https://www.fshare.vn/login',data)
			if response and response.status==302:
				self.hd['Cookie']=response.cookiestring;self.logged='success'
				mess(u'Login thành công','Fshare.vn')
			else:mess(u'Login không thành công!','Fshare.vn')
	
	def logout(self):
		if self.logged:
			response = self.fetch('https://www.fshare.vn/logout')
			if response and response.status==302:self.logged=None;mess(u'Logout thành công','Fshare.vn')
			else:mess(u'Logout không thành công!','Fshare.vn')
	
	def get_maxlink(self,url):
		response=self.fetch(url);result=pw=None
		if not response:print 'Not response'
		elif response.status==302:result=response.headers['location']
		elif response.status==200:
			if re.search('<title>.*Lỗi 404.*</title>|"index-404"',response.body):
				mess(u'Tập tin quý khách yêu cầu không tồn tại!','Fshare.vn');result='fail'
			elif 'sử dụng nhiều địa chỉ IP' in response.body:
				mess(u'Quý khách đang sử dụng nhiều địa chỉ IP để tải xuống!','Fshare.vn',10000)
				result='fail'
			elif re.search('<i class="fa fa-star">',response.body):mess('Your Fshare acc is FREE','Fshare.vn')
			
			if re.search('class="fa fa-lock"',response.body):
				pw=get_input(u'Hãy nhập: Mật khẩu tập tin')
				if pw:
					try:
						data={'fs_csrf':xsearch('value="(.+?)" name="fs_csrf"',response.body),
						'DownloadForm[pwd]':pw,'ajax':'download-form','DownloadForm[linkcode]':url.split('/')[4]}
						response=self.fetch('https://www.fshare.vn/download/get',data).json
					except:response={}

					if not response:mess(u'Get maxspeed link fail!','Fshare.vn');result='fail'
					elif response.get('url'):result=response.get('url')
					elif response.get('DownloadForm_pwd'):mess(u'Mật khẩu không chính xác!','Fshare.vn')
					else: print response
			elif re.search('action="/download/get"',response.body):
				href='https://www.fshare.vn'+xsearch('action="(/download/get)"',response.body)
				fs_csrf=xsearch('value="(.+?)" name="fs_csrf"',response.body)
				downloadForm=xsearch('id="DownloadForm_linkcode" type="hidden" value="(.+?)"',response.body)
				data={'fs_csrf':fs_csrf,'DownloadForm[pwd]':'','DownloadForm[linkcode]':downloadForm,
						'ajax':'download-form','undefined':'undefined'}
				response=self.fetch(href,data)
				try:result=response.json.get('url')
				except:pass
		return result
	
	def get_token(self,url='https://www.fshare.vn/home'):
		self.hd['x-pjax']='true'
		response=self.fetch(url)
		if not response or response.status!=200:mess(u'Get home page fail!','Fshare.vn');return ''
		self.token=xsearch('data-token="(.+?)"',response.body)
		return self.token
	
	def get_folder(self,url):
		if '/file/' in url:return {'pagename':'','items':[]}
		response=self.fetch(url)
		body=response.body if response and response.status==200 else ''
		pagename=xsearch('<title>(.+?)</title>',body).replace('Fshare - ','')
		items=list()
		for content in re.findall('<div class="pull-left file_name(.+?)<div class="clearfix"></div>',body,re.S):
			item=re.search('data-id="(.+?)".+?href="(.+?)".+?title="(.+?)"',content)
			if item:
				size=xsearch('<div class="pull-left file_size align-right">(.+?)</div>',content).strip()
				id=item.group(1);type='file' if 'file' in item.group(2) else 'folder';title=item.group(3)
				if type=='file':link='https://www.fshare.vn/file/%s'%id
				elif re.search('(\w{10,20} )',title):
					iD=xsearch('(\w{10,20} )',title)
					if 'FOLDER' in iD:link='https://www.fshare.vn/folder/%s'%iD.replace('FOLDER','')
					elif 'FILE' in iD:link='https://www.fshare.vn/file/%s'%iD.replace('FILE','')
					else:
						link='https://www.fshare.vn/folder/%s'%iD
						try:
							if self.fetch(link).status!=200:link='https://www.fshare.vn/file/%s'%iD
						except:pass
					title=' '.join(s for s in title[title.find(' '):].split())
				else:link='https://www.fshare.vn/folder/%s'%id;title=' '.join(s for s in title.split())
				date=xsearch('"pull-left file_date_modify align-right">(.+?)</div>',content).strip()
				items.append((title,link,id,size,date))
		return {'pagename':pagename,'items':items}
	
	def myFshare_add(self,url,name):
		if not self.url_id:mess(u'Hãy set "Thư mục chia sẻ của tôi trên Fshare!"','myFshare');return
		id=url.split('/')[4]
		if [s for s in self.get_folder('https://www.fshare.vn/folder/'+self.url_id)['items'] if id in s[0]]:
			mess(u'This item already in MyFshare!','Fshare.vn');return
		token=self.get_token();name=id+('FOLDER ' if 'folder' in url else 'FILE ')+name
		data='{"token":"%s","name":"%s","in_dir":"%s"}'%(token,name,self.url_id)
		response=self.fetch('https://www.fshare.vn/api/fileops/createFolder',data)
		if response and response.status==200:mess(u'Add a item to MyFshare success','Fshare.vn')
		else:mess(u'Add a item to MyFshare fail!','Fshare.vn')
	
	def myFshare_remove(self,url):
		id=[s[2] for s in self.get_folder('https://www.fshare.vn/folder/'+self.url_id)['items'] if url==s[1]]
		id=id[0] if id else '';data='{"token":"%s","items":["%s"]}'%(self.get_token(),id.strip())
		response=self.fetch('https://www.fshare.vn/api/fileops/delete',data)
		if response and response.status==200:result=True;mess(u'Remove a item from MyFshare success','Fshare.vn')
		else:result=False;mess(u'Remove a item from MyFshare fail!','Fshare.vn')
		return result
	
	def myFshare_rename(self,url,new_name):
		id=[s[2] for s in self.get_folder('https://www.fshare.vn/folder/'+self.url_id)['items'] if url==s[1]]
		id=id[0] if id else '';data='{"token":"%s","new_name":"%s","file":"%s"}'%(self.get_token(),new_name,id)
		response=self.fetch('https://www.fshare.vn/api/fileops/rename',data)
		if response and response.status==200:result=True;mess(u'Rename a item in MyFshare success','Fshare.vn')
		else:result=False;mess(u'Rename a item in MyFshare fail!','Fshare.vn')
		return result
	
	def myFshare_upload(self,name,size,content):
		response=self.fetch('https://www.fshare.vn/home');result=False
		if not response or response.status!=200:
			response=self.fetch('https://www.fshare.vn/home')
			if not response or response.status!=200:mess(u'Get home page fail!','Fshare.vn');return result
		token=xsearch('data-token="(.+?)"',response.body)
		path=xsearch('data-id="%s" path-origin = "" data-path="(.+?)"'%self.url_id,response.body)
		SESSID=xsearch('session_id=(.+?)\W',str(self.hd))
		data='{"SESSID":"%s","name":"%s","size":"%s","path":"%s","token":"%s","secured":1}'%(
			SESSID,name,size,path,token);print data
		response=self.fetch('https://www.fshare.vn/api/session/upload',data)
		if response and response.status==200:
			response=self.fetch(response.json['location'],content)
			if response and response.status==200:result=True;mess(u'Upload file to MyFshare success','Fshare.vn')
		if result is False:mess(u'Upload file to MyFshare fail!','Fshare.vn');print response.status
		return result
	
	def Favorite_add(self,url):
		data='{"token":"%s","link":"%s"}'%(self.get_token(),url)
		response=self.fetch('https://www.fshare.vn/api/fileops/AddFavorite',data)
		if response and response.status==200:
			result=True;mess(u'Add a item to MyFshare Favorite success','Fshare.vn')
		else:result=False;mess(u'Add a item to MyFshare Favorite fail!','Fshare.vn')
		return result
	
	def Favorite_remove(self,name):
		data='{"token":"%s","items":["%s"],"status":0}'%(self.get_token(),name)
		response=self.fetch('https://www.fshare.vn/api/fileops/ChangeFavorite',data)
		if response and response.status==200:
			result=True;mess(u'Remove a item from MyFshare Favorite success','Fshare.vn')
		else:result=False;mess(u'Remove a item from MyFshare Favorite fail!','Fshare.vn')
		return result
	
	def add_folder(self,folder_name,in_dir_id='0'):
		token=self.get_token()
		#{"token":"49e3b84c0e4f1353491fed40eb964f485d091574","name":"abc","in_dir":"8NDKF9NA7T9I"}
		data='{"token":"%s","name":"%s","in_dir":"%s"}'%(token,folder_name,in_dir_id)
		response=self.fetch('https://www.fshare.vn/api/fileops/createFolder',data)
		try:result=response.json;result_code=result.get('code')
		except:result_code=0
		if result_code==200:
			#mess(result.get('msg')+' - '+result.get('folder',{}).get('name'),'Fshare.vn')
			result=result.get('folder',{}).get('linkcode')
		else:mess(u'Add folder fail !','Fshare.vn');result=''
		return result #folder ID created, empty if fail
	
	def remove_folder(self,parent_folder,folder_id):
		data='{"token":"%s","items":["%s"]}'%(self.get_token(),folder_id)
		self.hd['Referer']='https://www.fshare.vn/home/xshare_favourite'
		response=self.fetch('https://www.fshare.vn/api/fileops/delete',data)
		try:result=response.json;result_code=result.get('code')
		except:result_code=0
		if result_code==200:result=result.get('msg')
		else:result=''
		return result
	
	def get_myFolder(self,folder_name=''):
		self.hd['x-pjax']='true'
		url='https://www.fshare.vn/home/'+folder_name+'?_pjax=%23pjax_content'
		response=self.fetch(url)
		if response and response.status==200:
			items=re.findall('dl="(.+?)".+?f-name= "(.+?)"',response.body)
			items=[(s[1],'https://www.fshare.vn'+s[0]) for s in items]
		else:items=[]
		return items #(folder name,public url)
	
	def upload_file(self,fn):#Chua xong
		size=os.path.getsize(fn);name=os.path.basename(fn);path='/'
		session_id=xsearch('session_id=(.+?)\W',str(self.hd))
		data='{"SESSID":"%s","name":"%s","path":"%s","secured":"1","size":"%d","token":"%s"}'%(session_id,name,path,size,self.get_token())
		response=self.fetch('https://www.fshare.vn/api/session/upload',data)
		
		if response and response.status==200:
			try:response=urlfetch.fetch(response.json['location'].replace('http:','https:'),headers=self.hd,data=data)
			except:response= None
			if response and response.status==200:
				result=True;mess(u'Upload file to MyFshare success','Fshare.vn')
		#print response.status

	def remove_file(self,id):
		data='{"token": "%s", "items":["%s"]}'%(self.get_token(),id)
		response=self.fetch('https://www.fshare.vn/api/fileops/delete',data)
		
	def myFavourites_add(self,s):
		result=[]
		if not self.myFavourite_id:mess('Your Fshare Favourite ID not found!')
		else:
			import time
			loop=True;prefix=int(time.time());count=0;s=urllib2.base64.urlsafe_b64encode(s)
			while loop:
				folder_name='%d.%d.'%(prefix,count)+s[:230]
				if len(s)>230:s=s[230:];count+=1
				else:loop=False
				i=self.add_folder(folder_name,self.myFavourite_id)
				if i:result.append(i)
				else:loop=False#Chua xu ly delete neu that bai
		return result # list of folders ID created
	
	def myFavourites_loads(self):
		#(folder name,public url)
		myFolder=self.get_myFolder('xshare_favourite')
		f=[i[0] for i in myFolder if re.search('\d{10,}',i[0])]
		s=sorted([i.split('.') for i in f], key=lambda m:(m[0],m[1]))
		k=[]
		for i in list(set([i[0] for i in s])):
			try:m=urllib2.base64.urlsafe_b64decode(''.join(j[2] for j in s if j[0]==i))
			except:m=''
			if m:k.append(m+','+'-'.join(xsearch('(\w{10,})',j[1]) for j in myFolder if i in j[0]))
		return k
		
	def myFavourites_remove(self,ids):
		result=True
		for i in ids.split('-'):
			if not self.remove_folder('xshare_favourite',i):result=False
		return result

class chiasenhac:
	def __init__(self,username,password):
		self.session = urlfetch.Session(headers={'User_Agent':'Mozilla/5.0 (Android 4.4; Mobile; rv:42.0) Gecko/41.0 Firefox/42.0','Cookie':'vq=i%3A1080%3B; mq=i%3A500%3B'})
		self.urlhome='http://chiasenhac.com/'
		self.login(username,password)
	
	def fetch(self, url, data=''):
		try:response = self.session.fetch(url, data=data)
		except:response = None
		return response
	
	def login(self,username,password):
		data={'username':username,'password':password,'login':'Dang Nhap'}
		response=self.fetch('http://chiasenhac.com/login.php', data=data)
		if not response or response.status!=302:mess(u'Login Không thành công!','chiasenhac.com')

	def logout(self):
		self.fetch('http://chiasenhac.com/login.php?logout=true')

	def favourite(self, url,action='add'):
		href='http://chiasenhac.com/mp3/favourite/'+os.path.basename(url).replace('.','_%s.'%action)
		self.fetch(href)
	
	def get_favourite(self):
		response = self.fetch('http://chiasenhac.com/mp3/favourite')
		if response and response.status==200:body=response.body
		else:body=''
		return body

class phim3s_net:
	def __init__(self, username, password):
		self.session = urlfetch.Session(headers={'User_Agent':'Mozilla/5.0 (Android 4.4; Mobile; rv:42.0) Gecko/41.0 Firefox/42.0','X-Requested-With':'XMLHttpRequest','Cookie':''})
		self.login(username,password)
	
	def fetch(self, url, data=''):
		try:response = self.session.fetch(url, data=data)
		except:response = None
		return response
	
	def login(self, username, password):
		data={'username':username,'password':password}
		response=self.fetch('http://phim3s.net/member/login/', data=data)
		try:response=response.json
		except:response={}
		mess(u'%s'%response.get('message',['Login to phim3s.net fail !',''])[0],'Login to Phim3s.net')
	
	def get_bookmark(self):
		response=self.fetch('http://phim3s.net/ajax/member/get_bookmarks/')
		try:response=response.json
		except:response={}
		print response
		self.fetch('http://phim3s.net/member/logout/')
		return response

	def action_bookmark(self, url,action):#add_bookmark/remove_bookmark
		id=xsearch('_(\d+?)/',url)
		if id:
			url='http://phim3s.net/ajax/member/%s/?film_id=%s'%(action,id)
			response=self.fetch(url)
			try:response=response.json
			except:response={}
			mess(u'%s'%response.get('message','%s thất bại !'%action),'Phim3s.net bookmark')
			self.fetch('http://phim3s.net/member/logout/')

class tvhay:
	def __init__(self, s):
		try:
			w, i, s, e=s.split(',')
			s=self.dec(w, i, s, e)
			b=xsearch("(\w{100,},\w+,\w+,\w+)",s.replace("'",''))
			w, i, s, e=b.split(',')
			s=self.dec(w, i, s, e)
			b=xsearch("(\w{100,},\w+,\w+,\w+)",s.replace("'",''))
			w, i, s, e=b.split(',')
			s=self.dec(w, i, s, e)
		except:s=''
		self.string=s
	
	def dec(self, w, i, s, e):
		a=b=c=0;d=[];f=[]
		while (True):
			if a<5:f.append(w[a])
			elif a<len(w):d.append(w[a])
			a+=1
			if b<5:f.append(i[b])
			elif b<len(i):d.append(i[b])
			b+=1
			if c<5:f.append(s[c])
			elif c<len(s):d.append(s[c])
			c+=1
			if len(w)+len(i)+len(s)+len(e)==len(d)+len(f)+len(e):break


		b=0;k=[];h=''.join(f);g=''.join(d)
		for a in range(0,len(d),2):
			m=1 if ord(h[b])%2 else -1
			k.append(chr(int(g[a:a+2],36)-m))
			b+=1
			if b>=len(f):b=0

		return ''.join(k)
	
	def dec_(self, w, i, s, e):
		for s in range(0,len(w),2):
			i+=chr(int(w[s:s+2],36))
		return i

class hdvn:#from resources.lib.servers import hdvn;hdvn=hdvn()
	def __init__(self):
		self.hd={'User-Agent':'Mozilla/5.0','Referer':'http://www.hdvietnam.com/diendan/','Cookie':xrw('hdvietnam.cookie')}
		self.token=''
	
	def login(self):
		cookie=urllib2.HTTPCookieProcessor()
		opener=urllib2.build_opener(cookie)
		urllib2.install_opener(opener)
		pw=urllib2.hashlib.md5(addon.getSetting('passwordh')).hexdigest()
		user=addon.getSetting('usernameh')
		data ={"vb_login_username":user,"vb_login_md5password":pw,"do":"login"}
		url='http://www.hdvietnam.com/diendan/login.php?do=login'
		self.hd={'User-Agent': 'Mozilla/5.0'};hdvncookie=''
		content=self.getpage(url,urllib.urlencode(data))
		if re.search('<strong>%s</strong>'%user,content):
			hdvncookie=';'.join('%s=%s'%(i.name,i.value) for i in cookie.cookiejar)
			self.hd['Cookie']=hdvncookie
			self.token=xsearch('href="login.php[^"]+logouthash=(.+?)"',content)
			xrw(os.path.join(xsharefolder,'hdvietnam.cookie'),hdvncookie);
		else:mess(u'Login không thành công!','hdvietnam.com')

	def data_refresh(self,data):
		return re.sub('securitytoken=[^&]+','securitytoken='+self.token,data)
	
	def getpage(self,url,data=None,loop=False):
		hd=self.hd
		content=re.sub('\n\s*|amp;','',re.sub('>\s*<','><',xread(url,hd,data)))
		#f=open(r'd:\xoa.html','w');f.write(content);f.close()
		i=re.sub('<[^<]+>','',xsearch('class="blockrow restore">(.+)</div>',content))
		if i:
			i=' '.join(i.replace('&nbsp;',' ').replace('!','').replace(',','').split())
			if 'security token was missing' in i:content=content.replace('do=logout','')
			elif 'Ðề tài không tồn' in i:mess(i.decode('utf-8'),'HDVietnam.com');return content
		if loop and ('do=logout' not in content):
			self.login()
			if data :data=self.data_refresh(data)
			return self.getpage(url,data)
		token=xsearch('href="login.php[^"]+logouthash=(.+?)"',content)
		if token:self.token=token
		return content
	
	def getThanks1(self,thanks_data):
		show_href='http://www.hdvietnam.com/diendan/showthread.php';s=[]
		thanks_href='http://www.hdvietnam.com/diendan/post_thanks.php'
		for data in [i.replace('amp;','') for i in thanks_data]:
			i=self.getpage(thanks_href,data,loop=True)
			data=self.data_refresh(data).replace('post_thanks_add','whatever')
			s.append(self.getpage(show_href,data))
		return '=*='.join(s)
		
	def getThanks(self,data):
		show_href='http://www.hdvietnam.com/diendan/showthread.php';s=[]
		thanks_href='http://www.hdvietnam.com/diendan/post_thanks.php'
		i=self.getpage(thanks_href,data,loop=True)
		data=self.data_refresh(data).replace('post_thanks_add','whatever')
		return self.getpage(show_href,data)

	def getlink(self,url,buian=''):
		srv=['fshare.vn','4share.vn','tenlua.vn','subscene.com','hdvietnam.com','phudeviet.org']
		def s1(s):return [j for j in srv if j in s.lower()]
		def s2(string,href,c):#get title
			if buian:
				c=' '.join(i for i in c.split('=*=') if href in i)#Lay session co href
				p=c.find(href);i=0;s=''
				pattern='<div style="text-align[^"]+"><b><font size="\d">([^<]+?)</font></b>'
				while len(s)<10 and (p-i)>0:
					i+=100;s=xsearch(pattern,c[p-i:p]).strip()
					if [j for j in ('nội dung ẩn','Trailer','Download') if j in s]:s=''
			else:
				s=' '.join(i for i in re.sub('<[^<]+>','',string).split())
				if not s or [j for j in ('nội dung ẩn','Trailer','Download','http') if j in s]:
					c=' '.join(i for i in c.split('=*=') if href in i)#Lay session co href
					p=c.find(href);i=0;s=''
					while len(s)<5 and (p-i)>0:
						i+=50;s=xsearch('>([^<]+)<',c[p-i:p]).strip()
						if [j for j in ('nội dung ẩn','Trailer','Download') if j in s]:s=''
			return s if s else href

		def s3(href,img,c):#get img
			c=' '.join(i for i in c.split('=*=') if href in i)#Lay session co href
			p=c.find(href);i=0;s=''
			while not s and (p-i)>0:
				i+=100;s=xsearch('src="([^"]+)"',c[p-i:p])
				if not 'attachment.php' in s:s=''
			if not s:s=img
			return s

		if '#post' in url:url=url.split('#post')[0]
		content=self.getpage(url,loop=True)
		
		label=' '.join(re.sub('\[[^\[]+\]','',xsearch('<title>(.+?)</title>',content)).split())
		img=xsearch('<img src="([^"]+?\.jpg)"',content)
		if not img:img=xsearch('<img src="([^"]{300,})"',content)
		chuyenmuc=xsearch('<div class="morethread">(.+?)class="postfoot"',content)
		s=[]
		for i in re.findall('(<div class="posthead">.+?class="report")',content):
			i=i.replace('\\t','').replace('\\r','').replace('\\n','').replace('amp;','').replace('&gt;','-')
			if 'id="hide_fieldset"' in i:
				thanks=xsearch('(do=post_thanks_add[^"]+?)"',i).replace('amp;','')
				if thanks:i=i.replace('id="hide_fieldset"','-*-'+self.getThanks(thanks)+'-*-')
			s.append(i)
		
		content='\n=*=\n'.join(' '.join(i.split()) for i in s);s=''
		temp=re.findall('<a href="([^"]+?)" target="_blank">(.+?)</a>',content)
		temp1=[i for i in temp if s1(i[0])];n=[i[0] for i in temp1]
		temp=[i for i in re.findall('>(http[^<]+?)<',content) if '...' not in i and s1(i)]
		temp1+=[(i,'') for i in temp if i not in n];n=[];temp=[]
		
		for i in temp1:
			if 'chuyenlink.php' not in i[0] and 'members' not in i[0] and i[0] not in n:
				temp.append(i);n.append(i[0])
			elif 'phudeviet.org' in i[0]:
				j=urllib.unquote(xsearch('(phudeviet.org.+)',i[0]))
				if j and 'http://'+j not in n:temp.append(('http://'+j,i[1]));n.append('http://'+j)
		
		items=[(s2(i[1],i[0],content),i[0],s3(i[0],img,content)) for i in temp]
		items=[i for i in items if 'point fshare' not in i[0].lower()]
		
		#CÁC CHỦ ĐỀ CÙNG CHUYÊN MỤC
		for title,href in re.findall('<a title="(.+?)" href="(.+?)">',chuyenmuc):
			items.append((title,href,"morethread"))
		return items#title,href,img

	def getlink2(self,url,buian=''):
		if '#post' in url:url=url.split('#post')[0]
		content=self.getpage(url,loop=True)
		
		label=' '.join(re.sub('\[[^\[]+\]','',xsearch('<title>(.+?)</title>',content)).split())
		img=xsearch('<img src="([^"]+?\.jpg)"',content)
		chuyenmuc=xsearch('<div class="morethread">(.+?)class="postfoot"',content)
		s=re.findall('(<div class="posthead">.+?class="report")',content)
		
		thanks=re.findall('(do=post_thanks_add[^"]+?)"','\n'.join(i for i in s if 'id="hide_fieldset"' in i))
		s.append(self.getThanks(thanks))
			
		s='=*='.join(s)
		s=s.replace('\\t','').replace('\\r','').replace('\\n','').replace('amp;','').replace('&gt;','-')
		content=' '.join(s.split())
		
		srv=['fshare.vn','4share.vn','tenlua.vn','subscene.com','hdvietnam.com']
		def s1(s):return [j for j in srv if j in s.lower()]
		temp=re.findall('<a href="([^"]+?)" target="_blank">(.+?)</a>',content)
		temp1=[i for i in temp if s1(i[0])];n=[i[0] for i in temp1]
		temp=[i for i in re.findall('>(http[^<]+?)<',content) if '...' not in i and s1(i)]
		temp1+=[(i,'') for i in temp if i not in n];n=[];temp=[]
		for i in temp1:
			if 'chuyenlink.php' not in i[0] and 'members' not in i[0] and i[0] not in n:
				temp.append(i);n.append(i[0])
		
		def s2(string,href,c):#get title
			if buian:
				c=' '.join(i for i in c.split('=*=') if href in i)#Lay session co href
				p=c.find(href);i=0;s=''
				pattern='<div style="text-align[^"]+"><b><font size="\d">([^<]+?)</font></b>'
				while (len(s)<10 or 'dung ẩn' in s) and (p-i)>0:
					i+=100;s=xsearch(pattern,c[p-i:p]).strip()
			else:
				s=' '.join(i for i in re.sub('<[^<]+>','',string).split())
				if not s or 'http' in s:
					c=' '.join(i for i in c.split('=*=') if href in i)#Lay session co href
					p=c.find(href);i=0;s=''
					while (len(s)<10 or 'dung ẩn' in s) and (p-i)>0 and i<500:
						i+=50;s=xsearch('>([^<]+)<',c[p-i:p]).strip()
			return s if s else href
		
		def s3(href,img,c):#get img
			c=' '.join(i for i in c.split('=*=') if href in i)#Lay session co href
			p=c.find(href);i=0;s=''
			while not s and (p-i)>0:
				i+=100;s=xsearch('src="([^"]+)"',c[p-i:p])
				if not 'attachment.php' in s:s=''
			if not s:s=img
			return s
		
		items=[(s2(i[1],i[0],content),i[0],s3(i[0],img,content)) for i in temp]
		items=[i for i in items if 'point fshare' not in i[0].lower()]
		
		#CÁC CHỦ ĐỀ CÙNG CHUYÊN MỤC
		for title,href in re.findall('<a title="(.+?)" href="(.+?)">',chuyenmuc):
			items.append((title,href,"morethread"))
		return items#title,href,img

	def getlink1(self,url,buian=''):
		if '#post' in url:url=url.split('#post')[0]
		url='%s%s&styleid=9'%(url,'&mode=threaded' if '?' in url else '?mode=threaded')
		content=self.getpage(url,loop=True)
		if not content:
			mess('Xshare retry get room ...')
			url=url.replace('mode=threaded','mode=linear')
			content=self.getpage(url,loop=True)
		
		label=' '.join(re.sub('\[[^\[]+\]','',xsearch('<title>(.+?)</title>',content)).split())
		img=xsearch('<img src="([^"]+?\.jpg)"',content)
		chuyenmuc=xsearch('<div class="morethread">(.+?)class="postfoot"',content)
		s=re.findall('(pd\[.+)',content)
		if not s:s=re.findall('(<div class="posthead">.+?<div class="postfoot">)',content,re.DOTALL)
		
		thanks=re.findall('(do=post_thanks_add[^"]+?)"','\n'.join(i for i in s if 'id="hide_fieldset"' in i))
		show_href='http://www.hdvietnam.com/diendan/showthread.php'
		thanks_href='http://www.hdvietnam.com/diendan/post_thanks.php'
		for data in [i.replace('amp;','') for i in thanks]:
			i=self.getpage(thanks_href,data,loop=True)
			#token=xsearch('href="login.php[^"]+logouthash=(.+?)"',i)
			#data=re.sub('securitytoken=[^&]+','securitytoken='+token,data.replace('post_thanks_add','whatever'))
			data=self.data_refresh(data).replace('post_thanks_add','whatever')
			s.append(self.getpage(show_href,data))
			#temp=self.getpage(post_thanks,data.replace('post_thanks_add','post_thanks_remove_user'))
			
		s='=*='.join(s)
		s=s.replace('\\t','').replace('\\r','').replace('\\n','').replace('amp;','').replace('&gt;','-')
		content=' '.join(s.split())
		f=open(r'd:\xoa.html','w');f.write(content);f.close()
		srv=['fshare.vn','4share.vn','tenlua.vn','subscene.com','hdvietnam.com']
		def s1(s):return [j for j in srv if j in s.lower()]
		temp=re.findall('<a href="([^"]+?)" target="_blank">(.+?)</a>',content)
		temp1=[i for i in temp if s1(i[0])];n=[i[0] for i in temp1]
		temp=[i for i in re.findall('>(http[^<]+?)<',content) if '...' not in i and s1(i)]
		temp1+=[(i,'') for i in temp if i not in n];n=[];temp=[]
		for i in temp1:
			if 'chuyenlink.php' not in i[0] and 'members' not in i[0] and i[0] not in n:
				temp.append(i);n.append(i[0])
		
		def s2(string,href,c):#get title
			if buian:
				c=' '.join(i for i in c.split('=*=') if href in i)#Lay session co href
				p=c.find(href);i=0;s=''
				pattern='<div style="text-align[^"]+"><b><font size="\d">([^<]+?)</font></b>'
				while (len(s)<10 or 'dung ẩn' in s) and (p-i)>0:
					i+=100;s=xsearch(pattern,c[p-i:p]).strip()
			else:
				s=' '.join(i for i in re.sub('<[^<]+>','',string).split())
				if not s or 'http' in s:
					c=' '.join(i for i in c.split('=*=') if href in i)#Lay session co href
					p=c.find(href);i=0;s=''
					while (len(s)<10 or 'dung ẩn' in s) and (p-i)>0 and i<500:
						i+=50;s=xsearch('>([^<]+)<',c[p-i:p]).strip()
			return s if s else href
		
		def s3(href,img,c):#get img
			c=' '.join(i for i in c.split('=*=') if href in i)#Lay session co href
			p=c.find(href);i=0;s=''
			while not s and (p-i)>0:
				i+=100;s=xsearch('src="([^"]+)"',c[p-i:p])
				if not 'attachment.php' in s:s=''
			if not s:s=img
			return s
		
		items=[(s2(i[1],i[0],content),i[0],s3(i[0],img,content)) for i in temp]
		items=[i for i in items if 'point fshare' not in i[0].lower()]
		
		#CÁC CHỦ ĐỀ CÙNG CHUYÊN MỤC
		for title,href in re.findall('<a title="(.+?)" href="(.+?)">',chuyenmuc):
			items.append((title,href,"morethread"))
		return items#title,href,img

	def addRoom(self,url):
		roomid=xsearch('(\d{6,10})',url)
		url='http://www.hdvietnam.com/diendan/subscription.php?do=addsubscription&t='+roomid
		content=self.getpage(url);
		token=xsearch('name="securitytoken" value="(.+?)"',content)
		link=urllib.quote_plus(xsearch('name="url" value="(.+?)"',content))
		data='emailupdate=0&folderid=0&s=&securitytoken=%s&do=doaddsubscription&threadid=%s&url=%s'
		content=self.getpage('http://www.hdvietnam.com/diendan/subscription.php',data%(token,roomid,link))
		mess(xsearch('<p class="blockrow restore">(.+?)</p>',content).decode('utf-8'),'HDVietnam.com')
	
	def removeRoom(self,url):
		content=self.getpage(url);token=xsearch('name="securitytoken" value="(.+?)"',content)
		href=xsearch('href="(subscription.php\?do=removesubscription[^"]+?)"',content).replace('amp;','')
		if href:
			content=self.getpage('http://www.hdvietnam.com/diendan/'+href)
			mess(xsearch('<p class="blockrow restore">(.+?)</p>',content).decode('utf-8'),'HDVietnam.com')
			result=True
		else:result=False;mess('Link subscription remove not found!','HDVietnam.com')
		return result

class taiphim:
	def __init__(self,c):
		self.hd={'User-Agent':'Mozilla/5.0','Cookie':xrw('taiphimhd.cookie')}
		self.token=''
		self.c=c
	
	def login(self):
		data=urllib2.base64.b64decode('bG9naW49eHNoYXJlJTQwdGhhbmh0aGFpLm5ldCZyZWdpc3Rlcj0wJnBhc3N3b3JkPXhzaGFyZSZjb29raWVfY2hlY2s9MSZyZWRpcmVjdD0lMkYmX3hmVG9rZW49');url='http://taiphimhd.com/login/login';hd={'User-Agent':'Mozilla/5.0'}
		try:
			a=self.fetch(url,hd);hd['Cookie']=a.cookiestring;a=self.fetch(url,hd,data);self.hd['Cookie']=a.cookiestring
			if a.status==303:
				xrw(os.path.join(xsharefolder,'taiphimhd.cookie'),self.hd['Cookie'])
				print '---------------------------- Login OK'
		except:pass
	
	def fetch(self,url,headers=None,data=None):
		if not headers:headers=self.hd
		try:response=urlfetch.fetch(url,headers=headers,data=data)
		except:response=None
		
		return response
	
	def getThanks(self,s):
		id=xsearch('href="posts/(\d+)/like"',s)
		if id:
			mess('Thanked to %s'%xsearch('data-author="(.+?)"',s).strip())
			url='http://taiphimhd.com/posts/%s/like'%id
			b=self.fetch(url,data={'_xfToken':self.token,'_xfNoRedirect':'1','_xfResponseType':'json'})
			url='http://taiphimhd.com/posts/%s/like-hide-check'%id
			b=self.fetch(url,data={'_xfToken':self.token,'_xfNoRedirect':'1','_xfResponseType':'json'})
			try:s=b.body.replace('amp;','').replace('\\','')
			except:pass
		
		return s
	
	def getLink(self,b):
		def srvs(i):
			srv=['fshare.vn','4share.vn','tenlua.vn','subscene.com','taiphimhd.com','phudeviet.org']
			return [j for j in srv if j in i]
		def i_l(i,l): return i[0] not in [j[0] for j in l]
		l=[];loop=False
		for s in re.findall('(<li id="post.+?/li>)',b,re.DOTALL):
			if 'click nút Like để lấy link' in s:s=self.getThanks(s);loop=True
			if loop:l=[];continue
			else:
				img=xsearch('img src="(.+?)"',s);p='<a href="(.+?)" target="_blank"[^<]+?>(.+>)'
				l+=[(i[0],re.sub('<[^<]+>','',i[1]),img) for i in re.findall(p,s) if srvs(i[0])]
				p='href="([^"]+?)"[^<]+?><[^<]+?>([^<]+?)<'
				l+=[(i[0],i[1],'') for i in re.findall(p,s) if srvs(i[0]) and i[0] not in [j[0] for j in l]]
				l+=[(i,i,img) for i in re.findall('(http[^<]+?)<',s) if srvs(i) and i not in [j[0] for j in l]]
		
		n=[]
		for href,title,img in l:
			if re.search('"|,|\'|\?',href) or href in [j[0] for j in n]:continue
			s=b[b.find(href)-1000:b.find(href)]
			if xsearch('"(http[^"]+\.jpg)"',s):img=xsearch('"(http[^"]+\.jpg)"',s)
			if title in href or href in title:
				i='';fs=30
				while not i and fs>10:
					i=xsearch('style="font-size:.{,3}%d.{,5}">([^<]+)<'%fs,s);fs-=1
				if i:title=' '.join(i.split())
			if href and title.strip():n.append((href,' '.join(title.split()),img))
		
		return n#href,title,img
	
	def search(self,s):
		url='https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=20&hl=en&prettyPrint=false&source=gcsc&gss=.com&cx=006272920913781838063:kzk6oinlbd0&googlehost=www.google.com&callback=google.search.Search.apiary17955&q='+s
		a=self.fetch(url,headers={'User-Agent':'Mozilla/5.0'})
		import json
		try:j=json.loads(xsearch('\((\{.+?\})\)',a.body)).get('results')
		except:j=[]
		if not j:return []
		l=[]
		for i in j:
			title=i.get('title')
			href=re.sub('page-\d+','',i.get('url'))
			try:img=i['richSnippet']['cseImage']['src']
			except:img=''
			if href not in [m[1] for m in l]:l.append((title,href,img))
		
		return l
		
	def search1(self,s):
		url='http://taiphimhd.com/search/search'
		b=self.getContent(url)
		data={'keywords':urllib.quote_plus(s),'users':'','date':'','_xfToken':self.token}
		b=self.fetch(url,data=data)
		try:b=self.fetch(b.headers.get('location')).body
		except:b=''
		
		return b
	
	def xfetch(self,url,headers=None,data=None):
		b=xread(url,self.hd)
		try:response=urlfetch.fetch(url,headers=headers,data=data)
		except:response=None
		
		return response
	
	def getContent(self,url):
		#if '/posts/' in url:
		b=xread(url,self.hd)
		if not xsearch('href="(logout[^"]+?)"',b):self.login();b=xread(url,self.hd)
		else:print '---------------------------- cookie OK'
		#else:
		#	b=self.fetch(url)
		#	if not b or not xsearch('href="(logout[^"]+?)"',b.body):self.login();b=self.fetch(url)
		#	else:print '---------------------------- cookie OK'
		#	if b:b=b.body
		#	else:b=''

		self.token=urllib.unquote(xsearch('name="_xfToken" value="(.+?)"',b))
		
		return b
	
	def getPage(self,url):
		b=self.getContent(url);items=[('name','','')]
		i=self.getLink(b);urlhome='http://taiphimhd.com/'
		if not i:i=self.getLink(self.getContent(url))
		for href,title,img in i:
			if 'http' not in img:img=urlhome+img
			if 'http://taiphimhd.com/' in href:title=namecolor(title,self.c)
			items.append((title,href,img))
		
		items.append(('--Có thể bạn muốn xem--','',''))
		for s in [i for i in re.findall('(<li id="thread.+?/li>)',b,re.DOTALL) if 'data-author' in i]:
			href=xsearch('href="(threads/.+?)"',s)
			if 'http' not in href:href=urlhome+href
			img=xsearch('src="(.+?)"',s)
			if 'http' not in img:img=urlhome+img
			title=xsearch('data-previewUrl=".+?">(.+?)</a>',s)
			items.append((namecolor(title,self.c),href,img))
		
		return items

	def getLists(self,url):
		if '/find-new/' in url:b=xread(url);items=[]
		else:b=self.getContent(url);items=[]
		for href,title in re.findall('<h3 class="nodeTitle"><a href="([^"]+?)"[^<]+?">(.+?)</a></h3>',b):
			title=namecolor('[B]Mục %s[/B]'%title.replace('amp;',''),self.c)
			items.append((title,'http://taiphimhd.com/'+href,'ico'))

		for s in re.findall('(<li id="thread.+?/li>)',b,re.DOTALL):
			href=xsearch('href="(.+?)"',s)
			if 'http' not in href:href='http://taiphimhd.com/'+href
			img=xsearch('src="(.+?)"',s)
			if 'http' not in img:img='http://taiphimhd.com/'+img
			author=xsearch('data-author="(.+?)"',s)
			title='[COLOR gold]%s[/COLOR] '%author+xsearch('data-previewUrl=".+?">(.+?)</a>',s)
			items.append((namecolor(title,self.c),href,img))
		
		s=xsearch('(PageNavNext.+?/nav>)',b,1,re.DOTALL)
		if s:
			href='http://taiphimhd.com/'+xsearch('href="(.+?)" class="text">Tiếp',s)
			pages=xsearch('href="[^"]+?" class="">(\d+)</a>',s)
			items.append((pages,href,'next'))
		
		return items
		
	def getRSS(self,url):
		b=self.getContent(url);items=[]
		for s in [i for i in b.split('<item>') if '<author>' in i]:
			author=xsearch('<author>(.+?)</author>',s)
			title=xsearch('<title>(.+?)</title>',s)
			href=xsearch('href="(http://taiphimhd.com/threads/[^"]+?)"',s)
			img=xsearch('src="([^"]+?jpg)"',s)
			items.append((title,href,img))
			
		return items

class sieunhanh:
	def __init__(self):
		self.hd={'User-Agent':'Mozilla/5.0'}
		self.urlhome='http://hdsieunhanh.com/'
		self.color='orangered'

	def eps(self,url):
		content=xread(url);items=[]
		s=xsearch('(<ul class="list_episode".+?/ul>)',content,1,re.DOTALL)
		return re.findall('href="(.+?)">(.+?)</a>',s)

	def item(self,s):
		title=xsearch('alt="(.+?)"',s)
		href=xsearch('href="(.+?)"',s)
		if 'html' not in href:href=self.urlhome+href
		img=xsearch('src="(.+?)"',s)
		rate=xsearch('"rate">([^<]+?)</span>',s)
		if rate:title='%s [COLOR green]%s[/COLOR]'%(title,rate)
		eps=' '.join(re.sub('<[^<]+?>','',xsearch('(<span class="label-range">.+?<strong>\d+?</strong>)',s)).split())
		if eps:title='%s [COLOR gold](%s)[/COLOR]'%(namecolor(title,self.color),eps);dir=True
		else:dir=False
		return (title,href,img,dir)
		
	def page(self,url):
		content=xread(url);items=[]
		for s in [i for i in content.split('<div class="block-base movie">') if 'data-id' in i]:items.append(self.item(s))
			
		pn=xsearch('<a href="([^"]+?)">Sau</a>',content)
		if pn:
			pn=self.urlhome+pn.replace('amp;','')
			pages=xsearch('=(\d+)">Cuối</a></li></ul>',content)
			title='[COLOR lime]Page next: page/%s[/COLOR]'%pages
			items.append((title,pn,'image',True))
		return items#title,href,img

	def search(self,s):
		url='http://hdsieunhanh.com/tim-kiem.html?term='+urllib.quote_plus(s)
		self.hd['X-Requested-With']='XMLHttpRequest';items=[];b=xread(url,self.hd)
		if not b:mess('Get search fail','hdsieunhanh.com');return items
		try:j=json.loads(b)
		except:j={}
		for s in ('director','phim','actor','show'):
			for i in j.get(s,[]):
				title=i.get('name').encode('utf-8')+' - '+i.get('extension').encode('utf-8')
				href=i.get('link')
				img=i.get('image')
				eps=(i.get('last_episode')+'/'+i.get('total_episode')) if i.get('total_episode')>'1' else ''
				eps=eps.encode('utf-8')
				if not eps:dir=False
				else:title='%s [COLOR blue]%s[/COLOR]'%(namecolor(title,self.color),eps);dir=True
				items.append((title,href,img,dir))
		if not items:mess(u'Không tìm thấy dữ liệu vui lòng thử lại!','hdsieunhanh.com')
		return items
	
	def maxLink(self,url):
		content=xread(url);link=''
		s=re.findall("file[^']+?'([^']+?)'[^']+?label:'([^']+?)'",content)
		if get_setting('resolut')=='Max':
			items=sorted(list(set([(i[0],rsl(i[1])) for i in s])), key=lambda k: int(k[1]),reverse=True)
		else:items=sorted(list(set([(i[0],rsl(i[1])) for i in s])), key=lambda k: int(k[1]))
		return items

def gibberishAES(string, key=''):
	import ctypes
	def aa(l,s=4):
		a=[]
		for i in range(0,len(l),s):a.append((l[i:i+s]))
		return a

	def j2p(v):return ctypes.c_int(v).value
	def rshift(val, n): return (val % 0x100000000) >> n

	e = 14
	r = 8
	n = False
		
	def f(e):
		try:result=urllib.quote(e)
		except:result=str(e)
		return result
		
	def c(e):
		try:result=urllib.quote(e, safe='~()*!.\'')
		except:result=str(e)
		return result

	def t(e):
		f = [0]*len(e)
		if 16 >len(e):
			r = 16 - len(e)
			f = [r, r, r, r, r, r, r, r, r, r, r, r, r, r, r, r]
		for n in range(len(e)):f[n] = e[n]
		return f

	def o(e):
		n = ""
		for r in len(e):n += ("0" if 16 > e[r] else "") + format(e[r], 'x')
		return n

	def u(e, r):
		c = []
		if not r:e=f(e)
		for n in range(len(e)):c.append(ord(e[n]))
		return c

	def i(n):
		if n==128:e = 10; r = 4
		elif n==192:e = 12;r = 6
		elif n==256:e = 14;r = 8

	def b(e):
		n = []
		for r in range(e):n.append(256)
		return n

	def h(n, f):
		d=[];t= 3 if e >= 12 else 2; i = n + f; d.append(L(i));u=[c for c in d[0]]
		for c in range(1,t):d.append(L(d[c - 1] + i));u+=d[c]
		return {'key': u[0 : 4 * r],'iv': u[4 * r : 4 * r + 16]}

	def a1(e, r=False):
		c = ""
		if (r):
			n = e[15]
			#if n > 16:print "Decryption error: Maybe bad key"
			if 16 != n:
				for f in range(16 - n):c += chr(e[f])
		else:
			for f in range(16):c += chr(e[f])
		return c

	def a(e, r=False):
		if not r:c=''.join(chr(e[f])for f in range(16))
		elif 16!=e[15]:c=''.join(chr(e[f]) for f in range(16-e[15]))
		else:c=''
		return c

	def v(e, r, n, f=''):
		r = S(r); o = len(e) / 16; u = [0]*o
		d=[e[16 * t: 16 * (t + 1)] for t in range(o)]
		for t in range(len(d) - 1,-1,-1):
			u[t] = p(d[t], r)
			u[t] = x(u[t], n) if 0 == t else x(u[t], d[t - 1])
		
		i=''.join(a(u[t]) for t in range(o-1))
		i += a(u[o-1], True)
		return i if f else c(i)

	def s(r, f):
		n = False
		t = M(r, f, 0)
		for c in (1, e + 1 ,1):
			t = g(t)
			t = y(t)
			if e > c:t = k(t)
			t = M(t, f, c)
		return t

	def p(r, f):
		n = True
		t = M(r, f, e)
		for c in range(e - 1,-1,-1):
			t = y(t,n)
			t = g(t,n)
			t = M(t, f, c)
			if c > 0 : t = k(t,n)
		return t

	def g(e,n=True):#OK
		f = D if n else B; c = [0]*16
		for r in range(16):c[r] = f[e[r]]
		return c

	def y(e,n=True):
		f = []
		if n: c = [0, 13, 10, 7, 4, 1, 14, 11, 8, 5, 2, 15, 12, 9, 6, 3] 
		else:c =[0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]
		for r in range(16):f.append(e[c[r]])
		return f

	def k(e,n=True):
		f = [0]*16
		if (n):
			for r in range(4):
				f[4 * r] = F[e[4 * r]] ^ R[e[1 + 4 * r]] ^ j[e[2 + 4 * r]] ^ z[e[3 + 4 * r]]
				f[1 + 4 * r] = z[e[4 * r]] ^ F[e[1 + 4 * r]] ^ R[e[2 + 4 * r]] ^ j[e[3 + 4 * r]]
				f[2 + 4 * r] = j[e[4 * r]] ^ z[e[1 + 4 * r]] ^ F[e[2 + 4 * r]] ^ R[e[3 + 4 * r]]
				f[3 + 4 * r] = R[e[4 * r]] ^ j[e[1 + 4 * r]] ^ z[e[2 + 4 * r]] ^ F[e[3 + 4 * r]]
		else:
			for r in range(4):
				f[4 * r] = E[e[4 * r]] ^ U[e[1 + 4 * r]] ^ e[2 + 4 * r] ^ e[3 + 4 * r]
				f[1 + 4 * r] = e[4 * r] ^ E[e[1 + 4 * r]] ^ U[e[2 + 4 * r]] ^ e[3 + 4 * r]
				f[2 + 4 * r] = e[4 * r] ^ e[1 + 4 * r] ^ E[e[2 + 4 * r]] ^ U[e[3 + 4 * r]]
				f[3 + 4 * r] = U[e[4 * r]] ^ e[1 + 4 * r] ^ e[2 + 4 * r] ^ E[e[3 + 4 * r]]
		return f	

	def M(e, r, n):#OK
		c = [0]*16
		for f in range(16):c[f] = e[f] ^ r[n][f]
		return c

	def x(e, r):
		f = [0]*16
		for n in  range(16):f[n] = e[n] ^ r[n]
		return f

	def S(n):#r=8;e=14
		o=[[n[4 * f + i] for i in range(4)] for f in range(r)]
		
		for f in range(r,4 * (e + 1)):
			d=[t for t in o[f-1]]
			if 0 == f % r:d = m(w(d)); d[0] ^= K[f / r - 1]
			elif r > 6 and 4 == f % r : d = m(d)
			o.append([o[f - r][t] ^ d[t] for t in range(4)])
		
		u = []
		for f in range(e + 1):
			u.append([])
			for a in range(4):u[f]+=o[4 * f + a]
		return u

	def m(e):
		return [B[e[r]] for r in range(4)]

	def w(e):
		e.insert(4,e[0])
		e.remove(e[4])
		return e

	def A(e, r):return [int(e[n:n+r], 16) for n in range(0,len(e),r)]

	def C(e):
		n=[0]*len(e)
		for r in range(len(e)):n[e[r]] = r
		return n

	def I(e, r):
		f=0
		for n in range(8):
			f = f ^ e if 1 == (1 & r) else f
			e = j2p(283 ^ e << 1) if e > 127 else j2p(e << 1)
			r >>= 1
		return f

	def O(e):
		n = [0]*256
		for r in range(256):n[r] = I(e, r)
		return n

	B = A("637c777bf26b6fc53001672bfed7ab76ca82c97dfa5947f0add4a2af9ca472c0b7fd9326363ff7cc34a5e5f171d8311504c723c31896059a071280e2eb27b27509832c1a1b6e5aa0523bd6b329e32f8453d100ed20fcb15b6acbbe394a4c58cfd0efaafb434d338545f9027f503c9fa851a3408f929d38f5bcb6da2110fff3d2cd0c13ec5f974417c4a77e3d645d197360814fdc222a908846eeb814de5e0bdbe0323a0a4906245cc2d3ac629195e479e7c8376d8dd54ea96c56f4ea657aae08ba78252e1ca6b4c6e8dd741f4bbd8b8a703eb5664803f60e613557b986c11d9ee1f8981169d98e949b1e87e9ce5528df8ca1890dbfe6426841992d0fb054bb16", 2)
	D = C(B)
	K = A("01020408102040801b366cd8ab4d9a2f5ebc63c697356ad4b37dfaefc591", 2)
	E = O(2)
	U = O(3)
	z = O(9)
	R = O(11)
	j = O(13)
	F = O(14)

	def G(e, r, n):
		c = b(8); t = h(u(r, n), c); a = t.key; o = t.iv; d = [83, 97, 108, 116, 101, 100, 95, 95]+c
		e = u(e, n)
		f = l(e, a, o)
		f = d+f
		return T.encode(f)

	def H(e, r, n=''):
		f = decode(e)
		c = f[8 : 16]
		t = h(u(r, n), c)
		a = t['key']
		o = t['iv']
		f = f[16 : len(f)]
		return v(f, a, o, n)

	def decode(r):#OK
		def indexOfchar(n):
			try:a=e.index(r[n])
			except:a=-1
			return a
		
		e="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
		r=r.replace('\n','');f=[];c=[0]*4
		for n in range(0,len(r),4):
			for i in range(len(c)):c[i]=indexOfchar(n+i)
			f.append(j2p(c[0]<<2|c[1]>>4))
			f.append(j2p((15&c[1])<<4|c[2]>>2))
			f.append(j2p((3&c[2])<<6|c[3]))
		return f[0:len(f)-len(f)%16]

	def L(e):
		def r(e, r):return j2p(e << r) | j2p(rshift(e, 32-r))

		def n(e, r):
			c = 2147483648 & e
			t = 2147483648 & r
			n = 1073741824 & e
			f = 1073741824 & r
			a = (1073741823 & e) + (1073741823 & r)
			i = 2147483648^a^c^t
			j = 3221225472^a^c^t
			k = 1073741824^a^c^t
			return j2p(i if n & f else ((j if 1073741824 & a else k) if n | f else a^c^t))		

		def f(e, r, n):return j2p(e & r) | j2p(~e & n)

		def c(e, r, n):return j2p(e & n) | j2p(r & ~n)

		def t(e, r, n):return e ^ r ^ n

		def a(e, r, n):return r ^ (e | ~n)

		def o(e, c, t, a, o, d, u):
			e = n(e, n(n(f(c, t, a), o), u))
			return n(r(e, d), c)

		def d(e, f, t, a, o, d, u):
			e = n(e, n(n(c(f, t, a), o), u))
			return n(r(e, d), f)

		def u(e, f, c, a, o, d, u):
				e = n(e, n(n(t(f, c, a), o), u))
				return n(r(e, d), f)

		def i(e, f, c, t, o, d, u):
			e = n(e, n(n(a(f, c, t), o), u))
			return n(r(e, d), f)

		def b(e):
			n=len(e); f = n + 8; c = (f - f % 64) / 64; t = 16 * (c + 1); a = [0]*t; o = 0
			for d in range(n):r = (d - d % 4) / 4; o = 8 * (d % 4);	a[r] = a[r] | j2p(e[d] << o)
			d+=1
			r = (d - d % 4) / 4
			o = 8 * (d % 4)
			a[r] = a[r] | j2p(128 << o)
			a[t - 2] = j2p(n << 3)
			a[t - 1] = j2p(rshift(n,29))
			return a

		def h(e):
			f = []
			for n in range(4):
				r = j2p(255 & rshift(e, 8 * n))
				f.append(r)
			return f

		m = A("67452301efcdab8998badcfe10325476d76aa478e8c7b756242070dbc1bdceeef57c0faf4787c62aa8304613fd469501698098d88b44f7afffff5bb1895cd7be6b901122fd987193a679438e49b40821f61e2562c040b340265e5a51e9b6c7aad62f105d02441453d8a1e681e7d3fbc821e1cde6c33707d6f4d50d87455a14eda9e3e905fcefa3f8676f02d98d2a4c8afffa39428771f6816d9d6122fde5380ca4beea444bdecfa9f6bb4b60bebfbc70289b7ec6eaa127fad4ef308504881d05d9d4d039e6db99e51fa27cf8c4ac5665f4292244432aff97ab9423a7fc93a039655b59c38f0ccc92ffeff47d85845dd16fa87e4ffe2ce6e0a30143144e0811a1f7537e82bd3af2352ad7d2bbeb86d391", 8)
		S = [];  S = b(e); y = m[0]; k = m[1]; M = m[2]; x = m[3]; l = 0
		for l in range(0,len(S),16):
			v = y
			s = k
			p = M
			g = x
			y = o(y, k, M, x, S[l + 0], 7, m[4])
			x = o(x, y, k, M, S[l + 1], 12, m[5])
			M = o(M, x, y, k, S[l + 2], 17, m[6])
			k = o(k, M, x, y, S[l + 3], 22, m[7])
			y = o(y, k, M, x, S[l + 4], 7, m[8])
			x = o(x, y, k, M, S[l + 5], 12, m[9])
			M = o(M, x, y, k, S[l + 6], 17, m[10])
			k = o(k, M, x, y, S[l + 7], 22, m[11])
			y = o(y, k, M, x, S[l + 8], 7, m[12])
			x = o(x, y, k, M, S[l + 9], 12, m[13])
			M = o(M, x, y, k, S[l + 10], 17, m[14])
			k = o(k, M, x, y, S[l + 11], 22, m[15])
			y = o(y, k, M, x, S[l + 12], 7, m[16])
			x = o(x, y, k, M, S[l + 13], 12, m[17])
			M = o(M, x, y, k, S[l + 14], 17, m[18])
			k = o(k, M, x, y, S[l + 15], 22, m[19])
			y = d(y, k, M, x, S[l + 1], 5, m[20])
			x = d(x, y, k, M, S[l + 6], 9, m[21])
			M = d(M, x, y, k, S[l + 11], 14, m[22])
			k = d(k, M, x, y, S[l + 0], 20, m[23])
			y = d(y, k, M, x, S[l + 5], 5, m[24])
			x = d(x, y, k, M, S[l + 10], 9, m[25])
			M = d(M, x, y, k, S[l + 15], 14, m[26])
			k = d(k, M, x, y, S[l + 4], 20, m[27])
			y = d(y, k, M, x, S[l + 9], 5, m[28])
			x = d(x, y, k, M, S[l + 14], 9, m[29])
			M = d(M, x, y, k, S[l + 3], 14, m[30])
			k = d(k, M, x, y, S[l + 8], 20, m[31])
			y = d(y, k, M, x, S[l + 13], 5, m[32])
			x = d(x, y, k, M, S[l + 2], 9, m[33])
			M = d(M, x, y, k, S[l + 7], 14, m[34])
			k = d(k, M, x, y, S[l + 12], 20, m[35])
			y = u(y, k, M, x, S[l + 5], 4, m[36])
			x = u(x, y, k, M, S[l + 8], 11, m[37])
			M = u(M, x, y, k, S[l + 11], 16, m[38])
			k = u(k, M, x, y, S[l + 14], 23, m[39])
			y = u(y, k, M, x, S[l + 1], 4, m[40])
			x = u(x, y, k, M, S[l + 4], 11, m[41])
			M = u(M, x, y, k, S[l + 7], 16, m[42])
			k = u(k, M, x, y, S[l + 10], 23, m[43])
			y = u(y, k, M, x, S[l + 13], 4, m[44])
			x = u(x, y, k, M, S[l + 0], 11, m[45])
			M = u(M, x, y, k, S[l + 3], 16, m[46])
			k = u(k, M, x, y, S[l + 6], 23, m[47])
			y = u(y, k, M, x, S[l + 9], 4, m[48])
			x = u(x, y, k, M, S[l + 12], 11, m[49])
			M = u(M, x, y, k, S[l + 15], 16, m[50])
			k = u(k, M, x, y, S[l + 2], 23, m[51])
			y = i(y, k, M, x, S[l + 0], 6, m[52])
			x = i(x, y, k, M, S[l + 7], 10, m[53])
			M = i(M, x, y, k, S[l + 14], 15, m[54])
			k = i(k, M, x, y, S[l + 5], 21, m[55])
			y = i(y, k, M, x, S[l + 12], 6, m[56])
			x = i(x, y, k, M, S[l + 3], 10, m[57])
			M = i(M, x, y, k, S[l + 10], 15, m[58])
			k = i(k, M, x, y, S[l + 1], 21, m[59])
			y = i(y, k, M, x, S[l + 8], 6, m[60])
			x = i(x, y, k, M, S[l + 15], 10, m[61])
			M = i(M, x, y, k, S[l + 6], 15, m[62])
			k = i(k, M, x, y, S[l + 13], 21, m[63])
			y = i(y, k, M, x, S[l + 4], 6, m[64])
			x = i(x, y, k, M, S[l + 11], 10, m[65])
			M = i(M, x, y, k, S[l + 2], 15, m[66])
			k = i(k, M, x, y, S[l + 9], 21, m[67])
			y = n(y, v)
			k = n(k, s)
			M = n(M, p)
			x = n(x, g)
		return h(y)+h(k)+h(M)+h(x)

		
	def recode(b):
		def getcode(s):
			w, i, s, e=s.split(',')
			a=b=c=0;d=[];f=[]
			while True:
				if a < 5:f.append(w[a])
				elif a < len(w):d.append(w[a])
				a+=1
				
				if  b < 5 :f.append(i[b])
				elif  b < len(i):d.append(i[b])
				b+=1
				
				if  c < 5:f.append(s[c])
				elif  c < len(s):d.append(s[c])
				c+=1
				
				if len(w) + len(i) + len(s) + len(e) == len(d) + len(f) + len(e):break

			k=''.join(s for s in d);m=''.join(s for s in f);b=0;o=[]
			for a in range(0,len(d),2):
				n = -1
				if ord(m[b]) % 2:n = 1
				o.append(chr(int(k[a:a+2], 36) - n))
				b+=1
				if b >= len(f):b = 0
			return ''.join(s for s in o)
		l=0
		while l<5 or 'decodeLink' not in b:
			try:b=getcode(xsearch("(\w{100,},\w+,\w+,\w+)",b.replace("'",'')));l+=1
			except:break
		return b
	
	return H(string, key) if key else recode(string)

