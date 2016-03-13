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
