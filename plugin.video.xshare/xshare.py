# -*- coding: utf-8 -*-
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,urllib,re,os,unicodedata,datetime,random,json

myaddon=xbmcaddon.Addon()
home=xbmc.translatePath(myaddon.getAddonInfo('path'))
datapath=xbmc.translatePath(os.path.join( xbmc.translatePath(myaddon.getAddonInfo('profile')),'data'))
iconpath=xbmc.translatePath(os.path.join( xbmc.translatePath(myaddon.getAddonInfo('profile')),'icon'))
sys.path.append(os.path.join(home,'resources','lib'));import urlfetch

search_file=os.path.join(datapath,"search.xml");data_path=os.path.join(home,'resources','data')

myfolder= myaddon.getSetting('thumuccucbo').decode('utf-8');copyxml=myaddon.getSetting('copyxml')
if not os.path.exists(myfolder):myfolder=os.path.join(datapath,'myfolder')
subsfolder=os.path.join(myfolder,'subs');tempfolder=os.path.join(myfolder,'temp')
rows=int(myaddon.getSetting('sodonghienthi'))
googlesearch=myaddon.getSetting('googlesearch')
thumucrieng='https://www.fshare.vn/folder/'+myaddon.getSetting('thumucrieng').upper()

media_ext=['aif','iff','m3u','m4a','mid','mp3','mpa','ra','wav','wma','3g2','3gp','asf','asx','avi','flv','mov','mp4','mpg','mkv','m4v','rm','swf','vob','wmv','bin','cue','dmg','iso','mdf','toast','vcd','ts','flac']
color={'fshare':'[COLOR gold]','vaphim':'[COLOR gold]','phimfshare':'[COLOR khaki]','4share':'[COLOR blue]','tenlua':'[COLOR fuchsia]','fptplay':'[COLOR orange]','trangtiep':'[COLOR lime]','search':'[COLOR lime]','ifile':'[COLOR blue]','hdvietnam':'[COLOR crimson]','xshare':'[COLOR blue]','subscene':'[COLOR green]','megabox':'[COLOR orangered]','dangcaphd':'[COLOR yellow]'};icon={}
for hd in ['xshare','4share', 'dangcaphd', 'downsub', 'favorite', 'fptplay', 'fshare', 'gsearch', 'hdvietnam', 'icon', 'id', 'ifiletv', 'isearch', 'khophim', 'maxspeed', 'megabox', 'movie', 'msearch', 'myfolder', 'myfshare', 'phimfs', 'serverphimkhac', 'setting', 'tenlua', 'vaphim']:
	icon.setdefault(hd,os.path.join(iconpath,'%s.png'%hd))
hd = {'User-Agent' : 'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}

def mess(message, timeShown=5000,title=''):
	xbmc.executebuiltin((u'XBMC.Notification(%s,%s,%s,%s)'%('Xshare [COLOR green]%s[/COLOR]'%title,message,timeShown,icon['icon'])).encode("utf-8"))

def mess_yesno(title='[COLOR green]Xshare[/COLOR]', line1='', line2=''):
	dialog=xbmcgui.Dialog()#dialog.yesno(heading, line1[, line2, line3,nolabel,yeslabel])
	return dialog.yesno(title,line1,line2)

def no_accent(s):
	s=re.sub(u'Đ','D',str2u(s));s=re.sub(u'đ','d',s)
	return unicodedata.normalize('NFKD', unicode(s)).encode('ASCII', 'ignore')

def str2u(s):
	if type(s)==str:
		try:s=s.decode('utf-8','ignore')
		except:pass
	return s

def joinpath(p1,p2):
	try:p=os.path.join(p1,p2)
	except:p=os.path.join(p1,str2u(p2))
	return p

def init_file():
	if not os.path.exists(xbmc.translatePath(myaddon.getAddonInfo('profile'))):
		os.mkdir(xbmc.translatePath(myaddon.getAddonInfo('profile')))
	for i in (datapath,iconpath,myfolder,subsfolder,tempfolder):
		if not os.path.exists(i):os.mkdir(i)
	xmlheader='<?xml version="1.0" encoding="utf-8">\n';p=datapath;q=myfolder
	for i in [(p,'search.xml'),(p,'hdvietnam.xml'),(p,'favourites.xml'),(q,'mylist.xml')]:
		if not os.path.isfile(joinpath(i[0],i[1])):
			if not makerequest(joinpath(i[0],i[1]),string=xmlheader,attr='w'):
				mess(u'Không tạo được file %s'%str2u(i[1]))

def xshare_group(object,group):
	return object.group(group) if object else ''

def delete_files(folder,mark='',temp='ok'):
	for file in os.listdir(folder):
		if os.path.isfile(joinpath(folder,file)) and (not mark or mark in file):
			try:os.remove(joinpath(folder,file))
			except:temp='';pass
	return temp

def endxbmc():xbmcplugin.endOfDirectory(int(sys.argv[1]))

def xbmcsetResolvedUrl(url,name=''):
	item=xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item);endxbmc()
	if myaddon.getSetting('autoload_sub')=='true':
		if name:url=name
		urltitle=urllib.unquote(os.path.splitext(os.path.basename(url))[0]).lower()
		urltitle='.'+'.'.join(s for s in re.sub('_|\W+',' ',re.split('\d\d\d\d',urltitle)[0]).split())+'.'
		subfile='';items=[]
		for file in os.listdir(subsfolder):
			filefullpath=joinpath(subsfolder,file).encode('utf-8')
			filename=re.sub('vie\.|eng\.','',os.path.splitext(file)[0].lower().encode('utf-8'))
			filename=re.split('\d\d\d\d',filename)[0];count=0
			for word in re.sub('_|\W+',' ',filename).split():
				if '.%s.'%word in urltitle:count+=1
			if count:items.append((count,filefullpath))
		for item in items:
			if item[0]>=count:count=item[0];subfile=item[1]
		if subfile:
			xbmc.sleep(1000);xbmc.Player().setSubtitles(subfile)
			mess(u'[B][COLOR green]%s[/B][/COLOR]'%str2u(os.path.basename(subfile)),20000,'Auto load sub')

def addir(name,link,img='',fanart='',mode=0,page=0,query='',isFolder=False):
	ok=True;name=re.sub(',|\|.*\||\||\<.*\>','',name)
	item=xbmcgui.ListItem(name,iconImage=img,thumbnailImage=img)
	query=menuContext(name,link,img,fanart,mode,query,item)
	item.setInfo(type="Video", infoLabels={"title":name})
	item.setProperty('Fanart_Image',fanart)
	u=sys.argv[0]+"?url="+urllib.quote_plus(link)+"&img="+urllib.quote_plus(img)+"&fanart="+urllib.quote_plus(fanart)+"&mode="+str(mode)+"&page="+str(page)+"&query="+query+"&name="+name
	if not isFolder:item.setProperty('IsPlayable', 'true')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=isFolder)
	return ok

def addirs(name,href,img='',fanart='',query=''):
	name=clean_string(name)
	if '18+' in name and myaddon.getSetting('phim18')=="false":return
	if not fanart and iconpath not in img:fanart=img
	if 'xml' in query:
		if name=='mylist.xml':name=color['subscene']+name+'[/COLOR]'
		query=query.replace('xml','');name='%sList xml[/COLOR]-%s'%(color['fptplay'],name)
		addir(name,href,img,fanart,mode=97,query=query,isFolder=True)
	elif query=='file':addir(name,href,img=icon['icon'],mode=96,query=query,isFolder=True)
	elif 'www.fshare.vn/file' in href:
		if str2u('phụ đề việt') in str2u(name).lower():
			name=color['fshare']+'Phụ đề Việt[/COLOR]-%s'%name
			addir(name,href,img,fanart,mode=3,query=query,isFolder=True)
		else:addir(color['fshare']+'Fshare[/COLOR]-%s'%name,href,img,fanart,mode=3,query=query)
	elif 'www.fshare.vn/folder' in href:
		if str2u('Mục chia sẻ của') in str2u(name):name=color['trangtiep']+name+'[/COLOR]'
		else:name=color['fshare']+name+'[/COLOR]'
		addir(name,href,img,fanart,mode=90,query=query,isFolder=True)
	elif '4share.vn/d/' in href:
		addir(color['4share']+name+'[/COLOR]',href,img,fanart,mode=38,query=query,isFolder=True)
	elif '4share.vn' in href:
		addir(color['4share']+'4share[/COLOR]-%s'%name,href,img,fanart,mode=3,query=query)
	elif 'tenlua.vn/fm/folder/' in href or '#download' in href:
		addir(color['tenlua']+name+'[/COLOR]',href,img,fanart,mode=95,query=query,isFolder=True)
	elif 'tenlua.vn' in href:
		addir(color['tenlua']+'TenLua[/COLOR]-%s'%name,href,img,fanart,mode=3,query=query)
	elif 'subscene.com' in href:
		addir(color['subscene']+'Subscene[/COLOR]-%s'%name,href,img,fanart,mode=94,query='download',isFolder=True)
	elif 'http://pubvn.' in href:
		addir(color['4share']+name+'[/COLOR]',href,img,fanart,mode=38,query=query,isFolder=True)
	elif 'http://vuahd.tv' in href:
		addir(color['vuahd']+name+'[/COLOR]',href,img,fanart,mode=38,query=query,isFolder=True)

def menuContext(name,link,img,fanart,mode,query,item):
	if query.split('?')[0]=='Search':
		query=query.split('?')[1]
		item.addContextMenuItems(searchContext(name,link,img,fanart,mode))
	elif query.split('?')[0]=='ID':
		query=query.split('?')[1]
		command=searchContext(name,link,img,fanart,15)
		command+=favouritesContext(name,link,img,fanart,mode)
		item.addContextMenuItems(command)
	elif 'fshare.vn' in link or '4share.vn' in link or 'tenlua.vn' in link:#mode in (3,38,90,95):
		item.addContextMenuItems(favouritesContext(name,link,img,fanart,mode))
	elif myfolder in str2u(link):
		item.addContextMenuItems(make_myFile(name,link,img,fanart,mode,query))
	return query

def makeContext(name,link,img,fanart,mode,query):
	make=query.split()[0]
	if make=='Rename':colo=color['fshare']
	elif make=='Remove':colo=color['hdvietnam']
	else:colo=color['trangtiep']
	context=colo+query+'[/COLOR]'
	p=(myaddon.getAddonInfo('id'),mode,name,link,img,fanart,make)
	cmd='RunPlugin(plugin://%s/?mode=%d&name=%s&url=%s&img=%s&fanart=%s&query=%s)'%(p)
	return context,cmd

def searchContext(name,link,img,fanart,mode):
	command=[(makeContext(name,link,img,fanart,9,'Rename item'))]
	command.append((makeContext(name,link,img,fanart,9,'Remove item')))
	return command

def favouritesContext(name,link,img,fanart,mode):
	command=[];
	if type(link)==unicode:link=link.encode('utf-8')
	if link in makerequest(joinpath(datapath,"favourites.xml")):
		command.append((makeContext(name,link,img,fanart,98,'Rename in MyFavourites')))
		command.append((makeContext(name,link,img,fanart,98,'Remove from MyFavourites')))
	else:
		command.append((makeContext(name,link,img,fanart,98,'Add to MyFavourites')))
	if 'www.fshare.vn' in link:
		if query=='MyFshare':
			command.append((makeContext(name,link,img,fanart,11,'Remove from MyFshare')))
			command.append((makeContext(name,link,img,fanart,11,'Rename from MyFshare')))
		else:
			command.append((makeContext(name,link,img,fanart,11,'Add to MyFshare')))
	if link in makerequest(joinpath(myfolder,'mylist.xml')):
		command.append((makeContext(name,link,img,fanart,12,'Rename in Mylist.xml')))
		command.append((makeContext(name,link,img,fanart,12,'Remove from Mylist.xml')))
	else:
		command.append((makeContext(name,link,img,fanart,12,'Add to Mylist.xml')))
	command.append((makeContext(name,'addstring.xshare.vn',img,fanart,13,'Add item name to string search')))
	return command

def make_myFile(name,link,img,fanart,mode,query):
	name=re.sub('\[COLOR.{,12}\]|\[/COLOR\]|Fshare|4share|TenLua|List xml|-|:|"','',name).strip();command=[]
	if os.path.isfile(str2u(link)):
		command.append((makeContext(name,link,img,fanart,11,'Upload to MyFshare')));temp='file'
	else:temp='folder'
	command.append((makeContext(name,link,img,fanart,96,'Rename this %s'%temp)))
	command.append((makeContext(name,link,img,fanart,96,'Remove this %s'%temp)))
	return command

def make_mySearch(name,url,img,fanart,mode,query):
	attr='w';body=makerequest(search_file);r='<a href="%s">.+?</a>\n'%url
	if query=='Rename':
		string=get_input('Nhập chuổi mới',re.sub('\[.*\]-','',name)).strip()
		if not string or string==re.sub('\[.*\]-','',name):return
		string=' '.join(s for s in re.split(' |\.|\'|"\?',string));r1='<a href="%s">%s</a>\n'%(url,string)
		body=re.sub(r,r1,body) if re.search('http.?://',url) else body.replace(name,string)
	elif query=='Remove':
		body=re.sub(r,'',body) if re.search('http.?://',url) else re.sub('<a>%s</a>\n'%name,'',body)
	elif query=='Add':
		if not re.search(url,body):body='<a href="%s">%s</a>\n'%(url,name);attr='a'
		else:return
	elif query=='Input':
		query = get_input('Nhập chuổi tên phim cần tìm trên %s'%url);attr='a'
		if query:
			query = ' '.join(s for s in query.replace('"',"'").replace('?','').split() if s!='')
			if not re.search(query,body):body='<a>%s</a>\n'%query
			else:return query
		else:return ''
	elif query=='get':
		srv=url.split('.')[0];site='Google ' if mode==2 else ''
		name=color['search']+'%sSearch[/COLOR] trên %s%s: [/COLOR]Nhập chuỗi tìm kiếm mới'%(site,color[srv],url)
		addir(name,url,icon[srv],mode=mode,page=1,query='INP',isFolder=True)
		if myaddon.getSetting('history')=='true':
			for string in re.findall('<a>(.+?)</a>',makerequest(search_file)):
				addir(string,url,icon[srv],query='Search?'+string,page=4,mode=mode,isFolder=True)
		return
	if makerequest(search_file,string=body,attr=attr):
		if attr=='w':mess(u'%s chuổi thành công'%str2u(query));xbmc.executebuiltin("Container.Refresh")
	elif attr=='w':mess(u'%s chuổi thất bại'%str2u(query))
	return query

def make_myFshare(name,url,img,fanart,mode,query):#11
	myFshare=myaddon.getSetting('thumucrieng')
	if not myFshare or (myFshare=='RDA4FHXVE2UU' and myaddon.getSetting('usernamef')!='thai@thanhthai.net'):
		mess(u'Hãy set "Thư mục chia sẻ của tôi trên Fshare"');return
	elif query=='Add':
		href='https://www.fshare.vn/api/fileops/createFolder'
		title=xshare_group(re.search('(\w{10,20})',url),1)
		if title:
			title+=' %s'%re.sub('\[COLOR.{,12}\]|\[/COLOR\]|Fshare|4share|TenLua|List xml|-|:|"','',name)
			title=re.sub('.xml.*','.xml',title).replace('[','').replace(']','')
		else:mess(u'Nhận dạng link bị lỗi');return
	elif query=='Rename':
		href='https://www.fshare.vn/api/fileops/rename'
		body=make_request('https://www.fshare.vn/folder/%s'%myFshare)
		title=re.sub('\[COLOR.{,12}\]|\[/COLOR\]|Fshare|4share|TenLua|List xml|-|:|"','',name)
		id=re.search('data-id="(.+?)".*>(.*%s.*)</a></div>'%title,body)
		if id:old_name=id.group(2);id=id.group(1)
		else:return
		new_name=get_input('Sửa tên 1 mục trong MyFshare',title).strip()
		if not new_name or new_name==title:return
		else:new_name=re.sub(title,new_name,old_name)
	elif query=='Remove':
		href='https://www.fshare.vn/api/fileops/delete'
		id=os.path.basename(url);folder=False
		body=make_request('https://www.fshare.vn/folder/%s'%myFshare)
		for data_id,data_type,data_path in re.findall('data-id="(.+?)" data-type="(.+?)" data-path="(.+?)"',body):
			if data_id==id and data_type=='folder':folder=True;break
			elif id in data_path:id=data_id;break
		if folder:
			line1='Thư mục: %s'%name
			line2='Có thể có dữ liệu quan trọng của bạn! %sBạn muốn xóa không?[/COLOR]'%color['tenlua']
			traloi=mess_yesno('Xshare - Cảnh báo nguy hiểm!',line1,line2)
			if traloi==0:mess(u'OK ! xshare chưa làm gì cả!'); return
	elif query=='Upload':
		href='https://www.fshare.vn/api/session/upload'
		try:size=os.path.getsize(str2u(url))
		except:pass
		if size>10**7:mess(u'Add-on chưa hỗ trợ upload file>10MB');return
		try:f=open(str2u(url),'rb');content=f.read();f.close()
		except:mess(u'Không đọc được file %s'%str2u(url));return
	
	hd['Cookie']=loginfshare()
	if not hd['Cookie']:return
	body=make_request('https://www.fshare.vn/home', headers=hd)
	token=xshare_group(re.search('data-token="(.+?)"',body),1)
	if query=='Add':
		data='{"token":"%s","name":"%s","in_dir":"%s"}'%(token,title,myaddon.getSetting('thumucrieng'))
		noti='Add to MyFshare'
	elif query=='Rename':
		data='{"token":"%s","new_name":"%s","file":"%s"}'%(token,new_name,id);noti='Rename in MyFshare'
	elif query=='Remove':data='{"token":"%s","items":["%s"]}'%(token,id);noti='Remove from MyFshare'
	elif query=='Upload':
		SESSID=hd['Cookie'].split('=')[1]
		name=re.sub('\[COLOR.{,12}\]|\[/COLOR\]|Fshare|4share|TenLua|List xml|-|:|"','',os.path.basename(url))
		path=xshare_group(re.search('data-id="%s" path-origin = "" data-path="(.+?)"'%myFshare,body),1)
		data='{"SESSID":"%s","name":"%s","size":"%s","path":"%s","token":"%s","secured":1}'%(SESSID,name,size,path,token)
		response=make_post(href,hd,data)
		if response and response.status==200:
			href=response.json['location'];data=content;noti='Upload to MyFshare'
		else:mess(u'Không lấy được link upload');return
	
	response=make_post(href,hd,data);logout_site(hd['Cookie'],'https://www.fshare.vn/logout')
	if response and response.status==200:
		mess(u'%s thành công'%noti)
		if query!='Add' and query!='Upload':xbmc.executebuiltin("Container.Refresh");mess(u'Đang reload list')
	else:mess(u'%s không thành công'%noti)
	return

def make_favourites(name,url,img,fanart,mode,query):
	favourites=joinpath(datapath,"favourites.xml")
	name=re.sub('\[COLOR.{,12}\]|\[/COLOR\]|Fshare|4share|TenLua|List xml|-|:|"','',name).strip()
	if query=='Add':
		if url.strip() in makerequest(favourites):mess(u'Mục này đã có trong MyFavourites');return
		if img==fanart:fanart=''
		string='<a href="%s" img="%s" fanart="%s">%s</a>\n'%(url.strip(),img,fanart,name)
		if makerequest(favourites,string=string,attr='a'):mess(u'Đã thêm 1 mục vào MyFavourites')
		else:mess(u'Thêm 1 mục vào xshare favourites thất bại')
	elif query=='Rename':
		title = get_input('Sửa tên trong mục MyFavourites',name).strip()
		if not title or title==name:return 'no'
		body=makerequest(favourites)
		string=re.search('((<a href="%s" img=".*?" fanart=".*?">).+?</a>)'%(url),body)
		if string:
			body=body.replace(xshare_group(string,1),xshare_group(string,2)+title+'</a>')
			if makerequest(favourites,string=body,attr='w'):
				mess(u'Đã sửa 1 mục trong MyFavourites')
				xbmc.executebuiltin("Container.Refresh")
			else:mess(u'Sửa 1 mục trong MyFavourites thất bại')
		else:mess(u'Sửa 1 mục trong MyFavourites thất bại')
	elif query=='Remove':
		body=makerequest(favourites)
		string=re.search('(<a href="%s" img=".*?" fanart=".*?">.+?</a>)'%(url),body)
		if string:
			body=body.replace(xshare_group(string,1)+'\n','')
			if makerequest(favourites,string=body,attr='w'):
				mess(u'Đã xóa 1 mục trong xshare favourites')
				xbmc.executebuiltin("Container.Refresh")
			else:mess(u'Xóa 1 mục trong xshare favourites thất bại')
		else:mess(u'Xóa 1 mục trong xshare favourites thất bại')
	else:
		items=re.findall('<a href="(.+?)" img="(.*?)" fanart="(.*?)">(.+?)</a>',makerequest(favourites))
		for href,img,fanart,name in items:addirs(name,href,img,fanart)
	return

def make_mylist(name,url,img,fanart,mode,query):
	mylist=joinpath(myfolder,'mylist.xml')
	name=re.sub('\[COLOR.{,12}\]|\[/COLOR\]|Fshare|4share|TenLua|List xml|-|:|"','',name).strip()
	if query=='Add':
		if url.strip() in makerequest(mylist):mess(u'Mục này đã có trong MyList');return
		if img==fanart:fanart=''
		string='<a href="%s" img="%s" fanart="%s">%s</a>\n'%(url.strip(),img,fanart,name)
		if makerequest(mylist,string=string,attr='a'):mess(u'Đã thêm 1 mục vào mylist.xml')
		else:mess(u'Thêm vào mylist.xml thất bại')
	elif query=='Rename':
		title = get_input('Sửa tên 1 mục trong mylist.xml',name)
		if not title or title==name:return 'no'
		string1='<a href="%s" img=".*?" fanart=".*?">.+?</a>'%url
		string2='<a href="%s" img=".*?" fanart=".*?">%s</a>'%(url,title)
		body=re.sub(string1,string2,makerequest(mylist))
		if makerequest(mylist,string=body,attr='w'):
			mess(u'Đã sửa 1 mục trong mylist.xml');xbmc.executebuiltin("Container.Refresh")
		else:mess(u'Sửa 1 mục trong mylist.xml thất bại')
	elif query=='Remove':
		string='<a href="%s" img=".*?" fanart=".*?">.+?</a>\n'%url
		body=re.sub(string,'',makerequest(mylist))
		if makerequest(mylist,string=body,attr='w'):
			mess(u'Đã xóa 1 mục trong mylist.xml');xbmc.executebuiltin("Container.Refresh")
		else:mess(u'Xóa 1 mục trong mylist.xml thất bại')
	return

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
	except: 
		mess(u'[COLOR red]Lỗi kết nối tới: %s[/COLOR]'%xshare_group(re.search('//(.+?)/',str2u(url)),1))
		print 'Make Request Error: %s'%url;resp=''
	return resp#unicode:body=response.text

def make_post(url,headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'},data=''):
	try:
		if data:response=urlfetch.post(url=url,headers=headers,data=data)
		else:response=urlfetch.post(url=url,headers=headers)
	except:mess(u'Không truy cập được %s'%str2u(url));response=''
	return response

def makerequest(file,string='',attr='r'):
	file=str2u(file)
	if attr=='r':
		try:f=open(file);body=f.read();f.close()
		except:mess(u'Lỗi đọc file: %s'%str2u(os.path.basename(file)));body=''
	else:
		try:f=open(file,attr);f.write(string);f.close();body=string
		except:mess(u'Lỗi ghi file: %s'%str2u(os.path.basename(file)));body=''
	return body

def rename_file(sf,df,kq='ok'):
	try:
		if os.path.isfile(df):os.remove(df)
		os.rename(sf,df)
	except:kq='';pass
	return kq

def download_subs(url):
	response=make_request(url,resp='o');downloaded=''
	if not response or response.status!=200:return
	if int(response.getheaders()[0][1])<10485760:#size<10MB
		if myaddon.getSetting('autodel_sub')=='true':delete_files(subsfolder)
		filename=urllib.unquote(os.path.basename(url));delete_files(tempfolder)
		subfile=joinpath(tempfolder,re.sub('\[.+?\]','',filename))
		if makerequest(subfile,string=response.body,attr="wb"):
			if 	response.body[0] in 'R-P':
				xbmc.sleep(500);f1=subfile.encode('utf-8');f2=tempfolder.encode('utf-8')
				xbmc.executebuiltin('XBMC.Extract("%s","%s")'%(f1,f2),True);os.remove(subfile)
				exts = [".srt", ".sub", ".txt", ".smi", ".ssa", ".ass"];sub_list=[]
				for file in os.listdir(tempfolder):
					tempfile=joinpath(tempfolder,file)
					if os.path.isfile(tempfile) and os.path.splitext(tempfile)[1] in exts:
						if re.search('vietname|vie',filename):
							if rename_file(tempfile,joinpath(subsfolder,'Vie.%s'%re.sub(',|"|\'','',file))):
								downloaded='ok'
						elif rename_file(tempfile,joinpath(subsfolder,re.sub(',|"|\'','',file))):downloaded='ok'
			elif rename_file(subfile,joinpath(subsfolder,'Vie.%s'%re.sub('\[.+?\]','',filename))):downloaded='ok'
		else:mess(u'Lỗi download sub')
		if downloaded:mess(u'Đã download sub vào Subsfolder')
	else:mess(u'Oh! Sorry. [COLOR red]Không chơi được file rar[/COLOR]')
	return downloaded

def get_input(title=u"", default=u""):
	result = ''
	keyboard = xbmc.Keyboard(default, title)
	keyboard.doModal()
	if keyboard.isConfirmed():
		result = keyboard.getText()
	return result

def tenlua_get_detail_and_starting(idf,headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}):
	data='[{"a":"filemanager_builddownload_getinfo","n":"%s","r":%s}]'%(idf,str(random.random()))
	response=make_post('https://api2.tenlua.vn/',headers,data)
	return response.json[0] if response else {'type':'none'}

def resolve_url(url,xml=False):
	if 'fshare.vn' in url.lower():url=url.replace('http:','https:');hd['Cookie']=loginfshare();srv='fshare.vn'
	elif '4share.vn' in url.lower():hd['Cookie']=login4share();srv='4share.vn'
	elif 'tenlua.vn' in url.lower():
		hd['Cookie'] = logintenlua();srv='tenlua.vn'
		idf=xshare_group(re.search('\w{14,20}',url),0)
		if not idf:idf=url.split('/download/')[1].split('/')[0]
		download_info=tenlua_get_detail_and_starting(idf,hd)
		if 'n' in download_info and os.path.splitext(download_info['n'])[1][1:].lower() not in media_ext:
			mess('sorry! this is not a media file');return 'fail'
		if 'dlink' in download_info:url=download_info['dlink']
		elif 'url' in download_info:url=download_info['url'];mess(u'Slowly direct link!')
		else:mess(u'Không get được max speed link!');return 'fail'
	cookie = hd['Cookie']
	response=make_request(url,headers=hd,resp='o')
	if not response:mess(u'Không kết nối được server %s'%srv);xbmc.sleep(500);logout_site(cookie,url);return 'fail'
	if response.status==302:direct_link=response.headers['location']
	elif response.status==200 and 'fshare.vn' in url.lower():direct_link=resolve_url_fshare200(url,response,hd)
	elif response.status==200 and '4share.vn' in url.lower():
		FileDownload=re.search("<a href='(http://.{3,5}4share.vn.+?)'> <h4>(.+?)</h4>",response.body)
		if FileDownload:direct_link=xshare_group(FileDownload,1);srv=xshare_group(FileDownload,2)
		else:direct_link='fail'
	else:direct_link='fail'
	logout_site(cookie,url)
	if direct_link=='fail':
		if 'fshare.vn' not in url.lower():mess(u'Không get được max speed direct link!')
		return 'fail'
	if xml:return direct_link
	if direct_link!='fail' and not check_media_ext(direct_link,srv):return 'fail'
	xbmcsetResolvedUrl(direct_link);return ''

def check_media_ext(direct_link,srv):
	check=True;message='sorry! this is not a media file'
	sub_ext=['rar','zip','srt','sub','txt','smi','ssa','ass','nfo']
	file_ext=os.path.splitext(direct_link)[1][1:].lower()
	if 'fshare.vn' in direct_link and file_ext not in media_ext:
		if file_ext in sub_ext:download_subs(direct_link)
		else:mess(message)
		check=False
	elif '4share.vn' in direct_link and os.path.splitext(srv)[1][1:].lower() not in media_ext:
		if os.path.splitext(srv)[1][1:].lower() in sub_ext:
			download_subs(direct_link)
		else:mess(message)
		check=False
	return check

def resolve_url_fshare200(url,response,hd):
	fs_csrf=xshare_group(re.search('value="(.+?)" name="fs_csrf"',response.body),1);pw=''
	if re.search('id="DownloadForm_pwd" type="password"',response.body):
		pw = get_input(u'Hãy nhập: Mật khẩu tập tin')
		if pw is None or pw=='':mess(u'Bạn đã không nhập password!');return 'fail'
	data={'fs_csrf':fs_csrf,'DownloadForm[pwd]':pw,'ajax':'download-form'};hd['referer']=url
	data=urllib.urlencode(data);resp=make_post('https://www.fshare.vn/download/get',hd,data)
	try:
		if 'url' in resp.json.keys():direct_link=resp.json['url'].encode('utf-8')
		else:
			retry=1
			while retry<4:
				mess(u'[COLOR red]Đang cố gắng get link lại lần %d[/COLOR]'%retry)
				xbmc.sleep(2000);resp=make_request(url,headers=hd,resp='o')
				if not resp:mess(u'Không kết nối được server %s'%srv);return 'fail'
				elif resp.status==302:direct_link=resp.headers['location'];return direct_link
				else:retry+=1
			string=resp.json.items()[0][1] if len(resp.json.items()[0][1])>1 else resp.json.items()[0][1][0]
			mess(string);direct_link='fail'
	except:
		if 'Lỗi 404' in xshare_group(re.search('<title>(.+?)</title>',response.body),1):
			mess(u'Tập tin quý khách yêu cầu không tồn tại')
		elif 'đang là thành viên thường' in response.body:mess(u'Quý khách hiện đang là thành viên thường')
		direct_link='fail'
	return direct_link

def logout_site(cookie,url):
	def logout(cookie,url,site):
		hd['Cookie']=cookie
		mess(u'Logout %s %sthành công'%(site,'' if make_request(url,hd,resp='s')==302 else u'không '))
	if cookie and myaddon.getSetting('logoutf')=="true":
		if 'fshare.vn' in url.lower():logout(cookie,'https://www.fshare.vn/logout','Fshare.vn')
		elif '4share.vn' in url.lower():logout(cookie,'http://4share.vn/default/index/logout','4share.vn')
		elif 'dangcaphd.com' in url.lower():logout(cookie,'http://dangcaphd.com/logout.html','dangcaphd.com')
		elif 'tenlua.vn' in url.lower():logouttenlua(cookie)

def loginfshare():
	url = "https://www.fshare.vn/login";response=make_request(url,resp='o')
	if not response:mess(u'Lỗi kết nối Fshare.vn');return ''
	fs_csrf=xshare_group(re.search('value="(.+?)".*name="fs_csrf',response.body),1)
	hd['Cookie']=response.cookiestring;response.close()
	form_fields = {
		"LoginForm[email]": myaddon.getSetting('usernamef'), 
		"LoginForm[password]": myaddon.getSetting('passwordf'),"LoginForm[rememberMe]": "0",
		"fs_csrf":fs_csrf}
	response=make_post(url,hd,urllib.urlencode(form_fields))
	if response and response.status==302:mess(u'Login Fshare.vn thành công',timeShown=100);f=response.cookiestring
	else:mess(u'Login Fshare.vn không thành công');f=''
	return f

def login4share(headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}):
	form_fields = {"username":myaddon.getSetting('username4'),"password":myaddon.getSetting('password4')}
	response=make_post('http://up.4share.vn/index/login',headers,urllib.urlencode(form_fields))
	if response and response.status==302:mess(u'Login 4share.vn thành công',timeShown=100);f=response.cookiestring
	else:mess(u'Login 4share.vn không thành công');f=''
	return f

def logintenlua(headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}):
	user=myaddon.getSetting('usernamet');pw=myaddon.getSetting('passwordt')
	data='[{"a":"user_login","user":"'+user+'","password":"'+pw+'","permanent":"true"}]'
	response=make_post('https://api2.tenlua.vn/',headers,data)
	if response and response.body!='[-1]':mess(u'Login tenlua.vn thành công');f=response.headers.get('set-cookie')
	else:mess(u'Login tenlua.vn không thành công');f=''
	return f

def logouttenlua(cookie):
	hd['Cookie']=cookie
	response=make_post('https://api2.tenlua.vn/',hd,'a=user_logout')
	if response:mess(u'Logout tenlua.vn thành công')
	else:mess(u"Logout tenlua.vn không thành công")

def loginhdvietnam(headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}):
	url='http://www.hdvietnam.com/diendan/login.php';
	user=myaddon.getSetting('usernameh');pw=myaddon.getSetting('passwordh')
	form_fields ={"vb_login_username":user,"vb_login_password":pw,"do":"login"}
	response=make_post(url,headers,urllib.urlencode(form_fields))
	if response and 'vbseo_loggedin=yes' in response.cookiestring:
		f=response.cookiestring;myaddon.setSetting('cookie',f)
	else:mess(u'Login hdvietnam.com không thành công');f=''
	return f

def trangtiep(query,items):
	if 'Trang' in query.split('?')[0]:
		trang=int(query.split('?')[0].split('Trang')[1])
		query=query.split('?')[1]
	else:trang=1
	del items[0:(trang-1)*rows]
	trang+=1
	return trang,query,items

def hdvn_get_link(url,fanart='',temp=[]):
	room=xshare_group(re.search('http://www.hdvietnam.com/diendan/(.+?)/',url),1)
	if not room or room not in ['150-thu-vien-link-phim','33-fshare-vn','271-web-dl-hdtv','324-bluray-remux','77-mhd-sd','78-bluray-nguyen-goc','311-tenlua-vn','315-web-dl-hdtv','316-mhd-sd','317-bluray-nguyen-goc','323-bluray-remux','65-megashare-vn','146-up-4share-vn','277-web-dl-hdtv','147-mhd-sd','265-phim-co-audio-viet','110-3d','116-phim-tai-lieu-documentaries','123-phim-hoat-hinh','57-phim-bo-series','157-phim-cho-ios-android']:return temp
	hd['Cookie']=myaddon.getSetting('cookie')
	body=make_request(url,headers=hd)
	bossroom=hdvn_boss_room(url,body)
	if not bossroom:return temp
	if myaddon.getSetting('hdvnfindall')=='false':
		if bossroom.lower() not in myaddon.getSetting('uploaders').lower().split('-'):return temp
	if 'post_thanks_separator' not in body and myaddon.getSetting('usernameh') not in body:
		hd['Cookie']=loginhdvietnam()
		body=make_request(url,headers=hd)
	title=xshare_group(re.search('<title>(.+?)</title>',body),1)
	if not title:return temp
	else:title=re.sub('\||\[.*\]|\(.*\)|\{.*\}|amp;','',title).strip()
	title='[%s] %s'%(bossroom,title);mess(url.split('/')[len(url.split('/'))-1],100)
	img=xshare_group(re.search('<a rel="nofollow" href="(.+?)" class="highslide"',body),1)
	pattern_link='(https?://www.fshare.vn/\w{4,6}/\w{10,14})'
	pattern_link+='|(http://4share.vn/./\w{14,20})|(https?://w?w?w?/?tenlua.vn/.*?)[ |"|<]'
	pattern_link+='|(http://subscene.com/subtitles/.+?)[ |"|\'|<]'
	items=re.findall(pattern_link,hdvn_body_thanked(body,hd,bossroom))
	for hrefs in items:
		for href in hrefs:
			if not href:continue
			href=correct_link(href)
			if not href or href in temp:continue
			temp.append(href);addirs(title,href,img,fanart)
	return temp

def hdvn_boss_room(url,body):
	if re.search('-\d{1,3}\.html',url):
		body=make_request(re.sub('-\d{1,3}\.html','.html',url))
	pattern='id="postcount\d{5,8}" name="1">.{,1000}line popupctrl.{40,55}/\d{4,10}-(.+?).html"'
	boss=re.search(pattern,body,re.DOTALL)
	return xshare_group(boss,1)

def hdvn_body_thanked(body,hd,bossroom):
	sec_token= xshare_group(re.search('name="securitytoken" value="(.{50,60})"',body),1)
	home='http://www.hdvietnam.com/diendan/';thanks_data=[];content=''
	pattern='id="postcount(\d{5,8})".{,1000}line popupctrl.{40,55}/\d{4,10}-(.+?)\.html'
	items=re.findall(pattern,body,re.DOTALL);dataremove='do=post_thanks_remove_user&using_ajax=1'
	if not items:return''
	for id_post,name in items:
		if name==bossroom:
			data='do=post_thanks_add&using_ajax=1&p=%s&securitytoken=%s'%(id_post,sec_token)
			make_post(home+'post_thanks.php',hd,data)
			data='do=whatever&p=%s&all=%s&securitytoken=%s'%(id_post,id_post,sec_token)
			content+=make_post(home+'showthread.php',hd,data).body
			if not re.search('return post_thanks_remove_user.%s'%id_post,body):
				thanks_data.append('%s&p=%s&securitytoken=%s'%(dataremove,id_post,sec_token))
	for data in thanks_data:make_post(home+'post_thanks.php',hd,data)
	return content

def hdvn_thank_xshare(hd):
	if myaddon.getSetting('usernameh')!='thaitni' and myaddon.getSetting('thank2xshare')=='true':
		temp=myaddon.getSetting('pagethanked').split('-');url='http://www.hdvietnam.com/diendan/229-android-box/'
		try:p=temp[0];p0=temp[1];p1=temp[2];room=temp[3]
		except:p=p0=p1=room='0'
		if p<'1':p='1'
		url0='997745-xshare-xbmc-hd-video-subtitles-fshare';url1='947935-xfshare-fshare-xbmc-xem-phim-tren'
		url=url+url0 if room=='0' else url+url1
		url=url+'.html' if p=='1' else url+'-'+p+'.html'
		response=make_request(url,headers=hd,resp='o')
		if response.status==301:
			if room=='0':myaddon.setSetting('pagethanked','%s-%s-%s-%s'%(p1,str(int(p)-1),p1,'1'))
			else:myaddon.setSetting('pagethanked','%s-%s-%s-%s'%(p0,p0,str(int(p)-1),'0'))
			return
		pattern='id="postcount(\d{5,8})".{,1000}line popupctrl.{40,55}/\d{4,10}-(.+?)\.html'
		sec_token= xshare_group(re.search('name="securitytoken" value="(.{50,60})"',response.body),1)
		if not sec_token:return
		for id,name in re.findall(pattern,response.body,re.DOTALL):
			if name=='thaitni':
				data='do=post_thanks_add&using_ajax=1&p=%s&securitytoken=%s'%(id,sec_token)
				make_post('http://www.hdvietnam.com/diendan/post_thanks.php',hd,data)
		myaddon.setSetting('pagethanked','%s-%s-%s-%s'%(str(int(p)+1),p0,p1,room))

def google_ifile(url,name,temp=[]):
	if 'http://ifile.tv/phim/' not in url:return temp
	mess(url,100)
	for url4share,fanart,name2,catalog in ifile_tv_4share(url):
		if not name2:name2=name
		if url4share not in temp:temp.append(url4share);addirs(name2,url4share,fanart,fanart)
	return temp

def google_vaphim(url,temp=[]):
	if url=='http://vaphim.com/':return temp
	elif '/tag/' in url:
		pattern='class="entry-title"><a href="(.+?)" rel="bookmark"'
		url=xshare_group(re.search(pattern,make_request(url)),1)
		if not url:return temp
	mess(url,100)
	for img,fanart,href,name in vp2fshare(url):
		if href not in temp:temp.append(href);addirs(name,href,img,fanart)
	return temp

def google_search_api(url,start,string,items):#url:fshare.vn,4share.vn,tenlua.vn,hdvietnam.com
	string_search = urllib.quote_plus('"%s"'%string)
	href = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=large&'
	href+='start=%s&q=site:%s+%s'%(start,url.lower(),string_search)
	json=make_request(href,resp='j')
	if not json:mess(u'Lỗi get %s'%str2u(href));return items,'end'
	if json['responseStatus']!=200:
		mess(u'Google: nghi ngờ lạm dụng Dịch vụ. Tự động chuyển sang web search',1000)
		return google_search_web(url,start+'xshare',string,items)
	data=json['responseData']
	if not data or not data['results']:mess(u'Không tìm được tên phim phù hợp');return items,'end'
	currentPage=int(data['cursor']['currentPageIndex'])+1;nextPage=0
	for i in data['results']:
		if 'tenlua' in url and re.search('\w{16,20}/(.*)\Z',i['url'].encode('utf-8')):
			name=xshare_group(re.search('\w{16,20}/(.*)\Z',i['url'].encode('utf-8')),1)
		else: name=i['titleNoFormatting'].encode('utf-8')
		name=re.sub('\||<.+?>|\[.*\]|\(.*\)','',name.split(':')[0]).strip()
		if name and 'Forum' not in name and 'server-nuoc-ngoai' not in i['url']:
			items.append((name,i['url'].encode('utf-8')))
	start=str(int(start)+8)
	if start not in ' '.join(s['start'] for s in data['cursor']['pages']):start='end'
	return items,start

def google_search(url,query,mode,page,items=[]):
	srv=url.split('.')[0]
	if page==0:make_mySearch('',url,'','',mode,'get')
	elif page==1:
		query=make_mySearch('',url,'','','','Input')
		return google_search(url,query,mode,page=4) if query else 'no'
	else:
		query=no_accent(query);tempurl=[];templink=[]
		if '?' in query:
			start=query.split('?')[1];query=query.split('?')[0]
		else:start='0'
		if googlesearch=='Web' or 'xshare' in start:items,start=google_search_web(url,start,query,items)
		else:items,start=google_search_api(url,start,query,items)
		if not items:return 'no'
		for name,link in sorted(items,key=lambda l:l[0]):
			if link in templink:continue
			if url=='hdvietnam.com':tempurl=hdvn_get_link(link,temp=tempurl)
			elif url=='vaphim.com':tempurl=google_vaphim(link,temp=tempurl)
			elif url=='ifile.tv':tempurl=google_ifile(link,name,temp=tempurl)
			elif url=='4share.vn' and 'docs.4share' not in link:tempurl=doc_Trang4share(link,temp=tempurl)
			else:addirs(name,link,icon[srv])
			templink.append(link)
		if start!='end':
			name=color['trangtiep']+'Trang tiep theo...trang %s[/COLOR]'%str(page-2)
			addir(name,url,icon[srv],mode=mode,query='%s?%s'%(query,start),page=page+1,isFolder=True)
	return ''

def google_search_web(url,start,query,items):
	num='20';google = 'https://www.google.com.vn/search?hl=vi&ie=utf-8&oe=utf-8&num=%s&'%num
	string_search = urllib.quote_plus('"%s"'%query);srv=url.split('.')[0]
	if 'xshare' in start:start=start.replace('xshare','');xshare='yes'
	else:xshare=''
	href=google+'start=%s&q=site:%s+%s'%(start,url.lower(),string_search)
	body=make_request(href)
	if '<TITLE>302 Moved</TITLE>' in body:
		mess(u'Google từ chối dịch vụ do bạn đã truy cập quá nhiều');return items,'end'
	links=re.findall('<a href="(.{,300})" onmousedown=".{,200}">(.{,200})</a></h3>',body)
	for link,name in links:items.append((name,link))
	start=str(int(start)+int(num))
	if 'start=%s'%start not in body:start='end'
	elif 'xshare':start=start+'xshare'
	return items,start

def open_category(query): #category.xml
	pattern='<a server="(...)" category="(.+?)" mode="(..)" color="(.*?)" icon="(.*?)">(.+?)</a>'
	items=re.findall(pattern,makerequest(joinpath(data_path,'category.xml')))
	for server,category,mode,colo,icon,name in items:
		if (server!=query) or (("18" in category) and (myaddon.getSetting('phim18')=="false")):continue
		if query=='VPH' and mode!='10':q='vaphim.xml'
		elif query=='IFI' and mode!='10':q='ifiletv.xml'
		else:q=category
		name='[COLOR '+colo+']'+name+'[/COLOR]';icon=joinpath(iconpath,icon)
		addir(name,category,icon,home+'/fanart.jpg',mode=int(mode),page=0,query=q,isFolder=(mode!='16'))

def main_menu(category,page,mode,query): #Doc list tu vaphim.xml hoac ifiletv.xml
	items = doc_xml(joinpath(datapath,query),para=category);pages=len(items)/rows+1
	del items[0:page*rows];count=0;down=len(items)
	for id,img,fanart,href,name in items:
		down-=1;addirs(name,href,img,fanart);count+=1
		if count>rows and down>10:break
	if down>10:
		page+=1;name=color['trangtiep']+'Trang tiep theo...trang %d/%d[/COLOR]'%(page+1,pages)
		addir(name,category,icon['icon'],mode=mode,page=page,query=query,isFolder=True)

def update_xml(items_new,items_old,filename): #update vaphim,ifiletv xml
	try:items = sorted(items_new+items_old,key=lambda l:int(l[1]),reverse=True)
	except:items = items_new+items_old
	content='<?xml version="1.0" encoding="utf-8">\n'
	for id_tip,id_htm,category,img,fanart,href,fullname in items:
		content+='<a id_tip="%s" id="%s" category="%s" img="%s" fanart="%s" href="%s">%s</a>\n'%(id_tip,id_htm,category,img,fanart,href,fullname)
	if makerequest(joinpath(datapath,filename),string=content,attr='w'):
		mess(u"Đã cập nhật được %d phim"%len(items_new))
	else: mess(u'Đã xảy ra lỗi cập nhật')
	return

def vp_update():
	items_old, id_old = read_items_old("vaphim.xml")
	mess(u'Đang kiểm tra dữ liệu cập nhật của Vaphim...')

	new_items = vaphim_page('http://vaphim.com/category/phim-2/');items_new=[];str_items_old=str(items_old)
	for id_tip,id_htm,category,href in new_items:
		if id_htm not in id_old:
			try:
				for img,fanart,href,fullname in vp2fshare(href): # vp2fshare:img,fanart,href,fullname
					if href not in str_items_old:
						fullname=' '.join(s for s in fullname.split())
						items_new.append((id_tip,id_htm,category,img,fanart,href,fullname))
			except:continue
	if items_new:update_xml(items_new,items_old,"vaphim.xml")
	else:mess(u'Không có phim mới...')
	return 'ok'

def vp_update_rss():
	items=rss_content('http://feed.vaphim.com/category/phim-2/feed/')
	id_old=re.findall('id="(\d{5})" category',makerequest(joinpath(datapath,"vaphim.xml")))
	category={'Phim Lẻ':'phim-le','Phim Bộ':'series','Phim Bộ Hàn':'korean-series','Phim Bộ Hồng Kông':'hongkong-series','Phim Bộ Mỹ':'us-tv-series','Phim Tài Liệu':'documentary','Phim 18+':'18','Hoạt Hình':'animation','Huyền Bí':'mystery','Viễn Tưởng':'sci-fi','3D':'3d','Cao Bồi':'western','Chiến Tranh':'war','Thiếu Nhi':'family','Hài Hước':'comedy','Hành Động':'action','Hình Sự':'crime','Rùng Rợn':'thriller','Tâm Lý':'drama','TVB':'tvb','Kinh Dị':'horror','Lãng Mạn':'romance','Lịch Sử':'history','Phiêu Lưu':'adventure','Thần Thoại':'fantasy','Thuyết Minh':'thuyet-minh-tieng-viet','Hồng Kông':'hongkong','Ấn Độ':'india','Việt Nam':'vietnamese','Hàn Quốc':'korean'}
	content_new=''
	pattern='(https?://www.fshare.vn/\w{4,6}/\w{10,14})" target="_blank">(.+?)</a>'
	for item in items:
		cate=''
		for i in item.findall('category'):
			if i.text.encode('utf-8') in category:
				cate+=category[i.text.encode('utf-8')]+' '
			else:break
		cate=cate.strip()
		idf=xshare_group(re.search('(\d{5})',item.findtext('guid')),1)
		if not idf or not cate or idf in id_old:continue
		
		name=item.findtext('title')
		content=item.findtext('contentencoded')
		img=re.findall('img src="(.+?jpg)["|?| ]',content)
		if len(img)>1:fanart=img[1];img=re.sub('-134x193','',img[0])
		elif len(img)>0:fanart=img=re.sub('-134x193','',img[0])
		else:fanart=img=''
		
		for link,title in re.findall(pattern,content):
			link=link.lower();idp=xshare_group(re.search('(\w{10,14})',link),1)
			if 'fshare.vn/file' in link:url='https://www.fshare.vn/file/%s'%idp.upper()
			else:url='https://www.fshare.vn/folder/%s'%idp.upper()
			content_new+='<a id_tip="" id="%s" category="%s" img="%s" fanart="%s" href="%s">%s</a>\n'%(idf,cate,img,fanart,url,name+' - '+title)
	if content_new:
		makerequest(joinpath(datapath,"vaphim.xml"),string=content_new.encode('utf-8'),attr='a')

def vaphim_page(url):
	body=make_request(url);items_new=[]
	if str('<h2>Search Results</h2>') in body:return []
	items=re.findall('<li class="post-(.+?)">\s*.*\s*<a data="(\d{,6})" title=.+href="(.+?)">',body)
	for category,ID,href in items:
		if ('game' not in category) and ('video' not in category) and ('phn-mm' not in category):
			category=' '.join([s[s.find('-')+1:] for s in category.rsplit(' ') if 'category' in s])
			items_new.append(('',ID,category,href))
	return items_new #vaphim_page1(url):'',ID,category,href

def clean_string(string):
	return ' '.join(s for s in re.sub('Fshare|-|4share|Tenlua|&.+?;','',string).split())

def vp2fshare(url):
	body = make_request(url);combs=[]
	category=xshare_group(re.search('<div id="post-(\d{,6})".*\s.*</strong><a(.*?)\d{,5}</div>',body),2)
	if not re.search('"http://vaphim.com/category/.{,8}[i|v].{,4}/.{,20}"',category):return combs
	if '<p><strong>' in body:#tuyen tap
		pattern='<strong>(.+?)</strong>|src="(.+)\?.{,10}"|(https?://www.fshare.vn/\w{4,6}/\w{10,14}).{,20}>(.+?)</a>'
		pattern+='|"(http://subscene.com/subtitles/.+?)"'
		body=body[body.find('<p><strong>'):]
		while '<div class="cf5_wpts_cl">' in body:
			temp=body[:body.find('<div class="cf5_wpts_cl">')]
			body=body[len(temp)+len('<div class="cf5_wpts_cl">'):]
			items=re.findall(pattern,temp)
			if len(items)>2:#ton tai link fshare
				title=re.sub('&#.* ','',items[0][0]).strip()+' - ' if items[0][0] else ''
				if items[1][1]:img=fanart=items[1][1]
				else:img=fanart=''
				nname=''
				for n,i,href,name,subs in items:
					if "fshare.vn" in href:combs.append((img,fanart,href.replace('http:','https:'),title+name))
					elif "subscene.com" in subs:combs.append((img,fanart,subs,title+nname))
					nname=name
	else:
		pattern='<title>(.+?)</title>|<meta itemprop="name" .?content="(.+?)"'
		pattern+='|<meta itemprop="image" .?content="(.+?)"|<div id="attachment.*"><img src="(.+?\.jpg).{,10}" '
		pattern+='|<img src="(.+jpg).{,10}".{,100}size-full'
		pattern+='|(https?://www.fshare.vn/\w{4,6}/\w{10,14}).{,20}>(.+?)</a>|"(http://subscene.com/subtitles/.+?)"'
		items=re.findall(pattern,body)
		if len(items)>4:#ton tai link fshare
			if items[1][1]:title=items[1][1]+' - '
			elif items[0][0]:title=items[0][0]+' - '
			else:title=''
			if items[2][2]:img=fanart=re.sub('-\d{,4}x\d{,5}','',items[2][2])
			elif items[3][3]:img=fanart=re.sub('-\d{,4}x\d{,5}','',items[3][3])
			else:img=fanart=''
			if items[4][4]:fanart=items[4][4]
			nname=''
			for t,n,i,f,im,href,name,subs in items:
				if "fshare.vn" in href:combs.append((img,fanart,href.replace('http:','https:'),title+name))
				elif "subscene.com" in subs:combs.append((img,fanart,subs,title+nname))
				nname=name
	return combs #(img,fanart,href,fullname)

def vp_phimmoi():
	txtfile=joinpath(data_path,'vaphim_moi'+datetime.date.today().strftime("%d")+'.txt')
	if os.path.isfile(txtfile):#Load file da cap nhat
		try:items=eval(makerequest(txtfile))
		except:items=[]
		for name,href,img,fanart in items:addirs(name,href,img,fanart)
	else:#Doc file cu trong khi cap nhat
		content=''
		for file in os.listdir(data_path):
			if 'vaphim_moi' in file:content=makerequest(joinpath(data_path,file));break
		try:items=eval(content)
		except:items=[]
		if items:
			for name,href,img,fanart in items:addirs(name,href,img,fanart)
		else:mess(u'Đang cập nhật dữ liệu - chọn lại sau 30 giây nữa nhé!')

def vp_xemnhieu():
	txtfile=joinpath(data_path,'vp_xemnhieu'+datetime.date.today().strftime("%d")+'.txt')
	if os.path.isfile(txtfile):#Load file da cap nhat
		try:items=eval(makerequest(txtfile))
		except:items=[]
		for name,href,img,fanart,url in items:addirs(name,href,img,fanart)
	else:#Doc file cu trong khi cap nhat
		content=''
		for file in os.listdir(data_path):
			if 'vp_xemnhieu' in file:content=makerequest(joinpath(data_path,file));break
		try:items=eval(content)
		except:items=[]
		if items:
			for name,href,img,fanart,url in items:addirs(name,href,img,fanart)
		else:mess(u'Đang cập nhật dữ liệu - chọn lại sau 30 giây nữa nhé!')

def vp_make_datanew():
	txtfile=joinpath(data_path,'vp_xemnhieu'+datetime.date.today().strftime("%d")+'.txt')
	if not os.path.isfile(txtfile):
		content_old='';list_new=[];url_new=''
		for file in os.listdir(data_path):
			if 'vp_xemnhieu' in file:content_old=makerequest(joinpath(data_path,file));break
		try:items_old=eval(content_old)
		except:items_old=[]
		urls=re.findall('<li><a href="(http://vaphim.com.+?)"',make_request('http://vaphim.com/request/'))
		for url in urls:
			if url not in content_old: #vp2fshare(url):img,fanart,href,fullname
				for img,fanart,href,name in vp2fshare(url):list_new.append((re.sub('&.* ','',name),href,img,fanart,url))
			else:url_new+=url+'*'
		if list_new:
			for name,href,img,fanart,url in items_old:
				if url in url_new:list_new.append((name,href,img,fanart,url))
			delete_files(data_path,mark='vp_xemnhieu');makerequest(txtfile,string=str(list_new),attr='w')
	txtfile=joinpath(data_path,'vaphim_moi'+datetime.date.today().strftime("%d")+'.txt');list_new=[]
	if not os.path.isfile(txtfile):
		id_new='-'.join(s for s in re.findall('data="(.+?)" title',make_request('http://vaphim.com')))
		for id_tip,id,category,img,fanart,href,name in doc_xml(joinpath(datapath,'vaphim.xml')):
			if id in id_new:list_new.append((name,href,img,fanart))
		if list_new:
			delete_files(data_path,mark='vaphim_moi');makerequest(txtfile,string=str(list_new),attr='w')

def daklak47(name,url,img):
	reps = make_request(url)
	if reps.status==302:
		req=reps.headers['location']
		url = req.replace('http:','https:')
		if 'www.fshare.vn/folder/' in url:mess(u"Chưa xử lý trường hợp đọc folder trên 47daklak.com");return
		else:resolve_url(url)
	else: mess(u"Không tìm thấy link trên %s"%str2u(url))

def ifile_home(name,url,img,mode,page,query):
	pattern='href=".+(\d{5}).+" class="mosaic-backdrop"'
	if url=="demo" or query=="demo":#ifile de nghi
		url='http://ifile.tv/phim' if url=="demo" else url
		pattern='a href=".+(\d{5})\.htm">.*\s.*\s.*<img src=".+?" title=".+?"';query="demo"
	elif url=="index" or query=="index":#xem nhieu
		hd['Referer']='http://ifile.tv/phim/page/1' if url=="index" else url
		response=make_post('http://ifile.tv/phim/index/filter/type/special_filter',hd,'type=special_filter&filter_by_view_desc=1')
		hd['Cookie']=response.cookiestring;query='index';hd['Referer']=='http://ifile.tv/phim/index'
		url='http://ifile.tv/phim' if url=="index" else url
	elif url=="new":url='http://ifile.tv/phim'#Moi nhat
	body=make_request(url,headers=hd)
	id_new='-'.join(s for s in re.findall(pattern,body))
	for id_tip,id,category,img,fanart,href,name in doc_xml(joinpath(datapath,"ifiletv.xml")):
		if id in id_new:addirs(name,href,img,fanart)
	pattern='<a href=".{,20}/(\d{1,3})" title="Next" > Next</a>.*\s.*<a href=".{,20}/(\d{1,3})" title="End" >End</a>'
	trang=re.search(pattern,body)
	if trang and query!="demo":
		page=xshare_group(trang,1);trangcuoi=xshare_group(trang,2);url='http://ifile.tv/phim/page/%s'%page
		name=color['trangtiep']+'Trang tiếp theo: trang %s/%s[/COLOR]'%(page,trangcuoi)
		addir(name,url,img,fanart,mode,page=page,query=query,isFolder=True)
		
def doc_list_xml(url,filename='',page=0):
	if not page:
		items=doc_xml(url,filename=filename)
		makerequest(joinpath(data_path,'temp.txt'),string=str(items),attr='w')
	else:f=open(joinpath(data_path,'temp.txt'));items=eval(f.readlines()[0]);f.close()
	pages=len(items)/rows+1
	del items[0:page*rows];count=0
	for id,href,img,fanart,name in items:
		if '47daklak.com' in href: addir(name,href,img,mode=47)
		else: addirs(name,href,img,fanart)
		count+=1
		if count>rows and len(items)>(rows+10):break
	if len(items)>(rows+10):
		page+=1;name=color['trangtiep']+'Trang tiep theo...trang %d/%d[/COLOR]'%(page+1,pages)
		addir(name,url,iconpath+'khophim.png',mode=97,page=page,isFolder=True)

def doc_xml(url,filename='',para=''): 
	if (datapath in url) or (myfolder in str2u(url)):body=makerequest(url)
	else:body=make_request(resolve_url(url,xml=True))

	if ('vaphim' in url) or ('ifiletv' in url) or ('phimfshare' in url) or ('hdvietnam' in url):
		if para and para[:6]=='search':
			if ('phimfshare' in url) or ('hdvietnam' in url):
				r='href="(.+?)" img="(.+?)">(.*%s.*)</a>'%para[7:];items=[]
				for href,img,name in re.compile(r, re.I).findall(no_accent(body)):
					items.append((img,img,href,name))
			else:
				r='img="(.*?)" fanart="(.*?)" href="(.+?)">(.*%s.*)</a>'%para[7:]
				items=re.compile(r, re.I).findall(no_accent(body))
		else:
			if not para:r='<a id_tip="(.*?)" id="(.+?)" category="(.*?)" img="(.*?)" fanart="(.*?)" href="(.+?)">(.+?)</a>'
			elif para=='post1': r='id="(.+?)"'
			else: #Doc theo category
				r='<a.*id="(.+?)" category=".*%s.*" img="(.*?)" fanart="(.*?)" href="(.+?)">(.+?)</a>'%para
			items = sorted(re.findall(r,body),key=lambda l:l[0], reverse=True)
	else:#Doc cac list xml khac
		r='<a.+id="(.*?)".+href="(.+?)".+img="(.*?)".+fanart="(.*?)".*>(.+?)</a>'
		items = re.compile(r).findall(body)
		if len(items)<1:items = re.findall('.+()href="(.+?)".+img="(.*?)".*()>(.+?)</a>',body)
		if len(items)<1:items = re.findall('.+()href="(.+?)".*()()>(.+?)</a>',body)
		if (copyxml=="true") and ('http' in url) and (len(items)>0) :
			filename=re.sub('\.xml.*','.xml',filename.replace('[COLOR orange]List xml[/COLOR]-',''))
			filename=re.sub('\[.{1,10}\]','',filename);f_fullpath=joinpath(myfolder,filename)
			if not os.path.isfile(f_fullpath):
				string='<?xml version="1.0" encoding="utf-8">\n'
				for id,href,img,fanart,name in items:
					string+='<a id="%s" href="%s" img="%s" fanart="%s">%s</a>\n'%(id,href,img,fanart,name)
				if makerequest(f_fullpath,string=string,attr='w'):
					mess(u'Đã tải file %s vào MyFolder'%str2u(filename))
	return items

def fshare_page_file(url):
	body = make_request(url)
	name=clean_string(xshare_group(re.search('<title>(.+?)</title>',body),1))
	if not name or 'Lỗi 404' in name:mess(u'Không tìm thấy nội dung quý khách yêu cầu');return 'no'
	size=xshare_group(re.search('<i class="fa fa-hdd-o"></i>(.+?)</div>',body),1).strip()
	return name+' - '+size

def doc_TrangFshare(name,url,img,fanart,query=''):
	def fshare_remove_item(url,query):
		if query=='hdvn':
			pattern='<a date=".+?" href="%s" img=".*?">.+?</a>\n'%url
			body=re.sub(pattern,'',makerequest(joinpath(datapath,"hdvietnam.xml")))
			makerequest(joinpath(datapath,"hdvietnam.xml"),body,'w')
	pageIndex=filescount=rowscount=files_count=0;name_return=name
	if 'pageIndex' in url:
		pageIndex=int(url.split('?')[1].split('=')[1]);filescount=int(url.split('?')[2].split('=')[1])
		rowscount=int(url.split('?')[3].split('=')[1])
	body = make_request(url);name=clean_string(xshare_group(re.search('<title>(.+?)</title>',body),1))
	if not name or 'Lỗi 404' in name:mess(u'Không tìm thấy nội dung quý khách yêu cầu');return 'no'
	if '/file/' in url:
		size=xshare_group(re.search('<i class="fa fa-hdd-o"></i>(.+?)</div>',body),1).strip()
		items=[('',url,name,size,'')] #return url,name,size
	else:
		files_count=xshare_group(re.search('Số lượng:(.+?)</div>',body),1).strip()
		files_count=int(files_count) if files_count else filescount
		if files_count==0:mess(u'Thư mục trống');fshare_remove_item(url,query);return 'no'
		pattern='data-id="(.+?)" .+? href="(.+?)".+title="(.+?)".*\s.*\s.*\s.*<.+?>(.+?)</div>.*\s.*<.+?>(.+?)</div>'
		items=re.findall(pattern,body)
		if url.strip()==thumucrieng and items:
			items=sorted(items,key=lambda l:(l[4][6:]+l[4][3:5]+l[4][:2]), reverse=True)
	idtxtfile=joinpath(data_path,'id.txt');makeidtxtfile=False
	for id,href,name,size,date in items:
		if re.search('/folder/\w{10,14}\?p=',href): #Thu muc con
			temp=xshare_group(re.search('(\w{10,14} )',name),1)
			if temp:id=temp
			id=id.upper();temp=False
			try:temp=ids.has_key(id)
			except:
				try:ids=eval(makerequest(idtxtfile))
				except:ids={}
				temp=ids.has_key(id)
			if temp:href='https://www.fshare.vn/%s/%s'%(ids[id],id)
			else:href=check_id_fshare(id);ids[id]='file' if '/file/' in href else 'folder';makeidtxtfile=True
			name=re.sub('\w{10,14} ','',name);img=icon['fshare'] if not img else img
		if url.strip()==thumucrieng:query='thumucrieng';img=icon['myfshare']
		if 'www.fshare.vn/file' in href:
			if name.strip()[-3:].lower()=='xml':query+='xml';img=icon['khophim']
			#elif name.strip()[-3:].lower()=='m3u':
			elif len(size.strip())>2:name=name+" - "+size;img=icon['fshare'] if not img else img
		addirs(name,href.replace('http:','https:'),img,fanart,query)
	if makeidtxtfile:makerequest(idtxtfile,string=str(ids),attr='w')
	rowscount+=len(items)
	if ('/folder/' in url) and (rowscount<files_count):
		files_count=str(files_count);rowscount=str(rowscount);page=str(pageIndex+2);pageIndex=str(pageIndex+1)
		url=url.split('?')[0]+'?pageIndex=%s?files_count=%s?rows_count=%s'%(pageIndex,files_count,rowscount)
		name=color['trangtiep']+'Trang tiep theo...trang %s[/COLOR]'%page
		addir(name,url,img,fanart,mode=90,query=query,isFolder=True)
	return name_return

def doc_Trang4share(url,temp=[]):#38
	if '4share.vn/d/' in url:
		response=make_request(url)
		pattern="<a href='(.+?)' target='.+?'><image src = '.+?'>(.+?)<.*?><td style='text-align: right'>(.+?)</td>"
		pattern+="|<a href='(.+?)'>.*\s.*<image src = '.+?'>(.+?)</a></div>"
		for href,name,size,folder_link,folder_name in re.findall(pattern,response):
			if href:name=name.strip()+' - '+size.strip();href='http://4share.vn'+href
			else:href='http://4share.vn'+folder_link;name=folder_name.strip()
			if href not in temp:temp.append((href));addirs(name,href)
	elif '4share.vn/f/' in url:
		name_size=re.search('Filename:.{,10}>(.+?)</strong>.{,20}>(.+?)</strong>',make_request(url))
		if name_size:
			name=xshare_group(name_size,1)+' - '+xshare_group(name_size,2)
			if url not in temp:temp.append((url));addirs(name,url)
	return temp

def doc_thumuccucbo(name,url,img,fanart,mode,query):
	if url=='thumuccucbo':url=myfolder
	url=str2u(url)
	if query=='Remove':
		if os.path.isfile(url):
			try:os.remove(url);mess(u'Đã xóa file: %s'%str2u(url));xbmc.executebuiltin("Container.Refresh")
			except:mess(u'Lỗi xóa file')
		else:
			import shutil
			try:shutil.rmtree(url);mess(u'Đã xóa thư mục: %s'%str2u(url));xbmc.executebuiltin("Container.Refresh")
			except:mess(u'Lỗi xóa thư mục')
	elif query=='Rename':
		name=str2u(os.path.basename(url))
		name_new = get_input('xshare - Rename file/folder (chú ý phần mở rộng)',name)
		if name_new and name_new!=name:
			if rename_file(url,joinpath(os.path.dirname(url),name_new)):
				mess(u'Đã đổi tên file/folder: %s'%str2u(url));xbmc.executebuiltin("Container.Refresh")
			else:mess(u'Lỗi Rename file/folder')
	elif myfolder in url and query!='file':
		try:url=unicode(url,'utf8')
		except:url=str2u(url)
		for dirname,dirnames,filenames in os.walk(url):
			if dirname==url:
				for filename in filenames:
					filenamefullpath = joinpath(dirname, filename)
					if os.path.isfile(filenamefullpath):
						filename=filename.encode('utf-8');filenamefullpath=filenamefullpath.encode('utf-8')
						file_ext=os.path.splitext(filenamefullpath)[1][1:].lower()
						if file_ext in media_ext:
							item = xbmcgui.ListItem(filename, iconImage=icon['khophim'])
							query=menuContext(filename,filenamefullpath,'','',mode,query,item)
							xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=filenamefullpath,listitem=item)
						elif file_ext=='xml':addirs(filename,filenamefullpath,icon['khophim'],query='xml')
						else:addirs(filename,filenamefullpath,query='file')
			else:
				dirname=dirname.encode('utf-8')
				name='%sThư mục %s[/COLOR]'%(color['trangtiep'],dirname)
				addir(name,dirname,img=icon['icon'],mode=mode,query=dirname,isFolder=True)
		return
	else:mess(u'Chưa xử lý kiểu file này')
	return 'no'

def play_maxspeed_link(): 
	query = get_input('Hãy nhập max speed link của Fshare, 4share hoặc tênlửa')
	if query is None or query=='':return 'no'
	query = query.replace(' ','')
	if len(query)<50:mess(u'Bạn nhập link ID chưa đúng: '+query);return 'no'
	xbmcsetResolvedUrl(query)
	return ''

def lay_link_tenlua(href):
	idf=xshare_group(re.search('\w{14,20}',href),0)
	if not idf:return
	response=tenlua_get_detail_and_starting(idf)
	if response["type"]=="file":
		name=response['n'].encode('utf-8');url="https://www.tenlua.vn/download/"+idf
		addir(name,url,mode=3)
	elif response["type"]=="folder":
		for item in response['content']:
			lay_link_tenlua(item['link'])

def check_id_fshare(id):
	url='https://www.fshare.vn/folder/%s'%id
	if make_request(url,resp='o').status!=200:url=url.replace('folder','file')
	return url

def check_id_4share(id):
	url='http://4share.vn/f/%s/'%id;name=''
	item=re.search('<center>.+?<strong>(.+?)</strong>.+?<strong>(.+?)</strong></center>',make_request(url))
	if item:name=xshare_group(item,1)+' - '+xshare_group(item,2)
	else:
		url='http://4share.vn/d/%s/'%id
		items=re.findall("<br/><b>(.+?)</b>|<a href='(/f/\w+)|<a href='(/d/\w+)'>",make_request(url))
		if len(items)>1:name=items[0][0]
	return name,url

def check_id_tenlua(id):
	response=tenlua_get_detail_and_starting(id);name=url=''
	if response["type"]=="file":name=response['n'];url="https://www.tenlua.vn/download/"+id
	elif response["type"]=="folder":name=response["folder_name"];url="https://www.tenlua.vn/fm/folder/"+id
	return name,url

def id_2url(url,name='',mode=0,page=0,query=''):
	def find_id_internal(id):
		items={};r1='href="(.+%s.*)" img="(.*?)">(.+?)</a>';r2='img="(.*?)" fanart=".*?" href="(.+%s.*)">(.+?)</a>'
		files='phimfshare.xml-hdvietnam.xml'
		for file in ['vaphim.xml','ifiletv.xml','phimfshare.xml','hdvietnam.xml']:
			body=makerequest(joinpath(datapath,file));id=id.lower() if len(id)>13 else id
			item=re.search(r1%id,body) if file in files else re.search(r2%id,body)
			if item:
				items['name']=xshare_group(item,3);	items['href']=xshare_group(item,1 if file in files else 2)
				items['img']=xshare_group(item,2 if file in files else 1);break
		return items
	if query=='MyFshare':query=thumucrieng;page=4
	if page==0:
		name='Nhập ID phim %sFshare[/COLOR]-%s4share[/COLOR] hoặc %stenlua[/COLOR]'%(color['fshare'],color['4share'],color['tenlua'])
		addir(name,url,icon['icon'],mode=mode,query=query,page=1,isFolder=True)
		for href,name in re.findall('<a href="(.+?)">(.+?)</a>',makerequest(search_file)):
			addirs(name,href,icon['id'],query='ID?'+query)
	elif page == 1:#Nhập ID mới
		idf = get_input('Hãy nhập chuỗi ID link của Fshare-4share hoặc tenlua');record=[]
		if idf is None or idf.strip()=='':return 'no'
		idf = xshare_group(re.search('(\w{10,20})',''.join(s for s in idf.split()).upper()),1)
		if len(idf)<10:mess(u'Bạn nhập ID link chưa đúng: '+idf);return 'no'
		items=find_id_internal(idf)
		if items:addirs(items['name'],items['href'],items['img']);record.append((items['href'],items['name']))
		elif len(idf)<13:
			url=check_id_fshare(idf);query='fshare'
			if url:name=doc_TrangFshare(name,url,icon[query],'')
			if url and name and name!='no':items['name']=name;items['href']=url;items['img']=icon['id']
		else:
			query='4share';name,url=check_id_4share(idf)
			if name:addirs(name,url,icon[query])
			else:
				query='tenlua';name,url=check_id_tenlua(idf)
				if name:addirs(name,url,icon[query])
			if name:items['name']=name;items['href']=url;items['img']=icon['id']
		if items:make_mySearch(items['name'],items['href'],items['img'],'',mode,'Add')
		else:mess(u'Không tìm được link có ID: '+idf);return 'no'
	elif page == 4:#Mở thư mục chia sẻ trên Fshare
		doc_TrangFshare(name,query,iconpath+'fshare.png','')
	return ''

def ifile_tv_page(url):
	items=[]
	try: 
		pattern='id="(\d{,6})".{,300}<a href="(.+?)".{,300}src="(.+?)".{,300}"red">(.+?)</font>'
		item = re.compile(pattern,re.DOTALL).findall(make_request(url))
		for id_tip,href,img,name in item:
			http='http://ifile.tv';href=http+href;id_htm=href.rsplit('.')[2];img=http+img;name=name.strip()
			items.append((id_tip,id_htm,href,img,name))
	except:print 'ifile_tv_page Error: '+ url
	return items #id_tip,id_htm,href,img,name

def ifile_tv_4share(url):
	items = []
	body = make_request(url)
	pattern="href='/(.+?)'>.+?</a></u>|<div class='arrow_news'> <a.+>(.+?)</a>|<img src= '(.+?)' style='width: 100%'>"
	pattern+="|<b>(.+?)</b><br/><b>|<b>(http://4share.vn.+?)</b>.{,20}<b>(.+?)</b>"
	pattern+="|href='(http://subscene.com/subtitles/.+?)'"
	category=name=img=''
	for c,n1,i,n2,url4share,size,urlsubscene in re.findall(pattern,body):
		category+=xshare_group(re.search('phim/(.+?)\.\d{,6}',c),1)+' '
		if n1:name=n1
		if n2 and not name:name=n2
		if i:img=i
		if url4share and url4share not in items:
			category=' '.join(s for s in category.split())
			name=clean_string(name)+' - '+size;url4share=urllib.unquote(url4share)
			items.append((url4share,'http://ifile.tv'+img,name,category))
		if urlsubscene and urlsubscene not in items:
			category=' '.join(s for s in category.split())
			name=clean_string(name)+' - '+size;urlsubscene=urllib.unquote(urlsubscene)
			items.append((urlsubscene,'http://ifile.tv'+img,name,category))
	return items

def ifile_update():
	items_old, id_old = read_items_old("ifiletv.xml")
	mess(u'Đang kiểm tra dữ liệu cập nhật của ifile.tv...')
	items_new = []#id_tip,id_htm,href,img,name
	for id_tip,id_htm,href,img,name in ifile_tv_page('http://ifile.tv/') :
		if id_htm not in id_old:
			for url4share,fanart,name2,catalog in ifile_tv_4share(href):
				fullname=name2 if name in name2 else name
				fullname=' '.join(s for s in fullname.split())
				items_new.append((id_tip,id_htm,catalog,img,fanart,url4share,fullname))
	if items_new:update_xml(items_new,items_old,"ifiletv.xml")
	else:mess(u'Không có phim mới...')
	return 'ok'

def read_items_old(filename,id_old=[]):
	items_old = doc_xml(joinpath(datapath,filename))
	for i in items_old:id_old.append((i[1]))
	return items_old, id_old

def read_all_filexml(fn="vaphim.xml",string_search='',lists=[],index=[]):
	if string_search:lists = lists+doc_xml(joinpath(datapath,fn),para='search:'+string_search)
	else:lists = lists+doc_xml(joinpath(datapath,fn))
	if not string_search:
		for id_tip,id_htm,category,img,fanart,url,name in lists:index.append((id_htm))
	return lists,index

def phimfshare_search(url,string,mode,temp=[],p=0):
	string,trang,p=trang_search(string)
	start=(int(trang)-1)*20;s=no_accent(string)
	apiary=str(random.randrange(10**3,10**5)) if trang=='1' else p
	url_search='https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&'
	url_search+='rsz=filtered_cse&num=20&hl=vi&prettyPrint=false&source=gcsc&gss=.com&googlehost=www.google.com&'
	url_search+='sig=23952f7483f1bca4119a89c020d13def&cx=005609294674567689888:qyuk9aoqwmg&q=%s'%urllib.quote_plus(s)
	url_search+='&start=%d&callback=google.search.Search.apiary%s&nocache'%(start,apiary)
	body=make_request(url_search)
	results=xshare_group(re.search('(\(\{"cursor".+?\}\));',body),1)
	if not results:return 'no'
	true='true';false='false'#xu ly loi khi results co chua bien true,false
	results=eval(results)
	for i in results["results"]:
		fanart=''
		if 'richSnippet' in i and 'cseThumbnail' in i['richSnippet'] and 'src' in i['richSnippet']['cseThumbnail']:
			fanart=i['richSnippet']['cseThumbnail']['src']
		if 'url' not in i:continue
		mess(i['url'].split('/')[len(i['url'].split('/'))-2])
		response=make_request(i['url'])
		name=xshare_group(re.search('<title> (.+?)</title>',response),1)
		if not name:continue
		img=xshare_group(re.search('<img src="(.+?)" border="0" alt="" />',response),1)
		name=' '.join(s for s in re.sub('\[.+?\]|\(.+?\)|\|.*\||MuLtI|Fshare|fshare|amp;','',name).split())
		for server,link in getlinkPFS(response):
			addirs(name,link,img,fanart)
	trangtiep_google_custom(url,results,string,mode,trang,start,apiary)
	return ''

def hdvn_search(url,string,mode,temp=[],p='0'):
	string,trang,p=trang_search(string)
	start=(int(trang)-1)*20
	apiary=str(random.randrange(10**3,10**5)) if trang=='1' else p
	url_search='https://www.googleapis.com/customsearch/v1element?'
	url_search+='key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=20&'
	url_search+='hl=vi&prettyPrint=false&source=gcsc&gss=.com&sig=23952f7483f1bca4119a89c020d13def&'
	url_search+='cx=006389339354059003744:dxv8n47myyg&googlehost=www.google.com&start=%d&'%start
	url_search+='q=%s&callback=google.search.Search.apiary%s&nocache'%(urllib.quote_plus(string),apiary)
	body=make_request(url_search)
	results=xshare_group(re.search('(\(\{"cursor".+?\}\));',body),1)
	if not results:return 'no'
	results=eval(results)
	for i in results["results"]:
		fanart=''
		if 'richSnippet' in i and 'cseThumbnail' in i['richSnippet'] and 'src' in i['richSnippet']['cseThumbnail']:
			fanart=i['richSnippet']['cseThumbnail']['src']
		if 'url' in i:
			j=hdvn_get_link(i['url'],fanart)
			if j:temp+=j
	if 'cursor' in results and 'pages' in results['cursor']:
		if str(int(start)+20) in ' '.join(s['start'] for s in results['cursor']['pages']) and len(temp)<10 and int(trang)%3>0:
			trang=str(int(trang)+1)
			return hdvn_search(url,'%s?%s?%s'%(string,trang,p),mode,temp)
	trangtiep_google_custom(url,results,string,mode,trang,start,apiary)
	return ''

def trangtiep_google_custom(url,results,string,mode,trang,start,apiary):
	if 'cursor' in results and 'pages' in results['cursor']:
		if str(int(start)+20) in ' '.join(s['start'] for s in results['cursor']['pages']):
			trang=str(int(trang)+1)
			name=color['trangtiep']+'Trang tiep theo...trang %s[/COLOR]'%trang
			addir(name,url,icon[url.split('.')[0]],mode=mode,page=4,query='%s?%s?%s'%(string,trang,apiary),isFolder=True)

def fourshare_search(url,string,mode,temp=[],p=0):
	string,trang,p=trang_search(string)	
	href='http://4share.vn/search?page=%s&str=%s'%(trang,urllib.quote_plus(string))#+' mkv'
	pattern="<a target='_blank' href='(.+?)'>(.+?)</a><.{,40}>(.+?)</td>"
	body=make_request(href)
	items = re.findall(pattern,body);temp=[]
	for href,name,size in items:
		if os.path.splitext(name)[1][1:].lower().strip() not in media_ext:continue
		name=name+' - '+size;href='http://4share.vn%s'%href
		if href not in temp:temp.append(href);addirs(name,href)
	trang=str(int(trang)+1)
	if trang in ' '.join(s for s in re.findall("search\?page=(\d{,2})",body)) and len(temp)<10 and int(trang)%15>0:
		return fourshare_search(url,'%s?%s'%(string,trang),mode,temp,p)
	p=str(int(p)+1)
	if trang in ' '.join(s for s in re.findall("search\?page=(\d{,2})",body)):
		addir(color['trangtiep']+'Trang tiep theo...trang %s[/COLOR]'%p,url,icon['4share'],mode=mode,page=4,query='%s?%s?%s'%(string,trang,p),isFolder=True)
	return ''

def trang_search(string):
	if len(string.split('?'))==3:p=string.split('?')[2];trang=string.split('?')[1];string=string.split('?')[0]
	elif len(string.split('?'))==2:p=1;trang=string.split('?')[1];string=string.split('?')[0]
	else:p=trang='1'
	return string,trang,p

def tenlua_search(url,string,mode,temp=[]):
	string,trang,p=trang_search(string)
	href='https://api2.tenlua.vn/search?keyword=%s&page=%s'%(urllib.quote_plus("%s"%string),trang)
	response = make_request(href,resp='j')
	if int(response['pagging']['total'])==0:mess(u'Không tìm được tên phim phù hợp');return 'no'
	for item in response['items']:
		if item is None or item['ext'] not in media_ext:continue
		idf=item['h']
		link=tenlua_get_detail_and_starting(idf)
		if link["type"]=="none":continue
		elif link["type"]=="file":name=link['n'];href="https://www.tenlua.vn/download/%s"%idf
		elif link["type"]=="folder":name=link["folder_name"];href="https://www.tenlua.vn/fm/folder/%s"%idf
		if href not in temp:temp.append(href);addirs(name,href,icon['tenlua'])
	trang=str(int(trang)+1)
	if int(response['pagging']['pages'])>=int(trang) and len(temp)<10 and int(trang)%15>0:
		return tenlua_search(url,'%s?%s?%s'%(string,trang,p),mode,temp)
	p=str(int(p)+1)
	if int(response['pagging']['pages'])>=int(trang):
		name=color['trangtiep']+'Trang tiep theo...trang %s[/COLOR]'%p
		addir(name,url,icon['tenlua'],mode=mode,page=4,query='%s?%s?%s'%(string,trang,p),isFolder=True)
	return ''

def ifile_search(url,string,mode,temp=[]):
	string,trang,p=trang_search(string)	
	url_search = 'http://ifile.tv/search?search_module=phim&search_name=1&'
	url_search += 'search_content=1&time_sort=new&search_string="%s"'%urllib.quote_plus(string)
	bodys = re.findall("<td>(.*?)</b>",make_request(url_search));items = []
	for body in bodys:
		items+=re.findall("<a.+href='(.+?)'.+src='(.+?)'.+(\d{5}).+>(.+?)</a>",body)
	if not items:mess(u'Không tìm được tên phim phù hợp');return 'no'
	items_xml,id_xml = read_all_filexml(fn="ifiletv.xml")
	for href,img,id_htm,name in items:
		if id_htm in id_xml:
			index = id_xml.index(id_htm)
			while id_xml[index] == id_htm:
				temp.append((items_xml[index]));index +=1 
		else:
			for url4share,fanart,name2,catalog in ifile_tv_4share('http://ifile.tv'+href):
				temp.append(('',id_htm,catalog,img,fanart,url4share,name))
	for id_tip,id_htm,catalog,img,fanart,href,name in temp:addirs(name,href,img,fanart)
	return ''

def vaphim_search(url,string,mode,temp=[],p=0):
	string,trang,p=trang_search(string)
	url_search='http://vaphim.com/page/%s/?s=%s'%(trang,urllib.quote_plus(string))
	items = vaphim_page(url_search)
	if not items:
		mess(u'Không tìm được tên phim phù hợp');return 'no'
	items_xml,id_xml = read_all_filexml()
	for id_tip,id_htm,category,href in items:
		if id_htm in id_xml:
			index = id_xml.index(id_htm)
			while id_xml[index] == id_htm:
				temp.append((items_xml[index]));index +=1 
		else:
			mess(href)
			for img,fanart,link,name in vp2fshare(href):
				temp.append((id_tip,id_htm,category,img,fanart,link,name))
	for id_tip,id_htm,catalog,img,fanart,href,name in temp:addirs(name,href,img,fanart)
	pattern="class='pages'>(.+?)<.+span><a href='(.+?)' class='page larger'>(\d{,3})</a>"
	page_tag=re.search(pattern,make_request(url_search))
	if page_tag:
		trang=str(int(trang)+1)
		name=color['trangtiep']+'Tiep theo %s...trang %s[/COLOR]'%(xshare_group(page_tag,1),xshare_group(page_tag,3))
		addir(name,url,icon[url.split('.')[0]],mode=mode,page=4,query='%s?%s?%s'%(string,trang,p),isFolder=True)
	return ''

def internal_search(url,string,mode,temp=[],p=0):
	string,trang,p=trang_search(string);items=[]
	if trang=='1':
		for fn in ['vaphim.xml','ifiletv.xml','phimfshare.xml','hdvietnam.xml']:
			items,index=read_all_filexml(fn=fn,string_search=".*".join(string.split()),lists=items)
		items=sorted(items,key=lambda l:no_accent(l[3]).lower());p=str(len(items))
		if not items:mess(u'Không tìm thấy phim nào có chuổi phù hợp');return
		if len(items)>(rows+rows/2):makerequest(joinpath(data_path,'temp.txt'),string=str(items),attr='w')
	else:f=open(joinpath(data_path,'temp.txt'));items=eval(f.readlines()[0]);f.close()

	trang=int(trang);del items[:rows*(trang-1)]
	if len(items)>(rows+rows/2):
		del items[rows:];trang=str(trang+1)
	else:trang=''
	for img,fanart,href,name in items:addirs(name,href,img,fanart)
	if trang:
		name=color['trangtiep']+'Trang tiep theo...trang %s/%s[/COLOR]'%(trang,str(int(p)/rows+1))
		addir(name,url,icon['icon'],mode=mode,page=4,query='%s?%s?%s'%(string,trang,p),isFolder=True)

def xshare_search(name,url,query,mode,page,items=[]):#13
	if url=='addstring.xshare.vn':
		name=re.sub('\[COLOR.{,12}\]|\[/COLOR\]|Fshare|4share|TenLua|Subscene|List xml|-|:|"','',name).strip()
		if not re.search(name,makerequest(search_file)):
			makerequest(search_file,string='<a>%s</a>\n'%name,attr='a')
			mess(u'Đã thêm tên phim này vào DS tìm kiếm')
	elif page==0:make_mySearch('',url,'','',mode,'get')
	elif page==1:
		query=make_mySearch('',url,'','','','Input')
		return xshare_search(name,url,query,mode,4,items) if query else 'no'
	elif page==4:
		query=no_accent(query)
		if url=='vaphim.com':vaphim_search(url,query,mode)
		elif url=='phimfshare.com':phimfshare_search(url,query,mode)
		elif url=='tenlua.vn':tenlua_search(url,query,mode)
		elif url=='4share.vn':fourshare_search(url,query,mode)
		elif url=='ifile.tv':ifile_search(url,query,mode)
		elif url=='hdvietnam.com':hdvn_search(url,query,mode)
		elif url=='xshare.vn':internal_search(url,query,mode)
	return ''

def updatePFS():#6+
	items=rss_content('http://phimfshare.com/external.php?type=RSS2')
	content_new=''
	fphimfshare=joinpath(datapath,'phimfshare.xml')
	content_old=makerequest(fphimfshare)
	idf_old=re.findall('<a id="(.+?)" server',content_old)
	for item in items:
		idf=xshare_group(re.search('-(\d{5})',item.findtext('link')),1)
		if not idf or idf in idf_old:continue
		name=re.sub('\[.*\]|\(.*\)|\|.*\|','',item.findtext('title')).strip()
		content=item.findtext('contentencoded')
		img=xshare_group(re.search('img src="(.+?jpg)["|?| ]',content),1)
		for server,link in getlinkPFS(content):
			if link not in content_new:
				content_new+='<a id="%s" server="%s" href="%s" img="%s">%s</a>\n'%(idf,server,link,img,name)
	if content_new:
		makerequest(fphimfshare,string=content_new.encode('utf-8'),attr='a')
		mess('PhimFshare.com data Auto update completed')

def getlinkPFS(content):#6+
	items=[]
	pattern='(https?://www.fshare.vn/\w{4,6}/\w{10,14})|(http://4share.vn/./\w{14,20})|(https?://w?w?w?/?tenlua.vn/.*?)[ |"|<]'
	for links in re.findall(pattern,content):
		if links:
			for link in links:
				idf=xshare_group(re.search('(\w{10,20})',link),1)
				if idf:
					link=link.lower()
					if 'fshare.vn/file' in link:url='https://www.fshare.vn/file/%s'%idf.upper();server="fshare"
					elif 'fshare.vn/folder' in link:url='https://www.fshare.vn/folder/%s'%idf.upper();server="fshare"
					elif 'tenlua.vn' in link and ('folder/' in link or '#download' in link) and len(idf)>16:
						url='https://tenlua.vn/fm/folder/%s'%idf;server="tenlua"
					elif 'tenlua.vn' in link and len(idf)>16:url='https://tenlua.vn/download/%s'%idf;server="tenlua"
					elif '4share.vn' in link:url=link;server="4share"
					else:continue
					items.append((server,url))
	return items

def phimFshare(name,url,mode,page,query):#6
	fphimfshare=joinpath(datapath,'phimfshare.xml')
	home='http://phimfshare.com/'
	if query=='phimfshare.com':make_mySearch('',url,'','',mode,'get');return ''
	elif page==4 and name==query:return phimFshare('Search',url,mode,page,query)
	elif name=='Search':
		search_string = urllib.quote_plus(query)
		url='https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&'
		url+='rsz=filtered_cse&num=15&hl=vi&prettyPrint=false&source=gcsc&gss=.com&'
		url+='sig=23952f7483f1bca4119a89c020d13def&cx=005609294674567689888:qyuk9aoqwmg&q='+search_string
		url+='&googlehost=www.google.com&callback=google.search.Search.apiary'
		body=make_request(url)
		items =re.findall('()"url":"(http://phimfshare.com/.+?)"()()',body)
		if not items:mess(u'Không tìm thấy phim có chứa chuổi tìm kiếm');return 'no'
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		return phimFshare('Search',url,mode,page,query) if query else 'no'
	elif query=='PhimMoi':
		body=make_request(home)
		items=re.findall('()<a href="(.+?)" ()class="title">(.+?)</a>',body)
	else:
		if home not in url:url=home+url+'/'
		body=make_request(url)
		pattern='<img class="preview" src="(.+?)" .+? class=".+?" href="(.+?)" id="thread_title_(.+?)">(.+?)</a>'
		items=re.findall(pattern,body)
	
	content_old=makerequest(fphimfshare);content_new=''
	for img,href,idf,name in items:
		if not idf or len(idf)<5:
			idf=xshare_group(re.search('-(\d{5})',href),1)
			if not idf:continue
		items_old=re.findall('<a id="%s" server="(.+?)" href="(.+?)" img="(.*?)">(.+?)</a>'%idf,content_old)
		if items_old:
			for ser_,href_,img_,name_ in items_old:
				addirs(name_,href_,img_,img_)
		else:
			mess(href.split('/')[len(href.split('/'))-2])
			response=make_request(href)
			temp=xshare_group(re.search('<title> (.+?)</title>',response),1)
			if temp:name=temp
			elif not name:continue
			if not img:img=xshare_group(re.search('<img src="(.+?)" border="0" alt="" />',response),1)
			name=' '.join(s for s in re.sub('\[.+?\]|\(.+?\)|MuLtI|Fshare|fshare','',name).split())
			for server,link in getlinkPFS(response):
				if link not in content_new:
					content_new+='<a id="%s" server="%s" href="%s" img="%s">%s</a>\n'%(idf,server,link,img,name)
				addirs(name,link,img,img)
	if content_new:makerequest(fphimfshare,string=content_new,attr='a')
	href=xshare_group(re.search('<a rel="next" href="(.+?)" title=".+?">',body),1)
	if href:
		if not page:page=1
		page+=1;name=color['trangtiep']+'Trang tiếp theo - Trang '+str(page)+' ...[/COLOR]'
		addir(name,href,iconpath+'fshare.png',mode=mode,page=page,query=query,isFolder=True)
	return ''

def rss_content(url):
	from xml.etree import ElementTree as etree
	reddit_file = make_request(url)
	reddit_file = reddit_file.replace('content:encoded','contentencoded')
	try:
		reddit_root = etree.fromstring(reddit_file)
		items=reddit_root.findall('channel/item')
	except:
		mess('Update rss %s fail'%str2u(url))
		items=[]
	return items

def correct_link(url):
	if 'tenlua.vn' in url:idf=xshare_group(re.search('(\w{16,20})',url),1)
	elif 'subscene.com' in url and '...' not in url:idf='ok'
	else:idf=xshare_group(re.search('(\w{10,20})',url),1)
	if idf:
		url=url.lower()
		if 'fshare.vn/file' in url:url='https://www.fshare.vn/file/%s'%idf.upper()
		elif 'fshare.vn/folder' in url:url='https://www.fshare.vn/folder/%s'%idf.upper()
		elif 'tenlua.vn' in url and ('folder/' in url or '#download' in url) and len(idf)>16:
			url='https://tenlua.vn/fm/folder/%s'%idf
		elif 'tenlua.vn' in url and len(idf)>16:url='https://tenlua.vn/download/%s'%idf
		elif '4share.vn' or 'subscene.com'in url:url=url
	else:url=''
	return url

def hdvn_rss(url):
	items = rss_content(url)
	pattern_link='(https?://www.fshare.vn/\w{4,6}/\w{10,14})|(http://4share.vn/./\w{14,20})|(https?://w?w?w?/?tenlua.vn/.*?)[ |"|<]|(http://subscene.com/subtitles/.+?)[ |"|\'|<]';temp=[]
	for item in items:
		contentencoded=item.findtext('contentencoded')
		img=xshare_group(re.search('a href="([\w|:|/|\.]+\.\w{3})" class="highslide"',contentencoded),1)
		links=re.findall(pattern_link,contentencoded)
		if not links:continue
		name=re.sub('\{.{,20}\}|\[.{,20}\]|\(.{,20}\)|\|.{,20}\|','',item.findtext('title'))
		name=re.sub('\{.*\}|\[.*\]|\(.*}\)|\|.{.*}\|','',name).strip()
		for link in links:
			for url in link:
				url=correct_link(url)
				if not url or url in str(temp):continue
				temp.append((url,img,name))
	return temp
	
def hdvn_update(items=[]):#33-146-311-265-110-116-123-57-157
	if not items:
		home='http://www.hdvietnam.com/diendan/external.php?type=RSS2'
		hd['Cookie']=loginhdvietnam();hdvn_thank_xshare(hd);items=hdvn_rss(home)
		mess(u'Đang cập nhật data từ tất cả các nguồn RSS %s của hdvietnam.com'%homnay)
		for item in '33-146-311-265-110-116-123-57-157'.split('-'):
			items+=hdvn_rss('%s&forumids=%s'%(home,item))
	file_hdvn=joinpath(datapath,"hdvietnam.xml");string=''
	index_old=re.findall('href="(.+?)"',makerequest(file_hdvn))
	for url,img,name in items:
		if url not in index_old:
			index_old.append(url)
			string+='<a date="%s" href="%s" img="%s">%s</a>\n'%(homnay,url,img,name)
	if string:makerequest(file_hdvn,string=string.encode('utf-8'),attr='a')

def hdvietnam(name,url,img,fanart,mode,page,query):
	if url in '000-UPD':
		if query in '000-UPD':
			hom_nay=homnay
			if query=='UPD':hdvn_update();mess(u'Đã cập nhật thành công RSS data %s của hdvietnam.com'%homnay)
		else:hom_nay=query
		body=makerequest(joinpath(datapath,"hdvietnam.xml"));ngaytruoc=''
		items=re.findall('date="%s" href="(.+?)" img="(.+?)">(.+?)</a>'%hom_nay,body)
		for href,img,name in sorted(items,key=lambda k:k[2].lower()):
			#if 'www.fshare.vn/file' in href:name=name+' ~  '+fshare_page_file(href)
			addirs(name,href,img,query='hdvn')
		for ngay in sorted(re.findall('date="(.+?)"',body),key=lambda k:k[6:]+k[3:5]+k[:2]):
			if ngay==hom_nay:break
			ngaytruoc=ngay
		if ngaytruoc!=hom_nay:
			name=color['trangtiep']+"Thông tin ngày %s[/COLOR]"%ngaytruoc
			addir(name,"000",icon["icon"],mode=mode,query=ngaytruoc,isFolder=True)
	elif re.search('\d\d',query):
		url='http://www.hdvietnam.com/diendan/external.php?type=RSS2&forumids=%s'%query
		items=hdvn_rss(url)
		for url,img,name in items:addirs(name,url,img,query='hdvn')
		endxbmc();hdvn_update(items)
	elif query=='MCS':
		body=make_request('http://www.hdvietnam.com/diendan/34-chia-se-phim/')
		pattern='<div class="forumbit_post L2">.{,500}<h2 class="forumtitle"><a href="(.+?)">(.+?)</a>'
		items=re.findall(pattern,body,re.DOTALL)
		for href,name in items:
			if '149-phim-theo-phan-loai' in href:query='PLP'
			elif xshare_group(re.search('/\d{1,3}-',href),0) in '/33-/311-/65-/146-/149-/150-':query='PL1'
			else:continue
			addir(color['hdvietnam']+name+'[/COLOR]',href,icon['hdvietnam'],fanart,mode,page,query,isFolder=True)
	elif query=='TVL':
		body=make_request(url)
		for name,img in re.findall('<font size="5">(.+?)</font>.{,400}<img src="(.+?)"',body,re.DOTALL):
			addir(color['hdvietnam']+name+'[/COLOR]',url,img,fanart,mode,page,'PL1',isFolder=True)
	elif query=='PLP':
		body=make_request(url)
		body=body[body.find('Phim theo phân loại</a>'):body.find('Xem HD trực tuyến</a>')]
		for href,name in re.findall('<a href="(.+?)">(.+?)</a>',body):
			addir(color['hdvietnam']+name+'[/COLOR]',href,icon['hdvietnam'],fanart,mode,page,'PL1',isFolder=True)
	elif query=='PL1':
		body=make_request(url,headers=hd)
		if url.split('/')[4] in '33-fshare-vn 311-tenlua-vn 65-megashare-vn 146-up-4share-vn':
			for href,name in re.findall('<h2 class="forumtitle"><a href="(.+?)">(.+?)</a></h2>',body):
				addir(color['fshare']+name+'[/COLOR]',href,icon['hdvietnam'],fanart,mode,page,'PL1',isFolder=True)
		body=body[body.find('Normal Threads'):]
		items=re.findall('<a class="title.{,20}" href="(.+?)" id=".+?">(.+?)</a>[\w\W]{200,500}<b>(.+?)</b>',body)
		for href,name,bossroom in items:
			name=color['hdvietnam']+bossroom+'[/COLOR] '+name
			addir(name,href,img,fanart,mode,page,'GET',isFolder=True)
		if page==0:url=url+'index2.html';page=2
		else:url=url.replace('index%s.html'%str(page),'index%s.html'%str(page+1));page+=1
		if re.search(url,body):
			name=color['trangtiep']+'Trang tiep theo...trang %d[/COLOR]'%page
			addir(name,url,img,fanart,mode,page,'PL1',isFolder=True)
	elif query=='GET':
		if 'xem-gi-hom-nay' in url:
			string='http://www.hdvietnam.com/diendan/clear.gif'
			if 'http://' in url:
				body=make_request(url)
				boss=xshare_group(re.search('line popupctrl.{40,55}/\d{4,10}-(.+?).html"',body),1)
				for temp,name,img in re.findall('(<font size="5">(.+?)</font>).{,400}<img src="(.+?)"',body,re.DOTALL):
					content=body[body.find(temp)+100:];temp=content.find('<font size="5">')
					content=content[:temp] if temp>0 else content[:content.find(string)]
					temp=re.findall('<a href="(.+?)" target="_blank">.+?</a>',content)
					if re.search('/33-|/311-|/65-|/146-|/149-|/150-',str(temp)):
						name1=re.sub('<.{1,5}>','',name);title=color['hdvietnam']+boss+'[/COLOR] '+name
						addir(title,url.replace('http://',''),img,img,mode,page,'GET',isFolder=True)
			else:
				body=make_request('http://'+url);name=re.sub('\[COLOR.+COLOR\] ','',name)
				body=body[body.find('<font size="5">'+name)+100:];temp=body.find('<font size="5">')
				body=body[:temp] if temp>0 else body[:body.find(string)]

				for href,name in re.findall('<a href="(.+?)" target="_blank">(.+?)</a>',body):
					if re.search('/\d{1,3}-',href):addir(name,href,img,fanart,mode,page,'GET',isFolder=True)
		else:hdvn_get_link(url)

def data_download_fromFshare(data1,data2):
	pattern='href="(.+?)" title="%s"'%data1;href='https://www.fshare.vn/folder/GZCI8AHAQJ75'
	data=xshare_group(re.search(pattern,make_request(href)),1).replace('http:','https:')
	url=resolve_url(data,True);kq=''
	if url=='fail':
		pattern='href="(.+?)" title="%s"'%data2
		data=xshare_group(re.search(pattern,make_request(href)),1).replace('http:','https:')
		response=make_request(data,headers=hd,resp='o')
		if response.status==302:url=response.headers['location']
	if url!='fail':
		body=make_request(url)
		if body:
			tempfile = joinpath(tempfolder,os.path.basename(url))
			if os.path.splitext(tempfile)[1]=='.zip' and makerequest(tempfile,string=body,attr='wb'):
				xbmc.sleep(500);f1=tempfile.encode('utf-8');f2=tempfolder.encode('utf-8')
				try:xbmc.executebuiltin('XBMC.Extract("%s","%s")' % (f1,f2), True);kq='ok'
				except:pass
			elif makerequest(re.sub('-hot','',tempfile),string=body,attr='wb'):kq='ok'
	return kq

def data_download():
	delete_files(tempfolder);init_file();download=downloadresult=''
	#Kiểm tra database
	files=['hdvietnam.xml','ifiletv.xml','phimfshare.xml','vaphim.xml']
	file_now=os.listdir(datapath)
	for file in files:
		if file not in file_now:download='download';break
	if not download:
		for file in file_now:
			size=os.path.getsize(joinpath(datapath,file))
			if file.lower()=='vaphim.xml' and size<4218000:download='download';break
			if file.lower()=='ifiletv.xml' and size<2611000:download='download';break
			if file.lower()=='hdvietnam.xml' and size<630000:download='download';break
			if file.lower()=='phimfshare.xml' and size<629000:download='download';break
	if download=='download':
		mess(u'Đang download database cho xshare')
		if data_download_fromFshare('data.zip','data-hot.zip'):downloadresult='yes'
	#Kiểm tra file fanart
	file=joinpath(home,'fanart.jpg')
	if (os.path.isfile(file) and os.path.getsize(file)<613860) or not os.path.isfile(file):
		if data_download_fromFshare('fanart.jpg','fanart-hot.jpg'):downloadresult='yes'
	#Kiểm tra bộ icon
	files=['4share.png','dangcaphd.png','downsub.png','favorite.png','fptplay.png','fshare.png','gsearch.png','hdvietnam.png','icon.png','id.png','ifiletv.png','isearch.png','khophim.png','maxspeed.png','megabox.png','movie.png','msearch.png','myfolder.png','myfshare.png','phimfs.png','serverphimkhac.png','setting.png','tenlua.png','vaphim.png','xshare.png']
	file_now=os.listdir(iconpath);download=''
	for file in files:
		if file not in file_now:download='download';break
	if download=='download':
		mess(u'Đang download bộ icon của LUC QUYET CHIEN cho xshare')
		if data_download_fromFshare('icon.zip','icon-hot.zip'):downloadresult='yes'
	
	kq='ok'
	if downloadresult:
		mess(u'Đang unzip......')
		for f in os.listdir(tempfolder):
			file=joinpath(tempfolder,f);ext=os.path.splitext(file)[1][1:].lower()
			if ext=='xml':dest_path=datapath
			elif ext=='png':dest_path=iconpath
			elif ext=='jpg':dest_path=home
			else:continue
			size=os.path.getsize(file);dest_file=joinpath(dest_path,f)
			if not os.path.isfile(dest_file) or os.path.getsize(dest_file)<size:
				if not rename_file(file,dest_file):kq=''
	if downloadresult and kq:mess(u'Download database cho xshare thành công!',10000)
	elif downloadresult:mess(u'Download database cho xshare thất bại!',10000)
	else:mess(u'Đã kiểm tra database cho xshare thành công!',10000)
	if kq:
		myaddon.setSetting('thank2xshare','true');myaddon.setSetting('checkdatabase','false')
		if os.path.isfile(joinpath(data_path,'checkdatabase.txt')):os.remove(joinpath(data_path,'checkdatabase.txt'))
		delete_files(tempfolder)
	return

def data_update():
	ngay=datetime.date.today().strftime("%Y%m%d");gio=datetime.datetime.now().strftime("%H")
	last_update=myaddon.getSetting('last_update');ngay=ngay+last_update[8:]
	try:
		if ngay>last_update:myaddon.setSetting('last_update',ngay);vp_update();ifile_update();updatePFS()
		if abs(int(gio)-int(last_update[8:]))>2:
			myaddon.setSetting('last_update',last_update[:8]+gio)
			hdvn_update();vp_update_rss()
			mess(u'Đã cập nhật danh mục phim từ các dữ liệu RSS')
	except:mess('Data update error');pass

def subscene(name,url,query):#,img='',fanart='',query=''
	if query=='subscene.com':
		href = get_input('Hãy nhập link của sub trên subscene.com','http://subscene.com/subtitles/')
		if href is None or href=='' or href=='http://subscene.com/subtitles/':return 'no'
	else:href=url
	if not re.search('\d{5,10}',href):
		if not os.path.basename(href):href=os.path.dirname(href)
		pattern='<a href="(/subtitles/.+?)">\s+<span class=".+?">\s*(.+?)\s+</span>\s+<span>\s+(.+?)\s+</span>'
		subs=re.findall(pattern,make_request(href,headers={'Cookie':'LanguageFilter=13,45'}))
		mess(u'Tên phim: %s'%str2u(name).replace('[COLOR green]Subscene[/COLOR]-',''),30000)
		for url,lang,name in sorted(subs,key=lambda l:l[1], reverse=True):
			name='Eng '+name if '/english/' in url else '[COLOR red]Vie[/COLOR]-'+name
			addirs(name,'http://subscene.com'+url,query='download')
		return ''
	pattern='<a href="(.+?)" rel="nofollow" onclick="DownloadSubtitle.+">'
	downloadlink='http://subscene.com' + xshare_group(re.search(pattern,make_request(href)),1)
	if len(downloadlink)<20:mess(u'Không tìm được maxspeed link sub');return
		
	if myaddon.getSetting('autodel_sub')=='true':delete_files(subsfolder)
	body=make_request(downloadlink);tempfile=joinpath(tempfolder,"subtitle.sub");delete_files(tempfolder)
	body=makerequest(tempfile,string=body,attr='wb')
	if body[0]=='R':typeid="rar"
	elif body[0]=='P':typeid="zip"
	else:typeid="srt"
	
	folder=tempfolder if typeid in "rar-zip" else subsfolder
	subfile=joinpath(folder,"subtitle."+typeid);rename_file(tempfile,subfile)
	
	if typeid in "rar-zip":
		f1=subfile.encode('utf-8');f2=tempfolder.encode('utf-8')
		xbmc.sleep(500)
		xbmc.executebuiltin('XBMC.Extract("%s","%s")'%(f1,f2),True);os.remove(subfile)
		exts = [".srt", ".sub", ".txt", ".smi", ".ssa", ".ass"];sub_list=[]
		for file in os.listdir(tempfolder):
			tempfile=joinpath(tempfolder,file)
			if os.path.isfile(tempfile) and os.path.splitext(tempfile)[1] in exts:
				if 'Eng' in name and myaddon.getSetting('autotrans_sub')=='true':
					mess(u'Google đang dịch sub từ tiếng Anh sang tiếng Việt', timeShown=20000)
					subfile=xshare_trans(tempfile)
					if rename_file(subfile,joinpath(subsfolder,'Vie.%s'%re.sub(',|"|\'','',file))):
						mess(u'Đã dịch xong sub từ tiếng Anh sang tiếng Việt');os.remove(tempfile)
					elif rename_file(tempfile,joinpath(subsfolder,'Eng.%s'%re.sub(',|"|\'','',file))):
						mess(u'Không dịch được sub, giữ nguyên bản tiếng Anh') 
				elif 'Eng' in name and rename_file(tempfile,joinpath(subsfolder,'Eng.%s'%re.sub(',|"|\'','',file))):
					mess(u'Đã download sub vào Subsfolder') 
				elif rename_file(tempfile,joinpath(subsfolder,'Vie.%s'%re.sub(',|"|\'','',file))):
					mess(u'Đã download sub vào Subsfolder') 
	return 'ok'

def xshare_trans(sourcefile):
	tempfile = joinpath(tempfolder,"temp"+os.path.splitext(sourcefile)[1])
	fs=open(sourcefile);ft=open(tempfile,'w');lineslist=[];substring=''
	for line in fs:
		if re.search('[a-zA-Z]',line):
			substring+='+'.join(''.join(re.split('<.+?>',line.replace('"',''))).strip().split())+'+xshare+'
			lineslist.append('xshare')
		else:
			lineslist.append(line.strip()+'\n')
			if len(substring)>1500:
				write_trans(ft,substring,lineslist)
				substring='';lineslist=[]
	if len(substring)>0:write_trans(ft,substring,lineslist)
	fs.close();ft.close()
	return tempfile

def write_trans(fo,string,m):
	translist=google_trans(string);j=0
	for i in m:
		if i=='xshare':
			try:fo.write(translist[j].strip()+'\n');j+=1
			except:pass
		else:fo.write(i)

def google_trans(s):
	hd={'User-Agent':'Mozilla/5.0','Accept-Language':'en-US,en;q=0.8,vi;q=0.6','Cookie':''}
	url='https://translate.google.com.vn/translate_a/single?oe=UTF-8&tl=vi&client=t&hl=vi&sl=en&dt=t&ie=UTF-8&q=%s'%s
	body= make_request(url,headers=hd)
	body=body.replace(',,"en"','').replace('[[[','').replace(']]]','')
	result=''
	for i in body.split('],['):
		research=xshare_group(re.search('"(.+?)","(.+?)"',i),1)
		if research:result+=research+' '
		else:print '%s :not research'%i
	return result.replace('Xshare','xshare').split('xshare')

def fptplay(name,url,img,mode,page,query):
	def fptplay_2s(string):
		return ' '.join(re.sub('&.+;',xshare_group(re.search('&(\w).+;',s),1),s) for s in string.split())
	def fptplay_getlink(id,name,mode,dir=True):
		response=make_post('http://fptplay.net/show/getlink?id=%s&episode=1&mobile=web'%id)
		if response and dir:
			json=response.json;url = json['quality'][0]['url'][0]['url']
			img = json['quality'][0]['thumb'];title = json['quality'][0]['title']
			if len(json['quality'])==1:addir(name.strip(),url,img,img,mode=mode,query='play')
			else:addir(color['fptplay']+name.strip()+"[/COLOR]",id,img,img,mode=mode,query='FP4',isFolder=True)
		elif response:
			for i in response.json['quality']:
				url = i['url'][0]['url']
				img = i['thumb']
				title = re.sub('\[.{,20}\]','',name.strip())+' - '+i['title'].encode('utf-8')
				addir(title,url,img,img,mode=mode,query='play')

	if query=="FPP":
		body=make_request('http://fptplay.net')
		name=color['search']+"Search trên fptplay.net[/COLOR]"
		addir(name,"fptplay.net/tim-kiem",icon['fptplay'],mode=mode,query="FPS",isFolder=True)
		name=color['fptplay']+'Trang chủ fptplay.net[/COLOR]'
		addir(name,"http://fptplay.net",icon['fptplay'],mode=mode,query='FP0',isFolder=True)
		start='top_menu reponsive';end='top_listitem';body=body[body.find(start):body.find(end)]
		for href,title in re.findall('<li ><a href="(http://fptplay.net/danh-muc/.+?)">(.+?)</a></li>',body):
			title=color['fptplay']+fptplay_2s(title)+'[/COLOR]'
			addir(title,href,icon['fptplay'],mode=mode,query='FP2',isFolder=True)
	elif query=="FPS":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return fptplay(name,url,img,mode,page,query)
		else:return 'no'
	elif url=="fptplay.net/tim-kiem":
		search_string = urllib.quote(query)
		url='http://fptplay.net/show/more?type=search&stucture_id=key&page=1&keyword=%s'%search_string
		return fptplay(name,url,img,mode,page,query='FP3')
	elif query=="FP0":
		body=make_request('http://fptplay.net')
		name=color['fptplay']+'Phổ biến hiện nay[/COLOR]'
		addir(name,'phim_popular',icon['fptplay'],mode=mode,query='FP1',isFolder=True)
		name=color['fptplay']+'Đặc sắc[/COLOR]'
		addir(name,'phim_trending',icon['fptplay'],mode=mode,query='FP1',isFolder=True)
		pattern='<a href="(.+?)" title="(.+?)" class="pull-left btn_arrow_right"></a>'
		items=re.findall(pattern,body)
		for href,title in items:
			title=color['fptplay']+fptplay_2s(title)+'[/COLOR]'
			addir(title,href,icon['fptplay'],mode=mode,query='FP1',isFolder=True)
	elif query=="FP1":
		body=make_request('http://fptplay.net')
		if 'phim_popular' in url:start='data-tooltip="phim_popular';end='data-tooltip="phim_trending'
		elif 'phim_trending' in url:start='data-tooltip="phim_trending';end='id="selTab_5284685d169a585a2449c489"'
		elif 'phim' in url:start='id="selTab_5284685d169a585a2449c489"';end='id="selTab_52847232169a585a2449c48c'
		elif 'tv-show' in url:start='id="selTab_52847232169a585a2449c48c';end='id="selTab_54fd271917dc136162a0c'
		elif 'thieu-nhi' in url:	start='id="selTab_54fd271917dc136162a0cf2d';end='id="selTab_52842df7169a580a79169'
		elif 'the-thao' in url:start='id="selTab_52842df7169a580a79169efd"';	end='id="selTab_5283310e169a585a05b920d'
		elif 'ca-nhac' in url:start='id="selTab_5283310e169a585a05b920de"';end='id="selTab_52842dd3169a580a79169efc'
		elif 'tong-hop' in url:start='id="selTab_52842dd3169a580a79169efc"';end='</body>'
		body=body[body.find(start):body.find(end)]
		pattern='<a href=".+?-(\w+)\.html".*alt="(.+?)"'
		items=re.findall(pattern,body);temp=[]
		for id,title in items:
			if id not in temp:temp.append(id);fptplay_getlink(id,fptplay_2s(title),mode)
	elif query=="FP2":
		pattern='<a href="(http://fptplay.net/the-loai/.+?)" title="(.+?)"'
		items=re.findall(pattern,make_request(url));temp=[]
		for href,name in items:
			if href not in temp:temp.append(href)
			else:continue
			name=color['fptplay']+fptplay_2s(name)+"[/COLOR]";id=xshare_group(re.search('(\w{22,26})',href),1)
			data='type=new&keyword=undefined&page=1&stucture_id=%s'%id;url='http://fptplay.net/show/more?%s'%data
			addir(name,url,icon["fptplay"],mode=mode,query="FP3",isFolder=True)
	elif query=="FP3":
		body=make_post(url).body
		if not body:mess(u'Lỗi get data từ fptplay.net');return 'no'
		items=re.findall('<a href=".+-(\w+)\.html".+class="title">(.+?)</a>',body)
		for id,title in items:fptplay_getlink(id,fptplay_2s(title),mode)
		if len(items)>35:
			page=xshare_group(re.search('page=(\d{1,3})',url),1);page=str(int(page)+1);
			url=re.sub('page=\d{1,3}','page='+page,url)
			name=color['trangtiep']+"Trang tiếp theo - Trang %s[/COLOR]"%page
			addir(name,url,icon["fptplay"],mode=mode,query="FP3",isFolder=True)
		elif not items:mess(u'Không tìm thấy dữ liệu');return 'no'
	elif query=="FP4":fptplay_getlink(url,name,mode,dir=False)
	elif query=='play':xbmcsetResolvedUrl(url)
	return ''

def megabox(name,url,mode,page,query):
	home='http://phim.megabox.vn/'
	def megabox_load_menu(items,mode):
		for href,name,img in items:
			if 'megabox.vn/clip-' in href:continue
			if os.path.splitext(href)[1][1:].lower()=='m3u8':
				addir(name.strip(),href+'|'+urllib.urlencode(hd),img,img,mode=mode,query='MGP')
				continue
			try:
				response=make_request(href,resp='o')
				if response.status==301:body=make_request(response.headers['location'])
				elif response.status==200:body=response.body
				else:continue
			except:continue
			links=re.findall('<a onclick=.getListEps\((.+?)\).{,20} href=.{,25}>(.+?)</a>',body)
			if len(links)==1:
				for link in links:
					folder='http://phim.megabox.vn/content/ajax_episode?id=%s&start=%s'%(link[0].split(',')[0].strip(),link[0].split(',')[1].strip())
					name='%s%s[/COLOR]: Tập %s'%(color['megabox'],name.strip(),link[1])
					addir(name,folder,img,img,mode=mode,query=os.path.dirname(href),isFolder=True)
			else:
				link=xshare_group(re.search("changeStreamUrl\('(.+?)'\)",body),1)
				if link:addir(name.strip(),link+'|'+urllib.urlencode(hd),img,img,mode=mode,query='MGP')
				else:addir(color['megabox']+name.strip()+'[/COLOR]',href,img,img,mode=mode,query='MG2',isFolder=True)

	if query=='megabox.vn':make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return megabox(query,url,mode,page,query)
		else:return 'no'
	elif query==name:
		search_string = urllib.quote_plus(query)
		body=make_post('http://phim.megabox.vn/tim-kiem?keyword=%s'%search_string).body;items=[]
		if not body:return 'no'
		pattern='a class=".+?" href="(.+?)".*<h3 class=.H3title.>(.+?)</h3>.*\s.*src="(.+?)"|<div class="gb-view-all">.?<a href="(.+?)">(.+?)</a>'
		links=re.findall(pattern,body)
		if not links:mess(u'Không tìm thấy dữ liệu phù hợp');return 'no'
		for href,name,img,link,title in links:
			if not link:items.append((href,name,img))
			else:
				megabox_load_menu(items,mode);items=[]
				if 'phim-le' in link:title=color['search']+title+' - phim lẻ[/COLOR]'
				else:title=color['search']+title+' - phim bộ[/COLOR]'
				addir(title,link,icon['megabox'],mode=mode,query="MG4",isFolder=True)
		if items:megabox_load_menu(items,mode)
	elif query in 'MGL-MGS':
		href='http://phim.megabox.vn/phim-le' if query=='MGL' else 'http://phim.megabox.vn/phim-bo'
		body=make_request(href)
		if url in 'MGL-MGS':
			body=body[body.find('<ul id="gen">'):body.find('<ul id="country">')]
			name=color['megabox']+'Tất cả thể loại[/COLOR]'
			addir(name,'MGQ',icon['megabox'],mode=mode,page=0,query="MGL",isFolder=True)
			for value,name in re.findall("<li value='(\d{1,2})' >(.+?)</li>",body):
				name=color['megabox']+name+'[/COLOR]'
				addir(name,'MGQ',icon['megabox'],mode=mode,page=int(value),query=query,isFolder=True)
		elif url=='MGQ':
			body=body[body.find('<ul id="country">'):body.find('<ul id="other">')]
			name=color['megabox']+'Tất cả Quốc gia[/COLOR]'
			url=href+'?cat=1&gen=%d'%page
			addir(name,url,icon['megabox'],mode=mode,query="MG4",isFolder=True)
			for value,name in re.findall("<li value='(\d{1,2})' >(.+?)</li>",body):
				name=color['megabox']+name+'[/COLOR]'
				url=href+'?cat=1&gen=%d&country=%s'%(page,value)
				addir(name,url,icon['megabox'],mode=mode,page=int(value),query="MG4",isFolder=True)
	elif query=='MGB':
		body=make_request(home,headers=hd);open_category("MGB")
		for href,name in re.findall('<li><a href="(.+?)" title="">(.+?)</a></li>',body):
			if 'Clip' in name:continue
			addir(color['megabox']+name+'[/COLOR]',href,icon['megabox'],mode=mode,query='MG4',isFolder=True)
	elif query=='MG0':
		body=make_request(home)
		for name in re.findall('"H2title">(.+?)</h2>',body):
			if 'Phim sắp chiếu' in name or 'clip' in name:continue
			if 'Phim Lẻ Mới Nhất' in name:
				content=make_request('http://phim.megabox.vn/ajaxschedule/home/?data=1',resp='j')
				href=re.search('"H2title"><a href="(.+?)" title="">(.+?)</h2>',content['event'].encode('utf-8'))
				if href:
					title=color['megabox']+xshare_group(href,2)+'[/COLOR]'
					addir(title,xshare_group(href,1),icon['megabox'],mode=mode,query='MG1',isFolder=True)
			href=re.search('href="(.+?)">(.+?)</a>',name)
			if not href:
				name=color['megabox']+re.sub('<.{,4}>','',name)+'[/COLOR]'
				addir(name,home,icon['megabox'],home,mode=mode,query='MG1',isFolder=True)
			else:
				name=color['megabox']+xshare_group(href,2)+'[/COLOR]'
				addir(name,xshare_group(href,1),icon['megabox'],mode=mode,query='MG1',isFolder=True)
	elif query=='MG1':
		if home not in url:url=home+url
		body=make_request(url)
		if 'megabox' in name.lower():
			#pattern="<li><a href='(.+?)'.?><img src='(.+?)' alt='Banner - (.+?)''.?></a>"
			pattern="<li><a href='(.+?)'.?><img src='(.+?)'.+?<a href='.+?'>(.+?)</a>"
			items1=re.findall(pattern,body);items=[]
			for href,img,name in items1:items.append((href,name,img))
			megabox_load_menu(items,mode)
		elif 'top 10 phim' in name.lower():
			pattern='<a class="tooltip thumb" href="(.+?)".+<h3 class=.H3title.>(.+?)</h3>.*\s.*<img src="(.+?)"'
			megabox_load_menu(re.findall(pattern,body),mode)
		elif 'xem' in name.lower():#xem nhieu nhat
			pattern='<a class=.thumb. title="" href="(.+?)">.*\s.*<img alt=.Poster (.+?). src="(.+?)"/>'
			items=re.findall(pattern,body)
			if 'phim le' in no_accent(name).lower():del items[20:]
			elif 'phim bo' in no_accent(name).lower():del items[:20];del items[20:]
			elif 'show' in no_accent(name).lower():
				temp=[]
				for i in items:
					if 'megabox.vn/show' in i[0]:temp.append((i))
				items=temp
			megabox_load_menu(items,mode)
		elif url!=home:
			pattern='a class=".+?" href="(.+?)".*<h3 class=.H3title.>(.+?)</h3>.*\s.*src="(.+?)"'
			megabox_load_menu(re.findall(pattern,body),mode)
	elif query=='MG2':
		body=make_request(url)
		if '/tag/' in url:
			pattern='href="(.+?)".+<h3 class=.H3title.>(.+?)</h3>.*\s.*src="(.+?)"'
			megabox_load_menu(re.findall(pattern,body),mode)
		else:
			img=xshare_group(re.search('<img alt=.+? src="(.+?)"/>',body),1)
			links=re.findall('<a onclick=.getListEps\((.+?)\).{,20} href=.{,25}>(.+?)</a>',body)
			for link in links:
				href='http://phim.megabox.vn/content/ajax_episode?id=%s&start=%s'%(link[0].split(',')[0].strip(),link[0].split(',')[1].strip())
				title='%s Tập: %s'%(name,link[1].encode('utf-8'))
				addir(title,href,img,img,mode=mode,query=os.path.dirname(url),isFolder=True)
	elif query=='MG3':
		tap=xshare_group(re.search('(\d{1,3}-\d{1,3})',name),1)
		if tap:
			for i in range(int(tap.split('-')[0]),int(tap.split('-')[1])+1):
				addir(re.sub('Banner - ','',name),link+'|'+urllib.urlencode(hd),img,img,mode=mode,query='MGP')
		body=make_request(url)
		img=xshare_group(re.search('<img alt=.+? src="(.+?)"/>',body),1)
		links=re.findall('<a onclick=.+?>(.+?)</a>',body)
		for link in links:
			addir(name+': Tập %s'%link,url,img,img,mode=mode,query='MG3',isFolder=True)
	elif query=='MG4':
		if home not in url:url=home+url
		body=make_request(url)
		pattern='a class=".+?" href="(.+?)".*<h3 class=.H3title.>(.+?)</h3>.*\s.*src="(.+?)"'
		items=re.findall(pattern,body)
		if not items:mess(u'Không tìm thấy dữ liệu phù hợp');return 'no'
		megabox_load_menu(items,mode)
		page_control=re.findall('>(\d{,3})</a></li><li class="next"><a href="(.+?(\d{1,3}).*?)">|<li class="last"><a href=".+?(\d{1,3}).*?">',body)
		if len(page_control)==2:
			name=color['trangtiep']+u'Trang tiếp theo: trang %s/%s[/COLOR]'%(page_control[0][2],page_control[0][0])
			addir(name,page_control[0][1],mode=mode,query='MG4',isFolder=True)
		elif len(page_control)==4:
			name=color['trangtiep']+u'Trang tiếp theo: trang %s/%s[/COLOR]'%(page_control[0][2],page_control[1][3])
			addir(name,page_control[0][1],mode=mode,query='MG4',isFolder=True)
	elif query=='MGP':xbmcsetResolvedUrl(url)
	elif query=='MBP':
		response=make_request(url,resp='o')
		if response.status==200:
			link=xshare_group(re.search("changeStreamUrl\('(.+?)'\)",response.body),1)
		elif response.status==301:
			link=xshare_group(re.search("changeStreamUrl\('(.+?)'\)",make_request(response.headers['location'])),1)
		else:mess(u'Không get được megabox maxspeed link');return 'no' 
		xbmcsetResolvedUrl(link+'|'+urllib.urlencode(hd))
	elif len(query)>3:
		for item in make_request(url,resp='j'):
			name=item['name']
			img='http://img.phim.megabox.vn/728x409'+item['image_banner']
			href=query+'/%s-%s.html'%(item['cat_id'],item['content_id'])
			addir(name,href,img,img,mode=mode,query='MBP')
	return ''

def dangcaphd(name,url,img,mode,page,query):
	home='http://dangcaphd.com/'
	def dangcaphd_get_page_control(body,mode,query):
		pattern='<a class="current">\d{1,5}</a><a href="(.+?)">(\d{1,5})</a>.*<a href=".+?page=(\d{1,5})">.+?</a></div>'
		page_control=re.search(pattern,body)
		if page_control:
			href=re.sub('&amp;','',xshare_group(page_control,1));trangke=xshare_group(page_control,2)
			tongtrang=int(xshare_group(page_control,3))/35+1
			name=color['trangtiep']+'Trang tiếp theo: trang %s/%d[/COLOR]'%(trangke,tongtrang)
			addir(name,href,mode=mode,query=query,isFolder=True)
	def dangcaphd_get_link(url):
		hd['Cookie']=login()
		body=make_request(url.replace('/movie-','/watch-'),headers=hd)
		if hd['Cookie']:logout_site(hd['Cookie'],'http://dangcaphd.com/logout.html')
		return re.findall('"(\d{,3})" _link="(.+?)" _sub="(.*?)"',body)
	def dangcaphd_download_sub(url):
		if myaddon.getSetting('autodel_sub')=='true':delete_files(subsfolder)
		subfullpathfilename=joinpath(subsfolder,'vie.%s'%os.path.basename(url));sub=''
		if os.path.splitext(subfullpathfilename)[1] in [".srt", ".sub", ".txt", ".smi", ".ssa", ".ass"]:
			if makerequest(subfullpathfilename,string=make_request(url),attr='wb'):sub=subfullpathfilename
		return sub
	def login(headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}):
		url="http://dangcaphd.com/login.html";u=myaddon.getSetting('mail_dchd');p=myaddon.getSetting('pass_dchd')
		response=make_post(url,headers,urllib.urlencode({"_submit":"true","email":u,"password": p}))
		try:
			if not response.json['login']:f=response.cookiestring;m='1';headers['Cookie']=f
			else:f='';m='2'
		except:f='';m='3'
		if m=='1' and re.search('Hết hạn.*</b></a></li>',make_request('http://dangcaphd.com/',headers=headers)):
			mess(u'[COLOR red]Tài khoản của bạn hết hạn sử dụng[/COLOR]')
			href='https://www.fshare.vn/folder/NCERC36BSSCY'#acc này do bạn vinhdo tặng
			hd=xshare_group(re.search('<title>.*xx(.+?)xx.*</title>',make_request(href)),1).split('=')
			data=urllib.urlencode({"_submit":"true","email":'%s@%s'%(hd[0],hd[1]),"password":hd[2]})
			resp=make_post(url,data=data)
			try:f=resp.cookiestring if not resp.json['login'] else ''
			except:f=''
		elif m=='1':mess(u'Login dangcaphd.com thành công')
		elif m=='2':mess('[COLOR red]'+re.sub('<..?>','',response.json['login'])+'[/COLOR]')
		elif m=='3':mess(u'[COLOR red]Login dangcaphd.com không thành công[/COLOR]')
		return f
		
	if query=='DHD':
		body=make_request(home)
		name=color['search']+"Search trên dangcaphd.com[/COLOR]"
		addir(name,"dangcaphd.com/movie/search.html",icon['dangcaphd'],mode=mode,query="DHS",isFolder=True)
		name=color['dangcaphd']+'Trang chủ dangcaphd.com[/COLOR]'
		addir(name,home,icon['dangcaphd'],mode=mode,query='DC0',isFolder=True)
		for name in re.findall('</i>(.+?)<span class="caret">',body):
			addir(color['dangcaphd']+name.strip()+'[/COLOR]',home,icon['dangcaphd'],mode=mode,query='DC1',isFolder=True)
		for href,name in re.findall('<a href="(.+?)"><i class=".+?"></i>(.+?)</a>',body):
			if 'channel.html' not in href and 'product.html' not in href:
				addir(color['dangcaphd']+name.strip()+'[/COLOR]',href,icon['dangcaphd'],mode=mode,query='DC2',isFolder=True)
	elif query=="DHS":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		return dangcaphd(name,url,img,mode,page,query) if query else 'no'
	elif url=="dangcaphd.com/movie/search.html":
		search_string = urllib.quote_plus(query)
		url='http://dangcaphd.com/movie/search.html?key=%s&search_movie=1'%search_string
		return dangcaphd(name,url,img,mode,page,query='DC2')
	elif query=='DC0':
		body=make_request(home)
		for href,name in re.findall('<a class="title" href="(.+?)"><i class="fa fa-film "></i>(.+?)</a>',body):
			addir(color['dangcaphd']+name.strip()+'[/COLOR]',href,icon['dangcaphd'],mode=mode,query='DC2',isFolder=True)
	elif query=='DC1':
		body=make_request(home)
		if 'the loai' in  no_accent(name).lower():
			for href,name in re.findall('<a href="(http://dangcaphd.com/cat.+?)" title="(.+?)">',body):
				addir(color['dangcaphd']+name.strip()+'[/COLOR]',href,icon['dangcaphd'],mode=mode,query='DC2',isFolder=True)
		if 'quoc gia' in  no_accent(name).lower():
			for href,name in re.findall('<a href="(http://dangcaphd.com/country.+?)" title="(.+?)">',body):
				addir(color['dangcaphd']+name.strip()+'[/COLOR]',href,icon['dangcaphd'],mode=mode,query='DC2',isFolder=True)
	elif query=='DC2':
		body=re.sub('\t|\n|\r|\f|\v','',make_request(url))
		items=re.findall('<a class="product.+?" href="(.+?)" title="(.+?)">.+?<img src="(.+?)" (.+?)</li>',body)
		for href,name,img,other in items:
			if re.search('<div class="sale">.+?</div>',other):
				name=name.strip()+'[/COLOR]'+' - ('+xshare_group(re.search('<div class="sale">(.+?)</div>',other),1)+')'
				addir(color['dangcaphd']+name,href,img,mode=mode,query='DC3',isFolder=True)
			else:addir(name.strip(),href,img,mode=mode,query='DCP')
		dangcaphd_get_page_control(body,mode,query)
	elif query=='DC3':
		for _epi,_link,_sub in dangcaphd_get_link(url):
			title=re.sub('\[.+?\]','',name.split('[/COLOR]')[0])+' - Tập '+_epi.strip()
			link=_link.replace(' ','%20').strip()+'xshare'+_sub.strip()
			addir(title,link,img,mode=mode,query='DCP')
	elif query=='DCP':
		subtitle=''
		if os.path.splitext(url)[1].lower()=='.html':
			links=dangcaphd_get_link(url)
			url=links[0][1].replace(' ','%20').strip()
			if links[0][2]:subtitle=dangcaphd_download_sub(links[0][2].strip())
		else:
			if url.split('xshare')[1]:subtitle=dangcaphd_download_sub(url.split('xshare')[1])
			url=url.split('xshare')[0]
		xbmcsetResolvedUrl(url)
		if subtitle:
			xbmc.sleep(500);xbmc.Player().setSubtitles(subtitle.encode('utf-8'));mess(u'Phụ đề của dangcaphd.com')

def vuahd(name,url,img,mode,page,query):
	color['vuahd']='[COLOR deeppink]';icon['vuahd']=icon['xshare'];home='http://vuahd.tv'
	def vuahd_login(headers=''):
		if not headers:
			url='http://vuahd.tv/accounts/login'
			response=make_request(url,resp='o');hd['Cookie']=response.cookiestring
			t=xshare_group(re.search("name='csrfmiddlewaretoken' value='(.+?)'",response.body),1)
			u=myaddon.getSetting('usernamev');p=myaddon.getSetting('passwordv')
			data=urllib.urlencode({'csrfmiddlewaretoken':t,'username':u,'password':p})
			response=make_post(url,hd,data)
			if response.status==302:
				f=response.cookiestring;hd['Cookie']=f
				if re.search('<b>Free</b></span>',make_request('http://vuahd.tv/accounts/profile/',headers=hd)):
					mess(u'[COLOR red]Tài khoản free chỉ xem được một số phim.[/COLOR]')
				else:mess(u'Login vuahd.tv thành công')
			else:mess(u'[COLOR red]Login vuahd.tv không thành công[/COLOR]');f=''
			return f
		else:make_request('http://vuahd.tv/accounts/logout',headers=headers)
	def namecolor(name):return '%s%s[/COLOR]'%(color['vuahd'],name)
	def vuahd_play(url):
		hd['Cookie']=vuahd_login();body=make_request(url,hd)
		href=xshare_group(re.search('<source src = "(.+?)"',body),1)
		if not href:href=xshare_group(re.search('file: "(.+?)"',body),1)
		if href:xbmcsetResolvedUrl(home+href);return
		else:mess(u'Không get được maxspeed link của vuahd.tv')
		vuahd_login(hd)
	def vuahd_search(string,page=1):
		body=make_request('http://vuahd.tv/movies/q/%s'%urllib.quote(string))
		for name,href,img,type in pubvn_page(body):
			addir(name,href,img,fanart,mode,page,query=type,isFolder=(type=='folder'))
		trangcuoi=xshare_group(re.search('class="vpage(\d{1,4})".{,5}>Cuối</a></li>',body),1).strip()
		if trangcuoi and int(trangcuoi)>page:
			name=color['trangtiep']+'Trang tiếp theo: trang %s/%s[/COLOR]'%(str(page+1),trangcuoi)
			addir(name,url,img,fanart,mode,page=page+1,query=string,isFolder=True)
		return ''
	if query=='vuahd.tv':
		name=color['search']+"Search trên vuahd.tv (pub.vn)[/COLOR]"
		addir(name,url,icon['isearch'],mode=mode,query='vuahdsearch',isFolder=True)
		items=re.findall('<li><a href=".+(\d{2})/" rel="external">(Phim.+?)</a></li>',make_request(home))
		for query,name in items:
			addir(namecolor(name),'http://vuahd.tv/1',icon['vuahd'],fanart,mode,page=1,query=query,isFolder=True)
		items=re.findall('<option id="sel_cat_(.+?)">(.+?)</option>',make_request(home))
		for query,name in items:
			addir('Thể loại-'+namecolor(name),'http://vuahd.tv/2',icon['vuahd'],fanart,mode,page=1,query=query,isFolder=True)
	elif query=='vuahdsearch':make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		string=make_mySearch('',url,'','','','Input')
		if string:vuahd(string,'http://vuahd.tv/3',img,mode,page=1,query='search')
	elif url=='vuahd.tv':vuahd(query,'http://vuahd.tv/3',img,mode,page=1,query='search')
	elif url=='http://vuahd.tv/1' and query=="00":#Phim bộ nhiều tập
		body=make_request('http://vuahd.tv/movies/tv-series/00/')
		for query,name in re.findall('<option id="sel_tvseries_cat_(.+?)">(.+?)</option>',body):
			addir(namecolor(name),'http://vuahd.tv/bo',home+img,fanart,mode=mode,page=1,query=query,isFolder=True)
	elif query=="eps":
		items=re.findall('<a href="#" class="btn-1 btnUpgrade">Xem (.+?)</a>',make_request(url));temp=[]
		for eps in items:
			if eps not in temp:
				temp.append(eps);title=eps+'-'+name;tap=xshare_group(re.search('(\d{1,3})',eps),1)
				if tap:tap=format(int(tap),'02d')
				else:continue
				addir(title,url.replace('tv-series/','')+'-%s'%tap,img,fanart,mode,page=page,query='play')
	elif query=="play":vuahd_play(url+'/watch')
	else:
		href='http://vuahd.tv/movies/'
		if url=='http://vuahd.tv/bo':url='%stv-series-items/%s/?page=%d'%(href,'00' if query=='0' else query,page)
		elif url=='http://vuahd.tv/2' and query=='0':url='%sall-items?page=%d'%(href,page)
		elif url in 'http://vuahd.tv/1-http://vuahd.tv/2':url='%scats/%s/items?page=%d'%(href,query,page)
		elif url=='http://vuahd.tv/3':url='%sq/%s'%(href,urllib.quote(name))
		else:url=re.sub('page=\d{1,3}','page=%d'%page,url) #Trang tiep theo
		body=make_request(url)
		items=re.findall('img src="(.+?)".{,500}<a href="(.+?)" title="(.+?)"',body,re.DOTALL)
		for img,href,name in items:
			if 'tv-series' in href:
				addir(namecolor(name),home+href,home+img,fanart,mode=mode,page=1,query='eps',isFolder=True)
			else:addir(name,home+href,home+img,fanart,mode,page=page,query='play')
		if items and len(items)>25:
			name=color['trangtiep']+'Trang tiếp theo: trang %s[/COLOR]'%str(page+1)
			addir(name,url,icon['vuahd'],fanart,mode,page=page+1,query='trangtiep',isFolder=True)
		
def pubvn(name,url,img,mode,page,query):
	color['pubvn']='[COLOR deepskyblue]';icon['pubvn']=icon['xshare'];home='http://pubvn.net/'
	def login():
		u=myaddon.getSetting('usernamep');p=myaddon.getSetting('passwordp')
		data='txtusername=%s&txtpass=%s&remeber_me1=0&sercurity_code='%(u,p)
		response=make_post(home+'phim/aj/action_login.php',data=data)
		if 'pub_userid=deleted' in response.cookiestring:mess(u'[COLOR red]Login pub.vn không thành công[/COLOR]')
		else:mess(u'Login pub.vn thành công')
		return {'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0','Cookie':response.cookiestring}
	def getiMovEps(url):
		hd=login();pattern='<input id="thread_id" type="hidden" value="(.+?)"/>'
		thread_id=xshare_group(re.search(pattern,make_request(url)),1);pattern='id="player" src="(.+?)"'
		iMovEps=xshare_group(re.search(pattern,make_request(home+'/bar/dodamde/'+thread_id,headers=hd)),1)
		return home+iMovEps,hd
	def pubvn_play(url):
		if '=' not in url:url,hd=getiMovEps(url)
		else:hd=login()
		body=make_request(url+'&server=3',headers=hd)
		id=re.search('iMov=(\d{4,6})&iEps=(\d{5,7})',url);mov_id=xshare_group(id,1);eps_id=xshare_group(id,2)
		log_id=xshare_group(re.search('log_id : (\d{5,7})',body),1)
		pub_id=xshare_group(re.search('pub_id : "(.+?)"',body),1)
		lte_id=xshare_group(re.search('lte_id : (\w{6,10})',body),1)
		sercur=xshare_group(re.search('sercur : (\w{6,10})',body),1)
		hash=xshare_group(re.search("hash : '(\w{8,10})'",body),1)
		dlink=xshare_group(re.search("file: '(.+?)'",body),1)
		data='action=update_last_watched&user_id=%s&mov_id=%s&eps_id=%s&time=93.78&per=1&hash=%s'
		data=data%(log_id,mov_id,eps_id,hash)
		make_post(home+'movie/vn/vasi_blahblah.php',hd,data)
		make_request(home+'phim/logout.php',headers=hd);xbmcsetResolvedUrl(dlink+'?start=0')
	def pubvn_Eps(url):
		body=make_request(url+'&server=3');temp=[];items=[]
		epslist=re.findall('{"ver_id":(.+?),"ver_name":"(.+?)","eps_list":(\[.+?\])}',body,re.DOTALL)
		for ver_id,ver_name,eps_list in epslist:
			if ver_name not in temp:
				temp.append(ver_name)
				try:
					for eps in eval(re.sub('true|false','""',eps_list)):
						href='%s=%s=%d'%(url.split('=')[0],url.split('=')[1],eps['id'])
						name=eps['name']+'-'+ver_name.strip() if len(epslist)>2 else eps['name']
						items.append((name,href))
				except:pass
		return items
	def pubvn_page(body,items=[]):
		pattern='</p></a>(.+?)<a href=".+?">.{,20}<img src="(.+?)".{,200}<a href="(.+?)" title="(.+?)">'
		for eps,img,href,title in re.findall(pattern,body,re.DOTALL):
			eps=xshare_group(re.search('<p>(\d{1,3}/\d{1,3})</p>',eps.strip()),1).split('/')[0]>'1'
			if eps:items.append(('%s%s[/COLOR]'%(color['pubvn'],title),home+href,img,'folder'))
			else:items.append((title,home+href,img,'play'))
		return items
	def pubvn_search(string,page=1):
		data='boxphim=Filter&txtsearch=%s&page=%d'%(urllib.quote_plus(string),page)
		body=make_post(home+'phim/aj/advancesearch.php',data=data).body
		for name,href,img,type in pubvn_page(body):
			addir(name,href,img,fanart,mode,page,query=type,isFolder=(type=='folder'))
		trangcuoi=xshare_group(re.search('class="vpage(\d{1,4})".{,5}>Cuối</a></li>',body),1).strip()
		if trangcuoi and int(trangcuoi)>page:
			name=color['trangtiep']+'Trang tiếp theo: trang %s/%s[/COLOR]'%(str(page+1),trangcuoi)
			addir(name,url,img,fanart,mode,page=page+1,query=string,isFolder=True)
		return ''
	def pubvn_make_txt(items,temps=[]):
		txtfile=joinpath(data_path,'pubvn'+datetime.date.today().strftime("%d")+'.txt')
		for href,name,img in items:
			body=make_request(home+href)
			thread_id=xshare_group(re.search('/bar/threads/(\d{3,6})',body),1)
			eps=xshare_group(re.search('<p>(\d{1,3}/\d{1,3})</p>',body),1);page=0
			if eps.split('/')[0]>'1':page=1;name=color['pubvn']+name+'[/COLOR]'
			temps.append((name,home+'/bar/dodamde/'+thread_id,img,page))
		if temps:delete_files(data_path,mark='pubvn');makerequest(txtfile,string=str(temps),attr='w')
	if query=='pubvn.tv':
		name=color['search']+"Search trên pubvn.tv (pub.vn)[/COLOR]"
		addir(name,url,icon['icon'],mode=mode,query='search',isFolder=True)
		body=make_request(home+'phim/home.php')
		#blmenu_childs=re.findall('<li><a menuid = "(.+?)" tabid="(.+?)">(.+?)</a></li>',body)
		for name in re.findall('<a class="Title_menu">(.+?)</a>',body):
			page+=1;name='%s%s[/COLOR]'%(color['pubvn'],name)
			addir(name,'Title_menu',img,fanart,mode,page,query='blmenu_childs',isFolder=True)
		body=body[body.find('Phim Hot'):body.find('<a>Phim lẻ</a>')]
		phimhots=re.findall('<a href="(.+?)" class=".+?" title="(.+?)\|.{,2000}src="(.+?)"',body,re.DOTALL)
		name='%sPhim HOT[/COLOR]'%color['pubvn']
		addir(name,'Phim_Hot',img,fanart,mode,page,query=query,isFolder=True)
		temp=[('Phim lẻ','32','126'),('Phim bộ Âu - Mỹ','60-1','126-1'),('Phim bộ Châu Á','60-2','126-2')]
		for name,cat_id,type in temp:
			addir('%s%s[/COLOR]'%(color['pubvn'],name),'Home_Main',img,fanart,mode,page=1,query=cat_id,isFolder=True)
			if myaddon.getSetting('phim18')=="true":
				name='%s%s[/COLOR]'%(color['pubvn'],name+' - 18+')
				addir(name,'Home_Main',img,fanart,mode,page=1,query=type,isFolder=True)
		endxbmc();pubvn_make_txt(phimhots)
	elif query=='search':make_mySearch('',url,'','',mode,'get')
	elif query=="INP":pubvn_search(make_mySearch('',url,'','','','Input'))
	elif url=='pubvn.tv':page=1 if 'Trang tiếp theo' not in name else page;pubvn_search(query,page)
	elif url=='Title_menu':
		body=make_request(home+'phim/home.php')
		blmenu_childs=re.findall('<li><a menuid = "(.+?)" tabid="(.+?)">(.+?)</a></li>',body)
		for menuid,tabid,name in blmenu_childs:
			if int(tabid)==page:
				addir('%s%s[/COLOR]'%(color['pubvn'],name),'blmenu_child',img,fanart,mode,page,query=menuid,isFolder=True)
	elif url=='blmenu_child':
		data='tabid=%s&menuid=%s'%(str(page),query)
		body=make_post(home+'phim/aj/aj_top.php',data=data).body
		pattern='<div class="film_poster">(.+?)<a href="(.+?)" class="tooltip1" title="(.+?)\|.{,2000}src="(.+?)" (.{,500}End class = film_poster)'
		for s1,href,title,img,s2 in re.findall(pattern,body,re.DOTALL):
			s1=xshare_group(re.search('<p>(\d{1,3}/\d{1,3})</p>',s1.strip()),1).split('/')[0]>'1'
			s2=xshare_group(re.search('<p>(\d{1,3}/\d{1,3})</p>',s2.strip()),1).split('/')[0]>'1'
			if s1 or s2:addir('%s%s[/COLOR]'%(color['pubvn'],title),home+href,img,fanart,mode,page,query='folder',isFolder=True)
			else:addir(title,home+href,img,fanart,mode,page,query='play')
	elif query=='folder':
		url,hd=getiMovEps(url)
		for eps,href in pubvn_Eps(url):
			addir(eps+' - '+re.sub('\[.?COLOR.{,12}\]','',name),href,img,fanart,mode,page,query='play')
	elif url=='Phim_Hot':
		fn='pubvn'+datetime.date.today().strftime("%d")+'.txt';txtfile=joinpath(data_path,fn)
		if not os.path.isfile(txtfile):
			for file in os.listdir(data_path):
				if 'pubvn' in file:txtfile=joinpath(data_path,file);break
		try:items=eval(makerequest(txtfile))
		except:items=[]
		if items:
			for name,href,img,page in items:
				addir(name,href,img,fanart,mode,page=page,query='dodamde',isFolder=(page==1))
		else:mess(u'Đang cập nhật dữ liệu - chọn lại sau 30 giây nữa nhé!')
	elif query=='dodamde':
		iMovEps=xshare_group(re.search('id="player" src="(.+?)"',make_request(url)),1)
		if page==0:pubvn_play(home+iMovEps)
		else:
			for eps,href in pubvn_Eps(home+iMovEps):
				addir(eps+' - '+re.sub('\[.?COLOR.{,15}\]','',name),href,img,fanart,mode,page,query='play')
	elif url=='Home_Main':
		url=home+'phim/aj/';data='cat_id=%s&type=%s&page=%s'
		if 'Phim lẻ' in name:url+='aj_phimle.php';data='cat_id=%s&page=%s'%(query,str(page))
		else:url+='aj_series.php';data=data%(query.split('-')[0],query.split('-')[1],str(page))
		body=make_post(url,data=data).body
		for title,href,img,type in pubvn_page(body):
			addir(title,href,img,fanart,mode,page,query=type,isFolder=(type=='folder'))
		trangcuoi=xshare_group(re.search('class="catpage(\d{1,4})".{,5}>Cuối</a></li>',body),1).strip()
		if trangcuoi and int(trangcuoi)>page:
			name=re.sub('\[.?COLOR.{,12}\]','',name).split('*')[0].strip()
			name=color['trangtiep']+'%s * Trang tiếp theo: trang %s/%s[/COLOR]'%(name,str(page+1),trangcuoi)
			addir(name,'Home_Main',img,fanart,mode,page=page+1,query=query,isFolder=True)
	elif query=='play':pubvn_play(url)

def hdviet(name,url,img,mode,page,query):
	color['hdviet']='[COLOR darkorange]';icon['hdviet']=os.path.join(iconpath,'hdviet.png')
	home='http://movies.hdviet.com/';direct_link='https://api-v2.hdviet.com/movie/play?movieid=%s'
	def namecolor(name):return '%s%s[/COLOR]'%(color['hdviet'],name)
	def login():
		u=myaddon.getSetting('userhdviet');p=myaddon.getSetting('passhdviet')
		import hashlib;data=urllib.urlencode({'email':u,'password':hashlib.md5(p).hexdigest()})
		response=make_post('http://movies.hdviet.com/dang-nhap.html',hd,data)
		try:resp=response.json
		except:resp={u'r': u'Lỗi đăng nhập hdviet.com', u'e': 3}
		mess(u'HDViet.com: '+resp['r'],1000);return (response.cookiestring if resp['e']==0 else '')
	def additems(body):
		links=re.findall('<a href="(.{,200})"><img src="(.+?)"(.+?)"h2-ttl3">(.+?)<span>(.+?)</span>',body)
		for link,img,temp,ttl3,title in links:
			title=ttl3.replace('&nbsp;','')+'-'+title
			isFolder=xshare_group(re.search('"labelchap2">(\d{1,3})</span>',temp),1)
			link=xshare_group(re.search('id="tooltip(\d{,10})"',temp),1).strip()
			if not isFolder:addir(title,link,img,fanart,mode,page,query='play')
			elif isFolder=='1':hdviet(title,link,img,mode,page,'folder')
			else:addir(namecolor(title),link,img,fanart,mode,page,query='folder',isFolder=True)
	def getResolvedUrl(id):
		response=make_request(direct_link%id,headers=hd,resp='j')
		return response['r'] if response else ''
	def hdviet_search(string):
		url='http://movies.hdviet.com/tim-kiem.html?keyword=%s'%urllib.quote(string)
		hdviet(name,url,img,mode,page,query='timkiem')
	if query=='hdviet.com':
		name=color['search']+"Search trên hdviet.com[/COLOR]"
		addir(name,'http://movies.hdviet.com/tim-kiem.html',icon['icon'],mode=mode,query='search',isFolder=True)
		body=make_request(home)
		items=re.findall('"mainitem" menuid="(.+?)" href="(.+?)" title=".+?">(.+?)</a>',body)
		for id,href,name in items:
			addir(namecolor(name),home,icon['hdviet'],fanart,mode,page,query=id,isFolder=True)
		addir(namecolor('Thể loại phim'),'the-loai',icon['icon'],mode=mode,query='the-loai-phim',isFolder=True)
		items=re.findall('"h2-ttl cf">.+?<a href="(.+?)" title=".+?" >(.+?)</a>',body)
		tempbody=body[body.find('h2-ttl cf')+10:]
		for href,name in items:
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,query='1',isFolder=True)
			subbody=tempbody[:tempbody.find('h2-ttl cf')];tempbody=tempbody[tempbody.find('h2-ttl cf')+10:]
			additems(subbody)
	elif query=='search':make_mySearch('','hdviet.com','','',mode,'get')
	elif query=="INP":hdviet_search(make_mySearch('',url,'','','','Input'))
	elif url=='hdviet.com':page=1 if 'Trang tiếp theo' not in name else page;hdviet_search(query)
	elif query=='the-loai-phim':
		for href,name in re.findall('<p><a href="(.+?)" title=".+?">(.+?)</a></p>',make_request(home)):
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,query='theloai',isFolder=True)
	elif query=='3' and url==home:#Phim lẻ
		items=re.findall('<a href="(.+?)" .?menuid="(.+?)" .?title=".+?" >(.+?)</a>',make_request(home))
		for href,id,name in items:
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,query=id,isFolder=True)
	elif query=='10' and url==home:#Phim bộ
		body=make_request(home)
		items=re.findall('<a href="(.+?)" menuid="(.+?)" title=".+?">(.+?)</a>',body)
		items+=re.findall('<a class="childparentlib" menuid="(.+?)" href="(.+?)" title=".+?">(\s.*.+?)</a>',body)
		for href,id,name in items:
			if 'au-my' in href:name='Phim bộ Âu Mỹ %s'%name.strip()
			elif 'hong-kong' in href:name='Phim bộ Hồng Kông %s'%name.strip()
			elif 'trung-quoc' in href:name='Phim bộ Trung Quốc %s'%name.strip()
			else:name='Phim bộ %s'%name.strip()
			if href in '38-39-40':temp=href;href=id;id=temp
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,query=id,isFolder=True)
	elif query=='folder':
		href='http://movies.hdviet.com/lay-danh-sach-tap-phim.html?id=%s'%url
		response=make_request(href,resp='j')
		if not response:return
		for eps in range(1,int(response["Sequence"])+1):
			title='Tập %s/%s-%s'%(format(eps,'0%dd'%len(response['Episode'])),str(response['Episode']),re.sub('\[.?COLOR.{,12}\]','',name))
			addir(title,'%s_e%d'%(url,eps),img,fanart,mode,page,query='play')
	elif query=='play':
		links=getResolvedUrl(url);linksub='';maxspeedlink=''
		if not links:mess(u'[COLOR red]HDViet.com: Get link thất bại[/COLOR]');return
		link=re.sub('_320_480_','_320_1920_vip_',links['LinkPlay'])
		href=link+'?audioindex=1' if myaddon.getSetting('hdvietaudio')=='true' else link
		allresolution=make_request(href)
		if len(allresolution)<100:
			href=link;allresolution=make_request(href)
			if len(allresolution)<100:mess(u'[COLOR red]HDViet.com: Get maxspeed link thất bại[/COLOR]');return
		hd['Cookie']=login();resolutions=['1920','1792','1280','1024','800','640','480']
		if not hd['Cookie']:resolution=4
		else:
			body=make_request('http://movies.hdviet.com/dang-ky-hdvip.html',headers=hd)
			maxresolution=myaddon.getSetting('hdvietresolution')
			if xshare_group(re.search('<span>HDVip</span>: (\d{1,3}) ngày</a>',body),1):
				resolution=0 if maxresolution=='1080' else 2
			else:resolution=3
		make_post('http://movies.hdviet.com/dang-xuat.html',headers=hd).close
		if resolution>2 and 'thai' not in myaddon.getSetting('userhdviet'):
			mess(u'[COLOR red]Hãy gia hạn acc VIP để có độ phân giải tối đa nhé.[/COLOR]',title=u'HDViet thông báo')
			xbmc.sleep(5000)
		for res in range(resolution,len(resolutions)):
			maxspeedlink=xshare_group(re.search('(http.+%s.+)\s'%resolutions[res],allresolution),1)
			if maxspeedlink:break
		if not maxspeedlink: maxspeedlink=href
		for source in ['Subtitle','SubtitleExt','SubtitleExtSe']:
			try:
				linksub=links['%s'%source]['VIE']['Source']
				if linksub:download_subs(linksub);break
			except:pass
		xbmcsetResolvedUrl(maxspeedlink,urllib.unquote(os.path.splitext(os.path.basename(linksub))[0]))
	else:
		body=make_request(url);body=body[body.find('box-movie-list'):body.find('h2-ttl cf')];additems(body)
		pages=re.findall('<li class=""><a href="(.+?)">(.+?)</a></li>',body[body.find('class="active"'):])
		if pages:
			pagenext=pages[0][1];pageend=pages[len(pages)-1][1]
			name='%sTrang tiếp theo: trang %s/%s[/COLOR]'%(color['trangtiep'],pagenext,pageend)
			addir(name,pages[0][0],img,fanart,mode,page,query,isFolder=True)

def hayhaytv(name,url,img,mode,page,query):
	color['hayhaytv']='[COLOR tomato]';icon['hayhaytv']=os.path.join(iconpath,'hayhaytv.png')
	home='http://www.hayhaytv.vn/';ajax=home+'ajax_hayhaytv.php'
	def namecolor(name):return '%s%s[/COLOR]'%(color['hayhaytv'],name)
	def login():
		u=myaddon.getSetting('userhayhay');p=myaddon.getSetting('passhayhay')
		data=urllib.urlencode({'email':u,'password':p,'remember_account':0})
		response=make_post('http://www.hayhaytv.vn/ajax_jsonp.php?p=jsonp_login',data=data)
		makerequest(joinpath(data_path,'hayhaytv.cookie'),response.cookiestring,attr="wb")
		return response.cookiestring
	def getmaxspeedlink(url,headers):
		body=make_request(url,headers=headers)
		id=xshare_group(re.search('FILM_ID\D{3,7}(\d{3,6})',body),1) if ".sub'" in body else ''
		url=xshare_group(re.search("initVideoUrl.+'(.+?)'",body),1)
		if 'cdnviet.com' not in url:url=xshare_group(re.search("initVideoUrlOld.+'(.+?)'",body),1)
		return url,id
	def getdata(id):#Đoạn code này sử dụng mã bảo mật từ add-on HayHayTV.vn
		url='https://www.fshare.vn/folder/5VNFUPO32P6F'
		hd=xshare_group(re.search('<title>.*xx(.+?)xx.*</title>',make_request(url)),1).split('-')
		data='device=xshare&secure_token=1.0&request='+urllib.quote('{"movie_id":"%s"}'%id)
		response=make_post('http://api.hayhaytv.vn/movie/movie_detail',{hd[0]:'%s %s'%(hd[1],hd[2])},data)
		try:json=response.json['data']
		except:json={}
		return json
	def getitems(body):
		p='<a data-tooltip.{,100}href="(.+?)".{,500}data-original="(.+?)".{,300}'
		p+='class="orange_color">(.+?)</span>.{,100}<span>(.*?)</span>'
		for href,img,name_e,name_v in re.findall(p,body,re.DOTALL):
			name=name_v+'-'+color['subscene']+name_e+'[/COLOR]' if name_v else name_e
			addir(name,href,img,fanart,mode,page,query='play')
	def hayhaytv_search(string):
		url='http://www.hayhaytv.vn/tim-kiem/%s/trang-1'%'-'.join(s for s in string.split())
		hayhaytv(name,url,img,mode,page=1,query='M3')

	if query=='hayhaytv.vn':
		name=color['search']+"Search trên hayhaytv.vn[/COLOR]"
		addir(name,'http://www.hayhaytv.vn/tim-kiem/',icon['icon'],mode=mode,query='search',isFolder=True)
		body=make_request(home)
		for href,name in re.findall('menu_fa_text.+?" href="(.+?)".*>(.+?)</a>',body):
			if name in 'PHIM LẺ-PHIM BỘ-SHOW':
				addir(namecolor(name),href,icon['hayhaytv'],fanart,mode,page,query='M1',isFolder=True)
		body=body[body.find('"title_h1_st1"'):body.find('"slider_box_sim slider_clip_box"')]
		items=re.findall('"title_h1_st1">.{,20}<a.{,20}href="(.+?)".{,20}>(.+?)</a>.{,20}</h2>',body,re.DOTALL)
		mucs={'su-kien':'q=su-kien&p=eventfilms&key=32386E61&page=1','phim-le':'p=phimle&page=1',
			'phim-bo':'p=phimbo&page=1','phim-chieu-rap':'p=phimle&phimchieurap&page=1','shows':'p=tvshow&page=1'}
		for href,name in items:
			muc=xshare_group(re.search('http://www.hayhaytv.vn/([\w|-]{1,20})',href),1)
			if muc and mucs[muc]:
				href='http://www.hayhaytv.vn/ajax_ht.php?'+mucs[muc] if 'su-kien' in href else ajax+'?'+mucs[muc]
				name=' '.join(s for s in name.replace('\n','').split() if s)
			else:name=name.replace('JJ','Just Japan')
			addir(namecolor(name),href,img,fanart,mode,page=1,query='M3' if 'su-kien' in href else 'M2',isFolder=True)
	elif query=='search':make_mySearch('','hayhaytv.vn','','',mode,'get')
	elif query=="INP":hayhaytv_search(make_mySearch('',url,'','','','Input'))
	elif url=='hayhaytv.vn':page=1 if 'Trang tiếp theo' not in name else page;hayhaytv_search(query)
	elif query=='M1':
		theloai=os.path.basename(url).replace('-','')
		if theloai=='shows':theloai='tvshow'
		body=make_request('http://www.hayhaytv.vn/tim-kiem');pattern='http.+/\w{1,6}-'
		body=body[body.find(url):];body=body[:body.find('mar-r20')]
		for href,name in re.findall('href="(.+?)".*?>(.+?)</a></li>',body):
			if href==url:href='%s?p=%s&page=1'%(ajax,theloai)
			else:id=re.sub(pattern,'',href);href='%s?p=%s&q=filter&id=%s&page=1'%(ajax,theloai,id)
			addir(namecolor(name),href,img,fanart,mode,page=1,query='M2',isFolder=True)
	elif query=='M2':
		if 'ajax' in url:
			body=make_post(re.sub('page=\d{1,3}','page=%d'%page,url)).body
			pattern='tooltip="(.+?)" href="(.+?)">\s.*"(http://img.+?)".*\s.*color">(.*?)<.*\s.*>(.*?)</span>'
			items=re.findall(pattern,body)
			ids=dict((re.findall('id="(sticky\d{1,3})".{,250}Số tập[\D]{,30}(\d{1,4})',body,re.DOTALL)))
			for stic,href,img,name_e,name_v in items:
				name=name_v+'-'+name_e if name_v else name_e
				if ids.has_key(stic) and ids[stic].strip()>'1':#? in ids.values()
					addir(namecolor(name),href,img,fanart,mode,page=1,query='folder'+ids[stic],isFolder=True)
				else:addir(name,href,img,fanart,mode,page,query='play')
			if len(items)>31 or ('p=tvshow' in url and len(items)>11):
				name='%sTrang tiếp theo: trang %s[/COLOR]'%(color['trangtiep'],page+1)
				addir(name,url,img,fanart,mode,page+1,query,isFolder=True)
			return
		elif 'jj' in url:#Just Japan
			pattern='href="(.+?)">\s.*src="(.+?)".*\s.*\s.*\s.*>(.*?)</a></p>\s.*>(.*?)</a></p>'
			for href,img,name_e,name_v in re.findall(pattern,make_request(url)):
				name=name_v+'-'+color['subscene']+name_e+'[/COLOR]' if name_v else name_e
				addir(name,href,img,fanart,mode,page,query='play')
	elif query=='M3':
		body=make_request(url);body=body[body.find('slide_child_div_dt'):];body=body[:body.find('class="paging"')]
		pattern='href="(.+?)".*\s.*alt="poster phim (.+?)" src="(.+?)"'
		items=re.findall(pattern,body)
		for href,name,img in items:
			if re.search('Tap-\d{1,3}',href):
				addir(namecolor(name),href,img,fanart,mode,page=1,query='folder',isFolder=True)
			else:addir(name,href,img,fanart,mode,page,query='play')
		if len(items)>14 or (len(items)>7 and 'su-kien' in url):
			temp='trang-' if 'trang-' in url else 'page=';url=re.sub('%s\d{1,3}'%temp,'%s%d'%(temp,page+1),url)
			name='%sTrang tiếp theo: trang %s[/COLOR]'%(color['trangtiep'],page+1)
			addir(name,url,img,fanart,mode,page+1,query,isFolder=True)
	elif query[:6]=='folder':
		if 'xem-show' in url:pattern='href="(.+?)".*src=".+?"\D*(\d{1,3})<'
		else:pattern='<a class=".*?" href="(.+?)"\D*(\d{1,3})<'
		resp=make_request(url,resp='o');body=resp.body if resp.status==200 else make_request(resp.headers['location'])
		items=re.findall(pattern,body)
		if not query[6:]:
			json=getdata(xshare_group(re.search('FILM_ID\D{3,7}(\d{3,6})',body),1))
			if json:query+=json['total_episode'].encode('utf-8')
		for href,epi in items:
			addir('Tập %s/%s-%s'%(epi,query[6:],re.sub('\[.?COLOR.{,12}\]','',name)),href,img,fanart,mode,page,query='play')
	elif query=='play':
		hd['Cookie']=makerequest(joinpath(data_path,'hayhaytv.cookie'))
		href,id=getmaxspeedlink(url,hd);sub=''
		if not href:hd['Cookie']=login();href,id=getmaxspeedlink(url,hd)
		if href:
			if id:
				json=getdata(id)
				if json:sub=download_subs(json['vn_subtitle'])
			xbmcsetResolvedUrl(href,json['vn_subtitle'] if sub else '')

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
homnay=datetime.date.today().strftime("%d/%m/%Y")
url=name=fanart=img=date=query=end=''
mode=page=0;temp=[]

try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:img=urllib.unquote_plus(params["img"])
except:pass
try:fanart=urllib.unquote_plus(params["fanart"])
except:pass
try:mode=int(params["mode"])
except:pass
try:page=int(params["page"])
except:pass
try:query=urllib.unquote_plus(params["query"])
except:pass#urllib.unquote
print "Main---------- Mode: "+str(mode),"URL: "+str(url),"Name: "+str(name),"query: "+str(query),"page: "+str(page)

if not mode:
	init_file();open_category("MMN");endxbmc();data_update()
	if myaddon.getSetting('checkdatabase')=='true' or os.path.isfile(joinpath(data_path,'checkdatabase.txt')):
		data_download()
elif mode==2:end=google_search(url,query,mode,page)
elif mode==3:end=resolve_url(url)
elif mode==4:vp_phimmoi()
elif mode==5:vp_xemnhieu()
elif mode==6:end=phimFshare(name,url,mode,page,query)
elif mode==7:end=fptplay(name,url,img,mode,page,query)
elif mode==8:hdvietnam(name,url,img,fanart,mode,page,query)
elif mode==9:make_mySearch(name,url,img,fanart,mode,query)
elif mode==10:open_category(query);endxbmc();vp_make_datanew()
elif mode==11:make_myFshare(name,url,img,fanart,mode,query)
elif mode==12:make_mylist(name,url,img,fanart,mode,query)
elif mode==13:end=xshare_search(name,url,query,mode,page)
elif mode==15:end=id_2url(url,name,mode,page,query)
elif mode==16:end=play_maxspeed_link()
elif mode==17:end=megabox(name,url,mode,page,query)
elif mode==18:dangcaphd(name,url,img,mode,page,query)
elif mode==19:pubvn(name,url,img,mode,page,query)
elif mode==20:end=vp_update()
elif mode==21:vuahd(name,url,img,mode,page,query)
elif mode==22:hdviet(name,url,img,mode,page,query)
elif mode==23:hayhaytv(name,url,img,mode,page,query)
elif mode==31:end=ifile_update()
elif mode==34:ifile_home(name,url,img,mode,page,query)
elif mode==38:doc_Trang4share(url)#38
elif mode==47:daklak47(name,url,img)
elif mode==90:end=doc_TrangFshare(name,url,img,fanart,query)
elif mode==91:main_menu(url,page,mode,query)
elif mode==94:end=subscene(name,url,query)
elif mode==95:lay_link_tenlua(url)
elif mode==96:end=doc_thumuccucbo(name,url,img,fanart,mode,query)
elif mode==97:doc_list_xml(url,name,page)
elif mode==98:make_favourites(name,url,img,fanart,mode,query)
elif mode==99:myaddon.openSettings();end='ok'
if not end or end not in 'no-ok':endxbmc()
#https://urlfetch.readthedocs.org/en/v0.5.3/examples.html
#http://hdonline.vn/ 1.207 hhtv 2, fpt 4, hplus.com.vn 5, phimhd3s 8, 
#addir(name,url,img,fanart,mode,page,query,isFolder)
#addirs(name,href,img='',fanart='',query='')
#ID co pass: THZA19WGMT Pass: thanhcoti 8357 8490 9262 9580
#Nếu có thể bác làm thêm mấy Addons trả phí, có Acc và pass có đăng nhập như kiểu fshare cho mấy Apk hot như HDon, vuahd...
#mình thấy pub.vn cũng nhiều phim và đường truyền rất lẹ ,nên nếu làm được trang này thì hay hơn là vuahd đó
# add thêm phần phụ lục (WEB-DL, HDTV; Bluray Remux; mHD, SD; Bluray nguyên gốc) vào trong phần Chia sẻ phim - Fshare.vn
#acc VIP còn hạn đền tháng 11. bác kiểm tra giúp e nhé :
#mail : anhvustore1@gmail.com
#pass : anhvustore
