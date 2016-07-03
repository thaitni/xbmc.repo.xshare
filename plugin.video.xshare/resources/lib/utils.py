# -*- coding: utf-8 -*-

import xbmc, xbmcaddon, urllib2

#addon=addon()
addon= xbmcaddon.Addon()
profile=xbmc.translatePath(addon.getAddonInfo('profile'))
datapath=urllib2.os.path.join(profile,'data')
tempfolder=xbmc.translatePath('special://temp')
xsharefolder=urllib2.os.path.join(tempfolder,'xshare')
icon=urllib2.os.path.join(profile,'icon','icon.png')

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

		self.data_folder	= urllib2.os.path.join(self.data_path,'data')
		self.icon_folder	= urllib2.os.path.join(self.data_path,'icon')
		self.icon			= urllib2.os.path.join(self.icon_folder,'icon.png')

def filetime(fn):#return hour
	fn=urllib2.os.path.join(xsharefolder,fn)
	t=urllib2.os.path.getmtime(fn) if urllib2.os.path.isfile(fn) else 0
	return int((urllib2.time.time()-t)/600)
	
def get_setting(name):return addon.getSetting(name)
def set_setting(name,value):addon.setSetting(name,value)
def mess(message='',title='',timeShown=5000):
	if not message:xbmc.executebuiltin("Dialog.Close(all, true)")
	else:
		title=': [COLOR blue]%s[/COLOR]'%title if title else ''
		s0='[COLOR green][B]Xshare[/B][/COLOR]'+title
		s1='[COLOR red]%s[/COLOR]'%message if '!' in message else u'[COLOR gold]%s[/COLOR]'%message
		#icon=addon.icon
		xbmc.executebuiltin((u'XBMC.Notification(%s,%s,%s,%s)'%(s0,s1,timeShown,icon)).encode("utf-8"))

def rsl(s):
	s=str(s).replace('HDG','').replace('HD','1080').replace('SD','640').replace('large','640').replace('medium','480')
	result=xsearch('(\d+)',s)
	return result if result else '240'

def ls(l):
	r=True if get_setting('resolut')=='Max' else False
	l=sorted(l, key=lambda k: int(k[1]),reverse=r)
	return l

def namecolor(name,c=''):return '[COLOR %s]%s[/COLOR]'%(c,name) if c else urllib2.re.sub('\[[^\[]+?\]','',name)
def xrw(fn,s=''):
	fn=urllib2.os.path.join(xsharefolder,fn)
	try:
		if s:f=open(fn,'w');f.write(s);s=fn
		else:f=open(fn);s=f.read()
		f.close()
	except:s=''
	return s

def xcookie(cookie=None):
	if cookie:ck=';'.join('%s=%s'%(i.name,i.value) for i in cookie.cookiejar)
	else:ck=urllib2.HTTPCookieProcessor();urllib2.install_opener(urllib2.build_opener(ck))
	return ck
	
def xread(url,headers={'User-Agent':'Mozilla/5.0'},data=None):
	req=urllib2.Request(url,data,headers)
	try:res=urllib2.urlopen(req, timeout=30);b=res.read();res.close()
	except:b=''
	return b

def xget(url,data=None,timeout=30):#b.getcode();b.headers.get('Set-Cookie');b.geturl()
	try:b=urllib2.urlopen(url,data,timeout)
	except:b=None
	return b

def get_input(title=u"", default=u""):
	result = ''
	keyboard = xbmc.Keyboard(default, title)
	keyboard.doModal()
	if keyboard.isConfirmed():
		result = keyboard.getText()
	return result.strip()

def xsearch(pattern,string,group=1,flags=0,result=''):
	try:s=urllib2.re.search(pattern,string,flags).group(group)
	except:s=result
	return s

def fmn(n):
	try:s=format(int(n), "8,d").replace(',','.').strip()
	except:s=str(n)
	return s

def s2u(s):return s.decode('utf-8') if isinstance(s,str) else s
def u2s(s):return s.encode('utf-8') if isinstance(s,unicode) else s
def unescape(string):return ' '.join(urllib2.re.sub('&.+;',xsearch('&(\w).+;',s,1),s) for s in string.split())
def s2c(s):
	def sc(s):i=xsearch('&#(\d+);',s);return urllib2.re.sub('&#\d+;',d.get(i,''),s) if i else s
	d={'192':'À','193':'Á','194':'Â','195':'Ă','202':'Ê','204':'Ì','205':'Í','211':'Ó','212':'Ô','217':'Ù','218':'Ú','224':'à','225':'á','226':'â','227':'ă','232':'è','233':'é','234':'ê','235':'ẽ','236':'ì','237':'í','242':'ò','243':'ó','244':'ô','245':'ỏ','249':'ù','250':'ú','253':'ý'}
	return ' '.join(sc(i) for i in s.split())
def s2c1(s):
	return ' '.join(urllib2.re.sub('&#\d+;',unichr(int(xsearch('&#(\d+);',i))),i) if xsearch('&#(\d+);',i) else i for i in s.split())
