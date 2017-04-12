# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcplugin, xbmcgui, json, re, os
from .kodi import xshareFolder, subsFolder, iconsFolder

def s2u(s):
	return s.decode('utf-8') if isinstance(s,str) else s

def u2s(s):
	return s.encode('utf-8') if isinstance(s,unicode) else s

def s2c(s):
	m = []
	for i in s.split():
		d = xsearch('&#(\d+);',i)
		m.append( re.sub('&#\d+;', unichr(int(d)).encode('utf-8'), i) if d else i )
	return ' '.join(m)

def namecolor(name,c=''):
	return '[COLOR %s]%s[/COLOR]'%(c,name) if c else re.sub('\[[^\[]+?\]','',name)

def filetime(fn):#return hour
	import urllib
	if ":" not in fn:
		fn = os.path.join(xshareFolder, fn)
	t = os.path.getmtime(fn) if os.path.isfile(fn) else 0
	return int((urllib.time.time()-t)/3600)

def xsearch(pattern,string,group=1,flags=0,result=''):
	try:s=re.search(pattern,string,flags).group(group)
	except:s=result
	return s

def xrw(fn,s='',a='w'):
	if ":" not in fn:
		fn = os.path.join(xshareFolder,fn)
	
	try:
		if s:
			if a=='w' : s = s.replace('\r\n','\n')
			f = open(fn, a)
			f.write(s)
		else:
			f = open(fn)
			s = f.read().replace('\r\n','\n')
		f.close()
	
	except:
		s = ''
	return s

def get_params(paramstring):
	from urlparse import parse_qsl
	params = dict(parse_qsl(paramstring))

	name  = params.get('name','')
	url   = params.get('url','')
	img   = params.get('img','')
	mode  = params.get('mode','')
	query = params.get('query','')
	page  = int(params.get('page', '1'))

	from kodi import log
	#log('============================================================')
	#log([name,url,img,mode,page,query])
	#log(url)
	#log(name)
	#log(query)
	log(params)
	log('==============================-=============================')

	return (name, url, img, mode, page, query)


def get_params1(params):
	def info(i):
		return i.split('=')[0],urllib.unquote_plus(i.split('=')[1])
	
	import urllib
	try    : param = dict(info(i) for i in params.split('?')[1].split('&') if '='in i)
	except : param = {}
	
	name  = param.get('name','')
	url   = param.get('url','')
	img   = param.get('img','')
	mode  = param.get('mode','')
	query = param.get('query','')
	try    : page = int(param.get('page'))
	except : page = 1
	from kodi import log;log(params)
	#log('============================================================')
	#log([name,url,img,mode,page,query])
	log(url)
	log(name)
	log('==============================-=============================')
	return (name,url,img,mode,page,query)

def setSubtitles(url):
	player = xbmc.Player()
	while not player.isPlaying():xbmc.sleep(1000)
	mess('Xshare auto load subtitle')
	player.setSubtitles(url)

def xread(url, headers={'User-Agent':'Mozilla/5.0'}, data=None, timeout=30, read=True):
	import urllib2
	req = urllib2.Request(url,data,headers)
	try:
		res = urllib2.urlopen(req, timeout=timeout)
		if read:
			hd = res.info().dict
			cookie = hd.get('set-cookie','')
			encoding = hd.get('content-encoding','')
			if encoding == 'gzip':
				import StringIO,gzip
				buf = StringIO.StringIO(res.read())
				f = gzip.GzipFile(fileobj=buf)
				b = f.read()
			else:
				b = res.read()
			res.close()
		else:
			b = res
	
	except : b = ''
	return b


def xsharetinyData(data=None):
	import json
	from .utils import xrw
	
	try: 
		if not data:
			j = json.loads(xrw('xsharetiny.json'))
		else:
			j = xrw('xsharetiny.json', json.dumps(data))
	
	except:
		j = {}
	
	return j


def getXshareData():
	url='http://pastebin.com/raw/QincDEYZ'
	try:j=requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=30).json()
	except:j={}
	return j

def deleteSubFolder():
	for fn in os.listdir(subsFolder):
		fp = os.path.join(subsFolder, fn)
		if os.path.isfile(fp):
			try    : os.remove(fp)
			except : pass

def downloadSubs(link,filename):
	deleteSubs();log(link)
	r=requests.get(link, headers={'User-Agent':'Mozilla/5.0'}, timeout=20)
	if [i for i in ('zip','rar') if i in r.headers.get('Content-Type')]:
		ext='zip' if 'zip' in r.headers.get('Content-Type') else 'rar'
		fn=os.path.join(xshareFolder,'temp.'+ext)
		b=xrw(fn,r.content,'wb')
		if b:
			cmd='XBMC.Extract("%s","%s")' % (fn, subsFolder)
			try:
				xbmc.executebuiltin(('%s'%cmd).encode('utf-8'), True)
				mess('Đã downloads subtitle files vào thư mục xshare sub')
			except:mess('Lỗi download files phụ đề!')
			os.remove(fn)
	else:
		try:fn=link.rsplit('/',1)[1]
		except:fn=filename
		if xrw(fn+'.vie',r.content,'s'):
			mess('Đã downloads subtitle file vào thư mục xshare sub')
		else:mess('Lỗi download file phụ đề!')
