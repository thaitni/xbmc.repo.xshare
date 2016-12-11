# -*- coding: utf-8 -*-

import xbmc, xbmcaddon, xbmcgui, urllib2
re=urllib2.re
os=urllib2.os
#addon=addon()
addon= xbmcaddon.Addon()
profile=xbmc.translatePath(addon.getAddonInfo('profile'))
datapath=os.path.join(profile,'data')
tempfolder=xbmc.translatePath('special://temp')
xsharefolder=os.path.join(profile,'xshare')
icon=os.path.join(profile,'icon','icon.png')
#b.getcode();b.headers.get('Set-Cookie');b.geturl()
class myaddon:
    def __init__(self):
		self.addon			= xbmcaddon.Addon()
		self.info			= self.addon.getAddonInfo
		self.name			= self.info('name')
		self.version		= self.info('version')
		self.get_setting	= self.addon.getSetting
		self.set_setting	= self.addon.setSetting

		self.src_path		= xbmc.translatePath(self.info('path'))
		self.data_path		= xbmc.translatePath(self.info('profile'))
		self.temp_path		= xbmc.translatePath('special://temp')

		self.data_folder	= os.path.join(self.data_path,'data')
		self.icon_folder	= os.path.join(self.data_path,'icon')
		self.icon			= os.path.join(self.icon_folder,'icon.png')

def filetime(fn):#return hour
	fn=os.path.join(xsharefolder,fn)
	t=os.path.getmtime(fn) if os.path.isfile(fn) else 0
	return int((urllib2.time.time()-t)/3600)

def siteName(url):
	url=url.split('?')[0]
	return url.rsplit('/',1)[1] if url.rsplit('/',1)[1] else url.rsplit('/',1)[0].rsplit('/',1)[1]

def get_setting(name):return addon.getSetting(name)
def set_setting(name,value):addon.setSetting(name,value)
def namecolor(name,c=''):return '[COLOR %s]%s[/COLOR]'%(c,name) if c else re.sub('\[[^\[]+?\]','',name)
def s2u(s):return s.decode('utf-8') if isinstance(s,str) else s
def u2s(s):return s.encode('utf-8') if isinstance(s,unicode) else s
def unescape(string):return ' '.join(re.sub('&.+;',xsearch('&(\w).+;',s,1),s) for s in string.split())
def xhref(s,p=''):return xsearch('href="(.+?)"',s,result=xsearch(p,s))
def xtitle(s,p=''):return ' '.join(xsearch('title="(.+?)"',s,result=xsearch(p,s)).split())
def ximg(s,p=''):return xsearch('src="(.+?)"',s,result=xsearch(p,s))
def refa(p,s,f=0):return re.findall(p,s,f)
def refas(p,s):return re.findall(p,s,re.S)
def mess(message='',title='',timeShown=5000):
	if message:
		title=': [COLOR blue]%s[/COLOR]'%title if title else ''
		s0='[COLOR green][B]Xshare[/B][/COLOR]'+title
		message=s2u(message)
		s1=u'[COLOR red]%s[/COLOR]'%message if '!' in message else u'[COLOR gold]%s[/COLOR]'%message
		xbmc.executebuiltin((u'XBMC.Notification(%s,%s,%s,%s)'%(s0,s1,timeShown,icon)).encode("utf-8"))
	else:xbmc.executebuiltin("Dialog.Close(all, true)")

def xselect(label,choices):
	dialog = xbmcgui.Dialog()
	return dialog.select(label, choices)

def googleItems(j,link='link',label='label'):#Thu nghiem tren phim14
	try:l=[(i.get(link),rsl(i.get(label))) for i in j]
	except:
		try:l=[(i.get(link),rsl(i.get('type'))) for i in j]
		except:
			try:l=[(i.get('file'),rsl(i.get('type'))) for i in j]
			except:l=''
	link=''
	if l:
		for href,label in ls(l):
			#link=xcheck(href.replace('\\',''))#;print href
			resp=xget(href.replace('\\',''))#;print href
			if resp:link=href;break
	return link

def rsl(s):
	s=str(s).replace('HDG','').replace('HD','1080').replace('SD','640').replace('large','640').replace('medium','480')
	s=s.replace('Auto','640').replace('AUTO','640')
	result=xsearch('(\d+)',s)
	return result if result else '240'

def ls(l):
	reverse=True if get_setting('resolut')=='Max' else False
	try:L=sorted(l, key=lambda k: int(k[1]),reverse=reverse)
	except:L=l
	return L

def xrw(fn,s=''):
	fn=os.path.join(xsharefolder,fn)
	try:
		if s:s=s.replace('\r\n','\n');f=open(fn,'w');f.write(s)
		else:f=open(fn);s=f.read().replace('\r\n','\n')
		f.close()
	except:s=''
	return s

def xcookie(cookie=None):
	if cookie:ck=';'.join('%s=%s'%(i.name,i.value) for i in cookie.cookiejar)
	else:ck=urllib2.HTTPCookieProcessor();urllib2.install_opener(urllib2.build_opener(ck))
	return ck
	
def xread(url,headers={'User-Agent':'Mozilla/5.0'},data=None,timeout=30):
	req=urllib2.Request(url,data,headers)
	try:
		res=urllib2.urlopen(req, timeout=timeout)
		hd=dict(res.headers.items())
		cookie=hd.get('set-cookie','')
		encoding=hd.get('content-encoding','')
		if encoding=='gzip':
			import StringIO,gzip
			buf=StringIO.StringIO(res.read())
			f=gzip.GzipFile(fileobj=buf)
			b=f.read()
		else:b=res.read()
		res.close()
	except:b=''
	return b

def xreadc(url,hd={'User_Agent':'Mozilla/5.0'},data='',c=''):
	cookie=urllib2.HTTPCookieProcessor()
	opener=urllib2.build_opener(cookie)
	urllib2.install_opener(opener)
	opener.addheaders=hd.items()
	if c:opener.addheaders=[('Cookie',c)]
	try:
		o=opener.open(url,data);b=o.read();o.close()
		b+='xshare%s'%';'.join('%s=%s'%(i.name,i.value) for i in cookie.cookiejar)
	except:b=''
	return b

def xget(url,hd={'User-Agent':'Mozilla/5.0'},data=None,timeout=30):#d=res.info().dict
	try:res=urllib2.urlopen(urllib2.Request(url,data,hd),timeout=timeout)
	except:res=None
	return res#res.info().get('content-length')

def xcheck(item,hd={'User-Agent':'Mozilla/5.0'},data=None,timeout=30):
	def check(url):
		req=urllib2.Request(url,data,hd)
		try:b=urllib2.urlopen(req,timeout=timeout);link=b.geturl();b.close()
		except:link=''
		return link
	link=''
	if type(item) in (str,unicode):link=check(item)
	elif type(item)==list:
		try:
			for href,title in item:
				link=check(href)
				if link:break
		except:mess('Link checked fail !','xshare')
	return link

def get_input(title=u"", default=u""):
	result = ''
	keyboard = xbmc.Keyboard(default, title)
	keyboard.doModal()
	if keyboard.isConfirmed():
		result = keyboard.getText()
	return result.strip()

def xsearch(pattern,string,group=1,flags=0,result=''):
	try:s=re.search(pattern,string,flags).group(group)
	except:s=result
	return s

def xsearchs(pattern,string):
	try:s=re.search(pattern,string,re.S).group(1)
	except:s=result
	return s

def fmn(n):
	try:s=format(int(n), "8,d").replace(',','.').strip()
	except:s=str(n)
	return s

def fixTitleEPS(i):
	p=[xsearch('(Tập.?\d+)|(tập.?\d+)|(TẬP.?\d+)',i),xsearch('(\WE.?\d+)',i)]
	if p[0]:i=re.sub(p[0],'Tập '+format(int(xsearch('(\d+)',p[0])),'02d'),i)
	elif p[1]:i=re.sub(p[1],'.E'+format(int(xsearch('(\d+)',p[1])),'02d'),i)
	return i

def vnu(s):
	dic={'&Aacute;':'Á','&aacute;':'á','&Agrave;':'À','&agrave;':'à','&acirc;':'â','&atilde;':'ã','&Egrave;':'È','&egrave;':'è','&Eacute;':'É','&eacute;':'é','&ecirc;':'ê','&Ograve;':'Ò','&ograve;':'ò','&Oacute;':'Ó','&oacute;':'ó','&Ocirc;':'Ô','&ocirc;':'ô','&otilde;':'õ','&Uacute;':'Ú','&uacute;':'ú','&Ugrave;':'Ù','&ugrave;':'ù','&Igrave;':'Ì','&igrave;':'ì','&Iacute;':'Í','&iacute;':'í','&Yacute;':'Ý','&yacute;':'ý','&bull;':'*'}
	for i in dic:s=s.replace(i,dic.get(i))
	return ' '.join(re.sub('&.+;',xsearch('&(\w).+;',i),i) for i in s.split())

def s2c(s):
	def sc(s):i=xsearch('&a?m?p?;?#(\d+);',s);return re.sub('&a?m?p?;?#\d+;',d.get(i,''),s) if i else s
	d={'192':'À','193':'Á','194':'Â','195':'Ă','202':'Ê','204':'Ì','205':'Í','211':'Ó','212':'Ô','217':'Ù','218':'Ú','224':'à','225':'á','226':'â','227':'ă','232':'è','233':'é','234':'ê','235':'ẽ','236':'ì','237':'í','242':'ò','243':'ó','244':'ô','245':'ỏ','249':'ù','250':'ú','253':'ý','039':"'"}
	return ' '.join(sc(i) for i in s.split()).replace('&amp;','&').replace('&quot;','"')

def s2c1(s):
	return ' '.join(re.sub('&#\d+;',unichr(int(xsearch('&#(\d+);',i))),i) if xsearch('&#(\d+);',i) else i for i in s.split())

def leechInfo(link):
	href='http://vnz-leech.com/checker/check.php?links=%s'
	headers={'Referer':'http://vnz-leech.com/checker/','User-Agent':'Mozilla/5.0'}
	b=xread(href%''.join(link.split()),headers)
	try:j=json.loads(b.replace('(','').replace(')',''))
	except:j={}
	def geti(j,i):return j.get(i,'').encode('utf-8')
	result='',''
	if j.get('status','')=='good_link':
		title='%s (%s)'%(geti(j,'filename'),geti(j,'filesize'))
		href=geti(j,'link')
		if title and href:result=title,href
	return result

def siteInfo(url):
	if '4share.vn/f/' in url.lower():
		url='http://4share.vn/f/%s/'%xsearch('/f/(\w+)',url)
		title,url=leechInfo(url)
	elif '4share.vn/d/' in url.lower():
		url='http://4share.vn/d/%s/'%xsearch('/d/(\w+)',url)
		b=xread(url)
		if '[Empty Folder]' in b:title=''
		else:title=xsearch("<title>(.+?)</title>",b).replace('4Share.vn - ','')
	elif 'fshare.vn' in url.lower():
		id=siteName(url).upper();link='https://www.fshare.vn/%s/'+id
		url=link%('file' if '/file/' in url.lower() else 'folder')
		b=xread(url)#,{'User-Agent':'Mozilla/5.0','x-requested-with':'XMLHttpRequest'})
		if b and '/file/' in url:
			s=xsearch('(<div class="file-info".+?data-owner)',b,1,re.S)
			m=xsearch('(<i class="fa fa-file.+?/div>)',s,1,re.S)
			title=' '.join(re.sub('<[^>]+?>','',m).split())
			if title:
				size=xsearch('(<i class="fa fa-hdd.+?/div>)',s,1,re.S)
				title=title+' '+re.sub('<[^>]+?>| ','',size)
			elif not xsearch('(<title>Lỗi 404</title>)',b):title,url=leechInfo(url)
		elif b:
			p='(<span class="glyphicon glyphicon-info.+?/div>)'
			size=re.sub('<[^>]+?>|Số lượng|:','',xsearch(p,b,1,re.S)).strip()
			if size and size>'0':
				title=xsearch('(<title>.+?</title>)',b)
				title='%s %s file(s)'%(' '.join(re.sub('<[^>]+?>|Fshare|-','',title).split()),size)
			else:title=''
		else:title,url=leechInfo(url)
	if not title:url=''
	return title,url

def getLinkFree1(url):
	data='url_download=https%3A%2F%2Fwww.fshare.vn%2Ffile%2F'+url.rsplit('/',1)[1]
	link='';loop=0
	while not link and loop < 2:
		b=xread('http://www.aku.vn/linksvip',data=data)
		link=xsearch('<a href=([^<]+?) target=_blank',b)
		if link and '/account/' in link:link=''
		elif link:mess('[COLOR cyan]Thanks to Nhat Vo Van[/COLOR]','get link from aku.vn')
		loop+=1
	
	d=[('ZnJlZXMuZnNoYXJlQGdtYWlsLmNvbToxMjM0NTY3','Trương Văn Hiếu','thuthuatvoz.com'),
		('cGhhbXF1b2N2aWV0aHA5MEBnbWFpbC5jb206Y2hvbmd5ZXV2bw==','Long Kwei Tei','Cong Dong KODIl Viet Nam'),
		('eHNoYXJlQHRoYW5odGhhaS5uZXQ6dGhhaXRuaUA=','xshare','xshare')]
	loop=0;l=len(d);j=[]
	while (not link or link=='fail') and loop < l:
		i=100
		while i not in j:
			i=urllib2.random.randint(0,l-1)
			if i not in j:j.append(i)
			else:i=100
		
		try:
			b=xreadc('http://www.fshare.vn')
			cookie=b.split('xshare')[1]
			fs_csrf=xsearch('value="(.+?)" name="fs_csrf"',b)
		except:cookie=fs_csrf=''
		u,p=urllib2.base64.b64decode(d[i][0]).split(':')
		data=urllib.urlencode({"LoginForm[email]":u,"LoginForm[password]":p,"fs_csrf":fs_csrf})
		hd={'Cookie':cookie,'Content-Type':'application/x-www-form-urlencoded'}
		conn = urllib2.httplib.HTTPSConnection('www.fshare.vn')
		conn.request('POST', '/login',data,hd)
		try:
			response=conn.getresponse()
			if response.status==302:
				cookie=response.getheader('set-cookie')
				mess('[COLOR cyan]Thanks to %s[/COLOR]'%d[i][1],d[i][2])
				xbmc.sleep(2000)
			else:cookie=''
		except:cookie=''
		hd={'User-Agent':'Mozilla/5.0','x-requested-with':'XMLHttpRequest','Cookie':cookie}
		b=xget(url,hd)
		link=b.geturl()
		if link==url:
			b=b.read()
			fs_csrf=xsearch('value="(.+?)" name="fs_csrf"',b)
			downloadForm=xsearch('id="DownloadForm_linkcode" type="hidden" value="(.+?)"',b)
			data={'fs_csrf':fs_csrf,'DownloadForm[linkcode]':downloadForm,'ajax':'download-form'}
			if xsearch('class="(fa fa-lock)"',b):
				data['DownloadForm[pwd]']=get_input(u'Hãy nhập: Mật khẩu tập tin')
			b=xread('https://www.fshare.vn/download/get',hd,urllib.urlencode(data))
			try:link=json.loads(b).get('url','')
			except:link='fail'
		xget('https://www.fshare.vn/logout',hd)
		loop+=1
	return link