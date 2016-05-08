# -*- coding: utf-8 -*-

import urlfetch, re, os, utils

class fshare:
    
	def __init__(self, username='', password='', id=''):
		self.url_id=id
		self.token=''
		self.logged=None
		self.hd={'User-Agent':'Mozilla/5.0 Gecko/20100101 Firefox/44.0','x-requested-with':'XMLHttpRequest'}
		if username:self.login(username,password)
	
	def fetch(self,url,data=None):
		try:response=urlfetch.fetch(url,headers=self.hd,data=data)
		except:response= None
		return response
	
	def login(self,username,password):
		response = self.fetch('https://www.fshare.vn/login')
		if not response or response.status!=200:utils.mess('Connect to fshare.vn fails','Fshare.vn')
		else:
			fs_csrf=utils.xsearch('value="(.+?)" name="fs_csrf"',response.body)
			data={"LoginForm[email]":username,"LoginForm[password]":password,"fs_csrf":fs_csrf}
			self.hd['Cookie']=response.cookiestring
			response = self.fetch('https://www.fshare.vn/login',data)
			if response and response.status==302:
				self.hd['Cookie']=response.cookiestring
				utils.mess(u'Login thành công','Fshare.vn');self.logged='success'
			else:utils.mess(u'Login không thành công!','Fshare.vn')
	
	def logout(self):
		if self.logged:
			response = self.fetch('https://www.fshare.vn/logout')
			if response and response.status==302:utils.mess(u'Logout thành công','Fshare.vn');self.logged=None
			else:utils.mess(u'Logout không thành công!','Fshare.vn')
	
	def get_maxlink(self,url):
		response=self.fetch(url);result=pw=None
		if not response:print 'Not response'
		elif response.status==302:result=response.headers['location']
		elif response.status==200:
			if re.search('<title>.*Lỗi 404.*</title>|"index-404"',response.body):
				utils.mess(u'Tập tin quý khách yêu cầu không tồn tại!','Fshare.vn');result='fail'
			elif 'sử dụng nhiều địa chỉ IP' in response.body:
				utils.mess(u'Quý khách đang sử dụng nhiều địa chỉ IP để tải xuống!','Fshare.vn',10000)
				result='fail'
			elif re.search('<i class="fa fa-star">',response.body):utils.mess('Your Fshare acc is FREE','Fshare.vn')
			
			if re.search('class="fa fa-lock"',response.body):
				pw=utils.get_input(u'Hãy nhập: Mật khẩu tập tin')
				if pw:
					try:
						data={'fs_csrf':utils.xsearch('value="(.+?)" name="fs_csrf"',response.body),
						'DownloadForm[pwd]':pw,'ajax':'download-form','DownloadForm[linkcode]':url.split('/')[4]}
						response=self.fetch('https://www.fshare.vn/download/get',data).json
					except:response={}

					if not response:utils.mess(u'Get maxspeed link fail!','Fshare.vn');result='fail'
					elif response.get('url'):result=response.get('url')
					elif response.get('DownloadForm_pwd'):utils.mess(u'Mật khẩu không chính xác!','Fshare.vn')
					else: print response
			elif re.search('action="/download/get"',response.body):
				href='https://www.fshare.vn'+utils.xsearch('action="(/download/get)"',response.body)
				fs_csrf=utils.xsearch('value="(.+?)" name="fs_csrf"',response.body)
				downloadForm=utils.xsearch('id="DownloadForm_linkcode" type="hidden" value="(.+?)"',response.body)
				data={'fs_csrf':fs_csrf,'DownloadForm[pwd]':'','DownloadForm[linkcode]':downloadForm,
						'ajax':'download-form','undefined':'undefined'}
				response=self.fetch(href,data)
				try:result=response.json.get('url')
				except:pass
		return result
	
	def get_token(self,url='https://www.fshare.vn/home'):
		self.hd['x-pjax']='true'
		response=self.fetch(url)
		if not response or response.status!=200:utils.mess(u'Get home page fail!','Fshare.vn');return ''
		self.token=utils.xsearch('data-token="(.+?)"',response.body)
		return self.token
	
	def get_folder(self,url):
		if '/file/' in url:return {'pagename':'','items':[]}
		response=self.fetch(url)
		body=response.body if response and response.status==200 else ''
		pagename=utils.xsearch('<title>(.+?)</title>',body).replace('Fshare - ','')
		items=list()
		for content in re.findall('<div class="pull-left file_name(.+?)<div class="clearfix"></div>',body,re.S):
			item=re.search('data-id="(.+?)".+?href="(.+?)".+?title="(.+?)"',content)
			if item:
				size=utils.xsearch('<div class="pull-left file_size align-right">(.+?)</div>',content).strip()
				id=item.group(1);type='file' if 'file' in item.group(2) else 'folder';title=item.group(3)
				if type=='file':link='https://www.fshare.vn/file/%s'%id
				elif re.search('(\w{10,20} )',title):
					iD=utils.xsearch('(\w{10,20} )',title)
					if 'FOLDER' in iD:link='https://www.fshare.vn/folder/%s'%iD.replace('FOLDER','')
					elif 'FILE' in iD:link='https://www.fshare.vn/file/%s'%iD.replace('FILE','')
					else:
						link='https://www.fshare.vn/folder/%s'%iD
						try:
							if self.fetch(link).status!=200:link='https://www.fshare.vn/file/%s'%iD
						except:pass
					title=' '.join(s for s in title[title.find(' '):].split())
				else:link='https://www.fshare.vn/folder/%s'%id;title=' '.join(s for s in title.split())
				date=utils.xsearch('"pull-left file_date_modify align-right">(.+?)</div>',content).strip()
				items.append((title,link,id,size,date))
		return {'pagename':pagename,'items':items}
	
	def myFshare_add(self,url,name):
		if not self.url_id:utils.mess(u'Hãy set "Thư mục chia sẻ của tôi trên Fshare!"','myFshare');return
		id=url.split('/')[4]
		if [s for s in self.get_folder('https://www.fshare.vn/folder/'+self.url_id)['items'] if id in s[0]]:
			utils.mess(u'This item already in MyFshare!','Fshare.vn');return
		token=self.get_token();name=id+('FOLDER ' if 'folder' in url else 'FILE ')+name
		data='{"token":"%s","name":"%s","in_dir":"%s"}'%(token,name,self.url_id)
		response=self.fetch('https://www.fshare.vn/api/fileops/createFolder',data)
		if response and response.status==200:utils.mess(u'Add a item to MyFshare success','Fshare.vn')
		else:utils.mess(u'Add a item to MyFshare fail!','Fshare.vn')
	
	def myFshare_remove(self,url):
		id=[s[2] for s in self.get_folder('https://www.fshare.vn/folder/'+self.url_id)['items'] if url==s[1]]
		id=id[0] if id else '';data='{"token":"%s","items":["%s"]}'%(self.get_token(),id.strip())
		response=self.fetch('https://www.fshare.vn/api/fileops/delete',data)
		if response and response.status==200:result=True;utils.mess(u'Remove a item from MyFshare success','Fshare.vn')
		else:result=False;utils.mess(u'Remove a item from MyFshare fail!','Fshare.vn')
		return result
	
	def myFshare_rename(self,url,new_name):
		id=[s[2] for s in self.get_folder('https://www.fshare.vn/folder/'+self.url_id)['items'] if url==s[1]]
		id=id[0] if id else '';data='{"token":"%s","new_name":"%s","file":"%s"}'%(self.get_token(),new_name,id)
		response=self.fetch('https://www.fshare.vn/api/fileops/rename',data)
		if response and response.status==200:result=True;utils.mess(u'Rename a item in MyFshare success','Fshare.vn')
		else:result=False;utils.mess(u'Rename a item in MyFshare fail!','Fshare.vn')
		return result
	
	def myFshare_upload(self,name,size,content):
		response=self.fetch('https://www.fshare.vn/home');result=False
		if not response or response.status!=200:
			response=self.fetch('https://www.fshare.vn/home')
			if not response or response.status!=200:utils.mess(u'Get home page fail!','Fshare.vn');return result
		token=utils.xsearch('data-token="(.+?)"',response.body)
		path=utils.xsearch('data-id="%s" path-origin = "" data-path="(.+?)"'%self.url_id,response.body)
		SESSID=utils.xsearch('session_id=(.+?)\W',str(self.hd))
		data='{"SESSID":"%s","name":"%s","size":"%s","path":"%s","token":"%s","secured":1}'%(
			SESSID,name,size,path,token);print data
		response=self.fetch('https://www.fshare.vn/api/session/upload',data)
		if response and response.status==200:
			response=self.fetch(response.json['location'],content)
			if response and response.status==200:result=True;utils.mess(u'Upload file to MyFshare success','Fshare.vn')
		if result is False:utils.mess(u'Upload file to MyFshare fail!','Fshare.vn');print response.status
		return result
	
	def Favorite_add(self,url):
		data='{"token":"%s","link":"%s"}'%(self.get_token(),url)
		response=self.fetch('https://www.fshare.vn/api/fileops/AddFavorite',data)
		if response and response.status==200:
			result=True;utils.mess(u'Add a item to MyFshare Favorite success','Fshare.vn')
		else:result=False;utils.mess(u'Add a item to MyFshare Favorite fail!','Fshare.vn')
		return result
	
	def Favorite_remove(self,name):
		data='{"token":"%s","items":["%s"],"status":0}'%(self.get_token(),name)
		response=self.fetch('https://www.fshare.vn/api/fileops/ChangeFavorite',data)
		if response and response.status==200:
			result=True;utils.mess(u'Remove a item from MyFshare Favorite success','Fshare.vn')
		else:result=False;utils.mess(u'Remove a item from MyFshare Favorite fail!','Fshare.vn')
		return result
	
	def add_folder(self,folder_name,in_dir_id='0'):
		token=self.get_token()
		data='{"token":"%s","name":"%s","in_dir":"%s"}'%(token,folder_name,in_dir_id)
		response=self.fetch('https://www.fshare.vn/api/fileops/createFolder',data)
		try:result=response.json;result_code=result.get('code')
		except:result_code=0
		if result_code==200:
			utils.mess(result.get('msg')+' - '+result.get('folder',{}).get('name'),'Fshare.vn')
			result=result.get('folder',{}).get('linkcode')
		else:utils.mess(u'Add folder fail !','Fshare.vn');result=''
		return result
	
	def remove_folder(self,parent_folder,folder_id):
		data='{"token":"%s","items":["%s"]}'%(self.get_token(),folder_id)
		self.hd['Referer']='https://www.fshare.vn/home/xshare_favourite'
		response=self.fetch('https://www.fshare.vn/api/fileops/delete',data)
		try:result=response.json;result_code=result.get('code')
		except:result_code=0
		if result_code==200:
			utils.mess(result.get('msg'),'Fshare.vn');result='ok'
		else:utils.mess(u'Xóa mục thất bại','Fshare.vn');result=''
		return result
	
	def get_myFolder(self,folder_name=''):
		self.hd['x-pjax']='true'
		url='https://www.fshare.vn/home/'+folder_name+'?_pjax=%23pjax_content'
		response=self.fetch(url)
		if response and response.status==200:
			items=re.findall('dl="(.+?)".+?f-name= "(.+?)"',response.body)
			items=[(s[1],'https://www.fshare.vn'+s[0]) for s in items]
		else:items=[]
		return items #(fn,url)
	
	def upload_file(self,fn):#Chua xong
		size=os.path.getsize(fn);name=os.path.basename(fn);path='/'
		session_id=utils.xsearch('session_id=(.+?)\W',str(self.hd))
		data='{"SESSID":"%s","name":"%s","path":"%s","secured":"1","size":"%d","token":"%s"}'%(session_id,name,path,size,self.get_token())
		response=self.fetch('https://www.fshare.vn/api/session/upload',data)
		print 'a',data
		if response and response.status==200:
			print response.json['location']
			try:response=urlfetch.fetch(response.json['location'].replace('http:','https:'),headers=self.hd,data=data)#files=fn)
			except:response= None
			#response=self.fetch(response.json['location'],files=fn)
			if response and response.status==200:
				print response.json
				result=True;utils.mess(u'Upload file to MyFshare success','Fshare.vn')
		#print response.status

	def remove_file(self,id):
		data='{"token": "%s", "items":["%s"]}'%(self.get_token(),id)
		response=self.fetch('https://www.fshare.vn/api/fileops/delete',data)
		print response.json
		
class fshare1:#https://www.fshare.vn/home/Mục chia sẻ của thaitni/abc?pageIndex=1
    
	def __init__(self, username='', password='', myFshare=''):
		self.myFshare	=  myFshare
		self.logged		=  None
		self.session	=  urlfetch.Session(headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0',
							'x-requested-with':'XMLHttpRequest','content-type':'application/x-www-form-urlencoded','Cookie':''})
		if username:self.login(username,password)
	
	def fetch(self,url, data=''):
		try:response	=  self.session.fetch(url,data=data)
		except:response	=  None
		return response
	
	def login(self,username,password):
		response = self.fetch('https://www.fshare.vn/login')
		if not response or response.status!=200:utils.mess('Connect to fshare.vn fails','Fshare.vn')
		else:
			data = {"LoginForm[email]":username,"LoginForm[password]":password,
				"fs_csrf":utils.xsearch('value="(.+?)" name="fs_csrf"',response.body)}
			response = self.fetch('https://www.fshare.vn/login',data)
			if response and response.status==302:utils.mess(u'Login thành công','Fshare.vn');self.logged='success'
			else:utils.mess(u'Login không thành công!','Fshare.vn')
	
	def logout(self):
		if self.logged:
			response = self.fetch('https://www.fshare.vn/logout')
			if response and response.status==302:utils.mess(u'Logout thành công','Fshare.vn');self.logged=None
			else:utils.mess(u'Logout không thành công!','Fshare.vn')
	
	def get_maxlink(self,url):
		response=self.fetch(url);result=pw=None
		if not response:print 'Not response'
		elif response.status==302:result=response.headers['location']
		elif response.status==200:
			if re.search('<title>.*Lỗi 404.*</title>|"index-404"',response.body):
				utils.mess(u'Tập tin quý khách yêu cầu không tồn tại!','Fshare.vn');result='fail'
			elif re.search('<i class="fa fa-star">',response.body):utils.mess('Your Fshare acc is FREE','Fshare.vn')
			
			if re.search('class="fa fa-lock"',response.body):pw=utils.get_input(u'Hãy nhập: Mật khẩu tập tin')
			if pw:
				try:
					data={'fs_csrf':utils.xsearch('value="(.+?)" name="fs_csrf"',response.body),
					'DownloadForm[pwd]':pw,'ajax':'download-form','DownloadForm[linkcode]':url.split('/')[4]}
					response=self.fetch('https://www.fshare.vn/download/get',data).json
				except:response={}

				if not response:utils.mess(u'Get maxspeed link fail!','Fshare.vn');result='fail'
				elif response.get('url'):result=response.get('url')
				elif response.get('DownloadForm_pwd'):utils.mess(u'Mật khẩu không chính xác!','Fshare.vn')
				else: print response
		return result
	
	def get_token(self):
		response=self.fetch('https://www.fshare.vn/home')
		if not response or response.status!=200:
			content=self.fetch('https://www.fshare.vn/home')
			if not response or response.status!=200:utils.mess(u'Get home page fail!','Fshare.vn');return ''
		return utils.xsearch('data-token="(.+?)"',response.body)
	
	def get_folder(self,url):
		if '/file/' in url:return {'pagename':'','items':[]}
		response=self.fetch(url)
		if not response or response.status!=200:self.fetch(url)
		body=response.body if response and response.status==200 else ''
		pagename=utils.xsearch('<title>(.+?)</title>',body).replace('Fshare - ','')
		items=list()
		for content in re.findall('<div class="pull-left file_name(.+?)<div class="clearfix"></div>',body,re.S):
			item=re.search('data-id="(.+?)".+?href="(.+?)".+?title="(.+?)"',content)
			if item:
				size=utils.xsearch('<div class="pull-left file_size align-right">(.+?)</div>',content).strip()
				id=item.group(1);type='file' if 'file' in item.group(2) else 'folder';title=item.group(3)
				if type=='file':link='https://www.fshare.vn/file/%s'%id
				elif re.search('(\w{10,20} )',title):
					iD=utils.xsearch('(\w{10,20} )',title)
					if 'FOLDER' in iD:link='https://www.fshare.vn/folder/%s'%iD.replace('FOLDER','')
					elif 'FILE' in iD:link='https://www.fshare.vn/file/%s'%iD.replace('FILE','')
					else:
						link='https://www.fshare.vn/folder/%s'%iD
						try:
							if self.session.get(link).status!=200:link='https://www.fshare.vn/file/%s'%iD
						except:pass
					title=' '.join(s for s in title[title.find(' '):].split())
				else:link='https://www.fshare.vn/folder/%s'%id;title=' '.join(s for s in title.split())
				date=utils.xsearch('"pull-left file_date_modify align-right">(.+?)</div>',content).strip()
				items.append((title,link,id,size,date))
		return {'pagename':pagename,'items':items}
	
	def fpt_play_add(self,name='FPT_Play_Favorite'):
		token=self.get_token()
		data='{"token":"%s","name":"%s","in_dir":"%s"}'%(token,name,'0')
		response=self.fetch('https://www.fshare.vn/api/fileops/createFolder',data)
		if response and response.status==200:utils.mess(u'Add a item to MyFshare success','Fshare.vn')
		else:utils.mess(u'Add a item to MyFshare fail!','Fshare.vn')
		
	def myFshare_add(self,url,name):
		if not self.myFshare:utils.mess(u'Hãy set "Thư mục chia sẻ của tôi trên Fshare!"','myFshare');return
		id=url.split('/')[4]
		if [s for s in self.get_folder('https://www.fshare.vn/folder/'+self.myFshare)['items'] if id in s[0]]:
			utils.mess(u'This item already in MyFshare!','Fshare.vn');return
		token=self.get_token();name=id+('FOLDER ' if 'folder' in url else 'FILE ')+name
		data='{"token":"%s","name":"%s","in_dir":"%s"}'%(token,name,self.myFshare)
		response=self.fetch('https://www.fshare.vn/api/fileops/createFolder',data)
		if response and response.status==200:utils.mess(u'Add a item to MyFshare success','Fshare.vn')
		else:utils.mess(u'Add a item to MyFshare fail!','Fshare.vn')
	
	def myFshare_remove(self,url):
		id=[s[2] for s in self.get_folder('https://www.fshare.vn/folder/'+self.myFshare)['items'] if url==s[1]]
		id=id[0] if id else '';data='{"token":"%s","items":["%s"]}'%(self.get_token(),id.strip())
		response=self.fetch('https://www.fshare.vn/api/fileops/delete',data)
		if response and response.status==200:result=True;utils.mess(u'Remove a item from MyFshare success','Fshare.vn')
		else:result=False;utils.mess(u'Remove a item from MyFshare fail!','Fshare.vn')
		return result
	
	def myFshare_rename(self,url,new_name):
		id=[s[2] for s in self.get_folder('https://www.fshare.vn/folder/'+self.myFshare)['items'] if url==s[1]]
		id=id[0] if id else '';data='{"token":"%s","new_name":"%s","file":"%s"}'%(self.get_token(),new_name,id)
		response=self.fetch('https://www.fshare.vn/api/fileops/rename',data)
		if response and response.status==200:result=True;utils.mess(u'Rename a item in MyFshare success','Fshare.vn')
		else:result=False;utils.mess(u'Rename a item in MyFshare fail!','Fshare.vn')
		return result
	
	def myFshare_upload(self,name,size,content):
		response=self.fetch('https://www.fshare.vn/home');result=False
		if not response or response.status!=200:
			content=self.fetch('https://www.fshare.vn/home')
			if not response or response.status!=200:utils.mess(u'Get home page fail!','Fshare.vn');return result
		token=utils.xsearch('data-token="(.+?)"',response.body)
		path=utils.xsearch('data-id="%s" path-origin = "" data-path="(.+?)"'%self.myFshare,response.body)
		SESSID=self.session.cookies.get('session_id')
		data='{"SESSID":"%s","name":"%s","size":"%s","path":"%s","token":"%s","secured":1}'%(
			SESSID,name,size,path,token);print data
		response=self.fetch('https://www.fshare.vn/api/session/upload',data)
		if response and response.status==200:
			response=self.fetch(response.json['location'],content)
			if response and response.status==200:result=True;utils.mess(u'Upload file to MyFshare success','Fshare.vn')
		if result is False:utils.mess(u'Upload file to MyFshare fail!','Fshare.vn');print response.status
		return result
	
	def Favorite_add(self,url):
		data='{"token":"%s","link":"%s"}'%(self.get_token(),url)
		response=self.fetch('https://www.fshare.vn/api/fileops/AddFavorite',data)
		if response and response.status==200:
			result=True;utils.mess(u'Add a item to MyFshare Favorite success','Fshare.vn')
		else:result=False;utils.mess(u'Add a item to MyFshare Favorite fail!','Fshare.vn')
		return result
	
	def Favorite_remove(self,name):
		data='{"token":"%s","items":["%s"],"status":0}'%(self.get_token(),name)
		response=self.fetch('https://www.fshare.vn/api/fileops/ChangeFavorite',data)
		if response and response.status==200:
			result=True;utils.mess(u'Remove a item from MyFshare Favorite success','Fshare.vn')
		else:result=False;utils.mess(u'Remove a item from MyFshare Favorite fail!','Fshare.vn')
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
		if not response or response.status!=302:utils.mess(u'Login Không thành công!','chiasenhac.com')

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
		utils.mess(u'%s'%response.get('message',['Login to phim3s.net fail !',''])[0],'Login to Phim3s.net')
	
	def get_bookmark(self):
		response=self.fetch('http://phim3s.net/ajax/member/get_bookmarks/')
		try:response=response.json
		except:response={}
		print response
		self.fetch('http://phim3s.net/member/logout/')
		return response

	def action_bookmark(self, url,action):#add_bookmark/remove_bookmark
		id=utils.xsearch('_(\d+?)/',url)
		if id:
			url='http://phim3s.net/ajax/member/%s/?film_id=%s'%(action,id)
			response=self.fetch(url)
			try:response=response.json
			except:response={}
			utils.mess(u'%s'%response.get('message','%s thất bại !'%action),'Phim3s.net bookmark')
			self.fetch('http://phim3s.net/member/logout/')

class tvhay:
	def __init__(self, s):
		try:
			w, i, s, e=s.split(',')
			s=self.dec(w, i, s, e)
			b=utils.xsearch("(\w{100,},\w+,\w+,\w+)",s.replace("'",''))
			w, i, s, e=b.split(',')
			s=self.dec(w, i, s, e)
			b=utils.xsearch("(\w{100,},\w+,\w+,\w+)",s.replace("'",''))
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
			try:b=getcode(utils.xsearch("(\w{100,},\w+,\w+,\w+)",b.replace("'",'')));l+=1
			except:break
		return b
	
	return H(string, key) if key else recode(string)
	#e="U2FsdGVkX19NX5WpTrT1EkhOtMSV5geiQQnKWPaiUdnlt0thryUPPdZJPsq6fm2UaXTPxK7DU1Qsi+gsuCYH+GHzUajdakegpUjRrfL7yuCnj1DjnXCEQ9dCSq1DZJ9516CSJifBy1T8UixFNGkhExspmzP4DrNNUmTCXGqQNhuskj5zc8YntdkUunLRs57BDAImaZULEJ4I0loVXjzPxAoPTDV8tEfLi4HJoBm4+h54XnNR7cr1fuQ0qF8/rNJN8Rr2rXdnvikfa9mXEni2g4kOm+4G3+tMYglWxVewOVLR07qUbntzRrxIPuSEixpnQCW333llbZsOl4CNUzajo92r2osf5GrWzG5ntt5+wzbSRravBMmqK7YrJ/nFFLw1nd9IFj4o5S6KcSLdclMsIdfNlOzh6whU4SQkHEQULyDK8QVUyhNyxcqahilf6YXK+N95t2+ZtdVfE/nv0l5P9efPErWajCwJ5vv4de1gnloMMNlow87T6LB+jzpOYpsc29Qf21wXkRjNkZsEuHgb6kpnwdE/BisE/LwsIxil4PzMw3GXlKAlfHQZS1iah0bTQ9wI+c9AtBeZn5dOKtsrPaZLHf+HxnSpUQpmo6jK/MY="
	#r="bilutv.com45904818771133"
	#bilutv(e,r)