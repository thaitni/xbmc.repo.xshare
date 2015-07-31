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
hd={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81'}
media_ext=['aif','iff','m3u','m4a','mid','mp3','mpa','ra','wav','wma','3g2','3gp','asf','asx','avi','flv','mov','mp4','mpg','mkv','m4v','rm','swf','vob','wmv','bin','cue','dmg','iso','mdf','toast','vcd','ts','flac','m2ts']
icon={'icon':resource+'icon.png','fshare':resource+'fshare.png'}

def mess(message, timeShown=5000):
	notification=u'XBMC.Notification(%s,%s,%s,%s)'%('Xshare',message,timeShown,icon['icon'])
	xbmc.executebuiltin(notification.encode("utf-8"))

def xshare_group(object,group):
	return object.group(group) if object else ''

def get_input(title=u"", default=u""):
	result = ''
	keyboard = xbmc.Keyboard(default, title)
	keyboard.doModal()
	if keyboard.isConfirmed():
		result = keyboard.getText()
	return result
	
def make_request(url,headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'},resp='b'):
	try:
		response = urlfetch.get(url,headers=headers)
		if resp=='o':resp=response
		else:
			if resp=='j':resp=response.json
			elif resp=='s':resp=response.status
			else:resp=response.body
			response.close()
		return resp
	except: mess('Make Request Error')
	return resp

def makerequest(file,string='',attr='r'):
	if attr=='r':
		try:f=open(file);body=f.read();f.close()
		except:mess(u'Lỗi đọc file: %s'%os.path.basename(file));body=''
	else:
		try:f=open(file,attr);f.write(string);f.close();body=string
		except:mess(u'Lỗi ghi file: %s'%os.path.basename(file));body=''
	return body

def loginfshare():
	url = "https://www.fshare.vn/login";response=make_request(url,resp='o')
	if not response:mess(u'Lỗi kết nối Fshare.vn');return ''
	fs_csrf=xshare_group(re.search('value="(.+?)".*name="fs_csrf',response.body),1)
	hd['Cookie']=response.cookiestring;response.close()
	form_fields = {
		"LoginForm[email]": myaddon.getSetting('username'), 
		"LoginForm[password]": myaddon.getSetting('password'),"LoginForm[rememberMe]": "0",
		"fs_csrf":fs_csrf}
	response=urlfetch.post(url=url,headers=hd,data=urllib.urlencode(form_fields))
	if response and response.status==302:
		f=response.cookiestring;mess(u'[COLOR gold]Login Fshare.vn thành công[/COLOR]',timeShown=100)
	else:mess(u'[COLOR red]Login Fshare.vn thất bại[/COLOR]');f=''
	return f
	
def check_id_fshare(id):
	url='https://www.fshare.vn/folder/%s'%os.path.basename(id).upper()
	body=make_request(url,resp='o')
	if body.status!=200:url=url.replace('folder','file');body=make_request(url,resp='o')
	return url,body.body

def main(url='',query=''):#mode=1
	datafile=datapath+'xshare.xml'
	if query=='':
		addir('[COLOR gold]Nhập Fshare ID mới[/COLOR]','',icon['icon'],mode=1,query='new',isFolder=True)
		if not os.path.isfile(datafile):makerequest(datafile,'<?xml version="1.0" encoding="utf-8">\n','w')
		for href,name in re.findall('<a href="(.+?)">(.+?)</a>',makerequest(datafile)): 
			if '/file/' in href:addir(name,href,icon['fshare'],mode=2,query='ContextMenu')
			else:addir('[COLOR gold]'+name+'[/COLOR]',href,icon['fshare'],mode=1,query='ContextMenu',isFolder=True)
	elif query == 'new': #Nhập ID mới
		id = get_input('Hãy nhập ID phim của Fshare').strip()
		if not id:return 'no'
		if len(id)<10:mess(u'Bạn nhập ID link chưa đúng: '+id);return 'no'
		url,body=check_id_fshare(id)
		name=xshare_group(re.search('<title>Fshare - (.+?)</title>',body),1)
		if not name:name=url
		makerequest(datafile,'<a href="%s">%s</a>\n'%(url,name),'a')
		if '/file/' in url:addir(name,url,icon['fshare'],mode=2)
		else:return main(url,body)
	elif query == 'del_id':
		f=open(datafile);body=re.sub('<a href="%s">.+?</a>\n'%url,'',f.read());f.close()
		try:f=open(datafile,'w');f.write(body);f.close();mess(u'Đã xóa mục %s'%url)
		except:mess(u'Chưa xóa được mục %s'%url)
		xbmc.executebuiltin("Container.Refresh")
	else: 
		if query=='old':query=make_request(url)
		r='<div.+href="(.+?)".+title="(.+?)".*\s*.*\s*.*\s*<div class="pull-left file_size align-right">(.+?)</div>'
		for href,name,size in re.findall(r,query):
			addir(name,href.replace('http:','https:'),icon['fshare'],mode=2)	
	return ''
	
def play_url(url):
	hd['Cookie']=loginfshare();response=make_request(url,hd,'o')
	if response.status==302:direct_link=response.headers['location']
	elif response.status==200:
		fs_csrf=xshare_group(re.search('value="(.+?)" name="fs_csrf"',response.body),1);pw=''
		if re.search('id="DownloadForm_pwd" type="password"',response.body):
			pw=get_input(u'Hãy nhập: Mật khẩu tập tin')
			if pw is None or pw=='':mess(u'Bạn đã không nhập password!');return 'fail'
		data={'fs_csrf':fs_csrf,'DownloadForm[pwd]':pw,'ajax':'download-form'};hd['referer']=url
		resp=urlfetch.post(url='https://www.fshare.vn/download/get',headers=hd,data=urllib.urlencode(data))
		try:
			if 'url' in resp.json.keys():direct_link=resp.json['url'].encode('utf-8')
			else:
				retry=1;direct_link='fail'
				while retry<4:
					mess(u'[COLOR red]Đang cố gắng get link lại lần %d[/COLOR]'%retry)
					xbmc.sleep(2000);response=make_request(url,hd,'o')
					if response.status==302:direct_link=response.headers['location']
					else:retry+=1
				string=resp.json.items()[0][1] if len(resp.json.items()[0][1])>1 else resp.json.items()[0][1][0]
				if direct_link=='fail':mess(string)
		except:mess("Get link that bai");direct_link='fail'
	else:mess(u'[COLOR red]Get link that bai[/COLOR]');direct_link='fail'
	if myaddon.getSetting('logoutf')=="true":make_request("https://www.fshare.vn/logout",hd)
	if direct_link=='fail':return 'fail'
	if os.path.splitext(direct_link)[1][1:].lower() not in media_ext:mess('sorry! this is not a media file');return 'fail'
	item = xbmcgui.ListItem(path=direct_link)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,item)
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
if end == '':xbmcplugin.endOfDirectory(int(sys.argv[1]))