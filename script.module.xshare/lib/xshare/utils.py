# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcplugin, xbmcgui, requests, urllib, json, re, os
addon=xbmcaddon.Addon()
path=xbmc.translatePath(addon.getAddonInfo('path'))
xshareFolder=os.path.join(xbmc.translatePath('special://masterprofile/'),'xshare')
if not os.path.exists(xshareFolder):os.mkdir(xshareFolder)
xshareSub=os.path.join(xshareFolder,'subs')
if not os.path.exists(xshareSub):os.mkdir(xshareSub)
ico=os.path.join(path,'icon.png')

def log(s):
	if isinstance(s,basestring):xbmc.log(u2s(s))
	elif isinstance(s,list):xbmc.log('\n'.join(u2s(str(i).strip()) for i in s if i))
def s2u(s):return s.decode('utf-8') if isinstance(s,str) else s
def u2s(s):return s.encode('utf-8') if isinstance(s,unicode) else s
def s2c(s):
	def sc(s):i=xsearch('&a?m?p?;?#(\d+);',s);return re.sub('&a?m?p?;?#\d+;',d.get(i,''),s) if i else s
	d={'192':'À','193':'Á','194':'Â','195':'Ă','202':'Ê','204':'Ì','205':'Í','211':'Ó','212':'Ô','217':'Ù','218':'Ú','224':'à','225':'á','226':'â','227':'ă','232':'è','233':'é','234':'ê','235':'ẽ','236':'ì','237':'í','242':'ò','243':'ó','244':'ô','245':'ỏ','249':'ù','250':'ú','253':'ý','039':"'",'8211':'-'}
	return ' '.join(sc(i) for i in s.split()).replace('&amp;','&').replace('&quot;','"')

def mess(message='',title='',timeShown=5000):
	if message:
		message=u2s(message)
		title=': [COLOR blue]%s[/COLOR]'%title if title else ''
		s0='[COLOR green][B]Xshare[/B][/COLOR]'+title
		s1='[COLOR red]%s[/COLOR]'%message if '!' in message else '[COLOR gold]%s[/COLOR]'%message
		xbmc.executebuiltin(('XBMC.Notification(%s,%s,%s,%s)'%(s0,s1,timeShown,ico)))
	else:xbmc.executebuiltin("Dialog.Close(all, true)")

def namecolor(name,c=''):
	return '[COLOR %s]%s[/COLOR]'%(c,name) if c else re.sub('\[[^\[]+?\]','',name)

def filetime(fn):#return hour
	if len(fn) < 20:fn=os.path.join(xshareFolder,fn)
	t=os.path.getmtime(fn) if os.path.isfile(fn) else 0
	return int((urllib.time.time()-t)/3600)

def xsearch(pattern,string,group=1,flags=0,result=''):
	try:s=re.search(pattern,string,flags).group(group)
	except:s=result
	return s

def xrw(fn,s='',a='w'):
	if a=='s':a='w';fn=os.path.join(xshareSub,fn)
	elif len(fn) < 20:fn=os.path.join(xshareFolder,fn)
	try:
		if s and a in 'w-a':s=s.replace('\r\n','\n');f=open(fn,a);f.write(s)
		elif s:f=open(fn,a);f.write(s)
		else:f=open(fn);s=f.read().replace('\r\n','\n')
		f.close()
	except:s=''
	return s

def dc(data):
	for i in data:
		j=data.get(i,'')
		if j=="thaitni@":data[i]="thaitni@$&"
		elif j=="thanhxuyen@":data[i]="thanhxuyen$$$"
		elif j=="taidienbien@":data[i]="taidienbien%%%"
	return data

def get_input(title=u"", default=u""):
	result = ''
	keyboard = xbmc.Keyboard(default, title)
	keyboard.doModal()
	if keyboard.isConfirmed():
		result = keyboard.getText()
	if not result:result=''
	return result.strip()

def get_params(params):
	def info(i):return i.split('=')[0],urllib.unquote_plus(i.split('=')[1])
	try:param=dict(info(i) for i in params.split('?')[1].split('&') if '='in i)
	except:param={}
	log(str(param))
	name=param.get('name','')
	url=param.get('url','')
	img=param.get('img','')
	mode=param.get('mode','')
	try:page=int(param.get('page'))
	except:page=1
	query=param.get('query','')
	log('============================================================')
	log([name,url,img,mode,page,query])
	log('==============================-=============================')
	return (name,url,img,mode,page,query)

def setSubtitles(url):
	player = xbmc.Player()
	while not player.isPlaying():xbmc.sleep(1000)
	mess('Xshare auto load subtitle')
	player.setSubtitles(url)

def xread(url,headers={'User-Agent':'Mozilla/5.0'},data=None,timeout=30):
	try:
		r=requests.get(url, headers=headers, timeout=timeout)
		b=r.content
	except:b=''
	return b

def getXshareData():
	url='http://pastebin.com/raw/QincDEYZ'
	try:j=requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=30).json()
	except:j={}
	return j

def deleteSubs():
	for f in os.listdir(xshareSub):
		fn=os.path.join(xshareSub,f)
		if os.path.isfile(fn):os.remove(fn)

def downloadSubs(link,filename):
	deleteSubs();log(link)
	r=requests.get(link, headers={'User-Agent':'Mozilla/5.0'}, timeout=20)
	if [i for i in ('zip','rar') if i in r.headers.get('Content-Type')]:
		ext='zip' if 'zip' in r.headers.get('Content-Type') else 'rar'
		fn=os.path.join(xshareFolder,'temp.'+ext)
		b=xrw(fn,r.content,'wb')
		if b:
			cmd='XBMC.Extract("%s","%s")' % (fn, xshareSub)
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
