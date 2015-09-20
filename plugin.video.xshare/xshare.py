# -*- coding: utf-8 -*-
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,urllib,re,os,unicodedata,datetime,random,json

myaddon=xbmcaddon.Addon()
home=xbmc.translatePath(myaddon.getAddonInfo('path'));datapath=xbmc.translatePath(myaddon.getAddonInfo('profile'))
iconpath=os.path.join(datapath,'icon');datapath=os.path.join(datapath,'data')
sys.path.append(os.path.join(home,'resources','lib'));from urlfetch import get,post
search_file=os.path.join(datapath,"search.xml");data_path=os.path.join(home,'resources','data')
rows=int(myaddon.getSetting('sodonghienthi'));googlesearch=myaddon.getSetting('googlesearch')

media_ext=['aif','iff','m3u','m4a','mid','mp3','mpa','ra','wav','wma','3g2','3gp','asf','asx','avi','flv','mov','mp4','mpg','mkv','m4v','rm','swf','vob','wmv','bin','cue','dmg','iso','mdf','toast','vcd','ts','flac','m2ts']
color={'fshare':'[COLOR gold]','vaphim':'[COLOR gold]','phimfshare':'[COLOR khaki]','4share':'[COLOR blue]','tenlua':'[COLOR fuchsia]','fptplay':'[COLOR orange]','trangtiep':'[COLOR lime]','search':'[COLOR lime]','ifile':'[COLOR blue]','hdvietnam':'[COLOR red]','xshare':'[COLOR blue]','subscene':'[COLOR green]','megabox':'[COLOR orangered]','dangcaphd':'[COLOR yellow]'};icon={}
for hd in ['xshare','4share', 'dangcaphd', 'downsub', 'favorite', 'fptplay', 'fshare', 'gsearch', 'hdvietnam', 'icon', 'id', 'ifiletv', 'isearch', 'khophim', 'maxspeed', 'megabox', 'movie', 'msearch', 'myfolder', 'myfshare', 'phimfshare', 'serverphimkhac', 'setting', 'tenlua', 'vaphim']:
	icon.setdefault(hd,os.path.join(iconpath,'%s.png'%hd))
hd = {'User-Agent' : 'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}

def mess(message, timeShown=10000,title=''):
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

def s2u(s):
    if isinstance(s,str):s=s.decode('utf-8')
    return s
	
def unescape(string):
	return ' '.join(re.sub('&.+;',xsearch('&(\w).+;',s,1),s) for s in string.split())

def u2s(s):
	if isinstance(s,unicode):s=s.encode('utf-8')
	return s

def clean_string(string):
	return ' '.join(s for s in re.sub('Fshare|4share|Tenlua','',string).split())

def joinpath(p1,p2):
	try:p=os.path.join(p1,p2)
	except:p=os.path.join(p1,str2u(p2))
	return p

def init_file():
	datafolder=xbmc.translatePath(myaddon.getAddonInfo('profile'))
	for folder in (datafolder,datapath,iconpath,myfolder,subsfolder,tempfolder):
		if not os.path.exists(folder):os.mkdir(folder)
	xmlheader='<?xml version="1.0" encoding="utf-8">\n';p=datapath;q=myfolder
	for i in [(p,'search.xml'),(p,'hdvietnam.xml'),(p,'favourites.xml'),(p,'phimmoi.xml'),(p,'fpt.xml'),(q,'mylist.xml')]:
		file=joinpath(i[0],i[1])
		if not os.path.isfile(file):makerequest(file,xmlheader,'w')

def xshare_group(object,group):
	return object.group(group) if object else ''

def sub_body(content,s1,s2):
	if not isinstance(content,str):content=str(content)
	if s1 and s2:result=content[content.find(s1):content.find(s2)]
	elif s1:result=content[content.find(s1):]
	elif s2:result=content[:content.find(s2)]
	else:result=content
	return result

def json_rw(file,dicts={},key=''):
	if dicts:makerequest(joinpath(datapath,file),json.dumps(dicts),'w')
	else:
		try:dicts=json.loads(makerequest(joinpath(datapath,file)))
		except:dicts={}
		if key:dicts=dicts.get(key,())
	return dicts

def delete_files(folder,mark='',temp='ok'):
	for file in os.listdir(folder):
		if os.path.isfile(joinpath(folder,file)) and (not mark or mark in file):
			try:os.remove(joinpath(folder,file))
			except:temp='';pass
	return temp

def endxbmc():
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def xbmcsetResolvedUrl(url,name=''):
	item=xbmcgui.ListItem(path=url)
	if 'Maxlink' in name:
		if name!='Maxlink':name=name.replace('Maxlink','');item.setInfo('video', {'Title':name})
		else:item.setInfo('video', {'Title':os.path.basename(url)})
		name=''
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item);endxbmc()
	if myaddon.getSetting('autoload_sub')=='true' and name!='xshare':
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
	def xquote(href):return urllib.quote_plus(href)
	if '18+' in name and myaddon.getSetting('phim18')=="false":return
	name=unescape(re.sub(',|\|.*\||\||\<.*\>','',u2s(name)))
	item=xbmcgui.ListItem(name,iconImage=img,thumbnailImage=img)
	query=menuContext(name,link,img,fanart,mode,query,item)
	item.setInfo(type="Video", infoLabels={"title":name})
	if not fanart:fanart=joinpath(home,'fanart.jpg')
	item.setProperty('Fanart_Image',fanart)
	li='%s?name=%s&url=%s&img=%s&fanart=%s&mode=%d&page=%d&query=%s'
	li=li%(sys.argv[0],urllib.quote(name),xquote(link),xquote(img),xquote(fanart),mode,page,query)
	if not isFolder:item.setProperty('IsPlayable', 'true')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),li,item,isFolder)

def addirs(name,href,img='',fanart='',query=''):
	name=clean_string(name)
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
		if str2u('chia sẻ') in str2u(name):name=color['trangtiep']+name+'[/COLOR]'
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
	elif query in 'hdvietfolder-hdvietplay':
		item.addContextMenuItems(hdvietContext(name,link,img,fanart,mode))
	return query

def makeContext(name,link,img,fanart,mode,query):
	if query=='Add to MyFshare favorite':make='AddFavorite'
	elif query=='Remove from MyFshare favorite':make='RemoveFavorite'
	else:make=query.split()[0]
	if 'Rename' in make:colo=color['fshare']
	elif 'Remove' in make:colo=color['hdvietnam']
	else:colo=color['trangtiep']
	context=colo+query+'[/COLOR]'
	p=(myaddon.getAddonInfo('id'),mode,name,link,img,fanart,make)
	cmd='RunPlugin(plugin://%s/?mode=%d&name=%s&url=%s&img=%s&fanart=%s&query=%s)'%(p)
	return context,cmd

def hdvietContext(name,link,img,fanart,mode):
	context=color['trangtiep']+'Thêm vào phim yêu thích[/COLOR]'
	p=(myaddon.getAddonInfo('id'),mode,name,link.split('_')[0],img,fanart,'Themmucyeuthich')
	cmd='RunPlugin(plugin://%s/?mode=%d&name=%s&url=%s&img=%s&fanart=%s&query=%s)'%(p)
	command=[(context,cmd)]
	return command

def searchContext(name,link,img,fanart,mode):
	command=[(makeContext(name,link,img,fanart,9,'Rename item'))]
	command.append((makeContext(name,link,img,fanart,9,'Remove item')))
	return command

def favouritesContext(name,link,img,fanart,mode):
	def makecmd(mode,title):command.append((makeContext(name,link,img,fanart,mode,title)))
	command=[]
	if type(link)==unicode:link=link.encode('utf-8')
	if link in makerequest(joinpath(datapath,"favourites.xml")):	
		makecmd(98,'Rename in MyFavourites');makecmd(98,'Remove from MyFavourites')
	else:makecmd(98,'Add to MyFavourites')
	if 'www.fshare.vn' in link:
		if query=='MyFshare':makecmd(11,'Remove from MyFshare');makecmd(11,'Rename from MyFshare')
		else:makecmd(11,'Add to MyFshare')
		if query=='favorite':makecmd(11,'Remove from MyFshare favorite')
		else:makecmd(11,'Add to MyFshare favorite')
	if link in makerequest(joinpath(myfolder,'mylist.xml')):
		makecmd(12,'Rename in Mylist.xml');makecmd(12,'Remove from Mylist.xml')
	else:makecmd(12,'Add to Mylist.xml')
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
	def read_home():
		file=joinpath(tempfolder,'fshare.cookie');hd['Cookie']=makerequest(file)
		url='https://www.fshare.vn/home';body=make_request(url,hd)
		if not body:hd['Cookie']=loginfshare();body=make_request(url,hd);makerequest(file,hd['Cookie'],'w')
		return body
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
	elif query=='AddFavorite':href='https://www.fshare.vn/api/fileops/AddFavorite'
	elif query=='RemoveFavorite':href='https://www.fshare.vn/api/fileops/ChangeFavorite'
	else:return
	
	token=xshare_group(re.search('data-token="(.+?)"',read_home()),1)
	if not token:return
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
	elif query=='AddFavorite':
		data='{"token":"%s","link":"%s"}'%(token,url);noti='Add to My Fsha!re favorite'
	elif query=='RemoveFavorite':
		data='{"token":"%s","items":["%s"],"status":0}'%(token,os.path.basename(url))
		noti='Remove from My Fshare favorite'
	
	response=make_post(href,hd,data);logout_site(hd['Cookie'],'https://www.fshare.vn/logout')
	if response and response.status==200:
		mess(u'%s thành công'%noti)
		if not any(s for s in ['Add','Upload'] if s in query):
			xbmc.executebuiltin("Container.Refresh");mess(u'Đang reload list',1000)
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

def make_request(url,headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'},resp='b',maxr=0):
	try:
		if maxr==0:response=get(url,headers=headers)
		else:response=get(url,headers=headers,max_redirects=maxr)
		if resp=='o':resp=response
		else:
			if resp=='j':resp=response.json
			elif resp=='s':resp=response.status
			elif resp=='u':resp=response.text
			elif resp=='c':resp=response.cookiestring
			else:resp=response.body
			response.close()
	except: 
		mess(u'[COLOR red]Lỗi kết nối tới: %s[/COLOR]'%xshare_group(re.search('//(.+?)/',str2u(url)),1))
		resp='';print 'Make Request Error: %s'%url
	return resp#unicode:body=response.text

def make_post(url,headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'},data='',resp='o'):
	try:
		if data:response=post(url=url,headers=headers,data=data)
		else:response=post(url=url,headers=headers)
		if resp=='b':response=response.body
		elif resp=='j':response=response.json
	except:
		mess(u'Post link error: %s'%str2u(url));print 'Post link error: %s'%str2u(url)
		response={} if resp=='j' else ''
	return response

def makerequest(file,string='',attr='r'):
	file=str2u(file)
	if attr=='r':
		try:f=open(file);body=f.read();f.close()
		except:body=''
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
	try:filelength=int(dict(response.getheaders()).get('content-length'))
	except:filelength=10485760
	if filelength<10485760:#size<10MB
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
		if not response:return
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
	for id,title,href,img,fanart,category in vp_2fshare(url):
		if href not in temp:temp.append(href);addirs(title,href,img,fanart)
	return temp

def google_search_api(url,start,string,items):#url:fshare.vn,4share.vn,tenlua.vn,hdvietnam.com
	string_search = urllib.quote_plus('"%s"'%string)
	href = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=large&'
	href+='start=%s&q=site:%s+%s'%(start,url.lower(),string_search)
	json=make_request(href,resp='j')
	if not json:mess(u'Lỗi get %s'%str2u(href));return items,'end'
	if json['responseStatus']!=200:
		mess(u'Google: nghi ngờ lạm dụng Dịch vụ. Tự động chuyển sang web search',2000)
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
	pattern='<a server="(.+?)" category="(.+?)" mode="(\d\d)" color="(.*?)" icon="(.*?)">(.+?)</a>'
	items=re.findall(pattern,makerequest(joinpath(data_path,'category.xml')));q='';fanart=home+'/fanart.jpg'
	for server,category,mode,colo,icon,name in items:
		if (server!=query) or (("18" in category) and (myaddon.getSetting('phim18')=="false")):continue
		if query=='VPH' and mode!='10':q='vaphim.xml'
		elif query=='IFI' and mode!='10':q='ifiletv.xml'
		else:q=category
		name='[COLOR '+colo+']'+name+'[/COLOR]';icon=joinpath(iconpath,icon)
		addir(name,category,icon,fanart,mode=int(mode),page=0,query=q,isFolder=(mode!='16'))
	if q=='vaphim.xml':
		body=makerequest(joinpath(datapath,"vp_menu.txt"));icon=joinpath(iconpath,'vaphim.png')
		if not body:mess(u'[COLOR red]Đang update menu...[/COLOR]');vp_make_datanew();return
		for query,name in eval(body):
			if "18" in name and myaddon.getSetting('phim18')=="false":continue
			addir('%s%s[/COLOR]'%(color['vaphim'],name),'vaphim.xml',icon,fanart,92,1,query,True)

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
	contents='<?xml version="1.0" encoding="utf-8">\n'
	for id_tip,id_htm,category,img,fanart,href,fullname in items:
		content='<a id_tip="%s" id="%s" category="%s" img="%s" fanart="%s" href="%s">%s</a>\n'
		content=content%(id_tip,id_htm,category,img,fanart,href,fullname);contents+=content
	if makerequest(joinpath(datapath,filename),string=contents,attr='w'):
		mess(u'Đã cập nhật được %d phim'%len(items_new),2000,'[COLOR blue]%s auto update[/COLOR]'%filename)
	else: mess(u'Đã xảy ra lỗi cập nhật')
	return

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

def vp_page(url):#id,name,href,img,category
	pattern='<li class="post-(\d{4,6})(.+?)">.+?src="(.+?)".+?<h3 class="entry-title">'
	pattern+='<a href="(.+?)" rel="bookmark" >(.+?)</a>';items=[]
	for id,category,img,href,name in re.findall(pattern,make_request(url),re.DOTALL):
		category=' '.join(s.replace('category-','') for s in category.split() if 'category-' in s)
		if any(s for s in category.split() if s in 'game video-clip phn-mm ebooks'):continue
		name=' '.join(s for s in re.sub('<.+?>|&.+?; ?','',name).split());items.append((id,name,href,img,category))
	return items

def vp_2fshare(url):#id,title,href,img,fanart,category
	body=make_request(url);items=[]
	temp=re.search('<div id="post-(\d{4,6})" class="(.+?)">',body);id=xshare_group(temp,1)
	category=' '.join(s.replace('category-','') for s in xshare_group(temp,2).split() if 'category-' in s)
	if any(s for s in category.split() if s in 'game video-clip phn-mm ebooks'):return items
	temp=xshare_group(re.search('<title>(.+?)</title>',body),1)
	name=' '.join(s for s in re.sub('<.+?>|&.+?; ?|\||VaPhim.com','',temp).split())
	image=xshare_group(re.search('meta property="og:image" content="(.+?)"',body),1)
	pattern='<a href=".*?(fshare.vn/f.l.?e?r?/.+?|http://subscene.+?)".{,18}>(.+?)</a><'
	if 'collection' not in category:
		content=xshare_group(re.search('id="attachment_(.+?)"cf5_wpts_cl"',body,re.DOTALL),1)
		if not name:
			temp=xshare_group(re.search('class="wp-caption-text">(.+?)<',content),1)
			name=' '.join(s for s in re.sub('<.+?>|&.+?; ?','',temp).split())
		temp=re.findall('src="(.+?\.jpg|.+?\.png).{,10}"',content)
		img=temp[0] if len(temp)>0 else image;fanart=temp[1] if len(temp)>1 else ''
		for href,title in re.findall(pattern,content):
			if '//' in title:title=''
			title=' '.join(s for s in re.sub('<.+?>|&.+?; ?','',title).split() if s not in name)
			title='.'.join(s for s in title.split('.') if s not in name)
			title=name+' '+title;href=href.replace('fshare.vn','https://www.fshare.vn')
			items.append((id,title,href,img,fanart,category))
	else:
		body=body[body.find('"content"'):]
		links=re.findall(pattern,body)
		if body.find('"text-align: center;"')>0:begin='"text-align: center;"' 
		elif body.find('<p><strong>')>0:begin='<p><strong>'
		elif body.find('id="attachment_')>0:begin='id="attachment_'
		elif body.find('"wordpress-post-tabs"')>0:begin='"wordpress-post-tabs"'
		else:begin='"section"'
		for content in re.findall('(%s.+?"cf5_wpts_cl")'%begin,body,re.DOTALL):
			temp=re.findall('src="(.+?\.jpg|.+?\.png).{,10}"',content)
			img=temp[0] if len(temp)>0 else image;fanart=temp[1] if len(temp)>1 else ''
			title=xshare_group(re.search('<strong>(.+?)</strong>(</span></p>|</p>|<br />)',content),1)
			if not title:title=xshare_group(re.search('"wp-caption-text">(.+?)<',content),1)
			title=name+' '.join(s for s in re.sub('<.+?>|&.+?; ?','',title).split() if s not in name)
			for href,fn in re.findall(pattern,content):
				fn=' '.join(s for s in re.sub('<.+?>|&.+?; ?','',fn).split() if s not in title)
				fn='.'.join(s for s in fn.split('.') if s not in title)
				fn=title+' '+fn;href=href.replace('fshare.vn','https://www.fshare.vn')
				items.append((id,fn,href,img,fanart,category))
		if len(items)<len(links):
			temp='-'.join(os.path.basename(s[2]) for s in items)
			for href,fn in links:
				if os.path.basename(href) in temp:continue
				if '//' in fn:fn=''
				fn=' '.join(s for s in re.sub('<.+?>|&.+?; ?','',fn).split() if s not in name)
				fn='.'.join(s for s in fn.split('.') if s not in name)
				fn=name+' '+fn;href=href.replace('fshare.vn','https://www.fshare.vn')
				items.append((id,fn,href,image,fanart,category))
	return items

def vp_update(auto=True):#vp_2fshare(url):id,title,href,img,fanart,category
	mess(u'[COLOR green]Xshare database updating ...[/COLOR]',title='[COLOR gold]%s[/COLOR]'%homnay)
	if os.path.isfile(joinpath(tempfolder,'updating.txt')):return 'no'
	makerequest(joinpath(tempfolder,'updating.txt'),'','w')
	items=vp_page('http://vaphim.com/category/phim-2/');hrefs=[];items_new=[]
	if not items:delete_files(tempfolder);return 'No'
	try:ids=eval(makerequest(joinpath(datapath,"vp_update.txt")))
	except:ids=[]
	makerequest(joinpath(datapath,"vp_update.txt"),str([s[0] for s in items]),'w')
	items_old=doc_xml(joinpath(datapath,"vaphim.xml"));href_old=[s[5] for s in items_old]
	if auto:#update all in phim-2 page
		for href in [s[2] for s in items]:hrefs+=vp_2fshare(href)
	else:
		for href in [s[2] for s in items if s[0] not in ids]:hrefs+=vp_2fshare(href)
	for id,title,href,img,fanart,category in [s for s in hrefs if s[2] not in href_old]:
		items_new.append(('',id,category,img,fanart,href,title))
	if items_new:update_xml(items_new,items_old,"vaphim.xml")
	else:mess(u'Vaphim.com Không có phim mới...',5000,color['vaphim']+'Vaphim.com auto update[/COLOR]')
	delete_files(tempfolder)
	return 'ok'

def vp_list(name,url,img,mode,page,query):#92 query='phim-le'
	if url=='folder':
		items=list(set([s for s in doc_xml(joinpath(datapath,'vaphim.xml')) if s[1]==query]))
		for id_tip,id,category,img,fanart,href,name in items:addirs(name,href,img,fanart)
	elif url in 'vaphim.xml-collection':
		if url=='collection':query=url;url='vaphim.xml';page=1
		items=list(set([s for s in doc_xml(joinpath(datapath,'vaphim.xml')) if query in s[2]]))
		ids=list(set([s[1] for s in items]));ids.sort(reverse=True);pages=len(ids)/rows+1
		del ids[:(page-1)*rows];down=len(ids);del ids[rows:]
		for id in ids:vp_addir([s for s in items if s[1]==id])
		if down>rows:
			name=color['trangtiep']+'Trang tiep theo...trang %d/%d[/COLOR]'%(page+1,pages)
			addir(name,url,icon['icon'],mode=mode,page=page+1,query=query,isFolder=True)

def vp_addir(items):
	def namecolor(name):return '%s%s[/COLOR]'%(color['phimfshare'],name)
	if not items:return
	elif len(items)==1:
		for id_tip,id,category,img,fanart,href,name in items:addirs(name,href,img,fanart)
	else:
		id_tip,id,category,img,fanart,href,name=items[0]
		name='[COLOR goldenrod]'+subtitle_of_year(name).replace('(','')+'[/COLOR]'
		addir(name,'folder',img,fanart,92,1,id,True)
	
def vp_phimmoi():
	txtfile=joinpath(datapath,'vp_phimmoi.txt')
	if not os.path.isfile(txtfile):return
	ids=eval(makerequest(txtfile))
	items=[s for s in doc_xml(joinpath(datapath,'vaphim.xml')) if s[1] in ids]
	for id in ids:vp_addir([s for s in items if s[1]==id])

def vp_xemnhieu():
	txtfile=joinpath(datapath,'vp_xemnhieu.txt')
	if not os.path.isfile(txtfile):return
	names=eval(makerequest(txtfile))
	items=doc_xml(joinpath(datapath,'vaphim.xml'));i=0
	for name in names:vp_addir([s for s in items if name in s[6]])

def vp_chonloc():
	txtfile=joinpath(datapath,'vp_chonloc.txt')
	if not os.path.isfile(txtfile):return
	names=eval(makerequest(txtfile))
	items_xml=doc_xml(joinpath(datapath,"vaphim.xml"));ids=[s[1] for s in items_xml]
	for name in names:
		name=name.split('<br/>');nv=' '.join(s for s in re.sub('<.+?>|&.+?; ?','',name[0]).split())
		if len(name)<2:vp_addir([s for s in items_xml if nv in s[6]])
		else:ne=' '.join(s for s in name[1].split());vp_addir([s for s in items_xml if nv in s[6] or ne in s[6]])

def vp_make_datanew():
	body=make_request('http://vaphim.com/request/')
	names=re.findall('<li><a href=".+?" title=".+?">(.+?)<',body)
	if names:makerequest(joinpath(datapath,'vp_xemnhieu.txt'),string=str(names),attr='w')
	items=re.findall('<li><a href="/category.+?/([\w-]+?)/">(.+?)</a></li>',body)
	if items:makerequest(joinpath(datapath,"vp_menu.txt"),string=str(items),attr='w')
	body=make_request('http://vaphim.com/')
	items=re.findall('"post-(\d{4,6})(.+?)"',body);items_new=[]
	for id,category in items:
		category=' '.join(s.replace('category-','') for s in category.split() if 'category-' in s)
		if not any(s for s in category.split() if s in 'game video-clip phn-mm ebooks'):items_new.append(id)
	if items_new:makerequest(joinpath(datapath,'vp_phimmoi.txt'),string=str(items_new),attr='w')
	items=re.findall('rel="bookmark">(.+?)</a>',body)
	if items:makerequest(joinpath(datapath,"vp_chonloc.txt"),string=str(items),attr='w')

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
			string=para[7:].replace('(','.').replace(')','.')
			if ('phimfshare' in url) or ('hdvietnam' in url):
				r='href="(.+?)" img="(.+?)">(.*%s.*)</a>'%string
				items=[(s[1],s[1],s[0],s[2]) for s in re.findall(r,no_accent(body),re.IGNORECASE)]
			else:
				r='img="(.*?)" fanart="(.*?)" href="(.+?)">(.*%s.*)</a>'%string
				items=re.compile(r, re.I).findall(no_accent(body))
		else:
			if not para:r='<a id_tip="(.*?)" id="(.+?)" category="(.*?)" img="(.*?)" fanart="(.*?)" href="(.+?)">(.+?)</a>'
			else: #Doc theo category
				r='<a.*id="(.+?)" category=".*%s.*" img="(.*?)" fanart="(.*?)" href="(.+?)">(.+?)</a>'%para
			items = sorted(re.findall(r,body),key=lambda l:l[0], reverse=True)
	else:#Doc cac list xml khac
		r='<a.+id="(.*?)".+href="(.+?)".+img="(.*?)".+fanart="(.*?)".*>(.+?)</a>'
		items = re.compile(r).findall(body)
		if len(items)<1:items = re.findall('.+()href="(.+?)".+img="(.*?)".*()>(.+?)</a>',body)
		if len(items)<1:items = re.findall('.+()href="(.+?)".*()()>(.+?)</a>',body)
		if (myaddon.getSetting('copyxml')=="true") and ('http' in url) and (len(items)>0) :
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
	def read_favorite():
		file=joinpath(tempfolder,'fshare.cookie');hd['Cookie']=makerequest(file)
		url='https://www.fshare.vn/files/favorite';body=make_request(url,hd)
		if not body:
			hd['Cookie']=loginfshare();body=make_request(url,hd)
			makerequest(file,hd['Cookie'],'w');logout_site(hd['Cookie'],url)
		return body
	def fshare_remove_item(url,query):
		if query=='hdvn':
			pattern='<a date=".+?" href="%s" img=".*?">.+?</a>\n'%url
			body=re.sub(pattern,'',makerequest(joinpath(datapath,"hdvietnam.xml")))
			makerequest(joinpath(datapath,"hdvietnam.xml"),body,'w')
	pageIndex=filescount=rowscount=files_count=0;name_return=name
	if 'pageIndex' in url:
		pageIndex=int(url.split('?')[1].split('=')[1]);filescount=int(url.split('?')[2].split('=')[1])
		rowscount=int(url.split('?')[3].split('=')[1])
	if 'favorite' in url:body=read_favorite()
	else:body=make_request(url)
	name=clean_string(xshare_group(re.search('<title>(.+?)</title>',body),1))
	if not name or 'Lỗi 404' in name:mess(u'Không tìm thấy nội dung quý khách yêu cầu');return 'no'
	if '/file/' in url:
		size=xshare_group(re.search('<i class="fa fa-hdd-o"></i>(.+?)</div>',body),1).strip()
		items=[('',url,name,size,'')] #return url,name,size
	else:
		files_count=xshare_group(re.search('Số lượng:(.+?)</div>',body),1).strip()
		files_count=int(files_count) if files_count else filescount
		#if files_count==0 and query!='favorite':mess(u'Thư mục trống');fshare_remove_item(url,query);return 'no'
		pattern='data-id="(.+?)" .+? href="(.+?)".+title="(.+?)".*\s.*\s.*\s.*<.+?>(.+?)</div>.*\s.*<.+?>(.+?)</div>'
		items=re.findall(pattern,body)
		if not items:mess(u'[COLOR red]Thư mục trống[/COLOR]');return 'no'
		if url.strip()==thumucrieng:
			items=sorted(items,key=lambda l:(l[4][6:]+l[4][3:5]+l[4][:2]), reverse=True)
	idtxtfile=joinpath(datapath,'id.txt');makeidtxtfile=False
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
		if '/file/' in href:
			href='https://www.fshare.vn/file/'+os.path.basename(href)
			if name.strip()[-3:].lower()=='xml':query+='xml';img=icon['khophim']
			#elif name.strip()[-3:].lower()=='m3u':
			elif len(size.strip())>2:name=name+" - "+size;img=icon['fshare'] if not img else img
		else:href='https://www.fshare.vn/folder/'+os.path.basename(href)
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

def play_maxspeed_link(url):
	if not url or url=='Maxlink':
		query=get_input('Hãy nhập max speed link của Fshare, 4share hoặc tênlửa')
		if query is None or query=='':return 'no'
		url=query.replace(' ','');print url
	elif len(url)<13:
		fsend=getFsend(url)
		if fsend:url=fsend[0][1]
		else:mess(u'[COLOR red]Lỗi get Fsend[/COLOR]');return
	if check_media_ext(url,'fshare.vn'):xbmcsetResolvedUrl(url,'Maxlink')
	return ''

def getFsend(id):
	response=make_request('http://fsend.vn/'+id,hd,'o')#http://fsend.vn/2LJL4GPVZ48L file XXOA5LADP6FC folder
	hd['Cookie']=response.cookiestring
	token=xshare_group(re.search('"(.+?)"',urllib.unquote(response.cookiestring)),1)
	data={"fs_csrf":"%s"%token,"DownloadForm[speed]":"slow","ajax":"download-form","undefined":"undefined"}
	resp=make_post('http://fsend.vn/default/download',data=urllib.urlencode(data),headers=hd)
	if resp.status==200:
		try:json=resp.json
		except:json=''
	else:json=''
	if json and json['code']==200:items=[(os.path.basename(json['url']),json['url'],'')]
	elif json and json['code']==400:
		pattern='avatar. title="(.+?)".+?<p><b>(.+?)</b></p>.+?<a href="/(.+?)"';items=[]
		for title,size,id in re.findall(pattern,response.body,re.DOTALL):items.append((title,size,id))
	else:items=[]
	return items

def tenlua_getlink(href):
	idf=xshare_group(re.search('\w{14,20}',href),0)
	if not idf:return
	response=tenlua_get_detail_and_starting(idf)
	if response["type"]=="file":
		name=response['n'].encode('utf-8');url="https://www.tenlua.vn/download/"+idf
		addir(name,url,mode=3)
	elif response["type"]=="folder":
		for item in response['content']:
			tenlua_getlink(item['link'])

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
		name='Nhập ID (hoặc url) phim %sFshare (hoặc Fsend)[/COLOR]-%s4share[/COLOR] hoặc %stenlua[/COLOR]'%(color['fshare'],color['4share'],color['tenlua'])
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
			fsend=getFsend(idf)
			if fsend:
				for title,size,id in fsend:#title,size,id
					if id:addir(title+' - '+size,id,img=icon['fshare'],mode=16,query=id)
					else:addir(title,size,img=icon['fshare'],mode=16,query=size)
				name=fsend[0][0]
			elif url:name=doc_TrangFshare(name,url,icon[query],'')
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
		title=color['4share']+"Mục Link yêu thích của tôi trên Fshare (My fshare favorite)[/COLOR]"
		addir(title,"https://www.fshare.vn/files/favorite",img,fanart,mode=90,query='favorite',isFolder=True)
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
	items_old=doc_xml(joinpath(datapath,"ifiletv.xml"));id_old=[s[1] for s in items_old]
	items_new = []#id_tip,id_htm,href,img,name
	for id_tip,id_htm,href,img,name in ifile_tv_page('http://ifile.tv/') :
		if id_htm not in id_old:
			for url4share,fanart,name2,catalog in ifile_tv_4share(href):
				fullname=name2 if name in name2 else name
				fullname=' '.join(s for s in fullname.split())
				items_new.append((id_tip,id_htm,catalog,img,fanart,url4share,fullname))
	if items_new:update_xml(items_new,items_old,"ifiletv.xml")
	else:mess(u'Ifile.tv Không có phim mới...',5000,color['4share']+'Ifile.tv auto update[/COLOR]')
	return 'ok'

def read_all_filexml(fn="vaphim.xml",string_search='',lists=[],index=[]):
	if string_search:lists=lists+doc_xml(joinpath(datapath,fn),para='search:'+string_search)
	else:lists=lists+doc_xml(joinpath(datapath,fn))
	if not string_search:
		for id_tip,id_htm,category,img,fanart,url,name in lists:index.append((id_htm))
	return lists,index

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
	items=vp_page(url_search)#id,name,href,img,category
	if not items:mess(u'Không tìm được tên phim phù hợp');return 'no'
	ids=[s[0] for s in items]
	items=[s for s in doc_xml(joinpath(datapath,'vaphim.xml')) if s[1] in ids]
	for id in ids:vp_addir([s for s in items if s[1]==id])
	pattern="class='pages'>(.+?)<.+span><a href='(.+?)' class='page larger'>(\d{,3})</a>"
	page_tag=re.search(pattern,make_request(url_search))
	if page_tag:
		trang=str(int(trang)+1)
		name=color['trangtiep']+'Tiep theo %s...trang %s[/COLOR]'%(xshare_group(page_tag,1),xshare_group(page_tag,3))
		addir(name,url,icon[url.split('.')[0]],mode=mode,page=4,query='%s?%s?%s'%(string,trang,p),isFolder=True)
	return ''

def pfs_search(url,string,mode,temp=[],p=0):
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
		for server,link in pfs_getlink(response):
			addirs(name,link,img,fanart)
	trangtiep_google_custom(url,results,string,mode,trang,start,apiary)
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
		elif url=='phimfshare.com':pfs_search(url,query,mode)
		elif url=='tenlua.vn':tenlua_search(url,query,mode)
		elif url=='4share.vn':fourshare_search(url,query,mode)
		elif url=='ifile.tv':ifile_search(url,query,mode)
		elif url=='hdvietnam.com':hdvn_search(url,query,mode)
		elif url=='xshare.vn':internal_search(url,query,mode)
	return ''

def pfs_update():#6+
	items=rss_content('http://phimfshare.com/external.php?type=RSS2')
	content_new='';count=0
	fphimfshare=joinpath(datapath,'phimfshare.xml')
	content_old=makerequest(fphimfshare)
	idf_old=re.findall('<a id="(.+?)" server',content_old)
	for item in items:
		idf=xshare_group(re.search('-(\d{5})',item.findtext('link')),1)
		if not idf or idf in idf_old:continue
		name=re.sub('\[.*\]|\(.*\)|\|.*\|','',item.findtext('title')).strip()
		content=item.findtext('contentencoded')
		img=xshare_group(re.search('img src="(.+?jpg)["|?| ]',content),1)
		for server,link in pfs_getlink(content):
			if link not in content_new:
				count+=1
				content_new+='<a id="%s" server="%s" href="%s" img="%s">%s</a>\n'%(idf,server,link,img,name)
	if content_new:
		mess(u'Đã cập nhật được %d phim'%count,5000,color['phimfshare']+'Phimfshare.xml auto update[/COLOR]')
		makerequest(fphimfshare,string=content_new.encode('utf-8'),attr='a')

def pfs_getlink(content):#6+
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

def subtitle_of_year(title):
	string=xshare_group(re.search('(.+?20\d\d|.+?19\d\d)',title),1)
	string=re.sub(xshare_group(re.search('multi ',string,re.IGNORECASE),0),'',string)
	return string if string else title

def phimFshare(name,url,mode,page,query):#6
	fphimfshare=joinpath(datapath,'phimfshare.xml');home='http://phimfshare.com/';pagenext=''
	def pfs_page(url,pattern):
		body=make_request(url)
		return re.findall(pattern,body),xshare_group(re.search('<a rel="next" href="(.+?)" title=".+?">',body),1)
	def pfs_addir(items):
		for id,href,img,name in items:addirs(name,href,img)
	def pfs_xml():
		pattern='<a id="(.+?)" server=".+?" href="(.+?)" img="(.*?)">(.+?)</a>'
		return re.findall(pattern,makerequest(fphimfshare))
	
	if query=='phimfshare.com':make_mySearch('',url,'','',mode,'get');return ''
	elif page==4 and name==query:return phimFshare('Search',url,mode,page,query)
	elif name=='Search':
		search_string = urllib.quote_plus(query)
		url='https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&'
		url+='rsz=filtered_cse&num=15&hl=vi&prettyPrint=false&source=gcsc&gss=.com&'
		url+='sig=23952f7483f1bca4119a89c020d13def&cx=005609294674567689888:qyuk9aoqwmg&q='+search_string
		url+='&googlehost=www.google.com&callback=google.search.Search.apiary'
		items,pagenext=pfs_page(url,'()"url":"(http://phimfshare.com/.+?)"()()')
		if not items:mess(u'Không tìm thấy phim có chứa chuổi tìm kiếm');return 'no'
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		return phimFshare('Search',url,mode,page,query) if query else 'no'
	elif query=='PhimMoi':
		items,pagenext=pfs_page(home,'()<a href="(.+?)" ()class="title">(.+?)</a>')
	elif url=='folder':pfs_addir([s for s in pfs_xml() if query in s[3]]);return
	else:
		if home not in url:url=home+url+'/'
		pattern='<img class="preview" src="(.+?)" .+? class=".+?" href="(.+?)" id="thread_title_(.+?)">(.+?)</a>'
		items,pagenext=pfs_page(url,pattern)#img,href,id,title
		
	items=[(s[0],s[1],s[2] if len(s[2])>4 else xshare_group(re.search('-(\d{5})',s[1]),1),s[3]) for s in items]
	lists=[s for s in pfs_xml() if s[0] in [f[2] for f in items]]
	for name in list(set([subtitle_of_year(s[3]) for s in lists])):
		temp=[s for s in lists if name in s[3]]
		if not temp:continue
		elif len(temp)>1:
			id,href,img,title=temp[0];title=[s[3] for s in temp if '~' in s[3]]
			title=name+' ~ '+re.sub('.+?~ ?','',title[0]) if title and '~' not in name else name
			addir(color['phimfshare']+title+'[/COLOR]','folder',img,'',mode,page,name,True)
		else:pfs_addir(temp)
	if pagenext:
		page=2 if not page else page+1
		name=color['trangtiep']+'Trang tiếp theo - Trang '+str(page)+' ...[/COLOR]'
		addir(name,pagenext,iconpath+'fshare.png',mode=mode,page=page,query=query,isFolder=True)
	endxbmc();ids=[s[2] for s in items if s[2] not in list(set([f[0] for f in lists]))];content_new=''
	if ids:mess(u'[COLOR green]%s updating...[/COLOR]'%query,title='[COLOR gold]phimfshare.com[/COLOR]')
	for img,href,id,name in [s for s in items if s[2] in ids]:
		response=make_request(href)
		temp=xshare_group(re.search('<title> (.+?)</title>',response),1)
		if temp:name=temp
		elif not name:continue
		if not img:img=xshare_group(re.search('<img src="(.+?)" border="0" alt="" />',response),1)
		name=' '.join(s for s in re.sub('\[.+?\]|\(.+?\)|MuLtI|Fshare|fshare','',name).split())
		for server,link in pfs_getlink(response):
			if link not in content_new:
				content_new+='<a id="%s" server="%s" href="%s" img="%s">%s</a>\n'%(id,server,link,img,name)
	if content_new:makerequest(fphimfshare,string=content_new,attr='a');xbmc.executebuiltin("Container.Refresh")
	return ''

def rss_content(url):
	from xml.etree import ElementTree as etree
	reddit_file = make_request(url)
	reddit_file = reddit_file.replace('content:encoded','contentencoded')
	try:reddit_root = etree.fromstring(reddit_file);items=reddit_root.findall('channel/item')
	except:print 'Update rss %s fail'%str2u(url);items=[]
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
	if not items:return
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
	noti=False
	if not items:
		home='http://www.hdvietnam.com/diendan/external.php?type=RSS2';items=hdvn_rss(home);noti=True
		for item in '33-146-311-265-110-116-123-57-157'.split('-'):
			temp=hdvn_rss('%s&forumids=%s'%(home,item))
			if temp:items+=temp
	file=joinpath(datapath,"hdvietnam.xml");string='';count=0;temp=[]
	urls=re.findall('href="(.+?)"',makerequest(file))
	for url,img,name in [s for s in items if s[0] not in urls]:
		if url not in temp:
			temp.append(url);count+=1
			string+='<a date="%s" href="%s" img="%s">%s</a>\n'%(homnay,url,img,name)
	if string:
		makerequest(file,string.encode('utf-8'),'a')
		hd['Cookie']=loginhdvietnam();hdvn_thank_xshare(hd)
		mess(u'Đã cập nhật được %d phim'%count,5000,color['hdvietnam']+'hdvietnam.xml auto update %s[/COLOR]'%homnay)
	elif noti and not string:
		mess(u'Hdvietnam.com không có thông tin mới',5000,color['hdvietnam']+'hdvietnam.xml auto update[/COLOR]')
	return 'ok'

def hdvietnam(name,url,img,fanart,mode,page,query):
	def hdvn_addir(items):
		for name in list(set([subtitle_of_year(s[2]) for s in items])):
			lists=[s for s in items if name in s[2]]
			if not lists:continue
			elif len(lists)==1:href,img,title=lists[0];addirs(title,href,img,query='hdvn')
			else:
				href,img,title=lists[0]
				title=name+' ~ '+re.sub('.+?~ ?','',title) if '~' in title and '~' not in name else name
				addir(color['hdvietnam']+title+'[/COLOR]','folder',img,'',mode,page,name,True)
	if url in '000-UPD':
		if query in '000-UPD':
			hom_nay=homnay
			if query=='UPD':hdvn_update()
		else:hom_nay=query
		body=makerequest(joinpath(datapath,"hdvietnam.xml"));ngaytruoc=''
		items=re.findall('date="%s" href="(.+?)" img="(.+?)">(.+?)</a>'%hom_nay,body)
		if not items and query!='UPD':
			endxbmc();mess(u'[COLOR green]RSS %s updating...[/COLOR]'%hom_nay,title='[COLOR gold]hdvietnam.com[/COLOR]')
			hdvietnam(name,url,img,fanart,mode,page,'UPD');xbmc.executebuiltin("Container.Refresh");return
		hdvn_addir(items)
		for ngay in sorted(re.findall('date="(.+?)"',body),key=lambda k:k[6:]+k[3:5]+k[:2]):
			if ngay==hom_nay:break
			ngaytruoc=ngay
		if ngaytruoc!=hom_nay:
			name=color['trangtiep']+"Thông tin ngày %s[/COLOR]"%ngaytruoc
			addir(name,"000",icon["icon"],mode=mode,query=ngaytruoc,isFolder=True)
	elif url=='folder':
		body=makerequest(joinpath(datapath,"hdvietnam.xml"));temp=[]
		items=[s for s in re.findall('date=".+?" href="(.+?)" img="(.+?)">(.+?)</a>',body) if query in s[2]]
		for href,img,name in list(set(items)):
			if href not in temp:temp.append(href);addirs(name,href,img,query='hdvn')
	elif re.search('\d\d',query):
		url='http://www.hdvietnam.com/diendan/external.php?type=RSS2&forumids=%s'%query
		items=hdvn_rss(url);hdvn_addir(items)
		endxbmc();hdvn_update(items)
	elif query=='MCS':
		body=make_request('http://www.hdvietnam.com/diendan/34-chia-se-phim/')
		pattern='<div class="forumbit_post L2">.+?<a href="(.+?)">(.+?)</a></h2>'
		items=re.findall(pattern,body,re.DOTALL)
		for href,name in items:
			if '149-phim-theo-phan-loai' in href:query='PLP'
			elif xshare_group(re.search('/\d{1,3}-',href),0) in '/33-/311-/65-/146-/149-/150-':query='PL1'
			else:continue
			href='http://www.hdvietnam.com/diendan/'+href.split('&')[0]
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
		body=make_request(url,headers=hd,maxr=3)
		if url.split('=')[1] in '33 311 65 146':#33-fshare-vn,
			for href,name in re.findall('<h2 class="forumtitle"><a href="(.+?)">(.+?)</a></h2>',body):
				addir(color['fshare']+name+'[/COLOR]',href,icon['hdvietnam'],fanart,mode,page,'PL1',isFolder=True)
		for content in re.findall('<a class="title(.+?)</span>',body,re.DOTALL):
			href=xsearch('href="(.+?)" id=".+?">(.+?)</a>',content,1).split('&')[0]
			href='http://www.hdvietnam.com/diendan/%s&page=1000'%href
			name=re.sub('&.+?; ','',xsearch('href="(.+?)" id=".+?">(.+?)</a>',content,2))
			bossroom=xsearch('<b>(.+?)</b>',content,1)
			name='[COLOR yellow]%s[/COLOR] '%bossroom+name
			addir(name,href,img,fanart,mode,page,'GET',isFolder=True)
		if page==0:url=url+'index2.html';page=2
		else:url=url.replace('index%s.html'%str(page),'index%s.html'%str(page+1));page+=1
		if re.search(url,body):
			name=color['trangtiep']+'Trang tiep theo...trang %d[/COLOR]'%page
			addir(name,url,img,fanart,mode,page,'PL1',isFolder=True)
	#Thay doi cach tiep can hdvietnam: http://www.hdvietnam.com/diendan/34-chia-se-phim/
	#Phan loai:
	#http://www.hdvietnam.com/diendan/150-thu-vien-link-phim/
	#http://www.hdvietnam.com/diendan/33-fshare-vn, ...
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
				body=make_request(url,headers=hd,maxr=5);name=re.sub('\[COLOR.+COLOR\] ','',name)
				body=body[body.find('<font size="5">'+name)+100:];temp=body.find('<font size="5">')
				body=body[:temp] if temp>0 else body[:body.find(string)]

				for href,name in re.findall('<a href="(.+?)" target="_blank">(.+?)</a>',body):
					if re.search('/\d{1,3}-',href):addir(name,href,img,fanart,mode,page,'GET',isFolder=True)
		else:hdvn_get_link(url)

def data_download_fromFshare(data1,data2):
	def getflink(data):
		pattern='href="(.+?)" title="%s"'%data;href='https://www.fshare.vn/folder/GZCI8AHAQJ75'
		data=xshare_group(re.search(pattern,make_request(href)),1).replace('http:','https:')
		return resolve_url(data,True)
	
	kq='';url=getflink(data1)
	if url=='fail':url=getflink(data2)
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
	if os.path.isfile(joinpath(data_path,'htvonline.png')):
		rename_file(joinpath(data_path,'htvonline.png'),joinpath(iconpath,'htvonline.png'))
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
	if 'fpt.xml' not in file_now or os.path.getsize(joinpath(datapath,'fpt.xml'))<22345000:
		if data_download_fromFshare('fpt.zip','fpt-hot.zip'):downloadresult='yes'
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
	file=joinpath(datapath,"last_update.dat")
	last_update=datetime.datetime.fromtimestamp(os.path.getmtime(file) if os.path.isfile(file) else 0)
	if ngay>last_update.strftime("%Y%m%d"):
		makerequest(joinpath(datapath,"last_update.dat"),'','w');delete_files(tempfolder)
		try:vp_update();ifile_update();vp_make_datanew()
		except:mess('Data update error');pass
	if abs(int(gio)-int(last_update.strftime("%H")))>2:
		makerequest(joinpath(datapath,"last_update.dat"),'','w')
		try:hdvn_update();pfs_update()#;vp_update_rss()
		except:mess('RSS update error');pass

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
	def fpt2s(string):
		return ' '.join(re.sub('&.+;',xsearch('&(\w).+;',s,1),s) for s in string.split())
	def login():
		email=myaddon.getSetting('mail_fptplay');password=myaddon.getSetting('pass_fptplay')
		response=make_request('http://fptplay.net/user/login',headers=hd,resp='o',maxr=3)
		body=response.body;pattern='<input.+?value="(.+?)"><input.+?value="(.+?)">'
		csrf_token=xsearch(pattern,body,1);next=xsearch(pattern,body,2)
		data={'csrf_token':csrf_token,'next':next,'email':email,'password':password,'submit':'Đăng nhập'}
		hd['Cookie']=response.cookiestring
		response=make_post('https://moid.fptplay.net/',headers=hd,data=urllib.urlencode(data))
		hd['Cookie']=response.cookiestring;url='https://moid.fptplay.net/oauth2/authorize'
		if response.status==302:
			client_id=xsearch('client_id=(.+?)&',response.headers['location'],1)
			data={'client_id':client_id,'scope':'email','response_type':'code','confirm':'yes'}
			response=make_post(url,headers=hd,data=urllib.urlencode(data))
			if response.status==302:response=make_request(response.headers['location'],headers=hd,resp='o')
		if 'laravel_value' in response.cookiestring:
			mess(u'[COLOR green]Login fptplay.net thành công[/COLOR]');f=response.cookiestring
			makerequest(joinpath(datapath,'fptplay.cookie'),f,'w')
		else:mess(u'[COLOR red]Login fptplay.net không thành công[/COLOR]');f=''
		#get('https://fptplay.net/user/logout',headers=hd) status=302
		return f
	def colors(name,title):
		name=name.strip()+' '+title.strip()
		if 'Thuyết Minh' in name:name='[COLOR gold]TM[/COLOR] '+name
		elif 'Phụ Đề' in name:name='[COLOR green]PĐ[/COLOR] '+name
		elif 'Trailer' in name:name=name+' [COLOR red](Trailer)[/COLOR]'
		return name
	def getlinklivetv(id,headers='',href=''):
		headers['X-Requested-With']='XMLHttpRequest';headers['Referer']='http://fptplay.net/livetv'
		for quality in [3,2,1]:
			url='http://fptplay.net/show/getlinklivetv/?id=%s&quality=%d&mobile=web'%(id,quality)
			response=make_post(url,headers=headers)
			try:href=response.json['stream'];break
			except:
				try:
					if response.json['msg_code']=='login':href='login';break
				except:pass
		if not href:
			try:href=response.json['msg_code']
			except:href='Getting error'
		return href
	def getlink(id,name,url=''):
		hd['X-Requested-With']='XMLHttpRequest';hd['Referer']=url
		json=make_post('http://fptplay.net/show/getlink?id=%s&episode=1&mobile=web'%id,headers=hd,resp='j')
		if not json:return list()
		id=json.get('_id').encode('utf-8');items=list()
		for i in json.get('quality'):
			title=i['title'].encode('utf-8');img=i['thumb'].encode('utf-8')
			href=i['url'][0]['url'].encode('utf-8')
			items.append((id,href,img,title,name))
		return items
	def getdir(items,name,url=''):#id,img,title   name
		ids=[s[0] for s in items]
		if not items:mess(u'[COLOR red]Không get được data từ fptplay.net[/COLOR]');return 'no'
		pattern='<div id="(.+?)" name="(.+?)">(.+?)</div>'
		hrefs=[s for s in re.findall(pattern,makerequest(joinpath(datapath,'fpt.xml')),re.DOTALL) if s[0] in ids]
		ids=list(set([s[0] for s in hrefs]));string='';list_update=[]
		if any(s for s in items if s[0] not in ids):
			mess(u'%s [COLOR green]Updating ...[/COLOR]'%str2u(name),5000,'[COLOR orange]FPTPlay database Update[/COLOR]')
		for iD,img,name in items:
			name=fpt2s(name)
			if iD not in ids:
				lists=getlink(iD,name,url);string+='<div id="%s" name="%s">\n'%(iD,name)
				for id,href,thumb,title,name in lists:string+='<a href="%s" img="%s">%s</a>\n'%(href,thumb,title)
				string+='</div>\n'
			else:
				content=''.join(s[2] for s in hrefs if s[0]==iD);lists=[]
				for href,thumb,title in re.findall('<a href="(.+?)" img="(.*?)">(.*?)</a>',content):
					lists.append((iD,href,thumb,title,name))
			if len(lists)>2:
				addir(color['fptplay']+name+'[/COLOR]',iD,img,lists[0][2],mode,page,'folder',True)
			elif len(lists)>0:
				for id,href,thumb,title,name in lists:
					addir(colors(name,title),href,img,thumb,mode,page,'play')
					if re.search('Tập \d{1,2}',title):list_update.append((id,href,name))
		if string:
			makerequest(joinpath(datapath,'fpt.xml'),string,'a')
			mess(u'[COLOR green]FPTPlay database Updated[/COLOR]',1000,'[COLOR orange]FPTPlay database Update[/COLOR]')
		return list_update
	def update_list(items):
		direct_links=[s[1] for s in items];ids=[];string='';lists=[]
		for id,href,name in items:
			if id in ids:continue
			ids.append(id)
			lists=[s for s in getlink(id,name) if s[1] not in direct_links]#id,href,img,title,name
			if lists:
				string+='<div id="%s" name="%s">\n'%(id,name)
				for id,href,thumb,title,name in lists:
					string+='<a href="%s" img="%s">%s</a>\n'%(href,thumb,title)
				string+='</div>\n'
		if string:makerequest(joinpath(datapath,'fpt.xml'),string,'a')
		return True if string else False
	if not os.path.isfile(joinpath(datapath,'fptplay.cookie')):hd['Cookie']=login()
	else:hd['Cookie']=makerequest(joinpath(datapath,'fptplay.cookie'))
	if query=="FPP":
		body=make_request('http://fptplay.net',hd);href='http://fptplay.net/livetv'
		name=color['search']+"Search trên fptplay.net[/COLOR]"
		addir(name,"fptplay.net",icon['fptplay'],mode=mode,query="FPS",isFolder=True)
		addir(color['fptplay']+'Live TV[/COLOR]',href,icon['fptplay'],mode=mode,query='FTV',isFolder=True)
		if not body:return ''
		content=xsearch('"top_menu reponsive"(.+?)"top_listitem"',body,1,re.DOTALL)
		for href,title in re.findall('<li ><a href="(http://fptplay.net/danh-muc/.+?)">(.+?)</a></li>',content):
			title=color['fptplay']+fpt2s(title)+'[/COLOR]'
			addir(title,href,icon['fptplay'],mode=mode,query='FP2',isFolder=True)
		content=xsearch('<ul class="slide_banner">.+?<li>(.+?)</ul>',body,1,re.DOTALL)
		#iD,img,name
		pattern='<li>.+?src="(.+?)\?.+?title="(.+?)".+?-(\w+)\.html'
		items=[(s[2],s[0],s[1]) for s in re.findall(pattern,content,re.DOTALL) if len(s[2])>20]
		ids=[s[0] for s in items]
		content=xsearch('Phổ biến hiện nay</span>(.+?)title="Thể Thao"',body,1,re.DOTALL)
		pattern='<a href=".+?-(\w+)\.html".+?title="(.+?)".+?data-original="(.+?)\?'
		items+=[(s[0],s[2],s[1]) for s in re.findall(pattern,content) if s[0] not in ids]#id,img,title
		list_update=getdir(list(set(items)),'Home page')
		if list_update:endxbmc();update_list(list_update)
	elif query=="FTV":
		body=make_request(url,hd);i=1
		content=xsearch('Begin kenh truyen hinh(.+?)END Tong Hop',body,1,re.DOTALL)
		pattern='<a class=".+?" title="(.+?)".+?href="http://fptplay.net/livetv/(.+?)"(.+?)original="(.+?)\?.+?"'
		for name,href,lock,img in re.findall(pattern,content,re.DOTALL):
			j='00%d '%i if i<10 else '0%d '%i if i<100 else '%d '%i;name=j+fpt2s(name);i+=1
			if '"lock"' in lock:name=name+' ([COLOR red]Có phí[/COLOR])'
			addir(name,href,img,mode=mode,query="PTV")
	elif query=="PTV":
		href=getlinklivetv(url,hd)
		if 'm3u8' in href:xbmcsetResolvedUrl(href)
		elif href=='login':
			href=getlinklivetv(url,hd)
			if 'm3u8' in href:xbmcsetResolvedUrl(href)
			else:hd['Cookie']=login();href=getlinklivetv(url,hd)
			if 'm3u8' in href:xbmcsetResolvedUrl(href)
			else:mess(u'[COLOR red]%s[/COLOR]'%href,title='Fptplay LiveTV')
		else:mess(u'[COLOR red]%s[/COLOR]'%href,title='Fptplay LiveTV')
	elif query=="FPS":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return fptplay(name,url,img,mode,page,query)
		else:return 'no'
	elif url=="fptplay.net":
		search_string = urllib.quote(query)
		url='http://fptplay.net/show/more?type=search&stucture_id=key&page=1&keyword=%s'%search_string
		return fptplay(name,url,img,mode,page,query='FP3')
	elif query=="FP2":
		body=make_request(url,hd);pattern='<a href="(http://fptplay.net/the-loai/.+?)" title="(.+?)"';temp=[]
		for href,title in re.findall(pattern,body):
			if href in temp:continue
			temp.append(href)
			title=color['fptplay']+fpt2s(title)+"[/COLOR]";id=xsearch('(\w{22,26})',href,1)
			data='type=new&keyword=undefined&page=1&stucture_id=%s'%id;url='http://fptplay.net/show/more?%s'%data
			addir(title,url,icon["fptplay"],mode=mode,query="FP3",isFolder=True)
		content=xsearch('<ul class="slide_banner">.+?<li>(.+?)</ul>',body,1,re.DOTALL)
		#iD,img,name
		items=[(s[2],s[0],s[1]) for s in re.findall('src="(.+?)\?.+?title="(.+?)".+?-(\w+)\.html',content,re.DOTALL)]
		list_update=getdir(list(set(items)),name)
		if list_update:endxbmc();update_list(list_update)
	elif query=="FP3":
		body=make_post(url).body;page=xsearch('page=(\d{1,3})',url,1)
		if not body:mess(u'[COLOR red]Error get data/not found from fptplay.net[/COLOR]');return 'no'
		items=re.findall('<a href=".+-(\w+)\.html".+?src="(.+?)\?.+?alt="(.+?)"',body)
		list_update=getdir(items,name,url)
		if len(items)>35:
			page=str(int(page)+1)
			url=re.sub('page=\d{1,3}','page=%s'%page,url)
			name=color['trangtiep']+"Trang tiếp theo - Trang %s[/COLOR]"%page
			addir(name,url,icon["fptplay"],mode=mode,query="FP3",isFolder=True)
		if list_update:endxbmc();update_list(list_update)
	elif query=="folder":
		pattern='<div id="%s" name="(.+?)">(.+?)</div>'%url
		hrefs=re.findall(pattern,makerequest(joinpath(datapath,'fpt.xml')),re.DOTALL)
		content=''.join(s[1] for s in hrefs);items=re.findall('<a href="(.+?)" img="(.*?)">(.*?)</a>',content)
		for href,thumb,title in items:
			addir(colors(title,hrefs[0][0]),href,img,thumb,mode,page,'play')
		endxbmc()# Update 1 folder
		if update_list([(url,s[0],hrefs[0][0]) for s in items]):xbmc.executebuiltin("Container.Refresh")
	elif query=='play':xbmcsetResolvedUrl(url)
	return ''

def xsearch(pattern,string,group,flags=0):
	research=re.search(pattern,string,flags)
	if research:
		try:result=research.group(group)
		except:result=''
	else:result=''
	return result

def checkupdate(filename,folder=datapath):
	filecheck=joinpath(folder,filename)
	filetime=os.path.getmtime(filecheck) if os.path.isfile(filecheck) else 0
	last_update=datetime.datetime.fromtimestamp(filetime);timeformat='%Y%m%d%H'
	return int(datetime.datetime.now().strftime(timeformat))-int(last_update.strftime(timeformat))

def megabox(name,url,img,fanart,mode,page,query):
	home='http://phim.megabox.vn/'
	cat={1:'Phim lẻ',2:'Phim bộ',3:'Show',4:'Clip'}
	gen={1:'Hành động',2:'Phiêu lưu',3:'Ma kinh dị',4:'Tình cảm',5:'Hoạt hình',6:'Võ thuật',7:'Hài',8:'Tâm lý',9:'Kiếm hiệp',10:'Sử thi',11:'',12:'',13:'Hình sự',14:'',15:'Âm nhạc',16:'Khoa học',17:'Tài liệu',18:'Gia đình',21:'Chiến tranh',22:'Thể thao',25:'Độc-Lạ',27:'Khoa học viễn tưởng',28:'Ẩm thực',29:'Thời trang',30:'Điện ảnh',31:'Thiếu nhi',32:'Giáo dục',33:'TV-Show',34:'Live Show',36:'Công nghệ',37:'Khám phá thế giới',38:'Động vật',39:'Shock'}
	country={1:'Âu-Mỹ',2:'Hàn Quốc',3:'Hồng Kông',4:'Trung Quốc',5:'Nhật Bản',6:'Thái Lan',7:'Quốc Gia khác',8:'Mỹ',9:'Pháp',11:'Việt Nam',12:'Ấn Độ',13:'Philippines'}#get(url,headers=hd,maxr=2)
	def mes(string):mess(string,title=namecolor('megabox.vn'))
	def namecolor(name):return color['megabox']+name+'[/COLOR]'
	def get_id(url):return xsearch('-(\d{1,6})\.html',url,1)
	def duration(string):return xsearch('Thời lượng:<.+?> (.+?)</li>',string,1)
	def countview(string,tag='span'):return xsearch('class=.count-view.><%s></%s> (.+?)</span>'%(tag,tag),string,1)
	def thuyetminh(string):return color['subscene']+'TM[/COLOR] ' if xsearch('class=.ico-sub.',string,0) or string=='TM' else ''
	def phim18(string):return '[COLOR red][B]M+[/B][/COLOR] ' if xsearch('class=.ico-rating.',string,0) or string=='M+' else ''
	def episode(string):return xsearch('class=.esp.><i>(.+?)</span>',string,1).replace('</i>','')
	def update_dict(dict):
		body=make_request(home,headers=hd)
		#(phim-le,Phim lẻ),(phim-bo,Phim bộ),(show,Show),(clip,Clip)
		dict['MGB1']=re.findall('<li><a href="(.+?)" title="">(.+?)</a></li>',body)
		#(Lẻ Bộ Show Clip Mới Nhất, Chiếu Rạp) (Megabox giới thiệu, Top 10, sắp chiếu, lẻ-bộ-show-clip xem nhiều)
		dict['MGB2']=re.findall('"H2title">(.+?)</h2>',body)
		content=sub_body(body,'id="phimle"','id="phimbo"')
		dict['phim-letl']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[:content.find('Quốc gia')])
		dict['phim-leqg']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[content.find('Quốc gia'):])
		content=sub_body(body,'id="phimbo"','id="tvshow"')
		dict['phim-boqg']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[:content.find('Thể Loại')])
		dict['phim-botl']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[content.find('Thể Loại'):])
		content=sub_body(body,'id="tvshow"','id="clip"')
		dict['showtl']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[:content.find('Quốc gia')])
		dict['showqg']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[content.find('Quốc gia'):])
		content=sub_body(body,'id="clip"','class="search-toogle"')
		dict['cliptl']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content)
		dict['gioithieu']=re.findall("<li><a href='(.+?)'",sub_body(body,'class="hotFilmSlider"','id="bx-pager"'))
		dict['top10']=re.findall('href="(.+?)"',sub_body(body,'begin topFilm','end topFilm'))
		dict['sapchieu']=re.findall("<a href='(.+?)'>",sub_body(body,'Phim sắp chiếu','end primary'))
		for i in range(1,5):
			s1='id="subCate-%d"'%i;s2='id="ul-%d"'%i
			dict['subCate%d'%i]=re.findall('data=.(.+?). data1=.(.+?).>(.+?)</a>',sub_body(body,s1,s2))
		return json_rw(dict)
	def get_detail(urls,dict):
		mes('[COLOR green]Xshare database updating ...[/COLOR]')
		for url in urls:
			id=get_id(url);body=sub_body(make_request(url,maxr=3),'begin primary','end primary');tm='TM' if thuyetminh(body) else ''
			views=countview(body);esp=xsearch('Số tập <i>(.+?)</i>',body,1);p18='M+' if phim18(body) else ''
			items=re.findall('alt=\'(.+?)\' src="(.+?)"',body)
			if not items:continue
			elif len(items)==1:title=items[0][0];fanart=img=items[0][1]
			else:title=items[0][0];fanart=items[0][1];img=items[1][1]
			if esp:series='y'
			else:series='n';esp=duration(body)
			dict[id]=(series,title,img,fanart,views,esp,tm,p18)
		return dict
	def json_rw(dicts={}):
		if dicts:makerequest(joinpath(datapath,'megabox.json'),json.dumps(dicts),'w')
		else:
			try:dicts=json.loads(makerequest(joinpath(datapath,'megabox.json')))
			except:dicts={}
		return dicts
	def load_urls(urls):
		dict=json_rw();urls_old=[];urls_new=[];ids=[];update=False
		for url in urls:
			id=get_id(url)
			if not id:continue
			elif dict.has_key(id) and dict[id]:urls_old.append(url)
			else:urls_new.append(url)
			ids.append((id,url))
		if urls_new:dict=get_detail(urls_new,dict)
		for id,url in ids:
			try:tm=thuyetminh(dict[id][6])+phim18(dict[id][7])
			except:tm=''
			img=dict[id][2];fanart=dict[id][3]
			if dict[id][0]=='y':
				epi=xsearch('(.+?)\W(.*?)\Z',dict[id][5],1);eps=xsearch('(.+?)\W(.*?)\Z',dict[id][5],2)
				title=namecolor(dict[id][1])+color['subscene'];query='1episode'+eps;isFolder=True
				title=title+' - %s views:%s[/COLOR]'%(dict[id][5],dict[id][4])
			else:
				title=dict[id][1]+color['subscene']+' - (%s - views:%s)[/COLOR]'%(dict[id][5],dict[id][4].strip())
				query='mgbplay';isFolder=False
			addir(tm+title,url,img,fanart,mode,1,query,isFolder=isFolder)
		if urls_new:endxbmc();json_rw(get_detail(urls_old,dict));mes('[COLOR lime]Xshare database updated[/COLOR]')
	def put_items(items,tag='span'):#class='count-view'><span></span> 551</span>
		dict=json_rw();cl=color['subscene']
		href_old=[s[0] for s in items if get_id(s[0]) in dict]
		href_new=[s[0] for s in items if s[0] not in href_old]
		for href,name,dura,img,esp,view in items:
			id=get_id(href);views=countview(view,tag);dura=duration(dura)
			tm=thuyetminh(esp)+phim18(esp);esp=episode(esp);eps=xsearch('\W(.*)\Z',esp,1)
			if esp:title,query,series,isFolder=namecolor(name),'1episode'+eps,'y',True
			else:title,esp,query,series,isFolder=name,dura,'mgbplay','n',False
			title=tm+title+' %s%s views: %s[/COLOR]'%(cl,esp,views)
			try:fanart=dict[id][3] if href in href_old else img
			except:fanart=img
			p18='M+' if 'M+' in tm else '';tm='TM' if 'TM' in tm else ''
			dict[id]=(series,name,img,fanart,views,esp,tm,p18)
			addir(title,href,img,fanart,mode,1,query,isFolder)
		return href_new,dict
	def update_href_new(hrefs,dict):
		mes('[COLOR green]Xshare database updating ...[/COLOR]')
		for href in href_new:
			id=get_id(href);body=sub_body(make_request(href,maxr=3),'begin primary','end primary')
			items=re.findall('alt=\'(.+?)\' src="(.+?)"',body)
			if len(items)<2:continue
			series,name,img,fanart,views,esp,tm,p18=dict[id];fanart=items[0][1];img=items[1][1]
			dict[id]=(series,name,img,fanart,views,esp,tm,p18)
		json_rw(dict);mes('[COLOR lime]Xshare database updated[/COLOR]')
	
	if query=='megabox.vn':make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return megabox(query,url,img,fanart,mode,page,query)
		else:return 'no'
	elif query==name:#Search in megabox.vn
		search_string = urllib.quote_plus(query)
		body=make_post('http://phim.megabox.vn/tim-kiem?keyword=%s'%search_string).body
		body=sub_body(body,'class="item"','id="footer"')
		patt='<a class.+?href="(.+?)".+?title.>(.+?)</h3>(.+?)<img.+?src="(.+?)"(.+?)</a>.+?<a.+?a>(.+?)</div></div>'
		put_items(re.findall(patt,body,re.DOTALL))
	elif query=='MGB':
		dict=json_rw()
		if not dict.get('MGB1'):dict=update_dict(dict)
		name=color['search']+"Search trên megabox.vn[/COLOR]"
		addir(name,'megabox.vn',icon['megabox'],'',mode,1,'megabox.vn',True)
		for href,name in dict['MGB1']:#(phim-le,Phim lẻ),(phim-bo,Phim bộ),(show,Show),(clip,Clip)
			addir(color['megabox']+name+'[/COLOR]',href,icon['megabox'],'',mode,1,'mainmenu',True)
		for name in dict['MGB2']:
			if isinstance(name,unicode):name=name.encode('utf-8')
			result=re.search('href="(.+?)">(.+?)</a>',name)
			if result:#Lẻ Bộ Show Clip Mới Nhất, Chiếu Rạp
				title=namecolor(result.group(2));href=result.group(1)
				addir(title,href,icon['megabox'],'',mode,1,'subCate',True)
			else:#Megabox giới thiệu, Top 10, sắp chiếu, lẻ-bộ-show-clip xem nhiều
				title=namecolor(re.sub('<.+?>','',name+' trong ngày' if 'xem' in name else name))
				addir(title,home,icon['megabox'],'',mode,1,'xemnhieu',True)
		if checkupdate('megabox.json')>8:dict=update_dict(dict)
	elif query=='mainmenu' and url in ('phim-letl','phim-leqg','phim-botl','phim-boqg','showtl','showqg','cliptl'):
		dict=json_rw()
		for title,href in dict[url]:
			title=color['megabox']+title.replace('Phim ','')+'[/COLOR]'
			addir(title,href,icon['megabox'],'',mode,1,'mainmenu',True)
	elif query=='mainmenu':#url:(phim-le,phim-bo,show,clip)
		submenu={'phim-le':'Phim lẻ','phim-bo':'Phim bộ','show':'Show','clip':'Clip'}
		if url=='clip':
			title=color['xshare']+submenu[url]+' theo thể loại[/COLOR]'
			addir(title,url+'tl',icon['megabox'],'',mode,1,query,True)
		elif url in ('phim-le','phim-bo','show'):
			title=color['xshare']+submenu[url]+' theo thể loại[/COLOR]'
			addir(title,url+'tl',icon['megabox'],'',mode,1,query,True)
			title=color['xshare']+submenu[url]+' theo quốc gia[/COLOR]'
			addir(title,url+'qg',icon['megabox'],'',mode,1,query,True)
		pattern='<a class.+?href="(.+?)".+?title.>(.+?)</h3>(.+?)<img.+?src="(.+?)">(.+?)</a>.+?<a.+?a>(.+?)</div><'
		body=sub_body(make_request(home+url,maxr=3),'begin primary','end primary')
		href_new,dict=put_items(re.findall(pattern,body,re.DOTALL),'i')
		url_next=xsearch('<li class="next"><a href="(.+?)">',body,1)
		if url_next:
			page_end=xsearch('<span></span>Trang.{1,10}/(\d{1,3})</div>',body,1)
			page_next=xsearch('trang-(.+)\Z',url_next,1)
			name=color['trangtiep']+'Trang tiếp theo: trang %s/%s[/COLOR]'%(page_next,page_end)
			addir(name,url_next,icon['megabox'],'',mode,1,query,True)
		if href_new:endxbmc();update_href_new(href_new,dict)
	elif query=='mgbplay':
		url='/'.join((os.path.dirname(url),urllib.quote(os.path.basename(url))))
		body=make_request(url,resp='o',maxr=5);link=xsearch("changeStreamUrl\('(.+?)'\)",body.body,1)
		if not link:play_youtube(xsearch("\'(https://www.youtube.com/watch\?v=.+?)\'",body.body,1));return
		hd['Cookie']=body.cookiestring
		maxspeedlink=make_post('http://phim.megabox.vn/content/get_link_video',data={"link":"%s"%link}).body
		if maxspeedlink:
			name=re.sub(' \[COLOR.+?/COLOR\]','',name)
			xbmcsetResolvedUrl(maxspeedlink+'|'+urllib.urlencode(hd),name+'Maxlink')
		else:mes('[COLOR red]Get maxspeed link thất bại[/COLOR]')
	elif 'episode' in query:
		art=fanart.split('/banner/')[0] if fanart!=fanart.split('/banner/')[0] else ''
		href=os.path.dirname(url);id=get_id(url)
		start=query.split('episode')[0];eps=query.split('episode')[1]
		try: eps=int(eps)
		except:eps=int(xsearch('(\d{1,4})/\?',name,1) if xsearch('(\d{1,4})/\?',name,1) else '1')
		for epi in make_request('http://phim.megabox.vn/content/ajax_episode?id=%s&start=%s'%(id,start),resp='j'):
			name=epi['name'];href='%s/%s-%s.html'%(href,epi['cat_id'],epi['content_id'])
			if not art:fanart='http://img.phim.megabox.vn/300x168'+epi['image_banner']
			else:fanart=art+epi['image_banner']
			addir(name,href,img,fanart,mode,1,'mgbplay')
		if int(start)+30<eps:
			name=color['trangtiep']+u'Các tập tiếp theo: %d-%d[/COLOR]'%(int(start)+30,eps)
			addir(name,url,img,fanart,mode,1,'%depisode%d'%(int(start)+30,eps),True)
	elif 'Megabox giới thiệu' in name:dict=json_rw();load_urls(dict['gioithieu'])
	elif 'Top 10 phim trong ngày' in name:dict=json_rw();load_urls(dict['top10'])
	elif 'Phim sắp chiếu' in name:dict=json_rw();load_urls(dict['sapchieu'])
	elif query=='xemnhieu':#lẻ-bộ-show-clip xem nhiều
		cats={'lẻ':1,'bộ':2,'show':3,'clip':4};cat=[cats[s] for s in cats if s in name][0]
		href='http://phim.megabox.vn/mostviewed/ajax/?cat=%d&period=%d'
		period=[('ngày',1),('tuần',2),('tháng',3)];per=[s[0] for s in period if s[0] in name][0]
		for pe in period:
			if pe[0]==per:href=href%(cat,pe[1]);continue
			title=color['xshare']+re.sub('\[.?COLOR.*?\]','',name).replace(per,pe[0])+'[/COLOR]'
			addir(title,url,icon['megabox'],'',mode,1,query,True)
		load_urls(re.findall('<a href="(.+?)">',make_request(href,hd)))
	elif 'Phim Chiếu Rạp' in name or query=='phim-chieu-rap':
		href='http://phim.megabox.vn/t/phim-chieu-rap-29/phim-le/trang-%d'
		body=sub_body(make_request(href%page,maxr=3),'begin main','end main')
		pattern='<a class.+?href="(.+?)".+?title.>(.+?)</h3>(.+?)<img.+?src="(.+?)">(.+?)</a>.+?<a.+?a>(.+?)</div><'
		href_new,dict=put_items(re.findall(pattern,body,re.DOTALL))
		page_end=xsearch('<li class="last"><a href="t/phim-chieu-rap-29/phim-le/trang-(.+?)">',body,1)
		name=color['trangtiep']+'Trang tiếp theo: trang %d/%s[/COLOR]'%(page+1,page_end)
		addir(name,href,icon['megabox'],'',mode,page+1,'phim-chieu-rap',True)
		if href_new:endxbmc();update_href_new(href_new,dict)
	elif query=='subCate':#url=phim-le,phim-bo,t/phim-chieu-rap-29,show,clip
		if '/' in url:gen=url.split('/')[1];url=url.split('/')[0]
		else:gen='ALL'
		cat={'phim-le':('Lẻ',1),'phim-bo':('Bộ',2),'show':('Show',3),'clip':('Clip',4)}
		href='http://phim.megabox.vn/home/getcontent/?cat=%s&genre=%s&country=%s';dict=json_rw()
		for genre,country,gen_name in dict['subCate%d'%cat[url][1]]:
			gen_name=gen_name.encode('utf-8') if type(gen_name)==unicode else str2u(gen_name)
			if gen_name==gen:href=href%(cat[url][1],genre,country);continue
			title=color['xshare']+re.sub('\[.?COLOR.*?\]','',name);
			title=re.sub('%s.+\Z'%cat[url][0],cat[url][0]+' %s Mới Nhất[/COLOR]'%gen_name,title)
			addir(title,url+'/'+gen_name,icon['megabox'],'',mode,1,query,True)
		patt="<a class.+?href='(.+?)'.+?title.>(.+?)</h3>(.+?)<img.+?src='(.+?)'(.+?)</a>.+?<a.+?a>(.+?)</div></div>"
		put_items(re.findall(patt,make_request(href,hd),re.DOTALL),'i')
		cat={'phim-le':'Phim lẻ','phim-bo':'Phim bộ','show':'Show','clip':'Clip'}
		name=color['trangtiep']+'%s Xem Thêm...[/COLOR]'%cat[url]
		addir(name,url,icon['megabox'],'',mode,1,'mainmenu',True)
	return ''

def dangcaphd(name,url,img,mode,page,query):
	home='http://dangcaphd.com/'
	def dangcaphd_get_page_control(body,mode,query):
		pattern='<a class="current">\d{1,5}</a><a href="(.+?)">(\d{1,5})</a>.*<a href=".+?page=(\d{1,5})">.+?</a></div>'
		page_control=re.search(pattern,body)
		if page_control:
			href=re.sub('&amp;','',page_control.group(1));pagenext=page_control.group(2)
			pages=int(page_control.group(3))/rows+1
			name=color['trangtiep']+'Trang tiếp theo: trang %s/%d[/COLOR]'%(pagenext,pages)
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
	color['vuahd']='[COLOR deeppink]';icon['vuahd']=os.path.join(iconpath,'vuahd.png');home='http://vuahd.tv'
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
	color['pubvn']='[COLOR deepskyblue]';icon['pubvn']=os.path.join(iconpath,'pubvn.png');home='http://pubvn.tv/'
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
	home='http://movies.hdviet.com/'
	direct_link='https://api-v2.hdviet.com/movie/play?accesstokenkey=%s&movieid=%s'
	def namecolor(name):return '%s%s[/COLOR]'%(color['hdviet'],name)
	def getcookie():
		u=myaddon.getSetting('userhdviet');p=myaddon.getSetting('passhdviet')
		import hashlib;data=urllib.urlencode({'email':u,'password':hashlib.md5(p).hexdigest()})
		response=make_post('http://movies.hdviet.com/dang-nhap.html',hd,data)
		return response.cookiestring
	def login_hdviet():
		u=myaddon.getSetting('userhdviet');p=myaddon.getSetting('passhdviet')
		url='https://id.hdviet.com/authentication/login'
		response=make_post(url,data='email=%s&password=%s'%(u,p),resp='j')
		if response and response.get('error')==0:
			response=response.get('data')
			mess(u'[COLOR green]Login hdviet.com Success[/COLOR]',title='%sHDViet.com[/COLOR]'%color['hdviet'])
			json_rw('hdviet.cookie',response)
		elif response and response.get('error')==27:
			mess(u'[COLOR red]Acc bị khóa tạm thời. Vào web để login nhé!!![/COLOR]',title='%sHDViet.com[/COLOR]'%color['hdviet']);response=dict()
		elif response and response.get('error') in (25,22):
			mess(u'[COLOR red]%s[/COLOR]'%response.get('message'),title='%sHDViet.com[/COLOR]'%color['hdviet'])
			response=dict()
		else:
			import hashlib;data=urllib.urlencode({'email':u,'password':hashlib.md5(p).hexdigest()})
			response=make_post('http://movies.hdviet.com/dang-nhap.html',hd,data)
			try:resp=response.json
			except:resp={u'r': u'Lỗi đăng nhập hdviet.com', u'e': 3}
			if resp.get('e')==0:
				mess(u'[COLOR green]%s[/COLOR]'%resp['r'],title='%sHDViet.com[/COLOR]'%color['hdviet'])
				hd['Cookie']=response.cookiestring
				response=make_request('http://movies.hdviet.com/dieu-khoan-su-dung.html',headers=hd)
				import base64
				token=base64.b64decode(xsearch('<a class="userinfo".+?token=(.+?)"',response,1))
				response={'Cookie':hd['Cookie'],'access_token':token};json_rw('hdviet.cookie',response)
			else:response=dict();mess(u'[COLOR red]%s[/COLOR]'%resp['r'],title='%shdviet.com[/COLOR]'%color['hdviet'])
		url='http://movies.hdviet.com/dang-xuat.html?accesstokenkey=%s'
		make_post(url%response.get('access_token')).body
		return response
	def getResolvedUrl(id_film,loop=0):#Phim le/phim chieu/ke doi dau thien ac
		def getlinkhdviet(token,id_film):
			id_film=id_film.replace('_e','&ep=')
			response=make_request(direct_link%(token,id_film),resp='j')
			try:links=response['r'];link=response['r']['LinkPlay']
			except:links=dict()
			return links
		data=json_rw('hdviet.cookie')
		links=getlinkhdviet(data.get('access_token'),id_film)
		if not links:return links
		link=links.get('LinkPlay')
		if '0000000000000000000000' in link:
			data=login_hdviet();links=getlinkhdviet(data.get('access_token'),id_film);link=links.get('LinkPlay')
		if links:
			max_resolution='_1920_' if myaddon.getSetting('hdvietresolution')=='1080' else '_1280_'
			resolutions=['_1920_','_1885_','_1876_','_1866_','_1792_','_1280_','_1024_','_800_','_640_','_480_']
			if '_e' in id_film:link=re.sub('%s_e\d{1,3}_'%id_film.split('_')[0],'%s_'%id_film,link)
			href=link
			for resolution in resolutions:
				if resolution in link:link=link.replace(resolution,max_resolution);break
			extm3u=make_request(link);link=''
			if not extm3u:extm3u=make_request(href)
			for resolution in resolutions:
				if resolution in extm3u:link=xsearch('(http://.+%s.+m3u8)'%resolution,extm3u,1)
				if link:break
		if link and loop==0:
			response=make_request(link,resp='o')
			if response and 'filename' not in response.headers.get('content-disposition',''):
				data=login_hdviet();return getResolvedUrl(id_film,1)
		if link:
			audioindex=-1
			try:
				for audio in links.get('AudioExt'):
					if audio.get('Label')==u'Thuyết Minh':
						audioindex=int(audio.get('Index'))-1
				linksub='xshare' if audioindex>-1 else ''
			except:linksub=''
			if not linksub:
				for source in ['Subtitle','SubtitleExt','SubtitleExtSe']:
					try:
						linksub=links['%s'%source]['VIE']['Source']
						if linksub:
							if download_subs(linksub):break
					except:pass
			if audioindex>-1:link=link+'?audioindex=%d'%audioindex
		else:linksub=''
		return link,linksub
	def additems(body):
		pattern='<li class="mov-item".+?href="(.+?)".+?src="(.+?)".+?title="Phim (.+?)".+?<span(.+?) data-id="(.+?)">'
		data=re.findall(pattern,body,re.DOTALL);listitems=list()
		for href,img,title,detail,id_film in data:
			epi=xsearch('"labelchap2">(\d{1,3})</span>',detail,1);title=unescape(title)
			res=xsearch('id="fillprofile" class="icon-(.+?)11">',detail,1)
			res='[COLOR gold]SD[/COLOR]' if 'SD' in res else '[COLOR gold]HD[/COLOR]%s'%res
			phim18=xsearch('class="children11".+?>(.+?)</label></span>',detail,1)
			TM=xsearch('id="fillaudio" class="icon-(.+?)">',detail,1)
			TM='%s[COLOR green]%s[/COLOR][COLOR red]%s[/COLOR]'%(res,TM,phim18)
			plot=xsearch('<span class="cot1">(.+?)</span>',detail,1)
			year=xsearch('<span class="chil-date".+?>(.*?)</label></span>',detail,1)
			act=', '.join(s for s in re.findall('<a href="http://movies.hdviet.com/dien-vien/.+?">(.+?)</a>',detail))
			drt=', '.join(s for s in re.findall('<a href="http://movies.hdviet.com/dao-dien/.+?">(.+?)</a>',detail))
			rat=xsearch('<span class="fl-left">.+?<span>(.+?)</span>',detail,1)
			upl=xsearch('<span class="fl-right">.+?<span>(.+?)</span>',detail,1)
			if not epi:title=TM+' '+title;query='hdvietplay'
			elif epi=='1':query='hdvietfolder'
			else:title=TM+' '+namecolor(title)+' [COLOR green](%s)[/COLOR]'%epi;query='hdvietfolder'
			listItem = xbmcgui.ListItem(label=title,iconImage=img,thumbnailImage=img)
			if rat:rat='[COLOR tomato]IMDb:[/COLOR] %s, '%rat
			if upl:upl='[COLOR tomato]Uploader:[/COLOR] %s, '%upl
			if act:act='[COLOR tomato]Diễnviên:[/COLOR] %s, '%act
			if drt:drt='[COLOR tomato]Đạodiễn:[/COLOR] %s, '%drt
			plot=rat+upl+act+drt+'\n'+plot
			info={'title':title,'year':year,'rating':xsearch('(\d\.\d{1,2})',rat,1),'plot':plot,'episode':epi,'director':drt,'writer':act}
			listItem.setInfo(type="Video", infoLabels=info)
			listItem.setArt({"thumb":img,"poster":img,"fanart":img})
			if query=='hdvietplay':listItem.setProperty('IsPlayable', 'true')
			u=sys.argv[0]+"?url="+id_film+"&img="+urllib.quote_plus(img)+"&fanart="+urllib.quote_plus(img)+"&mode="+str(mode)+"&page="+str(page)+"&query="+query+"&name="+title
			listitems.append((u,listItem,False if query=='hdvietplay' else True))
		xbmcplugin.addDirectoryItems(int(sys.argv[1]),listitems,totalItems=len(listitems))
	def hdviet_search(string):
		url='http://movies.hdviet.com/tim-kiem.html?keyword=%s'%urllib.quote_plus(string)
		hdviet(name,url,img,mode,page,query='timkiem')
	if query=='hdviet.com':
		name=color['search']+"Search trên hdviet.com[/COLOR] (Hãy chọn độ phân giải trên settings nhé)"
		addir(name,'http://movies.hdviet.com/tim-kiem.html',icon['icon'],fanart,mode,1,'search',True)
		if checkupdate('hdviet.html')>8:body=makerequest(joinpath(datapath,'hdviet.html'),make_request(home),'w')
		else:body=makerequest(joinpath(datapath,'hdviet.html'))
		items=re.findall('"mainitem" menuid="(.+?)" href="(.+?)" title=".+?">(.+?)</a>',body)
		for id,href,name in items:
			addir(namecolor(name),home,icon['hdviet'],fanart,mode,1,id,True)
		addir(namecolor('Thể loại phim'),'the-loai',icon['icon'],fanart,mode,1,'the-loai-phim',True)
		url='http://movies.hdviet.com/phim-yeu-thich.html'
		addir(namecolor('Phim yêu thích'),url,icon['icon'],fanart,mode,1,'yeu-thich',True)
		items=re.findall('<div class="h2-ttl cf">.+?<a href="(.+?)" title=".+?" >(.+?)</a>.+?</div>(.+?)</ul>',body,re.DOTALL)
		for href,name,subbody in items:
			addir('%s%s[/COLOR]'%(color['search'],name),href,icon['hdviet'],fanart,mode,page,'1',True)
			additems(subbody)
	elif query=='search':make_mySearch('','hdviet.com','','',mode,'get')
	elif query=="INP":hdviet_search(make_mySearch('',url,'','','','Input'))
	elif url=='hdviet.com':page=1 if 'Trang tiếp theo' not in name else page;hdviet_search(query)
	elif query=='the-loai-phim':
		for href,name in re.findall('<p><a href="(.+?)" title=".+?">(.+?)</a></p>',makerequest(joinpath(datapath,'hdviet.html'))):
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,'theloai',True)
	elif query=='3' and url==home:#Phim lẻ
		items=re.findall('<a href="(.+?)" .?menuid="(.+?)" .?title=".+?" >(.+?)</a>',makerequest(joinpath(datapath,'hdviet.html')))
		for href,id,name in items:
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,id,True)
	elif query=='10' and url==home:#Phim bộ
		body=makerequest(joinpath(datapath,'hdviet.html'))
		items=re.findall('<a href="(.+?)" menuid="(.+?)" title=".+?">(.+?)</a>',body)
		items+=re.findall('<a class="childparentlib" menuid="(.+?)" href="(.+?)" title=".+?">(\s.*.+?)</a>',body)
		for href,id,name in items:
			if 'au-my' in href:name='Phim bộ Âu Mỹ %s'%name.strip()
			elif 'hong-kong' in href:name='Phim bộ Hồng Kông %s'%name.strip()
			elif 'trung-quoc' in href:name='Phim bộ Trung Quốc %s'%name.strip()
			else:name='Phim bộ %s'%name.strip()
			if href in '38-39-40':temp=href;href=id;id=temp
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,id,True)
	elif query=='hdvietfolder':
		href='http://movies.hdviet.com/lay-danh-sach-tap-phim.html?id=%s'%url
		response=make_request(href,resp='j')
		if not response:return
		for eps in range(1,int(response["Sequence"])+1):
			name=re.sub(' \[COLOR green\]\(\d{1,4}\)\[/COLOR\]','',name)
			title='Tập %s/%s-%s'%(format(eps,'0%dd'%len(response['Episode'])),str(response['Episode']),re.sub('\[.?COLOR.{,12}\]','',name))
			addir(title,'%s_e%d'%(url,eps),img,fanart,mode,page,'hdvietplay',False)
	elif query=='hdvietplay':
		link,sub=getResolvedUrl(url)
		if not link:mess(u'[COLOR red]Get link thất bại[/COLOR]',title='%sHDViet.com[/COLOR]'%color['hdviet'])
		else:
			if sub:
				mess(u'[COLOR green]Phụ đề của HDViet.com[/COLOR]',title='%sHDViet.com[/COLOR]'%color['hdviet'])
				sub=urllib.unquote(os.path.splitext(os.path.basename(sub))[0])
			xbmcsetResolvedUrl(link+'|'+urllib.urlencode(hd),sub)
	elif query=='Themmucyeuthich':
		hd['Cookie']=getcookie()
		body=make_post('http://movies.hdviet.com/them-phim-yeu-thich.html',hd,urllib.urlencode({"MovieID":"%s"%url}))
		try:mess(u'[COLOR green]%s[/COLOR]'%body.json['r'],title='%sHDViet.com[/COLOR]'%color['hdviet'])
		except:mess(u'[COLOR red]Lỗi thêm phim yêu thích[/COLOR]',title='%sHDViet.com[/COLOR]'%color['hdviet'])
	else:
		if query=='yeu-thich':hd['Cookie']=getcookie();body=make_request(url,hd)
		else:body=make_request(url)
		body=sub_body(body,'class="homesection"','class="h2-ttl cf"')
		additems(body)
		pages=re.findall('<li class=""><a href="(.+?)">(.+?)</a></li>',sub_body(body,'class="active"',''))
		if pages:
			pagenext=pages[0][1];pageend=pages[len(pages)-1][1]
			name='%sTrang tiếp theo: trang %s/%s[/COLOR]'%(color['trangtiep'],pagenext,pageend)
			addir(name,pages[0][0],img,fanart,mode,page,query,True)
		xbmc.executebuiltin('Container.SetViewMode(504)')

def play_youtube(url):#https://www.youtube.com/get_video_info?video_id=xhNy0jnAgzI
	def choice_solution(items,label_quality):#label_quality in ('quality','quality_label')
		url=''
		for solution in ('1080','720','medium','small'):
			for item in items:
				x,y=item.get(label_quality),item.get('type')
				if x and y and solution in x and 'video' in y and 'mp4' in y:
					url=urllib.unquote(item.get('url'));break
			if url:break
		return url
	url='https://www.youtube.com/watch?v=%s&spf=navigate-back'%xsearch('(\w{10,20})',url,1)
	data=make_request(url,resp='j',maxr=3);fmts=''
	if not data:return
	for i in range(0,len(data)):#'adaptive_fmts','url_encoded_fmt_stream_map'
		try:fmts=data[i]['data']['swfcfg']['args']['url_encoded_fmt_stream_map'];break
		except:pass
	data=[];link=''
	for items in fmts.split(','):
		dict={}
		for item in items.split('&'):
			try:dict[item.split('=')[0]]=item.split('=')[1]
			except:pass
		data.append(dict)
	link=choice_solution(data,'quality')
	if link:xbmcsetResolvedUrl(link,re.sub(' \[COLOR.+?/COLOR\]','',name)+'Maxlink')
	else:mess(u'[COLOR red]Get maxspeed link fail[/COLOR]',title='[COLOR green]youtube.com[/COLOR]')

def hayhaytv(name,url,img,fanart,mode,page,query):
	home='http://www.hayhaytv.vn/';ajax=home+'ajax_hayhaytv.php';api='http://api.hayhaytv.vn/'
	color['hayhaytv']='[COLOR tomato]';icon['hayhaytv']=os.path.join(iconpath,'hayhaytv.png')
	def login():
		u=myaddon.getSetting('userhayhay');p=myaddon.getSetting('passhayhay')
		data=urllib.urlencode({'email':u,'password':p,'remember_account':0})
		response=make_post('%sajax_jsonp.php?p=jsonp_login'%home,data=data)
		try:
			if response.json['success']=='success':
				mes(u'[COLOR green]Login hayhaytv thành công[/COLOR]');f=response.cookiestring
				makerequest(joinpath(datapath,'hayhaytv.cookie'),f,'w')
			else:mes(u'[COLOR red]Bạn hãy kiểm tra user/pass trên hayhaytv.vn[/COLOR]');f=''
		except:mes(u'[COLOR red]Login hayhaytv thấy bại[/COLOR]');f=''
		return f
	def mes(string):mess(string,title=namecolor('hayhaytv.vn'))
	def namecolor(name):return '%s%s[/COLOR]'%(color['hayhaytv'],name)
	def get_date(string):
		s=xsearch('/(\d{8})/',string,1)
		return '%s/%s/%s'%(s[:2],s[2:4],s[4:8]) if s else None
	def get_year(string):return xsearch('(20\d\d|19\d\d)',string,1)
	def get_idw(url):return xsearch('-(\w{6,20})\.html',url,1)
	def get_id(content):return xshare_group(re.search('FILM_ID\D{3,7}(\d{3,6})',content),1)
	def get_i(content,tag):return xsearch('<.+%s:.+>(.+?)?</li>'%tag,content,1).strip()
	def setskin():
		if xbmc.getSkinDir()=='skin.confluence':xbmc.executebuiltin('Container.SetViewMode(504)')
	def hayhaytv_search(string):
		url='http://www.hayhaytv.vn/tim-kiem/%s/trang-1'%'-'.join(s for s in string.split())
		hayhaytv(name,url,img,mode,page=1,query='M3')
	def getinfo(body,sticky=dict()):
		for stic,info,plot in re.findall('id="(sticky.+?)" class="atip">(.+?)<p>(.*?)</p>',body,re.DOTALL):
			gen=get_i(info,'Thể loại');ctry=get_i(info,'Quốc Gia');rat=get_i(info,'IMDB')
			dur=xsearch('(\d{1,4})',get_i(info,'Thời lượng'),1)
			eps=xsearch('<span>Số tập:</span>(.+?)</li>',info,1,re.DOTALL).strip()
			sticky[stic]=(eps,gen,ctry,dur,rat,plot)
		#pattern='<a.+?tooltip="(.+?)" href="(.+?)">.*?"(http://img.*?)".*?color">(.*?)</span>.*?<span>(.*?)</span>(.*?)</a>'
		pattern='tooltip="(.+?)".+?href="(.+?)">.+?"(http://img.+?)".+?color">(.*?)</span>.*?<span>(.*?)</span>(.*?)</a>'
		items=list()#vie,eng,href,img,epi,eps,gen,ctry,dur,rat,plot
		for stic,href,img,eng,vie,tap in re.findall(pattern,body,re.DOTALL):
			if sticky.get(stic):items.append(((vie,eng,href,img,xsearch('<p>(.+?)</p>',tap,1))+sticky[stic]))
		return items
	def update_home(adict):
		mes(u'[COLOR green] Database updating...[/COLOR]')
		body=make_request(home,headers=hd)
		if not body:return adict
		content=sub_body(body,'class="menu_header"','class="box_login"')
		adict['mar-r20']=[s for s in re.findall('menu_fa_text.+?" href="(.+?)".*>(.+?)</a>',body) if os.path.basename(s[0])]
		for href,item in re.findall('href="(.+?)".+?<a (.+?)</ul>',content,re.DOTALL):
			for link,name in adict['mar-r20']:
				if href==link and 'trailer' not in link:
					name=os.path.basename(href)
					adict['m-%s'%name]=re.findall('href="(.+?)".*?>(.+?)</a>',item)
		pattern='href="(.+?)".*?>(.+\s.+|.+?)</a>.*\s?.*</h2>'
		adict['main']=[(s[0],' '.join(s for s in s[1].split())) for s in re.findall(pattern,body)]
		content=sub_body(body,'class="banner_slider"','class="main"')
		adict['banner_slider']=re.findall('<h3><a href=".+-(\w{5,20})\.html"',content)
		for p in ('phimbo','phimle','tvshow','clip'):
			mes(u'[COLOR green] Database updating...%s[/COLOR]'%p)
			for page in range(1,100):
				url='http://www.hayhaytv.vn/ajax_hayhaytv.php?p=%s&page=%d'%(p,page)
				items=getinfo(make_post(url,resp='b'));items_new=[s for s in items if get_idw(s[2]) not in adict]
				for s in items:adict[get_idw(s[2])]=s
				if len(items_new)==0:break
		xbmc.executebuiltin("Dialog.Close(all, true)")
		return json_rw('hayhaytv.json',dicts=adict)
	def addDirs(items,page='1'):
		listitems=list()
		for item in items:
			vie,eng,href,img,epi,eps,gen,ctry,dur,rat,plot=item
			#vie,eng,href,img,fan,thumb,date,year,gen,ctry,dur,rat,rev,views,epi,eps,drt,act,upl,sea,plot=item
			href='%s/%s'%(os.path.dirname(href),urllib.quote(u2s(os.path.basename(href))))
			title=vie+' - '+eng if vie and eng else vie if vie else eng;dur=xsearch('(\d{1,4})',dur,1)
			if eps and eps!='1':query='readfolder';title=namecolor(title)+' %s/%s'%(epi if epi else '?',eps)
			else:query='play'
			fan=img.replace('/crop/','/');thumb=img.replace('/crop/','/thumb/')
			date=get_date(img);year=get_year(eng);sea=xsearch('Season (\d{1,2})',eng,1)
			listItem = xbmcgui.ListItem(label=title,iconImage=img,thumbnailImage=thumb)
			if rat:plot='[COLOR tomato]IMDB:[/COLOR] %s\n'%rat+plot
			info={'title':title,'date':date,'year':year,'duration':dur,'rating':rat,'country':ctry,'genre':gen+' [COLOR green]%s[/COLOR]'%ctry,'plot':plot,'Episode':epi,'Season':sea}
			listItem.setInfo(type="Video", infoLabels=info)
			listItem.setArt({"thumb":thumb,"poster":img,"fanart":fan})
			if query=='play':listItem.setProperty('IsPlayable', 'true')
			u=sys.argv[0]+"?url="+urllib.quote_plus(href)+"&img="+urllib.quote_plus(img)+"&fanart="+urllib.quote_plus(fan)+"&mode="+str(mode)+"&page="+str(page)+"&query="+query+"&name="+title
			listitems.append((u,listItem,False if query=='play' else True))
		xbmcplugin.addDirectoryItems(int(sys.argv[1]),listitems,totalItems=len(listitems))
		return len(listitems)
	def getlink(body):
		movie_id=get_id(body);pattern='<title>.*xx(.+?)xx.*</title>';print 'movie_id %s'%movie_id
		href=xsearch('<link rel="canonical" href="(.+?)"',body,1)
		list_episodes=dict(re.findall('class=.*?href="(.+?)".*?>\D*([\d-]+)</',body))
		tap=list_episodes.get(href);print 'Tap: %s'%tap
		s=xsearch(pattern,make_request('https://www.fshare.vn/folder/5VNFUPO32P6F'),1).split('-')
		hd={s[0]:'%s %s'%(s[1],s[2])};data={"secure_token":"1.0","request":'{"movie_id":"%s"}'%movie_id}
		response=make_post('%smovie/movie_detail'%api,hd,data,'j');print 'Tap %s'%tap
		if response.get('data') and response['data'].get('list_episode') and len(response['data']['list_episode'])>0:
			eps=response['data']['list_episode']
			ids=[(s.get('id'),s.get('vn_subtitle')) for s in eps if s.get('name')==tap or s.get('name')==u'Tập '+tap]
			if ids:movie_id,sub=ids[0];href='%sgetlink/movie_episode'%api
			else:href=sub=''
		else:
			href='%sgetlink/movie'%api
			try:sub=response['data']['vn_subtitle'];print 'movie_id %s'%movie_id
			except:sub=''
		if href:
			data["request"]='{"data":[{"type":"facebook","email":"%s"}]}'%myaddon.getSetting('userhayhay')
			response=make_post('%suser/signup_social_network'%api,hd,data,'j')
			if response:
				token=response['data']['token_app'];user_id=response['data']['user_id']
				data['request']='{"token":"%s","user_id":"%s","movie_id":"%s"}'%(token,user_id,movie_id)
				print data
				response=make_post(href,hd,data,'j')
				try:href=response['data']['link_play'][0]['mp3u8_link']
				except:href=''
		return href,sub

	if checkupdate('hayhaytv.cookie')>24:hd['Cookie']=login()
	else:hd['Cookie']=makerequest(joinpath(datapath,'hayhaytv.cookie'))
	if query=='hayhaytv.vn':
		name=color['search']+"Search trên hayhaytv.vn[/COLOR]"
		addir(name,'http://www.hayhaytv.vn/tim-kiem/',icon['hayhaytv'],fanart,mode,1,'search',True)
		addir(namecolor("HayhayTV giới thiệu"),'gioithieu',icon['hayhaytv'],fanart,mode,1,'gioithieu',True)
		adict=json_rw('hayhaytv.json')
		if not adict.get('mar-r20') or not adict.get('main'):adict=update_home(adict)
		for href,name in adict['mar-r20']:
			addir(namecolor(name),href,icon['hayhaytv'],fanart,mode,1,'mainmenu',True)
		for href,name in adict['main']:
			addir(namecolor(name),href,icon['hayhaytv'],fanart,mode,1,'submenu',True)
		if checkupdate('hayhaytv.json')>8 and not os.path.isfile(joinpath(datapath,'hayhaytv.tmp')):
			endxbmc();makerequest(joinpath(datapath,'hayhaytv.tmp'),'','w')
			adict=update_home(adict);delete_files(datapath,mark='hayhaytv.tmp')
	elif query=='search':make_mySearch('','hayhaytv.vn','','',mode,'get')
	elif query=="INP":hayhaytv_search(make_mySearch('',url,'','','','Input'))
	elif url=='hayhaytv.vn':page=1 if 'Trang tiếp theo' not in name else page;hayhaytv_search(query)
	if query=='gioithieu':
		adict=json_rw('hayhaytv.json')
		addDirs([adict.get(s) for s in adict.get('banner_slider')]);setskin()
	elif query=='mainmenu':
		theloai=os.path.basename(url).replace('-','');q='filter'
		if theloai=='shows':theloai='tvshow'
		elif theloai=='cliphay':theloai='clip';q='theloai'
		elif url=='http://www.hayhaytv.vn/trailer':
			href='http://www.hayhaytv.vn/ajax_hayhaytv.php?p=trailer&page=1'
			return hayhaytv(name,href,img,fanart,mode,1,'submenu')
		for href,name in json_rw('hayhaytv.json',key='m-%s'%os.path.basename(url)):
			addir(namecolor(name),href,img,fanart,mode,1,'submenu',True)
	elif query=='submenu':
		body=make_request(url,maxr=3);adict=json_rw('hayhaytv.json')
		if 'http://www.hayhaytv.vn/su-kien/' in url or 'q=su-kien' in url:
			ids=re.findall('<a title=".+?" href=".+-(\w{10,20})\.html"',body)
			if not ids:mes(u'[COLOR red]Hiện tại không có nội dung mục này.[/COLOR]');return 'no'
			addDirs([adict.get(s) for s in ids])
			urlnext=home+xsearch('class=.active.+?onclick=.+?"(ajax_ht.php.+?)"',body,1)
			pagenext=xsearch('page=(\d{1,4})',urlnext,1);pagelast=xsearch('trang-(\d{1,4})-.{,50}Cuối',body,1)
		else:
			items=getinfo(body)
			if not items:mes(u'[COLOR red]Hiện tại không có nội dung mục này.[/COLOR]');return 'no'
			addDirs(items);urlnext=home+xsearch('class=.active.+?"(ajax_hayhaytv.php.+?)"',body,1)
			pagenext=xsearch('page=(\d{1,4})',urlnext,1);pagelast=xsearch('Trang \d{1,4}/(\d{1,4})',body,1)
		if pagenext:
			name=re.sub('\[.+?\]','',name.split('-')[0].strip())
			name='%s%s - Trang tiếp theo: trang %s/%s[/COLOR]'%(color['trangtiep'],name,pagenext,pagelast)
			addir(name,urlnext,img,fanart,mode,page+1,'submenu',True)
		setskin()
	elif query=='readfolder':#Phim bo moi: Truy Tìm Kho Báu
		pages=0;adict=json_rw('hayhaytv.json')
		if page==1:
			body=sub_body(make_request(url,headers=hd,maxr=3),'<div id="new_player">','class="content_div"')
			list_episodes=re.findall('class=.*?href="(.+?)".*?>\D*([\d-]+)</',body);items=list()
			item=adict.get(get_idw(url))
			if item:vie,eng,href,img,epi,eps,gen,ctry,dur,rat,plot=item
			else:vie=re.sub('\[.+?\]','',s2u(name));eps=xsearch('\w{0,3}/(\d{1,4})',name,1);eng=epi=gen=ctry=dur=rat=plot=''
			for href,tap in list_episodes:
				vi=u'Tập %s/%s%s'%(tap,eps,'-'+vie if vie else '')
				items.append((vi,eng,href,img,epi,'',gen,ctry,dur,rat,plot))
			if 'http://www.hayhaytv.vn/xem-show' in url:
				pages=xsearch("onclick='paging\((\d{1,3})\)'> &raquo",body,1)
				pages=int(pages) if pages else 0;id=xsearch('episode_(.+?)_unactive',body,1)
				url='http://www.hayhaytv.vn/tvshow/paging?page=2&q=episode&id=%s&pages=%d'%(id,pages)
			if pages or len(items)>rows:makerequest(joinpath(datapath,"temp.txt"),str(items),'w')
		else:
			try:items=eval(makerequest(joinpath(datapath,"temp.txt")))
			except:items=[]
			if 'http://www.hayhaytv.vn/tvshow/paging' in url and items:
				vie,eng,href,img,epi,eps,gen,ctry,dur,rat,plot=items[0]
				body=make_post(url.split('?')[0],data=url.split('?')[1],resp='b');items=list()
				for href,tap in re.findall('class=.*?href="(.+?)".*?>\D*([\d-]+)</',body):
					vi=re.sub(u'Tập \d{1,4}/',u'Tập %s/'%tap,vie)
					items.append((vi,eng,href,img,epi,'',gen,ctry,dur,rat,plot))
				pages=xsearch('pages=(\d{1,4})\Z',url.split('?')[1],1)
				if pages and int(pages)>page:
					url=re.sub('page=\d{1,4}&','page=%s&'%str(page+1),url);pages=int(pages)
				else:pages=0
		if 'http://www.hayhaytv.vn/tvshow' not in url:
			pages=len(items)/(rows+1)+1;del items[:rows*(page-1)];del items[rows:]
		addDirs(items)
		if pages>page:
			name=color['trangtiep']+'Trang tiếp theo...trang %d/%d[/COLOR]'%(page+1,pages)
			addir(namecolor(name),url,img,fanart,mode,page+1,'readfolder',True)
		setskin()
	elif query=='play':
		print url
		body=make_request(url,headers=hd,maxr=3);trailer=xsearch("initTrailerUrl = '(.+?)'",body,1)
		if trailer:xbmcsetResolvedUrl(trailer)
		elif '/xem-clip/' not in url:
			if '/xem-show/' in url:mes(u'[COLOR red]Chưa code phần này !!![/COLOR]');return
			href,sub=getlink(body)
			if href:
				if sub and download_subs(sub):mes(u'[COLOR green]Phụ đề của hayhaytv.vn[/COLOR]')
				xbmcsetResolvedUrl(href,urllib.unquote(os.path.splitext(os.path.basename(sub))[0]))
			else:mes(u'[COLOR red]Get max link thất bại...[/COLOR]')
		else:
			href=xsearch('src="(http://www.youtube.com.+?)"',body,1)
			if href:play_youtube(href)
			else:mes('[COLOR red]Link youtube.com find not found ![/COLOR]')

def phimmoi(name,url,img,mode,page,query):
	color['phimmoi']='[COLOR ghostwhite]';icon['phimmoi']=os.path.join(iconpath,'phimmoi.png')
	home='http://www.phimmoi.net/';refresh=False;phimmoixml=joinpath(datapath,'phimmoi.xml')
	tempfolder=xbmc.translatePath('special://temp')
	def namecolor(name):return '%s%s[/COLOR]'%(color['phimmoi'],name)
	def mes(string):mess(string,title=namecolor('phimmoi.net'))
	def login_pm():
		u=myaddon.getSetting('userphimmoi');p=myaddon.getSetting('passphimmoi')
		import hashlib;p=hashlib.md5(p).hexdigest()
		response=make_post('http://www.phimmoi.net/login/',data=urllib.urlencode({'username':u,'password_md5':p}))
		if response.status==302:
			mes(u'[COLOR green]Login thành công[/COLOR]');f=response.cookiestring
		else:mes(u'[COLOR red]Login không thành công[/COLOR]');f=''
		return f
	def search(string):
		url='http://www.phimmoi.net/tim-kiem/%s/'%urllib.quote_plus(string)
		phimmoi(name,url,img,mode,page=1,query='page')
	def getid(url):return xshare_group(re.search('-(\d{3,5})/',url),1)
	def geteps(string):
		try:url=json.loads(string)['url'];part=json.loads(string)['part']
		except:url=part=''
		return url,part
	def make_eps(url,eps):
		id=getid(url);content=makerequest(phimmoixml);string=''
		string_old=xshare_group(re.search('(<a id="%s" part=".+?"/>)'%id,content),1)
		for part_id in eps:string+=str(geteps(part_id)[1])+'-'
		string_new='<a id="%s" part="%s"/>\n'%(id,string[:len(string)-1])
		string=content.replace(string_old+'\n',string_new) if string_old else content+string_new
		makerequest(phimmoixml,string,'w')
	def addir_pm(items,name=''):#title,href,img,detail
		for title,href,img,detail in items:
			eps=xsearch('Tập ?(\d{,4}/\d{,4}|\?/\d{,4}|\d{,4})',detail,1)
			if not eps:
				epi=xsearch('class="eps">Trọn bộ ?(\d{1,4}) ?tập</div>',detail,1)
				if epi:eps='%s/%s'%(epi,epi)
			else:epi=eps.split('/')[0]
			try:epi=int(epi)
			except:epi=0
			dur=xsearch('>(\d{1,3}.?phút)',detail,1)
			if 'url=' in img:img=img.split('url=')[1]
			if eps:title='%s %s(%s)[/COLOR]'%(title,color['subscene'],eps)
			if dur:title='%s [COLOR gold]%s[/COLOR]'%(title,dur)
			if epi>1 or 'Phim bộ hot trong tuần' in name:query='folder';isFolder=True;title=namecolor(title)
			else:query='play';isFolder=False
			if 'Thuyết minh' in detail:title='[COLOR gold]TM[/COLOR] %s'%title
			label=xsearch('(HD[\w|-]*|SD[\w|-]*|Bản đẹp[\w|-]*)',detail,1)
			if label:title='%s - [COLOR green]%s[/COLOR]'%(title,label)
			addir(title,home+href,img,'',mode,page,query,isFolder)
		
	if query=='phimmoi.net':
		url={1:'phim-kinh-dien/',2:'phim-chieu-rap/',3:'tags/top+10+imdb+2014/',4:'login/'}
		name=color['search']+"Search trên phimmoi.net[/COLOR] (Chọn độ phân giải max trên settings nhé)"
		addir(name,'http://www.phimmoi.net/tim-kiem/',icon['phimmoi'],mode=mode,query='search',isFolder=True)
		addir(namecolor('Thể loại'),home+url[4],icon['phimmoi'],mode=mode,query='the-loai',isFolder=True)
		addir(namecolor('Quốc gia'),home+url[4],icon['phimmoi'],mode=mode,query='quoc-gia',isFolder=True)
		addir(namecolor('Phim lẻ'),home+url[4],icon['phimmoi'],mode=mode,query='phim-le',isFolder=True)
		addir(namecolor('Phim bộ'),home+url[4],icon['phimmoi'],mode=mode,query='phim-bo',isFolder=True)
		addir(namecolor('Phim kinh điển'),home+url[1],icon['phimmoi'],mode=mode,query='page',isFolder=True)
		addir(namecolor('Phim chiếu rạp'),home+url[2],icon['phimmoi'],mode=mode,query='page',isFolder=True)
		addir(namecolor('Top 10 IMDb 2014'),home+url[3],icon['phimmoi'],mode=mode,query='top10',isFolder=True)
		addir(namecolor('Phim đề cử'),home,icon['phimmoi'],mode=mode,query='de-cu',isFolder=True)
		addir(namecolor('Phim lẻ hot trong tuần'),home+url[4],icon['phimmoi'],mode=mode,query='lehot',isFolder=True)
		addir(namecolor('Phim bộ hot trong tuần'),home+url[4],icon['phimmoi'],mode=mode,query='bohot',isFolder=True)
		addir(namecolor('Phim lẻ mới'),home,icon['phimmoi'],mode=mode,query='tablemoi',isFolder=True)
		addir(namecolor('Phim bộ mới'),home,icon['phimmoi'],mode=mode,query='tabbomoi',isFolder=True)
		addir(namecolor('Phim bộ full'),home,icon['phimmoi'],mode=mode,query='tabbofull',isFolder=True)
		addir(namecolor('Phim chiếu rạp mới'),home,icon['phimmoi'],mode=mode,query='chieurapmoi',isFolder=True)
		addir(namecolor('Phim lẻ mới cập nhật'),home,icon['phimmoi'],mode=mode,query='lemoicapnhat',isFolder=True)
		addir(namecolor('Phim bộ mới cập nhật'),home,icon['phimmoi'],mode=mode,query='bomoicapnhat',isFolder=True)
		addir(namecolor('Phim hoạt hình mới cập nhật'),home,icon['phimmoi'],mode=mode,query='hoathinh',isFolder=True)
	if query=='home':
		name=color['search']+"Search trên phimmoi.net[/COLOR] (Chọn độ phân giải max trên settings nhé)"
		addir(name,'http://www.phimmoi.net/tim-kiem/',icon['phimmoi'],mode=mode,query='search',isFolder=True)
		body=makerequest(joinpath(tempfolder,'phimmoi.html'))
		content=xsearch('<ul id=".+?"(.+?)</ul></div>',body,1)
		for title in re.findall('<a>(.+?)</a>',content):
			addir(namecolor(title),'',icon['phimmoi'],mode=mode,query='menubar',isFolder=True)
		for href,title in re.findall('<a href="([\w|-]+/|http://www.phimmoi.net/tags/.*?)">(.+?)</a>',content):
			addir(namecolor(title),href,icon['phimmoi'],'',mode,1,'menubar',isFolder=True)
		for title in re.findall('<h2 class="right-box-header star-icon"><span>(.+?)</span>',body):
			addir(namecolor(title),'right-box',img,'',mode,1,'menubar',True)
		for title,content in re.findall('<h2 class="hidden">(.+?)</h2>(.+?)</div></li></ul>',body):
			addir('[COLOR lime]%s[/COLOR]'%title,'',img,'',mode,1,'no')
			pattern='title="(.+?)" href="(.+?)".+?\(\'(http.+?)\'\).+?</div></a>(.+?)</div></li>'
			addir_pm(re.findall(pattern,content))#title,href,img,detail
		for label,content in re.findall('class="title-list-index">(.+?)</span>(.+?)</div></div></div>',body):
			addir('[COLOR lime]%s[/COLOR]'%label,'',img,'',mode,1,'no')
			pattern='<li><a href="(.+?)" title="(.+?)">.+?<img src="(.+?)".+?<h3(.+?)</p>'
			items=re.findall(pattern,content)
			if items:addir_pm([(s[1],s[0],s[2],s[3]) for s in items])#title,href,img,detail
			else:
				pattern='"movie-item m-block" title="(.+?)" href="(.+?)".+?(http.+?\.jpg).+?<div(.+?)</div></a></li>'
				addir_pm(re.findall(pattern,content))#title,href,img,detail
		if checkupdate('phimmoi.html',tempfolder)>8:
			endxbmc();makerequest(joinpath(tempfolder,'phimmoi.html'),make_request('http://www.phimmoi.net/'),'w')
	elif query=='search':make_mySearch('','phimmoi.net','','',mode,'get')
	elif query=="INP":search(make_mySearch('',url,'','','','Input'))
	elif url=='phimmoi.net':page=1 if 'Trang tiếp theo' not in name else page;search(query)
	elif query=='menubar':
		if any(s for s in ['kinh','rap','tags','trailer'] if s in url):
			if 'tags' not in url:url=home+url
			return phimmoi(name,url,img,mode,page,'readpage')
		elif url=='right-box':
			if 'Phim đã đánh dấu' in name:
				hd['Cookie']=login_pm()
				token=xsearch("fx.token='(.+?)'",make_request('http://www.phimmoi.net/tu-phim/',headers=hd),1)
				url=home+'bookmark/load.html?_fxAjax=1&_fxResponseType=JSON&_fxToken=%s&idList=3008'%token
			else:
				pattern='<span>%s</span>(.+?</li></ul></div></div>)'%re.sub('\[/?COLOR.*?\]','',name).strip()
				content=xsearch(pattern,makerequest(joinpath(tempfolder,'phimmoi.html')),1)
				pattern='title="(.+?)" href="(.+?)">.+?\(\'(.+?)\'\).+?</span>(.+?)</a></li>'
				addir_pm(re.findall(pattern,content),name)#title,href,img,detail
		else:
			content=xsearch('<ul id=".+?"(.+?)</ul></div>',makerequest(joinpath(tempfolder,'phimmoi.html')),1)
			gen={'Thể loại':'the-loai','Quốc gia':'quoc-gia','Phim lẻ':'phim-le','Phim bộ':'phim-bo'}
			query=gen.get(re.sub('\[/?COLOR.*?\]|\(.+?\)','',name).strip())
			pattern='<a href="(%s/.*?)">(.+?)</a>'%query
			for href,title in re.findall(pattern,content):
				addir(namecolor(title),home+href,icon['phimmoi'],'',mode,1,'readpage',True)
	elif query in 'the-loai quoc-gia phim-le phim-bo':
		for href,name in re.findall('<li><a href="(%s/.*?)">(.+?)</a>'%query,make_request(url)):
			addir(namecolor(name),home+href,icon['phimmoi'],mode=mode,query='page',isFolder=True)
	elif query=='de-cu':
		body=make_request(url);body=body[body.find('Phim đề cử'):body.find('<!-- slider -->')]
		pattern='href="(.+?)" title="(.+?)".+?src="(.+?)".+?style=".+?">(.+?)</span>'
		for href,name,img,eps in re.findall(pattern,body):
			img=re.sub("http.*=http","http",img).replace("'","")
			epi=xshare_group(re.search('Tập (\d{1,3})/?',eps),1)
			if epi and int(epi)>1:query='folder';isFolder=True;name=namecolor(clean_string(name))
			else:query='play';isFolder=False;name=clean_string(name)
			name=name+color['subscene']+' ('+clean_string(eps)+')[/COLOR]'
			addir(name,home+href,img,fanart,mode,page,query=query,isFolder=isFolder)
	elif query in 'tablemoi-tabbomoi-tabbofull-lemoicapnhat-bomoicapnhat-chieurapmoi-hoathinh-top10-lehot-bohot':
		section={'lemoicapnhat':('"Phim lẻ mới nhất"','/Phim lẻ mới','.*?chap">(.+?)<.*?ribbon">(.+?)<'),
		'bomoicapnhat':('"Phim bộ mới nhất"','/Phim bộ mới','.*?chap">(.+?)<.*?ribbon">(.+?)<'),
		'chieurapmoi':('"Phim chiếu rạp mới nhất"','/Phim chiếu rạp','.*?chap">(.+?)<.*?ribbon">(.+?)<'),
		'hoathinh':('"Phim hoạt hình mới nhất"','/Phim hoạt hình mới','.*?chap">(.+?)<.*?ribbon">(.+?)<'),
		'top10':('"title-list-index"','"col-lg-4 sidebar"','.*?chap">(.+?)<()'),
		'tablemoi':('"tabs-1"','"tabs-2"','.*?eps">(.+?)<()'),
		'tabbomoi':('"tabs-2"','"tabs-3"','.*?eps">(.+?)<()'),
		'tabbofull':('"tabs-3"','- Phim chiếu rạp -','.*?eps">(.+?)<()'),
		'lehot':('Box: Top phim lẻ','/Box: Top phim lẻ','.*?view">(.+?)<()'),
		'bohot':('Box: Top phim bộ','/Box: Top phim bộ','.*?view">(.+?)<()')}
		pattern='title="(.+?)" href="(.+?)".*?url\((.+?)\)%s'%section[query][2]
		body=make_request(url);body=body[body.find(section[query][0]):body.find(section[query][1])]
		for name,href,img,eps,rib in re.findall(pattern,body,re.DOTALL):
			epi=xshare_group(re.search('Tập (\d{1,3})/?',eps+rib),1)
			if (epi and int(epi)>1) or 'bo' in query:query='folder';isFolder=True;name=namecolor(clean_string(name))
			else:query='play';isFolder=False;name=clean_string(name)
			name=name+color['subscene']+' (%s%s)[/COLOR]'%(eps.strip(),'-'+rib if rib else '')
			img=re.sub("http.*=http","http",img).replace("'","")
			addir(name,home+href,img,fanart,mode,page,query=query,isFolder=isFolder)
	elif query=='readpage':
		items=list();body=make_request(url)
		for content in re.findall('<li class="movie-item">(.+?)</li>',body,re.DOTALL):
			title=xsearch('title="(.+?)"',content,1);href=xsearch('href="(.+?)"',content,1)
			img=xsearch('\((http.+?)\)',content,1);detail=' '.join(re.findall('<span(.+?)</span>',content))
			items.append((title,href,img,detail))
		addir_pm(items)#title,href,img,detail
		urlnext=xshare_group(re.search('<li><a href="(.+?)">Trang kế.+?</a></li>',body),1)
		if urlnext:
			pagenext=xshare_group(re.search('/page-(\d{1,3})\.html',urlnext),1)
			name='%sTrang tiếp theo: trang %s[/COLOR]'%(color['trangtiep'],pagenext)
			addir(name,home+urlnext,img,fanart,mode,page,'readpage',True)
	elif query=='page':
		body=make_request(url);body=body[body.find('"list-movie"'):body.find('- Sidebar -')]
		ids=re.findall('<a id="(.+?)"',makerequest(phimmoixml))
		pattern='title="(.+?)" href="(.+?)".*?\((.+?)\).*?chap">(.*?)<()'
		if '/tim-kiem/' not in url:pattern=re.sub('\(\)','.*?ribbon">(.*?)<',pattern)
		for name,href,img,chap,rib in re.findall(pattern,body,re.DOTALL):
			epi=xsearch('Tập (\d{1,3})/?',chap+rib,1)
			if (epi and int(epi)>1) or '/tập' in chap:query='folder';isFolder=True;name=namecolor(clean_string(name))
			elif getid(href) in ids:query='part';isFolder=True;name=namecolor(clean_string(name))
			else:query='play';isFolder=False;name=clean_string(name)
			if 'Thuyết minh' in chap+'-'+rib:name='[COLOR gold]TM [/COLOR]'+name
			name=name+color['subscene']+' (%s%s)[/COLOR]'%(chap.strip(),'-'+rib.replace('|','') if rib else '')
			addir(name,home+href,img,fanart,mode,page,query=query,isFolder=isFolder)
		trangtiep=xshare_group(re.search('<li><a href="(.+?)">Trang kế.+?</a></li>',body),1)
		if trangtiep:
			trang=xshare_group(re.search('/page-(\d{1,3})\.html',trangtiep),1)
			name='%sTrang tiếp theo: trang %s[/COLOR]'%(color['trangtiep'],trang)
			addir(name,home+trangtiep,img,fanart,mode,page,'page',isFolder=True)
	elif query=='folder':
		body=make_request(url+'xem-phim.html');name=re.sub('\[/?COLOR.*?\]|\(.+?\)|\d{1,3} phút','',name).strip()
		for detail in re.findall('data-serverid="pcs"(.+?)</li></ul></div>',body,re.DOTALL):
			title=' '.join(s for s in xsearch('<h3 class="server-name">(.+?)</h3>',detail,1,re.DOTALL).split())
			if title and 'tập phim' not in title:addir('[COLOR lime]%s[/COLOR]'%title,'',img,'',mode,1,'no')
			label=name.replace('TM ','') if title and 'Thuyết minh' not in title else name
			for title,href in re.findall('title="(.+?)".+?href="(.+?)"',detail,re.DOTALL):
				addir(title+' '+label,home+href,img,fanart,mode,page,query='play')
	elif query=='folder1':
		body=make_request(url+'xem-phim.html');body=body[body.find('data-servername'):body.find('/List tập phim')]
		colo=['[COLOR blue]','[COLOR green]'];numb=0
		while body:
			temp=body.find('data-serverid');numb+=1
			if temp>0:content=body[:temp];body=body[temp+10:]
			else:content=body;body=''
			temp=re.search('data-servername=".+?" data-language="(.+?)"',content)
			if temp:
				temp='S%d-%s[/COLOR] '%(numb,'sub' if temp.group(1)=='subtitle' else 'TM')
				temp+=re.sub('\[.?COLOR.{,12}\]|\(Lượt xem.*?\)|TM','',name)
			else:temp='[/COLOR]'+re.sub('\[.?COLOR.{,12}\]|\(Lượt xem.*?\)|TM','',name)
			for href,title in re.findall('href="(.+?)">(\d{1,3}).{,10}</a>',content,re.DOTALL):
				title=colo[numb%2]+'Tập '+title.strip()+' '+temp
				addir(title,home+href,img,fanart,mode,page,query='play')
	elif query=='part':
		name=xshare_group(re.search('\[COLOR ghostwhite\](.+?)\[/COLOR\]',name),1)
		for part in xshare_group(re.search('<a id="%s" part="(.+?)"'%getid(url),makerequest(phimmoixml)),1).split('-'):
			addir('Part %s - '%part+name,url,img,fanart,mode,page,query='play')
	elif query=='play':
		href='http://www.phimmoi.net/player/v1.46/plugins/gkplugins_picasa2gdocs/plugins/plugins_player.php?url=%s'
		link_youtube=url;pyoutube="trailerUrl='(https://www.youtube.com/.+?)'"
		if '.html' not in url:url=url+'xem-phim.html'
		content=make_request(url,resp='o');hd['Cookie']=content.cookiestring
		content=sub_body(content.body,'- slider -','- Sidebar -')
		if not content:return play_youtube(xsearch(pyoutube,make_request(link_youtube),1))
		pattern='data-language="(.+?)".*href="(.+?)">.*\s.*Xem Full'
		links=dict(re.findall(pattern,content));body={};pattern="currentEpisode.url='(.+?)'"
		if not links:#Khong co ban full
			eps=[s.replace('\\','') for s in re.findall('({"episodeId":.+?})',content)]
			if not eps:body={};a=1
			elif len(eps)==1:body=make_post(href%geteps(eps[0])[0],headers=hd,resp='j');a=2
			elif xshare_group(re.search('Part (\d{1,3}) - ',name),1):
				part_id=int(xshare_group(re.search('Part (\d{1,3}) - ',name),1));epiurl='';a=3
				for epi in eps:
					if geteps(epi)[1]==part_id:epiurl=geteps(epi)[0];break
				body=make_post(href%epiurl,headers=hd,resp='j') if epiurl else ''
			elif 'xem-phim.html' not in url:
				print href%xshare_group(re.search(pattern,content),1)
				body=make_post(href%xshare_group(re.search(pattern,content),1),headers=hd,resp='j');a=4
			else:make_eps(url,eps);body=make_post(href%geteps(eps[0])[0],headers=hd,resp='j');a=5
		elif len(links)==1:#Chi co 1 ban full
			body=make_post(href%xshare_group(re.search(pattern,make_request(home+links.values()[0])),1),headers=hd,resp='j');a=6
		elif myaddon.getSetting('phimmoiaudio')=='true' and links.has_key('illustrate'):#sub Vie
			body=make_post(href%xshare_group(re.search(pattern,make_request(home+links['illustrate'])),1),headers=hd,resp='j');a=7
		elif links.has_key('subtitle'):#sub Eng
			body=make_post(href%xshare_group(re.search(pattern,make_request(home+links['subtitle'])),1),headers=hd,resp='j');a=8
		height=0;url='';maxresolution=int(myaddon.getSetting('phimmoiresolution'))
		#try:body=body.json["content"]
		#except:body=[]
		print 'aaaaaaaaaaaaaaaaaa',a
		for item in [s for s in body.get("content",list()) if 'video' in s.get('type')]:
			if item.has_key('height') and item['height']==maxresolution:url=item['url'];break
			elif item.has_key('height') and item['height']>height:height=item['height'];url=item['url']
		if not url:mess(u'[COLOR red]Không get được maxspeedlink hoặc link bị die[/COLOR]')
		xbmcsetResolvedUrl(url)

def htvonline(name,url,img,fanart,mode,page,query):
	tvurl='http://www.htvonline.com.vn/livetv';showurl='http://www.htvonline.com.vn/shows'
	phimurl='http://www.htvonline.com.vn/phim-viet-nam';hd['X-Requested-With']='XMLHttpRequest'
	tempfolder=xbmc.translatePath('special://temp');print tempfolder
	def namecolor(name):return '[COLOR yellowgreen]%s[/COLOR]'%name
	if query=='home':
		tv=makerequest(joinpath(tempfolder,'htvtv.html'));show=makerequest(joinpath(tempfolder,'htvshow.html'))
		phim=makerequest(joinpath(tempfolder,'htvphim.html'))
		for title in re.findall('<div class="view_title2"><div>(.+?)</div>',tv):
			addir(namecolor(title.replace(',','-')),tvurl,img,'',mode,page,'submenu',True)
		fanart=xsearch('<img width="487" height="274" src="(.+?)"',show,1)
		addir(namecolor('TV Shows'),showurl+'?page=1',fanart,fanart,mode,page,'submenu',True)
		fanart=xsearch('<img width="487" height="274" src="(.+?)"',phim,1)
		addir(namecolor('Phim'),phimurl+'?page=1',fanart,fanart,mode,page,'submenu',True)
		for title,detail in re.findall('<div class="view_title"><div>(.+?)</div>(.+?)</ul>',show,re.DOTALL):
			addir('[COLOR lime]%s[/COLOR]'%title,'',img,'',mode,1,'no')
			for href,label,img in re.findall('data-tooltip=".+?".+?<a href="(.+?)".+?<h2>(.+?)</h2>.+? src="(.+?)"',detail,re.DOTALL):
				addir(label,href,img,'',mode,page,'htvplay')
		if checkupdate('htvtv.html',tempfolder)>8:
			endxbmc();makerequest(joinpath(tempfolder,'htvtv.html'),make_request(tvurl),'w')
			makerequest(joinpath(tempfolder,'htvshow.html'),make_request(showurl),'w')
			makerequest(joinpath(tempfolder,'htvphim.html'),make_request(phimurl),'w')
	elif query=='submenu':
		if 'lịch phát sóng' in name:
			body=makerequest(joinpath(tempfolder,'htvtv.html'))
			href='http://www.htvonline.com.vn/livetv/show-schedule';chanels=('HTV','VTV','VTC')
			items=re.findall('value="(.+?)" data-imagesrc="(.+?)">(.+?)</option>',body)
			for chanel,img,title in sorted([s for s in items if [i for i in chanels if i in s[2]]],key=lambda l:l[2]):
				addir(namecolor(title.replace(',','-')),href,img,'',mode,int(chanel),'schedule',True)
		elif showurl in url or phimurl in url:
			if showurl in url:page1='htvshow.html';page2='htvshowpage.html'
			else:page1='htvphim.html';page2='htvphimpage.html'
			if 'page=1' in url:body=makerequest(joinpath(tempfolder,page1))
			else:body=makerequest(joinpath(tempfolder,page2))
			if phimurl in url and 'page=1' in url:
				for title,detail in re.findall('<div class="view_title"><div>(.+?)</div>(.+?)</ul>',body,re.DOTALL):
					addir('[COLOR lime]%s[/COLOR]'%title,'',img,'',mode,1,'no')
					for href,label,img in re.findall('data-tooltip=".+?".+?<a href="(.+?)".+?<h2>(.+?)</h2>.+? src="(.+?)"',detail,re.DOTALL):
						addir(label,href,img,'',mode,page,'htvplay')
			for href,label,img in re.findall('href="(.+?)".*\s.*\s.*alt="(.+?)" src="(.+?)"',body):
				addir(namecolor(label),href,img,'',mode,1,'episode_show',True)
			href_next=xsearch('<a class="btn_channel_next page_hr" href="(.+?)"></a>',body,1)
			if href_next:
				page_next=xsearch('page=(\d{1,3})\Z',href_next,1)
				page_end=xsearch('\?page=(\d{1,3})"><span aria-hidden="true">',body,1)
				label='%sTrang tiếp theo: trang %s/%s[/COLOR]'%(color['trangtiep'],page_next,page_end)
				addir(label,href_next,img,'',mode,page,query,True)
				endxbmc();hd['X-Requested-With']='XMLHttpRequest';body=make_post(href_next,headers=hd,resp='b')
				makerequest(joinpath(datapath,page2),body,'w')
		else:
			body=makerequest(joinpath(datapath,'htvtv.html'))
			for title,detail in re.findall('<div class="view_title2"><div>(.+?)</div>.+?<ul class="listtv group small livetvDetail">(.+?)</ul>',body,re.DOTALL):
				if title.replace(',','-') in name:
					for hplus,href,img in re.findall('href="(.+?)" data-original="(.+?)">.+?src="(.+?)"></a>',detail):
						addir(xsearch('/([\w|-]+)-\d',hplus,1).upper(),href,img,'',mode,page,'htvplay')
	elif query=='episode_show':
		pattern='<a data-tooltip=.+?href="(.+?)".*?>([ |\d|\w|-]+?)</'
		label=re.sub('\[.+?\]','',name);items=re.findall(pattern,make_request(url),re.DOTALL)
		for href,adate in items:
			addir('%s %s'%(label,adate),href,img,'',mode,page,'htvplay')
		if not items:addir(label,url,img,'',mode,page,'htvplay')
	elif query=='htvplay':
		body=make_request(url);maxlink=xsearch('"(http:.+?\.m3u8\?.+?)"',body,1)
		if '/xem-show/' in url and not xsearch('\d{1,2}-\d{1,2}-\d{4}',name,0):
			pattern='<a data-tooltip=".+?".+?href="%s".*\s.*>(.+?)</span></a>'%url
			adate=xsearch(pattern,body,1)
			if adate:name='%s %s'%(re.sub('\[.+?\]','',name),adate)
		xbmcsetResolvedUrl(maxlink,'Maxlink%s'%name)
	elif query=='schedule':
		body=make_post(url,hd,{'date':datetime.date.today().strftime("%Y-%m-%d"),'id_live':'%d'%page},'j')
		try:body=body.get('html')
		except:body=''
		items=re.findall('<b>(.+?)</b>.+?title="(.+?)"',body,re.DOTALL);now=datetime.datetime.now().strftime('%H')
		for frame,title in [s for s in items if s[0].strip()>str(int(now)-1)]:
			addir('[COLOR green]%s[/COLOR] %s'%(frame,namecolor(title)),url,img,'',mode,page,'no')

def get_params():#print json.dumps(json["content"],indent=2,sort_keys=True)
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
#addir:name,link,img,fanart,mode,page,query,isFolder
try:#Container.SetViewMode(num)
	myfolder=str2u(myaddon.getSetting('thumuccucbo'))
	if not os.path.exists(myfolder):myfolder=joinpath(datapath,'myfolder')
except:myfolder=joinpath(datapath,'myfolder')
subsfolder=joinpath(myfolder,'subs');tempfolder=joinpath(myfolder,'temp')
thumucrieng=''.join(s for s in myaddon.getSetting('thumucrieng').split()).upper()
if not thumucrieng or len(thumucrieng)<10:thumucrieng='RDA4FHXVE2UU'
thumucrieng='https://www.fshare.vn/folder/'+thumucrieng

xbmcplugin.setContent(int(sys.argv[1]), 'movies');params=get_params();mode=page=0;temp=[]
homnay=datetime.date.today().strftime("%d/%m/%Y");url=name=fanart=img=date=query=end=''

try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote(params["name"])
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
if not mode:#xbmc.executebuiltin("Dialog.Close(all, true)")
	init_file();open_category("MMN");endxbmc()
	if myaddon.getSetting('checkdatabase')=='true' or os.path.isfile(joinpath(data_path,'checkdatabase.txt')):
		data_download()
	data_update()
elif mode==1:vaphim(name,url,img,mode,page,query)
elif mode==2:end=google_search(url,query,mode,page)
elif mode==3:end=resolve_url(url)
elif mode==4:vp_phimmoi()
elif mode==5:vp_xemnhieu()
elif mode==6:end=phimFshare(name,url,mode,page,query)
elif mode==7:end=fptplay(name,url,img,mode,page,query)
elif mode==8:hdvietnam(name,url,img,fanart,mode,page,query)
elif mode==9:make_mySearch(name,url,img,fanart,mode,query)
elif mode==10:open_category(query)
elif mode==11:make_myFshare(name,url,img,fanart,mode,query)
elif mode==12:make_mylist(name,url,img,fanart,mode,query)
elif mode==13:end=xshare_search(name,url,query,mode,page)
elif mode==15:end=id_2url(url,name,mode,page,query)
elif mode==16:end=play_maxspeed_link(url)
elif mode==17:end=megabox(name,url,img,fanart,mode,page,query)
elif mode==18:dangcaphd(name,url,img,mode,page,query)
elif mode==19:pubvn(name,url,img,mode,page,query)
elif mode==20:end=vp_update(auto=False)
elif mode==21:vuahd(name,url,img,mode,page,query)
elif mode==22:hdviet(name,url,img,mode,page,query)
elif mode==23:end=hayhaytv(name,url,img,fanart,mode,page,query)
elif mode==24:phimmoi(name,url,img,mode,page,query)
elif mode==31:end=ifile_update()
elif mode==34:ifile_home(name,url,img,mode,page,query)
elif mode==38:doc_Trang4share(url)#38
elif mode==47:daklak47(name,url,img)
elif mode==50:htvonline(name,url,img,fanart,mode,page,query)
elif mode==90:end=doc_TrangFshare(name,url,img,fanart,query)
elif mode==91:main_menu(url,page,mode,query)
elif mode==92:vp_list(name,url,img,mode,page,query)
elif mode==93:vp_chonloc()
elif mode==94:end=subscene(name,url,query)
elif mode==95:tenlua_getlink(url)
elif mode==96:end=doc_thumuccucbo(name,url,img,fanart,mode,query)
elif mode==97:doc_list_xml(url,name,page)
elif mode==98:make_favourites(name,url,img,fanart,mode,query)
elif mode==99:myaddon.openSettings();end='ok'
if not end or end not in 'no-ok':endxbmc()
