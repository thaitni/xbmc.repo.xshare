#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import xbmcplugin,xbmcgui,xbmcaddon,urllib,re,os

myaddon = xbmcaddon.Addon(id="plugin.video.xshare.tiny")
home = myaddon.getAddonInfo('path')
resource = xbmc.translatePath(os.path.join(home,'resources/'))
sys.path.append(xbmc.translatePath(os.path.join(home, 'resources', 'lib')))
import urlfetch
datapath = xbmc.translatePath(os.path.join( xbmc.translatePath(myaddon.getAddonInfo('profile')),'data/'))
if not os.path.exists(xbmc.translatePath(myaddon.getAddonInfo('profile'))):
	os.mkdir(xbmc.translatePath(myaddon.getAddonInfo('profile')))
if not os.path.exists(datapath):os.mkdir(datapath)
language = myaddon.getLocalizedString
logoutf=myaddon.getSetting('logoutf')

hd={'User-Agent':'Mozilla/5.0','Accept-Language':'en-US,en;q=0.8,vi;q=0.6','Cookie':''}
media_ext=['aif','iff','m3u','m4a','mid','mp3','mpa','ra','wav','wma','3g2','3gp','asf','asx','avi','flv','mov','mp4','mpg','mkv','m4v','rm','swf','vob','wmv','bin','cue','dmg','iso','mdf','toast','vcd','ts','flac']

def mess(message, timeShown=5000):
	xbmc.executebuiltin((u'XBMC.Notification("%s","%s",%s)'%('Xshare',message,timeShown)).encode("utf-8"))

def get_input(title=u"", default=u""):
	result = ''
	keyboard = xbmc.Keyboard(default, title)
	keyboard.doModal()
	if keyboard.isConfirmed():
		result = keyboard.getText()
	return result
	
def make_request(url, headers={}):
	try:
		response = urlfetch.fetch(url,headers=headers)
		hd['Cookie'] = response.headers.get('set-cookie')
		body = response.body
		response.close()
	except: mess('Make Request Error: %s'%url);body=''
	return body

def loginfshare():
	url = "https://www.fshare.vn/login"
	form_fields = {
		"LoginForm[email]": myaddon.getSetting('username'), 
		"LoginForm[password]": myaddon.getSetting('password'),"LoginForm[rememberMe]": "0",
		"fs_csrf": re.search('value="(.+?)".*name="fs_csrf',make_request(url)).group(1)}
	response = urlfetch.post(url=url,headers=hd,data=urllib.urlencode(form_fields), follow_redirects=False)
	if response.status==302:mess(u'Login Fshare.vn thành công',timeShown=100);f=response.cookiestring
	else:mess(u'Login Fshare.vn không thành công');f=''
	return f
	
def check_id_fshare(ID):
	body=urlfetch.fetch('https://www.fshare.vn/folder/'+ID).body
	if re.search('download_folder',body):url='https://www.fshare.vn/folder/'+ID
	else:
		body=urlfetch.fetch('https://www.fshare.vn/file/'+ID).body
		if re.search('pull-right file_info',body):url='https://www.fshare.vn/file/'+ID
		else:body=url=''
	return body,url
	re.search("speed: (.+?).\s+fs_csrf: \'(.+?)\'",response)
	
def main(url='',query=''):#mode=1
	print 'aaa',url
	print 'aaa',query
	datafile=datapath+'xshare.xml'
	if query=='':
		addir('[COLOR gold]Nhập Fshare ID mới[/COLOR]','',resource+'icon.png',mode=1,query='new',isFolder=True)
		if not os.path.isfile(datafile):
			f=open(datafile,'w');f.write('<?xml version="1.0" encoding="utf-8">\n');f.close()
		else:
			f=open(datafile);items=re.findall('<a href="(.+?)">(.+?)</a>',f.read());f.close()
			for href,name in items: 
				if '/file/' in href:addir(name,href,resource+'fshare.png',mode=2,query='ContextMenu')
				else:addir('[COLOR gold]'+name+'[/COLOR]',href,resource+'fshare.png',mode=1,query='ContextMenu',isFolder=True)
		addir('[COLOR gold]Add-on setting[/COLOR]','',resource+'icon.png',mode=3,isFolder=True)
		return ''
	elif query == 'new': #Nhập ID mới
		iD = get_input('Hãy nhập ID phim của Fshare')
		if iD is None or iD=='':return 'no'
		iD = iD.strip().upper()
		if len(iD)<10:mess(u'Bạn nhập ID link chưa đúng: '+iD);return 'no'
		body,url=check_id_fshare(iD)
		if url=='':mess(u'Không tìm được phim có ID là: '+iD);return 'no'
		name=re.search('<title>Fshare - (.+?)</title>',body)
		if name:name=name.group(1)
		else:name=url
		f=open(datafile,'a');f.write('<a href="'+url+'">'+name+'</a>\n');f.close()
		if '/file/' in url:addir(name,url,resource+'fshare.png',mode=2)
		else:main(url,body);return ''
	elif query == 'del_id':
		f=open(datafile);items=re.findall('<a href="(.+?)">(.+?)</a>',f.read());f.close()
		content='<?xml version="1.0" encoding="utf-8">\n'
		for href,name in items:
			if href!=url:content+='<a href="%s">%s</a>\n'%(href,name)
		try:f=open(datafile,'w');f.write(content);f.close();mess(u'Đã xóa mục %s'%url)
		except:mess(u'Chưa xóa được mục %s'%url)
		xbmc.executebuiltin("Container.Refresh")
	else: 
		if query == 'old':query=urlfetch.fetch(url).body
		items = re.findall('<div.+href="(.+?)".+title="(.+?)".*\s*.*\s*.*\s*<div class="pull-left file_size align-right">(.+?)</div>',query)
		for href,name,size in items:
			addir(name,href.replace('http:','https:'),resource+'/fshare.png',mode=2)	
	return ''
	
def play_url(url):
	hd['Cookie'] = loginfshare()
	response = urlfetch.get(url, headers=hd, follow_redirects=False)
	if response.status==302: url=response.headers['location']
	elif response.status==200:
		data=re.search('<span class="glyphicon glyphicon-remove"><.+b>(.+?)</b></h3>',response.text)
		if data:mess(data.group(1));return 'fail'
		fs_csrf=re.search("speed: (.+?).\s+fs_csrf: '(.+?)'",response.body)
		if fs_csrf:
			data={'speed':'fast','fs_csrf':fs_csrf.group(2)}
			href='https://www.fshare.vn/download/index';data=urllib.urlencode(data)
			try:dlink=urlfetch.post(href,headers=hd,data=data,follow_redirects=False).json['url'].encode('utf-8')
			except:dlink='pass'
		else:dlink=='fail'
		if dlink=='pass' and "form-control pwd_input" in response.body: 
			pw = get_input('Hãy nhập mật khẩu của file này')
			if pw is None or pw=='':mess(u'Không get được max speed link!');return 'fail'
			data=urllib.urlencode({'fs_csrf':fs_csrf.group(2),'FilePwdForm[pwd]':pw})
			response=urlfetch.post(url,headers=hd,data=data,follow_redirects=False)
			if response.status == 302: url = response.headers['location']
			else:
				data={'speed':'fast','fs_csrf':fs_csrf.group(2)}
				href='https://www.fshare.vn/download/index';data=urllib.urlencode(data)
				try:url=urlfetch.post(href,headers=hd,data=data,follow_redirects=False).json['url'].encode('utf-8')
				except:url='fail'
		else:url=dlink
	if myaddon.getSetting('logoutf')=="true":
		try:urlfetch.get("https://www.fshare.vn/logout",headers=hd,follow_redirects=False)
		except:print "Logout fail"
	if os.path.splitext(url)[1][1:].lower() not in media_ext:mess('sorry! this is not a media file');return 'fail'
	if url=='fail':mess(u'Không get được Fshare maxspeed direct link!');return 'no'
	item = xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	return ''
	
def addir(name,link,img='',mode=0,query='',isFolder=False):
	ok=True
	item = xbmcgui.ListItem(name,iconImage=img,thumbnailImage=img)
	if query=='ContextMenu':
		query='old'
		command='RunPlugin(plugin://%s/?mode%d&url=%s&query=del_id)'%(myaddon.getAddonInfo('id'),1,link)
		command=[('[COLOR orangered]Xóa mục này[/COLOR]',command)]
		item.addContextMenuItems(command)
	infoLabels = {'title':name,'studio': myaddon.getAddonInfo('name')}
	item.setInfo('Video', infoLabels)
	u=sys.argv[0]+"?url="+urllib.quote_plus(link)+"&img="+urllib.quote_plus(img)+"&mode="+str(mode)+"&query="+query+"&name="+name
	if not isFolder:item.setProperty('IsPlayable', 'true')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=isFolder)
	return ok

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param

xbmcplugin.setContent(int(sys.argv[1]), 'movies')
params=get_params()
url=name=img=query=mode=end=''

try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:img=urllib.unquote_plus(params["img"])
except:pass
try:query=urllib.unquote_plus(params["query"])
except:pass
try:mode=int(params["mode"])
except:pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "query: "+str(query)

if mode=='' or mode==1 :end=main(url,query)
elif mode==2:end=play_url(url)
elif mode==3:myaddon.openSettings();end='ok'
if end == '':xbmcplugin.endOfDirectory(int(sys.argv[1]))