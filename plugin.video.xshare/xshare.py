# -*- coding: utf-8 -*-
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,urllib,re,os,unicodedata,datetime,random,json

myaddon=xbmcaddon.Addon()
home=xbmc.translatePath(myaddon.getAddonInfo('path'));datapath=xbmc.translatePath(myaddon.getAddonInfo('profile'))
iconpath=os.path.join(datapath,'icon');datapath=os.path.join(datapath,'data')
sys.path.append(os.path.join(home,'resources','lib'));from urlfetch import get,post
search_file=os.path.join(datapath,"search.xml");data_path=os.path.join(home,'resources','data')
try:rows=int(myaddon.getSetting('sodonghienthi'))
except:rows=30
tempfolder=xbmc.translatePath('special://temp')
xbmcplugin.setContent(int(sys.argv[1]), 'movies');homnay=datetime.date.today().strftime("%d/%m/%Y")

media_ext=['aif','iff','m3u','m3u8','m4a','mid','mp3','mpa','ra','wav','wma','3g2','3gp','asf','asx','avi','flv','mov','mp4','mpg','mkv','m4v','rm','swf','vob','wmv','bin','cue','dmg','iso','mdf','toast','vcd','ts','flac','m2ts','dtshd','nrg']
color={'fshare':'[COLOR gold]','vaphim':'[COLOR gold]','phimfshare':'[COLOR khaki]','4share':'[COLOR blue]','tenlua':'[COLOR fuchsia]','fptplay':'[COLOR orange]','trangtiep':'[COLOR lime]','search':'[COLOR lime]','ifile':'[COLOR blue]','hdvietnam':'[COLOR red]','xshare':'[COLOR blue]','subscene':'[COLOR green]','megabox':'[COLOR orangered]','dangcaphd':'[COLOR yellow]','hayhaytv':'[COLOR tomato]'};icon={}
for hd in ['xshare','4share','dangcaphd','downsub','favorite','fptplay','fshare','gsearch','hdvietnam','icon','id','ifiletv','ifile','isearch','khophim','maxspeed','megabox','movie','msearch','myfolder','myfshare','phimfshare','serverphimkhac','setting','tenlua','vaphim','hayhaytv']:
	icon.setdefault(hd,os.path.join(iconpath,'%s.png'%hd))
hd={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/600.1.4 Gecko/20100101 Firefox/41.0'}

def mess(message='',title='',timeShown=5000):
	if not message:xbmc.executebuiltin("Dialog.Close(all, true)")
	else:
		title=': [COLOR blue]%s[/COLOR]'%title if title else ''
		s0='[COLOR green][B]Xshare[/B][/COLOR]'+title
		s1='[COLOR red]%s[/COLOR]'%message if '!' in message else u'[COLOR gold]%s[/COLOR]'%message
		xbmc.executebuiltin((u'XBMC.Notification(%s,%s,%s,%s)'%(s0,s1,timeShown,icon['icon'])).encode("utf-8"))

def mess_yesno(title='[COLOR green]Xshare[/COLOR]', line1='', line2='',no='No',yes='Yes'):
	dialog=xbmcgui.Dialog()#dialog.yesno(heading, line1[, line2, line3,nolabel,yeslabel])
	return dialog.yesno(title,line1,line2,nolabel=no,yeslabel=yes)

def no_accent(s):
	s=re.sub(u'Đ','D',s2u(s));s=re.sub(u'đ','d',s)
	return unicodedata.normalize('NFKD', unicode(s)).encode('ASCII', 'ignore')

def s2u(s):return s.decode('utf-8') if isinstance(s,str) else s
def unescape(string):return ' '.join(re.sub('&.+;',xsearch('&(\w).+;',s,1),s) for s in string.split())
def u2s(s):return s.encode('utf-8') if isinstance(s,unicode) else s
def printdict(mydict):print json.dumps(mydict,indent=2);return ''
def add_sep_item(label):addir_info('[COLOR lime]--%s--[/COLOR]'%label,'',icon['xshare'],'',100,1,'no')
def labelsearch(label):return '%s%s[/COLOR]'%(color['search'],label)

def clean_string(string):
	return ' '.join(s for s in re.sub('Fshare|4share|Tenlua','',string).split())

def remove_tag(string):
	if '::' in string:string=string.split('::')[1]
	string=re.sub('\t|\n|\r|\f|\v|vn|Fshare|fshare|4share|4Share|TenLua|tenlua|List xml',' ',string)
	string=re.sub('\[/?COLOR.*?\]|\[\s*\]|\(.*?\)|\{.*?\}|<.*?>|\"|\'|-|\||,|&\w*;|/|br|\.',' ',string)
	return ' '.join(i for i in u2s(unescape(string)).split())

def joinpath(p1,p2):
	try:p=os.path.join(p1,p2)
	except:p=os.path.join(p1,s2u(p2))
	return p

def init_file():
	datafolder=xbmc.translatePath(myaddon.getAddonInfo('profile'))
	for folder in (datafolder,datapath,iconpath,myfolder,tempfolder,subsfolder,xsharefolder):
		if not os.path.exists(folder):os.mkdir(folder)
	xmlheader='<?xml version="1.0" encoding="utf-8">\n';p=datapath;q=myfolder
	for i in [(p,'search.xml'),(p,'hdvietnam.xml'),(p,'favourites.xml'),(p,'phimmoi.xml'),(p,'fpt.xml'),(q,'mylist.xml')]:
		file=joinpath(i[0],i[1])
		if not os.path.isfile(file):makerequest(file,xmlheader,'w')

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

def get_dict(dict,key_list=list(),result=''):
	for key in key_list:
		dict=dict.get(key,result)
		if dict==result:break
	return dict

def sets(lists):
	temp=list()
	for s in lists:
		if s not in temp:temp.append(s)
	return temp

def folders(folder,result=list()):#get files fullpath from folder and subfolders
	for f in os.listdir(folder):
		f=joinpath(folder,f)
		if os.path.isdir(f):folders(f,result)
		else:result.append(f)
	return result

def delete_files(folder,mark=''):
	temp='ok'
	for file in os.listdir(folder):
		if os.path.isfile(joinpath(folder,file)) and (not mark or mark in file):
			try:os.remove(joinpath(folder,file))
			except:temp='';pass
	return temp

def delete_folder(folder):
	for file in os.listdir(folder):
		try:
			files=joinpath(folder,file)
			if os.path.isdir(files):delete_folder(files);os.rmdir(files)
			#for f in os.listdir(files):
			#	os.remove(joinpath(files,f))
			else:os.remove(files)
		except:pass

def rename_file(sf,df,kq='ok'):
	try:
		if os.path.isfile(df):os.remove(df)
		os.rename(sf,df)
	except:kq='';pass
	return kq

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
			mess(u'%s'%s2u(os.path.basename(subfile)),'Auto load sub',20000)

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
		if 'phụ đề việt' in u2s(name).lower():
			name=color['fshare']+'Phụ đề Việt[/COLOR]-%s'%name
			addir(name,href,img,fanart,mode=3,query=query,isFolder=True)
		else:addir(color['fshare']+'Fshare[/COLOR]-%s'%name,href,img,fanart,mode=3,query=query)
	elif 'www.fshare.vn/folder' in href:
		if s2u('chia sẻ') in s2u(name):name=color['trangtiep']+name+'[/COLOR]'
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
	elif myfolder in s2u(link):
		item.addContextMenuItems(make_myFile(name,link,img,fanart,mode,query))
	elif query in 'hdvietfolder-hdvietplay':
		item.addContextMenuItems(hdvietContext(name,link,img,fanart,mode))
	return query

def makeContext(name,link,img,fanart,mode,query):
	if query=='Add to MyFshare favorite':make='AddFavorite'
	elif query=='Remove from MyFshare favorite':make='RemoveFavorite'
	elif query=='Remove All':make='Remove All'
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
	command.append((makeContext(name,link,img,fanart,9,'Remove All')))
	return command

def favouritesContext(name,link,img,fanart,mode):
	def makecmd(mode,title):command.append((makeContext(name,link,img,fanart,mode,title)))
	command=[];link=u2s(link)
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
	name=re.sub('\[/?COLOR.*?\]|Fshare|4share|TenLua|List xml|-|:|"','',name).strip();command=[]
	if os.path.isfile(s2u(link)):
		command.append((makeContext(name,link,img,fanart,11,'Upload to MyFshare')));temp='file'
	else:temp='folder'
	command.append((makeContext(name,link,img,fanart,96,'Rename this %s'%temp)))
	command.append((makeContext(name,link,img,fanart,96,'Remove this %s'%temp)))
	return command

def make_mySearch(name,url,img,fanart,mode,query):
	body=makerequest(search_file)
	if query=='Rename':
		label=' '.join(s for s in name.split())
		string=get_input('Nhập chuổi mới',re.sub('\[.*\]-','',label)).strip()
		if not string or string==label:return
		string=' '.join(s for s in string.split())
		if re.search('http.?://',url):
			content=re.sub('<a href="%s">.+?</a>\n'%url,'<a href="%s">%s</a>\n'%(url,string),body)
		else:content=body.replace(name,string)
		if body!=content:
			makerequest(search_file,content,'w')
			mess(u'Sửa 1 mục thành công');xbmc.executebuiltin("Container.Refresh")
	elif query=='Remove':
		name=re.sub('\(|\)|\[|\]|\{|\}|\?|\,|\+|\*','.',name)
		content=re.sub('<a href="%s">.+?</a>\n|<a>%s</a>\n'%(url,name),'',body)
		if body!=content:
			makerequest(search_file,content,'w')
			mess(u'Xóa 1 mục thành công');xbmc.executebuiltin("Container.Refresh")
	elif query=='Remove All':
		content=re.sub('<a href=".+?">.+?</a>\n','',body)
		if body!=content:
			makerequest(search_file,content,'w')
			mess(u'Xóa tất cả các mục thành công');xbmc.executebuiltin("Container.Refresh")
	elif query=='Add':
		if not re.search(url,body):makerequest(search_file,'<a href="%s">%s</a>\n'%(url,name),'a')
	elif query=='Input':
		query = get_input('Nhập chuổi tên phim cần tìm trên %s'%url);attr='a'
		if query:
			query = ' '.join(s for s in query.replace('"',"'").replace('?','').split() if s!='')
			if query not in body:
				makerequest(search_file,'<a>%s</a>\n'%query,'a');xbmc.executebuiltin("Container.Refresh")
		else:query=''
	elif query=='get':
		srv=url.split('.')[0];site='Google ' if mode==2 else ''
		name='%s%sSearch[/COLOR] trên %s%s[/COLOR] Nhập chuỗi tìm kiếm mới'%(color['search'],site,color[srv],url)
		addir_info(name,url,icon[srv],'',mode,1,'INP',True)
		menu={'MySearch':{'action':'Add','server':['xshare.vn']}}
		if myaddon.getSetting('history')=='true':
			#for s in re.findall('<a>(.+?)</a>',body):addir(s,url,icon[srv],'',mode,4,'Search?'+s,True)
			for s in re.findall('<a>(.+?)</a>',body):addir_info(s,url,icon[srv],'',mode,4,s,True,menu=menu)
	return query

def make_myFshare(name,url,img,fanart,mode,query):#11
	myFshare=myaddon.getSetting('thumucrieng')
	if not myFshare or (myFshare=='RDA4FHXVE2UU' and myaddon.getSetting('usernamef')!='thai@thanhthai.net'):
		mess(u'Hãy set "Thư mục chia sẻ của tôi trên Fshare!"','myFshare');return
	elif query=='Add':
		href='https://www.fshare.vn/api/fileops/createFolder'
		title=xsearch('(\w{10,20})',url,1)
		if title:
			title+=' %s'%re.sub('\[COLOR.{,12}\]|\[/COLOR\]|Fshare|4share|TenLua|List xml|-|:|"','',name)
			title=re.sub('.xml.*','.xml',title).replace('[','').replace(']','')
		else:mess(u'Nhận dạng link bị lỗi!','myFshare');return
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
			if traloi==0:mess(u'OK! xshare chưa làm gì cả!','myFshare'); return
	elif query=='Upload':
		href='https://www.fshare.vn/api/session/upload'
		try:size=os.path.getsize(s2u(url))
		except:pass
		if size>10**7:mess(u'Add-on chưa hỗ trợ upload file>10MB!','myFshare');return
		try:f=open(s2u(url),'rb');content=f.read();f.close()
		except:mess(u'Không đọc được file %s!'%s2u(url),'myFshare');return
	elif query=='AddFavorite':href='https://www.fshare.vn/api/fileops/AddFavorite'
	elif query=='RemoveFavorite':href='https://www.fshare.vn/api/fileops/ChangeFavorite'
	else:return
	
	hd['Cookie']=loginfshare();body=make_request('https://www.fshare.vn/home',hd)
	if not body:logout_site(hd['Cookie'],url);mess(u'Chưa GET được Fshare homepage của bạn!');return
	token=xsearch('data-token="(.+?)"',body,1)
	if query=='Add':
		data='{"token":"%s","name":"%s","in_dir":"%s"}'%(token,title,myFshare)
		noti='Add to MyFshare'
	elif query=='Rename':
		data='{"token":"%s","new_name":"%s","file":"%s"}'%(token,new_name,id);noti='Rename in MyFshare'
	elif query=='Remove':data='{"token":"%s","items":["%s"]}'%(token,id);noti='Remove from MyFshare'
	elif query=='Upload':
		SESSID=hd['Cookie'].split('=')[1]
		name=re.sub('\[COLOR.{,12}\]|\[/COLOR\]|Fshare|4share|TenLua|List xml|-|:|"','',os.path.basename(url))
		path=xsearch('data-id="%s" path-origin = "" data-path="(.+?)"'%myFshare,body,1)
		data='{"SESSID":"%s","name":"%s","size":"%s","path":"%s","token":"%s","secured":1}'%(SESSID,name,size,path,token)
		response=make_post(href,hd,data)
		if response and response.status==200:
			href=response.json['location'];data=content;noti='Upload to MyFshare'
		else:mess(u'Không lấy được link upload!','myFshare');return
	elif query=='AddFavorite':
		data='{"token":"%s","link":"%s"}'%(token,url);noti='Add to My Fshare favorite'
	elif query=='RemoveFavorite':
		data='{"token":"%s","items":["%s"],"status":0}'%(token,os.path.basename(url))
		noti='Remove from My Fshare favorite'
	
	response=make_post(href,hd,data);logout_site(hd['Cookie'],url)
	if response and response.status==200:
		mess(u'%s thành công'%noti,'myFshare')
		if not any(s for s in ['Add','Upload'] if s in query):xbmc.executebuiltin("Container.Refresh")
	else:mess(u'%s không thành công!'%noti,'myFshare')
	return

def make_favourites(name,url,img,fanart,mode,query):
	favourites=joinpath(datapath,"favourites.xml");name=remove_tag(name)
	if query=='Add':
		if url.strip() in makerequest(favourites):mess(u'Mục này đã có trong MyFavourites!','MyFavourites');return
		if img==fanart:fanart=''
		string='<a href="%s" img="%s" fanart="%s">%s</a>\n'%(url.strip(),img,fanart,name)
		if makerequest(favourites,string,'a'):mess(u'Đã thêm 1 mục vào MyFavourites','MyFavourites')
		else:mess(u'Thêm 1 mục vào MyFavourites thất bại!','MyFavourites')
	elif query=='Rename':
		title = get_input('Sửa tên trong mục MyFavourites',name).strip()
		if not title or title==name:return 'no'
		body=makerequest(favourites)
		string=re.search('((<a href="%s" img=".*?" fanart=".*?">).+?</a>)'%(url),body)
		if string:
			body=body.replace(string.group(1),string.group(2)+title+'</a>')
			if makerequest(favourites,body,'w'):
				mess(u'Đã sửa 1 mục trong MyFavourites','MyFavourites')
				xbmc.executebuiltin("Container.Refresh")
			else:mess(u'Sửa 1 mục trong MyFavourites thất bại!','MyFavourites')
		else:mess(u'Sửa 1 mục trong MyFavourites thất bại!','MyFavourites')
	elif query=='Remove':
		body=makerequest(favourites);string=xsearch('(<a href="%s" img=".*?" fanart=".*?">.+?</a>)'%(url),body,1)
		if string:
			body=body.replace(string+'\n','')
			if makerequest(favourites,body,'w'):
				mess(u'Đã xóa 1 mục trong xshare favourites','MyFavourites')
				xbmc.executebuiltin("Container.Refresh")
			else:mess(u'Xóa 1 mục trong xshare favourites thất bại!','MyFavourites')
		else:mess(u'Xóa 1 mục trong xshare favourites thất bại!','MyFavourites')
	else:
		items=re.findall('<a href="(.+?)" img="(.*?)" fanart="(.*?)">(.+?)</a>',makerequest(favourites))
		for href,img,fanart,name in items:addirs(name,href,img,fanart)
	return

def make_mylist(name,url,img,fanart,mode,query):
	mylist=joinpath(myfolder,'mylist.xml')
	name=re.sub('\[COLOR.{,12}\]|\[/COLOR\]|Fshare|4share|TenLua|List xml|-|:|"','',name).strip()
	if query=='Add':
		if url.strip() in makerequest(mylist):mess(u'Mục này đã có trong MyList!','MyList');return
		if img==fanart:fanart=''
		string='<a href="%s" img="%s" fanart="%s">%s</a>\n'%(url.strip(),img,fanart,name)
		if makerequest(mylist,string,'a'):mess(u'Đã thêm 1 mục vào mylist.xml','MyList')
		else:mess(u'Thêm vào mylist.xml thất bại!','MyList')
	elif query=='Rename':
		title = get_input('Sửa tên 1 mục trong mylist.xml',name)
		if not title or title==name:return 'no'
		string1='<a href="%s" img=".*?" fanart=".*?">.+?</a>'%url
		string2='<a href="%s" img=".*?" fanart=".*?">%s</a>'%(url,title)
		body=re.sub(string1,string2,makerequest(mylist))
		if makerequest(mylist,body,'w'):
			mess(u'Đã sửa 1 mục trong mylist.xml','MyList');xbmc.executebuiltin("Container.Refresh")
		else:mess(u'Sửa 1 mục trong mylist.xml thất bại!','MyList')
	elif query=='Remove':
		string='<a href="%s" img=".*?" fanart=".*?">.+?</a>\n'%url
		body=re.sub(string,'',makerequest(mylist))
		if makerequest(mylist,body,'w'):
			mess(u'Đã xóa 1 mục trong mylist.xml','MyList');xbmc.executebuiltin("Container.Refresh")
		else:mess(u'Xóa 1 mục trong mylist.xml thất bại!','MyList')
	return

def make_request(url,headers=hd,resp='b',maxr=0):
	try:
		if maxr==0:response=get(url,headers=headers,timeout=10)
		else:response=get(url,headers=headers,max_redirects=maxr,timeout=10)
		if resp=='o':resp=response
		else:
			if resp=='j':resp=response.json
			elif resp=='s':resp=response.status
			elif resp=='u':resp=response.text
			elif resp=='c':resp=response.cookiestring
			else:resp=response.body
			response.close()
	except:
		if resp=='j':resp=dict()
		elif resp=='s':resp=500
		else:resp=''
		if 'vaphim.com' not in url:
			mess(u'Lỗi kết nối tới: %s!'%xsearch('//(.{5,20}\.\w{2,3})',s2u(url),1),'make_request')
		print 'Lỗi kết nối tới: %s!'%u2s(url);
	return resp#unicode:body=response.text

def make_post(url,headers=hd,data='',resp='o'):
	try:
		if data:response=post(url=url,headers=headers,data=data,timeout=100)
		else:response=post(url=url,headers=headers,timeout=100)
		if resp=='b':response=response.body
		elif resp=='j':response=response.json
	except:
		mess(u'Post link error: %s!'%s2u(url),'make_post');print 'Post link error: %s'%u2s(url)
		response={} if resp=='j' else ''
	return response

def makerequest(file,body='',attr='r'):
	file=s2u(file)
	if attr=='r':
		try:f=open(file);body=f.read();f.close()
		except:body=''
	else:
		try:f=open(file,attr);f.write(body);f.close()
		except:mess(u'Lỗi ghi file: %s!'%s2u(os.path.basename(file)),'makerequest');body=''
	return body

def get_input(title=u"", default=u""):
	result = ''
	keyboard = xbmc.Keyboard(default, title)
	keyboard.doModal()
	if keyboard.isConfirmed():
		result = keyboard.getText()
	return result

def tenlua_get_detail_and_starting(id,headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}):
	data='[{"a":"filemanager_builddownload_getinfo","n":"%s","r":0}]'%id
	response=make_post('https://api2.tenlua.vn/',headers,data,resp='j')
	try:json=response[0]
	except:json={'type':'none'}
	return json

def fshare_resolve(url,xml):
	def get_pass_file():return get_input(u'Hãy nhập: Mật khẩu tập tin')
	hd['Cookie']=loginfshare();loops=range(6);direct_link=pass_file=error404=''
	if not hd['Cookie']:return 'fail'#login fail
	for loop in loops:
		if loop>0:mess(u'Get link lần thứ %d'%(loop+1),'fshare.vn');xbmc.sleep(3000)
		response=make_request(url,hd,resp='o')
		if not response:continue
		elif response.status==302:direct_link=response.headers['location'];break
		elif response.status==200:
			if 'Lỗi 404' in xsearch('<title>(.+?)</title>',response.body,1):
				error404='Y';mess(u'Tập tin quý khách yêu cầu không tồn tại!','fshare.vn');xbmc.sleep(3000);break
			elif re.search('<i class="fa fa-star">',response.body):
				xbmc.sleep(1000);mess('Your Fshare acc is FREE')
			if not pass_file and xsearch('(class="fa fa-lock")',response.body,1):pass_file=get_pass_file()
			fs_csrf=xsearch('value="(.+?)" name="fs_csrf',response.body,1)
			data={'fs_csrf':fs_csrf,'DownloadForm[pwd]':pass_file,
				'ajax':'download-form','DownloadForm[linkcode]':os.path.basename(url)}
			if fs_csrf:
				hd['referer']=url
				response=make_post('https://www.fshare.vn/download/get',hd,data,resp='j');hd.pop('referer')
				if response.get('url'):direct_link=response.get('url');break
				elif response.get('DownloadForm_pwd'):
					try:mess(response.get('DownloadForm_pwd')[0])
					except:mess(u'Mật khẩu chưa chính xác')
					xbmc.sleep(5000);break
		else:print 'response.status: %d'%response.status
	logout_site(hd['Cookie'],url)
	if not direct_link and not error404:mess('Sorry! Potay.com','fshare.vn');return 'fail'
	elif not direct_link:return 'fail'
	elif xml:return direct_link
	else:return xshare_resolve(direct_link,os.path.splitext(direct_link)[1][1:].lower())

def resolve_url(url,xml=False):
	urltemp=url.lower()
	if 'fshare.vn' in urltemp:result=fshare_resolve('https://www.%s'%xsearch('(fshare.vn.+?)\Z',url,1),xml)
	elif '4share.vn' in urltemp:result=fourshare_resolve(url)
	elif 'tenlua.vn' in urltemp:result=tenlua_resolve(url,xml)
	return result

def fourshare_resolve(url):
	hd['Cookie']=login4share()
	if not hd['Cookie']:return 'fail'#login fail
	response=make_request(url,hd,resp='o');logout_site(hd['Cookie'],url)
	if not response or response.status!=200:xbmc.sleep(2000);return 'fail'
	direct_link=xsearch("<a style='text-decoration:none' href='(.+?)'>",response.body,1)
	if not direct_link:
		direct_link=xsearch("Link Download.+?href='(.+?4share.vn.+?)'>",response.body)
		if not direct_link:
			mess(u'Không get được maxspeed link!','resolve_url');return 'fail'
	ext=os.path.splitext(xsearch('<title>(.+?)</title>',response.body,1))[1][1:].lower()
	return xshare_resolve(direct_link,ext)

def tenlua_resolve(url,xml):
	hd['Cookie']=logintenlua();id=xsearch('\w{14,20}',url,0);direct_link=''
	if not id:id=url.split('/download/')[1].split('/')[0]
	download_info=tenlua_get_detail_and_starting(id,hd);print download_info
	filename=u2s(download_info.get('n',''))
	ext=os.path.splitext(filename)[1][1:].lower()
	size=int(download_info.get('real_size','0'))
	dlink=download_info.get('dlink','')
	if not dlink:
		dlink=download_info.get('url','');mess(u'Slowly direct link!','resolve_url')
		if not dlink:mess(u'Không get được max speed link!','resolve_url');return 'fail'
	response=make_request(dlink,hd,resp='o',maxr=2);logout_site(hd['Cookie'],url)
	if response.history[1].status==302:return xshare_resolve(response.history[1].headers['location'],ext)
	else:mess(u'Không get được max speed link!','resolve_url');return 'fail'

def xshare_resolve(direct_link,ext='',filmlabel=''):
	def get_detail_maxlink(direct_link):
		response=make_request(direct_link,{'User-Agent':'xshare'},resp='o')
		if not response:return 'fail'
		detail=response.headers
		size=int(detail.get('content-length',0))
		filename=detail.get('content-disposition','').split('=')
		if len(filename)>1:filename=filename[1].replace('"','').replace("'","")
		else:filename=os.path.basename(direct_link)
		ext=os.path.splitext(filename)[1][1:].lower()
		return response,size,filename,ext
	
	if ext in media_ext:xbmcsetResolvedUrl(direct_link,filmlabel);return ''
	#elif ext in ['srt','sub','txt','smi','ssa','ass','nfo']:xbmcsetResolvedUrl(direct_link,filmlabel);return ''
	
	response,size,filename,ext=get_detail_maxlink(direct_link)
	if not ext:mess('sorry! this is not a media file','Check media extention');result='fail'
	elif ext in 'xml':result=doc_list_xml(direct_link,'list_xml')
	elif ext in media_ext:xbmcsetResolvedUrl(direct_link,filmlabel);result=''
	elif ext in ['rar','zip','srt','sub','txt','smi','ssa','ass','nfo']:
		result=xshare_download(response,size,filename,ext)
	else:mess('sorry! this is not a media file','xshare resolve');result='fail'
	return result

def xshare_download(response,size,filename,ext):
	def checkmedia(file):
		return os.path.isfile(file) and os.path.getsize(file)>1024**2 and os.path.splitext(file)[1][1:] in media_ext
	
	temp_path=joinpath(tempfolder,'temp');mediafile=False
	if not os.path.exists(temp_path):os.mkdir(temp_path)
	else:delete_folder(temp_path)
	tempfile=joinpath(temp_path,'tempfile.%s'%ext)
	
	if size<1024**2:#sub file
		if myaddon.getSetting('autodel_sub')=='true':delete_folder(subsfolder)
		content=makerequest(tempfile,response.body,"wb")
	elif size<2*1024**3:
		if size>1024**3:size_str='%d.%d GB'%(size/(1024**3),(size%(1024**3))/10**7)
		else:size_str='%d.%d MB'%(size/(1024**2),(size%(1024**2))/10**4)
		line1='[COLOR green]File: %s - %s[/COLOR]'%(filename,size_str)
		line2='Sẽ mất nhiều thời gian tải file vào "[B]Thư Mục Cục Bộ[/B]"!';content=''
		if size<100*1024**2 or  mess_yesno('xshare cảnh báo',line1,line2,'No - Không tải','Yes - Đồng Ý tải'):
			losslessfolder=joinpath(myfolder,'Lossless')
			if not os.path.exists(losslessfolder):os.mkdir(losslessfolder)
			if size>100*1024**2:endxbmc()
			f=open(tempfile,'wb');i=0;mess(u'Started Background download...',timeShown=50000);i=j=t=0;fn=''
			for chunk in response:
				f.write(chunk);i+=len(chunk)
				if i*10/size>j:j+=1;mess(u'Đã download được %d%%'%(j*10),timeShown=20000)
			f.close();mess(u'Đang Unzip...',timeShown=10000)
			xbmc.sleep(1000);xbmc.executebuiltin('XBMC.Extract("%s","%s")'%(tempfile,u2s(losslessfolder)),True)
			for filefullpath in folders(losslessfolder):
				if not checkmedia(filefullpath) and 'nrg' not in filefullpath:os.remove(filefullpath)
				elif os.path.getmtime(filefullpath)>t:fn=filefullpath;t=os.path.getmtime(fn)
			if fn and size<100*1024**2:#File nhỏ, gọi play
				xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=fn))
			mess(u'Đã download xong. Hãy mở Thư Mục Cục Bộ và thưởng thức tiếp nhé',timeShown=20000)
	else:mess(u'Sorry! Dung lượng file quá lớn. Chưa xử lý');content=''
	if not content:return 'no'
	sub_ext = [".srt", ".sub", ".txt", ".smi", ".ssa", ".ass"];sub_list=[];p=',|"|\''
	if content[0] in 'R-P':
		xbmc.sleep(1000);xbmc.executebuiltin('XBMC.Extract("%s")'%tempfile,True)
		for filefullpath in folders(temp_path):
			file=os.path.basename(filefullpath)
			if os.path.isfile(filefullpath) and os.path.splitext(filefullpath)[1] in sub_ext:
				if re.search('english|eng\.|\.eng',filename.lower()) and myaddon.getSetting('autotrans_sub')=='true':
					mess(u'Google đang dịch sub từ tiếng Anh sang tiếng Việt','Subs Downloader',timeShown=20000)
					filetemp=xshare_trans(filefullpath)
					if rename_file(filetemp,joinpath(subsfolder,'Vie.%s'%re.sub(p,'',file))):
						mess(u'Đã dịch xong sub từ tiếng Anh sang tiếng Việt','Subs Downloader')
					elif rename_file(filefullpath,joinpath(subsfolder,'Eng.%s'%re.sub(p,'',file))):
						mess(u'Không dịch được sub. Giữ nguyên bản tiếng Anh!','Subs Downloader') 
				elif re.search('english|eng\.|\.eng',filename.lower()) and rename_file(filefullpath,joinpath(subsfolder,'Eng.%s'%re.sub(p,'',file))):
					mess(u'Đã download sub vào Subsfolder','Subs Downloader') 
				elif re.search('vietnam|vie\.|\.vie',filename.lower()) and rename_file(filefullpath,joinpath(subsfolder,'Vie.%s'%re.sub(p,'',file))):
					mess(u'Đã download sub vào Subsfolder','Subs Downloader') 
				elif rename_file(filefullpath,joinpath(subsfolder,re.sub(',|"|\'','',file))):
					mess(u'Đã download sub vào Subsfolder','Subs Downloader') 
	elif rename_file(tempfile,joinpath(subsfolder,'Vie.%s'%filename)):
		mess(u'Đã download sub vào Subsfolder','Subs Downloader')
	return 'no'

def logout_site(cookie,url):
	def logout(cookie,url,site):
		hd['Cookie']=cookie
		mess(u'Logout %s %sthành công'%(site,'' if make_request(url,hd,resp='s')==302 else u'không '))
	if cookie and myaddon.getSetting('logoutf')=="true":
		if 'fshare.vn' in url.lower():logout(cookie,'https://www.fshare.vn/logout','Fshare.vn')
		elif '4share.vn' in url.lower():logout(cookie,'http://4share.vn/default/index/logout','4share.vn')
		elif 'dangcaphd.com' in url.lower():logout(cookie,'http://dangcaphd.com/logout.html','dangcaphd.com')
		elif 'tenlua.vn' in url.lower():logouttenlua(cookie)

def loginfshare(headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}):
	response=make_request("https://www.fshare.vn/login",resp='o');result=''
	if not response:mess(u'Lỗi kết nối Fshare.vn!','fshare.vn');return result
	fs_csrf=xsearch('value="(.+?)".*name="fs_csrf',response.body,1);headers['Cookie']=response.cookiestring
	username=myaddon.getSetting('usernamef');password=myaddon.getSetting('passwordf')
	form_fields = {"LoginForm[email]":username,"LoginForm[password]":password,"fs_csrf":fs_csrf}
	response=make_post("https://www.fshare.vn/login",headers,form_fields)
	if response.status==302:mess(u'Login thành công','Fshare.vn');result=response.cookiestring
	else:mess(u'Login không thành công!','Fshare.vn')
	return result

def login4share(headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}):
	form_fields = {"username":myaddon.getSetting('username4'),"password":myaddon.getSetting('password4')}
	response=make_post('http://up.4share.vn/index/login',headers,form_fields)
	if response and response.status==302:mess(u'Login thành công','4share.vn');f=response.cookiestring
	else:mess(u'Login không thành công!','4share.vn');f=''
	return f

def logintenlua(headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}):
	user=myaddon.getSetting('usernamet');pw=myaddon.getSetting('passwordt')
	data='[{"a":"user_login","user":"'+user+'","password":"'+pw+'","permanent":"true"}]'
	response=make_post('https://api2.tenlua.vn/',headers,data)
	if response and response.body!='[-1]':mess(u'Login thành công','tenlua.vn');f=response.headers.get('set-cookie')
	else:mess(u'Login không thành công!','tenlua.vn');f=''
	return f

def logouttenlua(cookie):
	hd['Cookie']=cookie
	response=make_post('https://api2.tenlua.vn/',hd,'a=user_logout')
	if response:mess(u'Logout thành công','tenlua.vn')
	else:mess(u'Logout không thành công!','tenlua.vn')

def loginhdvietnam():
	url='http://www.hdvietnam.com/diendan/login.php';import hashlib
	user=myaddon.getSetting('usernameh');pw=hashlib.md5(myaddon.getSetting('passwordh')).hexdigest()
	data ={"vb_login_username":user,"vb_login_md5password":pw,"do":"login"}
	response=make_post(url,hd,data,resp='o')
	if response.status==200 and user in response.body:
		mess(u'Login thành công','hdvietnam.com')
		f=response.cookiestring;makerequest(joinpath(datapath,'hdvietnam.cookie'),f,'w')
	else:mess(u'Login không thành công!','hdvietnam.com');f=''
	return f

def hdvn_get_link(url,fanart='',temp=[]):
	room=xsearch('http://www.hdvietnam.com/diendan/(.+?)/',url,1)
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
	title=xsearch('<title>(.+?)</title>',body,1)
	if not title:return temp
	else:title=re.sub('\||\[.*\]|\(.*\)|\{.*\}|amp;','',title).strip()
	title='[%s] %s'%(bossroom,title);mess(url.split('/')[len(url.split('/'))-1])
	img=xsearch('<a rel="nofollow" href="(.+?)" class="highslide"',body,1)
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
	mess()
	return temp

def hdvn_boss_room(url,body):
	if re.search('-\d{1,3}\.html',url):
		body=make_request(re.sub('-\d{1,3}\.html','.html',url))
	pattern='id="postcount\d{5,8}" name="1">.{,1000}line popupctrl.{40,55}/\d{4,10}-(.+?).html"'
	return xsearch(pattern,body,1,re.DOTALL)

def hdvn_body_thanked(body,hd,bossroom):
	sec_token= xsearch('name="securitytoken" value="(.{50,60})"',body,1)
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

def google_ifile(url,name,temp=[]):
	if 'http://ifile.tv/phim/' not in url:return temp
	mess(url)
	for url4share,fanart,name2,catalog in ifile_tv_4share(url):
		if not name2:name2=name
		if url4share not in temp:temp.append(url4share);addirs(name2,url4share,fanart,fanart)
	mess()
	return temp

def google_vaphim(url,temp=[]):
	if url=='http://vaphim.com/':return temp
	elif '/tag/' in url:
		pattern='class="entry-title"><a href="(.+?)" rel="bookmark"'
		url=xsearch(pattern,make_request(url),1)
		if not url:return temp
	mess(url)
	for id,title,href,img,fanart,category in vp_2fshare(url):
		if href not in temp:temp.append(href);addirs(title,href,img,fanart)
	mess()
	return temp

def search_get_page(name,url,img,fanart,mode,page,query):
	if 'vaphim.com/' in url:
		if url=='http://vaphim.com/':return
		elif '/tag/' in url:
			pattern='class="entry-title"><a href="(.+?)" rel="bookmark"'
			url=xsearch(pattern,make_request(url),1)
			if not url:return
		for id,title,href,img,fanart,category in vp_2fshare(url):
			addir_info(title,href,img,fanart)
	if '4share.vn/' in url.lower():
		for href,img,title,category in ifile_tv_4share(url):
			addir_info(title,href,img,fanart)
	if 'ifile.tv/' in url.lower():
		if 'http://ifile.tv/phim/' not in url:return 
		for url4share,fanart,name2,catalog in ifile_tv_4share(url):
			if not name2:name2=name
			addir_info(name2,url4share,fanart,fanart)

def google_search_api(url,start,string,items):#url:fshare.vn,4share.vn,tenlua.vn,hdvietnam.com
	string_search = urllib.quote_plus('"%s"'%string)
	href = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=large&'
	href+='start=%s&q=site:%s+%s'%(start,url.lower(),string_search)
	json=make_request(href,resp='j')
	if not json:return items,'end'
	if json.get('responseStatus')!=200 and myaddon.getSetting('googlesearch')=='API':
		mess(u'Google: nghi ngờ lạm dụng Dịch vụ. Tự động chuyển sang web search!','google_search_api')
		return google_search_web(url,start+'xshare',string,items)
	data=json.get('responseData',dict())
	if not data.get('results'):return items,'end'
	currentPage=int(data['cursor']['currentPageIndex'])+1;nextPage=0
	for item in data['results']:
		name=remove_tag(item['titleNoFormatting'])
		if len(name.split())<2:name=os.path.basename(item['url'])
		if 'tenlua' in url and not re.search('\w{14,20}/(.*)\Z',item['url']):continue
		elif not name or 'Forum' in name or 'server-nuoc-ngoai' in item['url']:continue
		elif 'chuyenlink.php' in item['url']:continue
		items.append((name,urllib.unquote(item['url'].encode('utf-8'))))
	start=str(int(start)+8)
	if start not in [s['start'] for s in data['cursor']['pages']]:start='end'
	return items,start

def google_search(url,query,mode,page,items=[]):
	srv=url.split('.')[0]
	if page==0:make_mySearch('',url,'','',mode,'get');return
	elif page==1:
		query=make_mySearch('',url,'','','','Input');page=2
		if query is None or not query.strip():return 'no'
	query=no_accent(query)
	if '?' in query:start=query.split('?')[1];query=query.split('?')[0]
	else:start='0'
	if myaddon.getSetting('googlesearch')=='Web' or 'xshare' in start:items,start=google_search_web(url,start,query,items)
	else:items,start=google_search_api(url,start,query,items)
	if len(items)<10 and start!='end' and myaddon.getSetting('googlesearch')=='API':
		return google_search(url,'%s?%s'%(query,start),mode,page,items)
	if not items and start=='end':mess(u'Không tìm thấy dữ liệu yêu cầu!','google_search');return 'no'
	for name,link in set(items):
		if url=='hdvietnam.com':addir_info(name,link,icon[srv],query='get_link_post')
		elif url=='vaphim.com':addir_info(name,link,icon[srv],query='vp_getpage')
		else:addir_info(name,link,icon[srv])
	if start!='end':
		name=color['trangtiep']+'Trang tiep theo...trang %s[/COLOR]'%str(page-2)
		addir_info(name,url,icon[srv],'',mode,page+1,'%s?%s'%(query,start),True)
	return ''

def google_search_web(url,start,query,items):
	num='30';google = 'https://www.google.com.vn/search?hl=vi&ie=utf-8&oe=utf-8&num=%s&'%num
	#num='30';google = 'https://www.google.com.vn/search?hl=vi&num=%s&'%num
	string_search = urllib.quote_plus('"%s"'%query);srv=url.split('.')[0]
	if 'xshare' in start:start=start.replace('xshare','');xshare='yes'
	else:xshare=''
	href=google+'start=%s&q=site:%s+%s'%(start,url.lower(),string_search);print href
	body=make_request(href,hd)#;a=makerequest(r'd:\xoa.html',body,'w')
	if '<TITLE>302 Moved</TITLE>' in body and myaddon.getSetting('googlesearch')=='Web':
		mess(u'Google: nghi ngờ lạm dụng Dịch vụ. Tự động chuyển sang API search!','google_search_web')
		return google_search_api(url,start,query,items)
		#return items,'end'
	#links=re.findall('<a href="(.{,300})" onmousedown=".{,200}">(.{,200})</a></h3>',body);print len(links)
	links=re.findall('<a href=".*?(http.+?)["|&].+?>(.+?)</a></h3>',body)
	for link,name in links:
		if 'tenlua.vn' in link and not re.search('\w{14,20}/(.*)\Z',link):continue
		elif not name or 'Forum' in name or 'server-nuoc-ngoai' in link:continue
		elif 'chuyenlink.php' in link:continue
		items.append((remove_tag(unescape(name)),link))
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
		if not body:mess(u'Đang update menu...','vaphim.com');vp_make_datanew();return
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
	if makerequest(joinpath(datapath,filename),contents,'w'):
		mess(u'Đã cập nhật được %d phim'%len(items_new),'%s Auto update'%filename)
	else: mess(u'Đã xảy ra lỗi cập nhật!','%s Auto update'%filename)
	return

def vp_page(url,body=''):#id,name,href,img,category
	pattern='<li class="post-(\d{4,6})(.+?)">.+?src="(.+?)".+?<h3 class="entry-title">'
	pattern+='<a href="(.+?)" rel="bookmark" >(.+?)</a>';items=[]
	if not body:body=make_request(url)
	for id,category,img,href,name in re.findall(pattern,body,re.DOTALL):
		category=' '.join(s.replace('category-','') for s in category.split() if 'category-' in s)
		if [s for s in ['game','video-clip','phn-mm','ebooks'] if s in category]:continue
		name=' '.join(s for s in re.sub('<.+?>|&.+?; ?','',name).split());items.append((id,name,href,img,category))
	return items

def vp_2fshare(url):#id,title,href,img,fanart,category
	response=make_request(url,hd,resp='o')
	if not response or response.status!=200:xbmc.sleep(15000);response=make_request(url,hd,resp='o')
	if not response or response.status!=200:return list()
	body=response.body
	items=list();id=xsearch("href='http://vaphim.com/\?p=(.+?)'",body,1)
	temp=xsearch('<div id=".+?" class="post-(.+?)">',body,1)
	category=' '.join(s.replace('category-','') for s in temp.split() if 'category-' in s)
	if not id or [s for s in category.split() if s in 'game video-clip phn-mm ebooks']:return items
	temp=xsearch('<title>(.+?)</title>',body,1)
	name=' '.join(s for s in re.sub('<.+?>|&.+?; ?|\||VaPhim.com','',temp).split())
	image=xsearch('meta property="og:image" content="(.+?)"',body,1)
	pattern='<a \w{4,6}=".*?(fshare.vn/f.l.?e?r?/.+?|http://subscene.+?)".{,18}>(.+?)</a><'
	if 'collection' not in category:
		content=xsearch('id="attachment_(.+?)"cf5_wpts_cl"',body,1,re.DOTALL)
		if not name:
			temp=xsearch('class="wp-caption-text">(.+?)<',content,1)
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
			title=xsearch('<strong>(.+?)</strong>(</span></p>|</p>|<br />)',content,1)
			if not title:title=xsearch('"wp-caption-text">(.+?)<',content,1)
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
	timenow=datetime.datetime.now().strftime('%Y%m%d%H')
	my_dict=json_rw('xshare.json');time_vp_update=my_dict.get('vp_update_time','0')
	if int(timenow)-int(time_vp_update)<1 and auto:return 'no'
	else:my_dict['vp_update_time']=timenow;my_dict=my_dict=json_rw('xshare.json',my_dict)
	items=vp_page('http://vaphim.com/category/phim-2/');hrefs=[];items_new=[]
	if not items:return 'no'
	ids=my_dict.get('vp_update_ids',list());mess(u'Vaphim updating ...',homnay)
	my_dict['vp_update_ids']=[s[0] for s in items];my_dict=json_rw('xshare.json',my_dict)
	items_old=doc_xml(joinpath(datapath,"vaphim.xml"));href_old=[s[5] for s in items_old]
	if auto:#update all in phim-2 page
		for href in [s[2] for s in items]:hrefs+=vp_2fshare(href)
	else:
		for href in [s[2] for s in items if s[0] not in ids]:
			mess('Vaphim updating...','vaphim.com');hrefs+=vp_2fshare(href)
	for id,title,href,img,fanart,category in [s for s in hrefs if s[2] not in href_old]:
		items_new.append(('',id,category,img,fanart,href,title))
	if items_new:update_xml(items_new,items_old,"vaphim.xml")
	else:mess(u'Không có phim mới...','Vaphim.com auto update')
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
	if names:makerequest(joinpath(datapath,'vp_xemnhieu.txt'),str(names),'w')
	items=re.findall('<li><a href="/category.+?/([\w-]+?)/">(.+?)</a></li>',body)
	if items:makerequest(joinpath(datapath,"vp_menu.txt"),str(items),'w')
	body=make_request('http://vaphim.com/')
	items=re.findall('"post-(\d{4,6})(.+?)"',body);items_new=[]
	for id,category in items:
		category=' '.join(s.replace('category-','') for s in category.split() if 'category-' in s)
		if not any(s for s in category.split() if s in 'game video-clip phn-mm ebooks'):items_new.append(id)
	if items_new:makerequest(joinpath(datapath,'vp_phimmoi.txt'),str(items_new),'w')
	items=re.findall('rel="bookmark">(.+?)</a>',body)
	if items:makerequest(joinpath(datapath,"vp_chonloc.txt"),str(items),'w')

def daklak47(name,url,img):
	reps = make_request(url)
	if reps.status==302:
		req=reps.headers['location']
		url = req.replace('http:','https:')
		if 'www.fshare.vn/folder/' in url:mess(u"Chưa xử lý trường hợp đọc folder trên 47daklak.com");return
		else:resolve_url(url)
	else: mess(u'Không tìm thấy link trên %s!'%s2u(url),'47daklak.com')

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
	url=xsearch('<a href="(.+?)" title="Next"',body,1)
	if url and query!="demo":
		page=xsearch('/(\d{1,3})',url,1);trangcuoi=xsearch('<a href=".+?/(\d{1,3})" title="End"',body,1)
		name=color['trangtiep']+'Trang tiếp theo: trang %s/%s[/COLOR]'%(page,trangcuoi)
		addir(name,'http://ifile.tv%s'%url,img,fanart,mode,int(page),query,True)
		
def doc_list_xml(url,filename='',page=1):
	if page<2:
		items=doc_xml(url,filename=filename);page=1
		makerequest(joinpath(tempfolder,'temp.txt'),str(items),'w')
	else:f=open(joinpath(tempfolder,'temp.txt'));items=eval(f.readlines()[0]);f.close()
	pages=len(items)/rows+1
	del items[0:(page-1)*rows];count=0
	for id,href,img,fanart,name in items:
		if '47daklak.com' in href: addir(name,href,img,mode=47)
		else: addirs(name,href,img,fanart)
		count+=1
		if count>rows and len(items)>(rows+10):break
	if len(items)>(rows+10):
		name=color['trangtiep']+'Trang tiep theo...trang %d/%d[/COLOR]'%(page+1,pages)
		addir(name,url,iconpath+'khophim.png','',97,page+1,'',isFolder=True)

def doc_xml(url,filename='',para=''): 
	if (datapath in url) or (myfolder in s2u(url)):body=makerequest(url)
	elif filename=='list_xml':body=make_request(url)
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
				if makerequest(f_fullpath,string,'w'):
					mess(u'Đã tải file %s vào MyFolder'%s2u(filename))
	return items

def fshare_page_file(url):
	body = make_request(url)
	name=clean_string(xsearch('<title>(.+?)</title>',body,1))
	if not name or 'Lỗi 404' in name:mess(u'Không tìm thấy nội dung quý khách yêu cầu!','fshare.vn');return 'no'
	size=xsearch('<i class="fa fa-hdd-o"></i>(.+?)</div>',body,1).strip()
	return name+' - '+size

def doc_TrangFshare(name,url,img,fanart,query=''):
	pageIndex=filescount=rowscount=files_count=0
	if 'pageIndex' in url:
		pageIndex=int(url.split('?')[1].split('=')[1]);filescount=int(url.split('?')[2].split('=')[1])
		rowscount=int(url.split('?')[3].split('=')[1])
	if 'favorite' in url:
		hd['Cookie']=loginfshare();body=make_request(url,hd);logout_site(hd['Cookie'],url)
	else:body=make_request(url)
	name=clean_string(xsearch('<title>(.+?)</title>',body,1));name_return=name
	if not name or 'Lỗi 404' in name:mess(u'Không tìm thấy nội dung quý khách yêu cầu!','fshare.vn');return 'no'
	if '/file/' in url:
		size=xsearch('<i class="fa fa-hdd-o"></i>(.+?)</div>',body,1).strip()
		items=[('',url,name,size,'')] #return url,name,size
	else:
		files_count=xsearch('Số lượng:(.+?)</div>',body,1).strip()
		files_count=int(files_count) if files_count else filescount
		pattern='data-id="(.+?)" .+? href="(.+?)".+title="(.+?)".*\s.*\s.*\s.*<.+?>(.+?)</div>.*\s.*<.+?>(.+?)</div>'
		items=re.findall(pattern,body)
		if not items:mess(u'Thư mục trống!','fshare.vn');return 'no'
		if url.strip()==thumucrieng:
			items=sorted(items,key=lambda l:(l[4][6:]+l[4][3:5]+l[4][:2]), reverse=True)
	idtxtfile=joinpath(datapath,'id.txt');makeidtxtfile=False
	for id,href,name,size,date in items:
		if re.search('/folder/\w{10,14}\?p=',href): #Thu muc con
			temp=xsearch('(\w{10,14} )',name,1)
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
	if makeidtxtfile:makerequest(idtxtfile,str(ids),'w')
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
			name=name_size.group(1)+' - '+name_size.group(2)
			if url not in temp:temp.append((url));addirs(name,url)
	return temp

def doc_thumuccucbo(name,url,img,fanart,mode,query):
	if url=='thumuccucbo':url=myfolder
	url=s2u(url)
	if query=='Remove':
		if os.path.isfile(url):
			try:os.remove(url);mess(u'Đã xóa file: %s'%s2u(url),'MyFolder');xbmc.executebuiltin("Container.Refresh")
			except:mess(u'Lỗi xóa file!','MyFolder')
		else:
			import shutil
			try:shutil.rmtree(url);mess(u'Đã xóa thư mục: %s'%s2u(url),'MyFolder');xbmc.executebuiltin("Container.Refresh")
			except:mess(u'Lỗi xóa thư mục!','MyFolder')
	elif query=='Rename':
		name=s2u(os.path.basename(url))
		name_new = get_input('xshare - Rename file/folder (chú ý phần mở rộng)',name)
		if name_new and name_new!=name:
			if rename_file(url,joinpath(os.path.dirname(url),name_new)):
				mess(u'Đã đổi tên file/folder: %s'%s2u(url),'MyFolder');xbmc.executebuiltin("Container.Refresh")
			else:mess(u'Lỗi Rename file/folder!','MyFolder')
	elif myfolder in url and query!='file':
		for filename in os.listdir(url):
			filenamefullpath = u2s(joinpath(url, filename));filename= u2s(filename)
			size=os.path.getsize(joinpath(url, filename))/1024
			if size>1024:size='%dMB'%(size/1024)
			else:size='%dKB'%size
			label=filename+' - %s'%size
			if os.path.isfile(joinpath(url, filename)):
				file_ext=os.path.splitext(filenamefullpath)[1][1:].lower()
				if file_ext in media_ext:
					item = xbmcgui.ListItem(label, iconImage=icon['khophim'])
					query=menuContext(label,filenamefullpath,'','',mode,query,item)
					xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=filenamefullpath,listitem=item)
				elif file_ext=='xml':addirs(label,filenamefullpath,icon['khophim'],query='xml')
				else:addirs(label,filenamefullpath,query='file')
			else:
				name='%s%s[/COLOR]'%(color['trangtiep'],filename)
				addir(name,filenamefullpath,icon['icon'],'',mode,1,filenamefullpath,True)
		return
	else:mess(u'Chưa xử lý kiểu file này','MyFolder')
	return 'no'

def play_maxspeed_link(url):
	if not url or url=='Maxlink':
		maxlink=get_input('Hãy nhập max speed link của Fshare, 4share hoặc tênlửa')
		if not maxlink or not maxlink.strip():return 'no'
		url=maxlink.replace(' ','')
	elif len(url)<13:
		fsend=getFsend(url)
		if fsend:url=fsend[0][1]
		else:mess(u'Lỗi get Fsend!','play_maxspeed_link');return 'no'
	return xshare_resolve(url,filmlabel='Maxlink')

def getFsend(id):
	response=make_request('http://fsend.vn/'+id,hd,'o')#http://fsend.vn/2LJL4GPVZ48L file XXOA5LADP6FC folder
	hd['Cookie']=response.cookiestring
	token=xsearch('"(.+?)"',urllib.unquote(response.cookiestring),1)
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
	idf=xsearch('\w{14,20}',href,0)
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

def id_2url(url,name='',mode=0,page=0,query=''):
	def check_id_tenlua(id):
		response=tenlua_get_detail_and_starting(id);name=url=''
		if response["type"]=="file":name=response['n'];url="https://www.tenlua.vn/download/"+id
		elif response["type"]=="folder":name=response["folder_name"];url="https://www.tenlua.vn/fm/folder/"+id
		return name,url
	def check_id_4share(id):
		url='http://4share.vn/f/%s/'%id;name=''
		item=re.search('<center>.+?<strong>(.+?)</strong>.+?<strong>(.+?)</strong></center>',make_request(url))
		if item:name=item.group(1)+' - '+item.group(2)
		else:
			url='http://4share.vn/d/%s/'%id
			items=re.findall("<br/><b>(.+?)</b>|<a href='(/f/\w+)|<a href='(/d/\w+)'>",make_request(url))
			if len(items)>1:name=items[0][0]
		return name,url
	def find_id_internal(id):
		r1='href="(.+%s.*)" img="(.*?)">(.+?)</a>';r2='img="(.*?)" fanart=".*?" href="(.+%s.*)">(.+?)</a>'
		items=dict();files='phimfshare.xml-hdvietnam.xml'
		for file in ['vaphim.xml','ifiletv.xml','phimfshare.xml','hdvietnam.xml']:
			body=makerequest(joinpath(datapath,file));id=id.lower() if len(id)>13 else id
			item=re.search(r1%id,body) if file in files else re.search(r2%id,body)
			if item:
				items['name']=item.group(3);items['href']=item.group(1 if file in files else 2)
				items['img']=item.group(2 if file in files else 1);break
		return items
	if query=='MyFshare':query=thumucrieng;page=4
	if page==0:
		name=color['search']+'Nhập ID (hoặc url) phim[/COLOR] %sFshare (hoặc Fsend)[/COLOR]-%s4share[/COLOR] hoặc %stenlua[/COLOR]'%(color['fshare'],color['4share'],color['tenlua'])
		addir(name,url,icon['icon'],mode=mode,query=query,page=1,isFolder=True)
		for href,name in re.findall('<a href="(.+?)">(.+?)</a>',makerequest(search_file)):
			q='ID?xml' if '.xml' in name else 'ID?'+query
			addirs(name,href,icon['id'],query=q)
	elif page == 1:#Nhập ID mới
		idf = get_input('Hãy nhập chuỗi ID link của Fshare-4share hoặc tenlua')#;record=[]
		if idf is None or idf.strip()=='':return 'no'
		idf = xsearch('(\w{10,20})',''.join(s for s in idf.split()).upper(),1)
		if len(idf)<10:mess(u'Bạn nhập ID link chưa đúng: %s!'%idf);return 'no'
		items=find_id_internal(idf)
		if items:addirs(items['name'],items['href'],items['img'])#;record.append((items['href'],items['name']))
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
		else:mess(u'Không tìm được link có ID: %s!'%idf);return 'no'
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
		category+=xsearch('phim/(.+?)\.\d{,6}',c,1)+' '
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
	mess(u'Ifile.tv auto updating ...',homnay)
	items_old=doc_xml(joinpath(datapath,"ifiletv.xml"));id_old=[s[1] for s in items_old]
	items_new = []#id_tip,id_htm,href,img,name
	for id_tip,id_htm,href,img,name in ifile_tv_page('http://ifile.tv/') :
		if id_htm not in id_old:
			for url4share,fanart,name2,catalog in ifile_tv_4share(href):
				fullname=name2 if name in name2 else name
				fullname=' '.join(s for s in fullname.split())
				items_new.append((id_tip,id_htm,catalog,img,fanart,url4share,fullname))
	if items_new:update_xml(items_new,items_old,"ifiletv.xml")
	else:mess(u'Không có phim mới...','Ifile.tv auto update')
	return 'ok'

def read_all_filexml(fn="vaphim.xml",string_search='',lists=[],index=[]):
	if string_search:lists=lists+doc_xml(joinpath(datapath,fn),para='search:'+string_search)
	else:lists=lists+doc_xml(joinpath(datapath,fn))
	if not string_search:
		for id_tip,id_htm,category,img,fanart,url,name in lists:index.append((id_htm))
	return lists,index

def googleapis_search(url,query,mode):
	if '?' not in query:start='0'
	else:start=query.split('?')[1];query=query.split('?')[0]
	if url=='hdvietnam.com':url_search='https://www.googleapis.com/customsearch/v1element?rsz=filtered_cse&num=20&key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&source=gcsc&gss=.com&cx=006389339354059003744:dxv8n47myyg&googlehost=www.google.com&sig=23952f7483f1bca4119a89c020d13def&nocache&start=%s&q=%s';ico=icon['hdvietnam']
	elif url=='phimfshare.com':url_search='https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=20&hl=vi&prettyPrint=false&source=gcsc&gss=.com&googlehost=www.google.com&sig=23952f7483f1bca4119a89c020d13def&cx=005609294674567689888:qyuk9aoqwmg&nocache&start=%s&q=%s';ico=icon['phimfshare']
	else:return list()
	url_search=url_search%(start,urllib.quote_plus(query))
	result=make_request(url_search,resp='j');items=list()
	if not result:return list()
	for item in result.get("results",dict()):
		href=urllib.unquote(item.get('url'))
		if not href:continue
		name=remove_tag(item.get('titleNoFormatting'))
		if len(name.split())<2:name=os.path.basename(item['url'])
		img=get_dict(item,['richSnippet','cseThumbnail','src'])
		if not img:img=ico
		fanart=get_dict(item,['richSnippet','cseImage','src'])
		items.append((name,href,img,fanart,0,1,'get_link_post'))
	page_dict=get_dict(result,['cursor','pages']);label=list();pages=0
	if page_dict:label=[s.get('label') for s in page_dict if s.get('start')==start]
	if label:label=label[0]+1;start=[s.get('start') for s in page_dict if s.get('label')==label]
	for item in page_dict:pages=item.get('label') if item.get('label',0)>pages else pages
	if label and start:
		label=color['trangtiep']+'Trang tiep theo...trang %d/%d[/COLOR]'%(label,pages)
		items.append((label,url,ico,'',mode,4,query+'?'+start[0]))
	return items

def xshare_search(name,url,query,mode,page,items=[]):#13
	def trang_search(string):
		if len(string.split('?'))==3:p=string.split('?')[2];trang=string.split('?')[1];string=string.split('?')[0]
		elif len(string.split('?'))==2:p=1;trang=string.split('?')[1];string=string.split('?')[0]
		else:p=trang='1'
		return string,trang,p

	if url=='addstring.xshare.vn' or query=='Add':
		name=remove_tag(name)
		if not re.search(name,makerequest(search_file)):
			makerequest(search_file,'<a>%s</a>\n'%name,'a')
			mess(u'Đã thêm tên phim này vào DS tìm kiếm')
	elif page==0:make_mySearch('',url,'','',mode,'get');return
	elif page==1:
		query=make_mySearch('',url,'','','','Input');page=2
		if query is None or not query.strip():return 'no'
	query=no_accent(query)
	
	if url=='vaphim.com':#print_dict(mp('http://vaphim.com/fast-search.php',data='term=hur+jun',resp='j'))
		query,trang,p=trang_search(query)
		url_search='http://vaphim.com/page/%s/?s=%s'%(trang,urllib.quote_plus(query))
		body=make_request(url_search)
		items=vp_page(url_search,body)#id,name,href,img,category
		if not items:mess(u'Không tìm được tên phim phù hợp!','vaphim.com search');return 'no'
		for id,name,href,img,category in items:
			addir_info(name,href,img,query='vp_getsubpage')
		page_tag=re.search("class='pages'>(.+?)<.+span><a href='(.+?)' class='page larger'>(\d{,3})</a>",body)
		if page_tag:
			trang=str(int(trang)+1)
			name=color['trangtiep']+'Tiep theo %s...trang %s[/COLOR]'%(page_tag.group(1),page_tag.group(3))
			addir_info(name,url,icon[url.split('.')[0]],'',mode,4,'%s?%s?%s'%(query,trang,p),True)
	elif url in 'phimfshare.com hdvietnam.com':
		items=googleapis_search(url,query,mode)
		if not items:return
		for name,url,img,fanart,mode,page,query in items:
			addir_info(name,url,img,fanart,mode,page,query)
	elif url=='tenlua.vn':#get_dict(dict,key_list=list(),result='')
		query,trang,p=trang_search(query)
		href='https://api2.tenlua.vn/search?keyword=%s&page=%s'%(urllib.quote_plus("%s"%query),trang)
		dict=make_request(href,resp='j')
		if int(get_dict(dict,['pagging','total'],'0'))==0:
			mess(u'Không tìm được tên phim phù hợp!','tenlua search');return 'no'
		for item in dict.get('items',{}):
			if item is None or item.get('ext','no') not in media_ext:continue
			id=item.get('h')
			link=tenlua_get_detail_and_starting(id)
			if link.get('type')=="none":continue
			elif link.get('type')=="file":name=link['n'];href="https://www.tenlua.vn/download/%s"%id
			elif link.get('type')=="folder":name=link["folder_name"];href="https://www.tenlua.vn/fm/folder/%s"%id
			if href not in items:items.append(href);addir_info(name,href,icon['tenlua'])
		trang=str(int(trang)+1)
		if int(get_dict(dict,['pagging','pages'],'0'))>=int(trang) and len(items)<10 and int(trang)%15>0:
			return xshare_search(name,url,'%s?%s?%s'%(query,trang,p),mode,page,items)
		p=str(int(p)+1)
		if int(get_dict(dict,['pagging','pages'],'0'))>=int(trang):
			name=color['trangtiep']+'Trang tiep theo...trang %s[/COLOR]'%p
			addir_info(name,url,icon['tenlua'],'',mode,4,'%s?%s?%s'%(query,trang,p),True)
	elif '4share.vn' in url:
		def ext_media(url):return os.path.splitext(url)[1][1:].lower().strip() in media_ext
		if url=='4share.vn':url='http://4share.vn/search?search_string='+urllib.quote_plus(query)
		pattern="<a href='(.+?)' target='_blank' title='(.+?)'>.+?</a>"
		body=make_request(url);items=[s for s in re.findall(pattern,body) if ext_media(s[0])]
		if not items:mess(u'Không tìm thấy dữ liệu yêu cầu!','xshare_search');return 'no'
		for href,title in items:addir_info(title,href.split()[0],icon['4share'])
		next=xsearch("<a href='([^<]+?)'> Next</a>",body,1)
		if next:
			title=color['trangtiep']+'Trang tiep theo...trang %s[/COLOR]'%xsearch('\?page=(\d{1,3})&',next,1)
			addir_info(title,'http://4share.vn'+next.replace(' ','+'),icon['4share'],'',mode,4,'',True)
	elif url=='ifile.tv':
		query,trang,p=trang_search(query)	
		url_search = 'http://ifile.tv/search?search_module=phim&search_name=1&'
		url_search += 'search_content=1&time_sort=new&search_string="%s"'%urllib.quote_plus(query)
		items = []
		for content in re.findall("<td>(.*?)</b>",make_request(url_search)):
			items+=re.findall("<a.+href='(.+?)'.+src='(.+?)'.+(\d{5}).+>(.+?)</a>",content)
		if not items:mess(u'Không tìm được tên phim phù hợp!','Ifile.tv search');return 'no'
		items_xml,id_xml = read_all_filexml(fn="ifiletv.xml")
		for href,img,id_htm,name in items:
			if id_htm in id_xml:
				index = id_xml.index(id_htm)
				while id_xml[index] == id_htm:
					temp.append((items_xml[index]));index +=1 
			else:
				for url4share,fanart,name2,catalog in ifile_tv_4share('http://ifile.tv'+href):
					temp.append(('',id_htm,catalog,img,fanart,url4share,name))
		for id_tip,id_htm,catalog,img,fanart,href,name in temp:addir_info(name,href,img,fanart)
	elif url=='xshare.vn':
		query,trang,p=trang_search(query);items=[]
		if trang=='1':
			for fn in ['vaphim.xml','ifiletv.xml','phimfshare.xml','hdvietnam.xml']:
				items,index=read_all_filexml(fn=fn,string_search=".*".join(query.split()),lists=items)
			items=sorted(items,key=lambda l:no_accent(l[3]).lower());p=str(len(items))
			if not items:mess(u'Không tìm thấy phim nào có chuổi phù hợp!','Xshare search');return
			if len(items)>(rows+rows/2):makerequest(joinpath(data_path,'temp.txt'),str(items),'w')
		else:f=open(joinpath(data_path,'temp.txt'));items=eval(f.readlines()[0]);f.close()
		trang=int(trang);del items[:rows*(trang-1)]
		if len(items)>(rows+rows/2):
			del items[rows:];trang=str(trang+1)
		else:trang=''
		for img,fanart,href,name in items:addir_info(name,href,img,fanart)
		if trang:
			name=color['trangtiep']+'Trang tiep theo...trang %s/%s[/COLOR]'%(trang,str(int(p)/rows+1))
			addir_info(name,url,icon['icon'],'',mode,4,'%s?%s?%s'%(query,trang,p),True)
	return ''

def pfs_update():
	timenow=datetime.datetime.now().strftime('%Y%m%d%H')
	my_dict=json_rw('xshare.json');pfs_update_time=my_dict.get('pfs_update_time','0')
	if int(timenow)-int(pfs_update_time)<5:return
	else:my_dict['pfs_update_time']=timenow;my_dict=json_rw('xshare.json',my_dict)
	mess(u'PhimFshare.com auto updating ...',homnay)
	body=make_request('http://phimfshare.com/external.php?type=RSS2');items=list()
	if not body:return
	phimfshare=makerequest(joinpath(datapath,'phimfshare.xml'));string='';count=0
	for item in re.findall('<item>(.+?)</item>',body,re.DOTALL):
		id=xsearch('<link>.*-(\d{5,6})/.*</link>',item,1)
		if not id:continue
		title=re.sub('<!\[CDATA\[|\]\]>','',xsearch('<title>(.+?)</title>',item,1))
		img=xsearch('img src="(.+?jpg)["|?| ]',item,1)
		content=xsearch('<content:encoded>(.+?)</content:encoded>',item,1,re.DOTALL)
		pattern='(https?://www.fshare.vn/\w{4,6}/\w{10,14}|http://4share.vn/./\w{14,20}|https?://w?w?w?/?tenlua.vn/.*?|http://subscene.com/subtitles/.+?)[ |"|\'|<]'
		for href in list(set([s for s in re.findall(pattern,content) if '..' not in s])):
			href=correct_link(href);server=xsearch('(\w{6,8})\.[v|c]',href,1)
			if href not in phimfshare:
				string+='<a id="%s" server="%s" href="%s" img="%s">%s</a>\n'%(id,server,href,img,title);count+=1
	if string:
		mess(u'Đã cập nhật được %d phim'%count,'Phimfshare auto update')
		makerequest(joinpath(datapath,'phimfshare.xml'),string,'a')
	else:mess(u'Không có phim mới','Phimfshare auto update')

def pfs_getlink(content):#6+
	items=[]
	pattern='(https?://www.fshare.vn/\w{4,6}/\w{10,14})|(http://4share.vn/./\w{14,20})|(https?://w?w?w?/?tenlua.vn/.*?)[ |"|<]'
	for links in re.findall(pattern,content):
		if links:
			for link in links:
				idf=xsearch('(\w{10,20})',link,1)
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
	string=re.split('20\d\d|19\d\d',title)[0]
	string=re.sub(xsearch('multi ',string,0,re.IGNORECASE),'',string)
	return string if string else title

def phimFshare(name,url,img,fanart,mode,page,query):#6
	fphimfshare=joinpath(datapath,'phimfshare.xml');home='http://phimfshare.com/';pagenext=''
	def pfs_page(url,pattern):
		body=make_request(url)
		return re.findall(pattern,body),xsearch('<a rel="next" href="(.+?)" title=".+?">',body,1)
	def pfs_addir(items):
		for id,href,img,name in items:addirs(name,href,img)
	def pfs_xml():
		pattern='<a id="(.+?)" server=".+?" href="(.+?)" img="(.*?)">(.+?)</a>'
		return re.findall(pattern,makerequest(fphimfshare))
	
	if query=='phimfshare.com':make_mySearch('',url,'','',mode,'get');return
	elif page==4 and name==query:return phimFshare('Search',url,img,fanart,mode,page,query)
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		return phimFshare('Search',url,img,fanart,mode,page,query) if query else 'no'
	elif name=='Search':
		items=googleapis_search('phimfshare.com',query,mode)
		items=[(s[2],s[1],'',s[0]) for s in items if 'Trang tiep theo' not in s[0]]
		if not items:mess(u'Không tìm thấy phim có chứa chuổi tìm kiếm!','phimFshare');return 'no'
	elif query=='get_link_post':
		response=make_request(url)
		img=xsearch('<img src="(.+?)" border="0" alt="" />',response,1)
		for server,href in pfs_getlink(response):addir_info(re.sub('\[/?COLOR.*?\]','',name),href,img)
		return
	elif query=='PhimMoi':
		items,pagenext=pfs_page(home,'()<a href="(.+?)" ()class="title">(.+?)</a>')
	elif url=='folder':pfs_addir([s for s in pfs_xml() if query in s[3]]);return
	else:
		if home not in url:url=home+url+'/'
		pattern='<img class="preview" src="(.+?)" .+? class=".+?" href="(.+?)" id="thread_title_(.+?)">(.+?)</a>'
		items,pagenext=pfs_page(url,pattern)#img,href,id,title
		
	items=[(s[0],s[1],s[2] if len(s[2])>4 else xsearch('-(\d{5})',s[1],1),s[3]) for s in items]
	lists=[s for s in pfs_xml() if s[0] in [f[2] for f in items]]
	for label in list(set([subtitle_of_year(s[3]) for s in lists])):
		temp=[s for s in lists if label in s[3]]
		if not temp:continue
		elif len(temp)>1:
			id,href,img,title=temp[0];title=[s[3] for s in temp if '~' in s[3]]
			title=label+' ~ '+re.sub('.+?~ ?','',title[0]) if title and '~' not in label else label
			addir(color['phimfshare']+title+'[/COLOR]','folder',img,'',mode,page,label,True)
		else:pfs_addir(temp)
	if pagenext:
		page=2 if not page else page+1
		label=color['trangtiep']+'Trang tiếp theo - Trang '+str(page)+' ...[/COLOR]'
		addir(label,pagenext,iconpath+'fshare.png',mode=mode,page=page,query=query,isFolder=True)
	if name=='Search':return
	endxbmc();ids=[s[2] for s in items if s[2] not in list(set([f[0] for f in lists]))];content_new=''
	if ids:mess(u'Databse updating...','phimfshare.com')
	for img,href,id,name in [s for s in items if s[2] in ids]:
		response=make_request(href)
		temp=xsearch('<title> (.+?)</title>',response,1)
		if temp:name=temp
		elif not name:continue
		if not img:img=xsearch('<img src="(.+?)" border="0" alt="" />',response,1)
		name=' '.join(s for s in re.sub('\[.+?\]|\(.+?\)|MuLtI|Fshare|fshare','',name).split())
		for server,link in pfs_getlink(response):
			if link not in content_new:
				content_new+='<a id="%s" server="%s" href="%s" img="%s">%s</a>\n'%(id,server,link,img,name)
	if content_new:makerequest(fphimfshare,content_new,'a');xbmc.executebuiltin("Container.Refresh")
	return ''

def correct_link(url):
	if 'tenlua.vn' in url:idf=xsearch('(\w{16,20})',url,1)
	elif 'subscene.com' in url and '...' not in url:idf='ok'
	else:idf=xsearch('(\w{10,20})',url,1)
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

def hdvn_update(items=[]):#33-146-311-265-110-116-123-57-157
	mess(u'HDVietnam.com auto updating ...',homnay)
	urlhome='http://www.hdvietnam.com/diendan/external.php?type=RSS2&forumids='
	if not items:
		pattern='(https?://www.fshare.vn/\w{4,6}/\w{10,14})|(http://4share.vn/./\w{14,20})|(https?://w?w?w?/?tenlua.vn/.*?)[ |"|<]|(http://subscene.com/subtitles/.+?)[ |"|\'|<]'
		for id in '-33-146-311-265-110-116-123-57-157'.split('-'):
			mess('hdvietnam forumids=%s updating ...'%id,homnay)
			for name,link,pubDate,img,description,uploader in hdvietnam_rss(urlhome+id):
				for links in re.findall(pattern,description):
					for href in [s for s in links if s and '...' not in s]:
						href=correct_link(href)
						if href not in str(items):items.append((href,img,name))
	file=joinpath(datapath,"hdvietnam.xml");string='';count=0
	urls=re.findall('href="(.+?)"',makerequest(file))
	for url,img,name in [s for s in items if s[0] not in urls]:
		string+='<a date="%s" href="%s" img="%s">%s</a>\n'%(homnay,url,img,name);count+=1
	if string:
		makerequest(file,string,'a')
		mess(u'Đã cập nhật được %d phim'%count,'hdvietnam update')
	else:mess(u'Không có phim mới','hdvietnam update')
	return 'ok'

def hdvietnam_rss(url):
	body=make_request(url);items=list()
	for data in re.findall('<item>(.+?)</item>',body,re.DOTALL):
		label=xsearch('<title><!\[CDATA\[(.+?)\]\]></title>',data,1)
		link=xsearch('<link>(.+?)</link>',data,1)
		pubDate=xsearch('<pubDate>(.+?)</pubDate>',data,1)
		description=xsearch('<description><!\[CDATA\[(.+?)\]\]></description>',data,1,re.DOTALL)
		uploader=xsearch('<dc:creator>(.+?)</dc:creator>',data,1);img=''
		for img in re.findall('Image: (http.+?\.jpg|http.+?\.png)',data):
			if not [s for s in ['kho-phim','chuyenlink.php','header-'] if s in img]:break
		items.append((label,link,pubDate,img,description,uploader))
	return items

def hdvietnam_get_body_token(url):
	hd['Cookie']=makerequest(joinpath(datapath,'hdvietnam.cookie'))
	body=make_request(url,hd,maxr=1);token=xsearch('name="securitytoken" value="(.+?)"',body,1)
	if not token or token=='guest':
		hd['Cookie']=loginhdvietnam();body=make_request(url,hd,maxr=1)
		token=xsearch('name="securitytoken" value="(.+?)"',body,1)
	return xshare_postks(body,hd,token)#body,token,hd['Cookie']

def hdvietnam(name,url,img,fanart,mode,page,query):
	col='[COLOR orangered]';ico=icon['hdvietnam'];tempfolder=xbmc.translatePath('special://temp')
	urlhome='http://www.hdvietnam.com/diendan/'
	def namecolor(name):return col+name+'[/COLOR]'
	def get_link_post(url):
		if '#post' in url:p=[xsearch('post(\d{4,10})',url,1)];url=url.split('#post')[0]
		else:p=''
		url='%s%s&styleid=9'%(url,'&mode=threaded' if '?' in url else '?mode=threaded')
		body,token,hd['Cookie']=hdvietnam_get_body_token(url)
		#id_post,id_user,label,url
		writeLink=re.findall('writeLink\((.+?),.+?,.+?, (.+?), ".*?", "(.+?)", ".*?", ".*?",.+?, "(.+?)"\)',body)
		if writeLink:id_boss=writeLink[0][1]
		else:id_boss=''
		id_post_boss=[s[0] for s in writeLink if s[1]==id_boss]
		if p:contents=re.findall('pd\[(%s)\] =(.+?)\n'%p,body)
		else:contents=[s for s in re.findall('pd\[(.+?)\] =(.+?)\n',body) if s[0] in id_post_boss]
		pattern1='<a href="(https?://www.fshare.vn/.{10,100}|https?://4share.vn/.{10,100}|https?://w?w?w?/?tenlua.vn/.{10,100}|http://subscene.com/subtitles/.{10,100})" target="_blank">(.+?)</a>'
		pattern2='(https?://www.fshare.vn/\w{4,6}/\w{10,14})|(http://4share.vn/./\w{14,20})|(https?://w?w?w?/?tenlua.vn/.*?)[ |"|<]|(http://subscene.com/subtitles/.+?)[ |"|\'|<]'
		showthread='http://www.hdvietnam.com/diendan/showthread.php'
		post_thanks='http://www.hdvietnam.com/diendan/post_thanks.php';items=list()
		for id_post,content in contents:
			if 'id="hide_fieldset"' in content:
				make_post(post_thanks,hd,'do=post_thanks_add&using_ajax=1&p=%s&securitytoken=%s'%(id_post,token))
				content=make_post(showthread,hd,'do=whatever&p=%s&securitytoken=%s'%(id_post,token),resp='b')
				make_post(post_thanks,hd,'do=post_thanks_remove_user&using_ajax=1&p=%s&securitytoken=%s'%(id_post,token))
			label=[s[2] for s in writeLink if s[0]==id_post]
			if label:label=label[0]
			elif re.split('\d{4}',label)[0] in name:label=remove_tag(name)
			else:label=remove_tag(xsearch('<font size=.+?>(.+?)</font>',content,1,re.DOTALL))
			label1=remove_tag(xsearch('id="post_message_.{,100}<b>(.+?)</b>',content,1))
			label2=remove_tag(xsearch('<b>(.{20,80})</b>',content,1));label2='%s - '%label2 if label2 else ''
			img=xsearch('img src="(.+?)"',content,1)
			if not img:img=xsearch('img src="(.+?\.jpg)"',content,1)
			for href,title in re.findall(pattern1,content):
				if [s for s in ['fshare.vn','4share.vn','tenlua.vn','subscene.com'] if s in title]:
					title=label1 if label1 else label2+label;items.append((0,title,href,img))
				elif [s for s in ['fshare.vn','4share.vn','tenlua.vn','subscene.com'] if s not in title]:
					items.append((0,remove_tag(title),href,img))
				elif 'showthread.php' in href:items.append((1,remove_tag(title),href,img))
			for links in re.findall(pattern2,content):
				title=label1 if label1 else label2+label
				for link in [s for s in links if s and '...' not in s]:
					if link not in str(items):items.append((0,title,link,img))
		items=[(s[1],s[2].replace('amp;',''),s[3]) for s in sorted(items)]
		#CÁC CHỦ ĐỀ CÙNG CHUYÊN MỤC
		content=xsearch('<div class="morethread">(.+?)"postfoot_container"',body,1)
		for title,href in re.findall('<a title="(.+?)" href="(.+?)">',content):
			items.append((title,href,"morethread"))
		return items#title,href,img 
	
	menu={'muctheodoi':{'action':'Add','server':['hdvietnam.com']}}
	menu['MyFshare']={'action':'Add','server':['fshare.vn']}
	menu['MyFavourites']={'action':'Add','server':['fshare.vn','4share.vn','tenlua.vn','subscene.com']}
	if url in '000-UPD':
		if query=='UPD':hdvn_update()
		body=makerequest(joinpath(datapath,"hdvietnam.xml"));homqua=''
		if not body:return
		dates=sorted(list(set(re.findall('date="(.+?)"',body))),key=lambda k:k[6:]+k[3:5]+k[:2],reverse=True)
		homnay=dates[0] if query in '000-UPD' else query
		items=re.findall('date="%s" href="(.+?)" img="(.+?)">(.+?)</a>'%homnay,body)
		for name in list(set([subtitle_of_year(s[2]) for s in items])):
			lists=[s for s in items if name in s[2]]
			if not lists:continue
			elif len(lists)==1:
				href,img,title=lists[0]
				addir_info(title,href,img,'',mode,1,'',True,menu=menu)
			else:
				href,img,title=lists[0]
				title=name+' ~ '+re.sub('.+?~ ?','',title) if '~' in title and '~' not in name else name
				addir_info(title,'hdvietnam.com',img,'',mode,1,name,True,menu=menu)
		if dates.index(homnay)+1<len(dates):
			homqua=dates[dates.index(homnay)+1]
			name=color['trangtiep']+"Thông tin ngày %s[/COLOR]"%homqua
			addir_info(name,"000",ico,'',mode,1,homqua,True)
	elif query=='get_room_id':
		id=get_input('Hãy nhập chuỗi ID Room của hdvietnam.com')
		if not id or not id.strip():return 'no'
		url='http://www.hdvietnam.com/diendan/showthread.php?t=%s'%id
		return hdvietnam(name,url,img,fanart,mode,page,'get_link_post')
	elif url=='hdvietnam.com':
		body=makerequest(joinpath(datapath,"hdvietnam.xml"));temp=[]
		items=[s for s in re.findall('date=".+?" href="(.+?)" img="(.+?)">(.+?)</a>',body) if query in s[2]]
		for href,img,name in list(set(items)):
			if href not in temp:
				temp.append(href)
				addir_info(name,href,img,menu=menu)
	elif 'muctheodoi' in query:
		if query=='muctheodoi':url='http://www.hdvietnam.com/diendan/subscription.php?folderid=0'
		body,token,hd['Cookie']=hdvietnam_get_body_token(url)
		if 'Add' in query:
			threadid=xsearch('RELPATH = "showthread.php\?t=(\d{6,10})[&|"]',body,1)
			data='do=doaddsubscription&threadid=%s&securitytoken=%s'%(threadid,token)
			response=make_post('http://www.hdvietnam.com/diendan/subscription.php',hd,data=data,resp='o')
			if response.status==200:mess(u'Thêm vào Mục đang theo dõi thành công','HDVietnam.com')
			else:mess(u'Thêm vào Mục đang theo dõi thất bại!','HDVietnam.com')
		elif 'Remove' in query:
			threadid=xsearch('RELPATH = "showthread.php\?t=(\d{6,10})[&|"]',body,1)
			url='http://www.hdvietnam.com/diendan/subscription.php?do=removesubscription&t=%s'%threadid
			if make_request(url,hd,resp='o').status==200:mess(u'Xóa khỏi Mục đang theo dõi thành công','HDVietnam.com');xbmc.executebuiltin("Container.Refresh")
			else:mess(u'Xóa khỏi Mục đang theo dõi thất bại!','HDVietnam.com')
		else:
			menu={'muctheodoi':{'action':'Remove','server':['hdvietnam.com']}}
			for href,title in re.findall('<a class="title.*?" href="(.+?)" id=".+?">(.+?)</a>',body):
				addir_info(namecolor(title),urlhome+href,ico,'',mode,1,'get_link_post',True,menu=menu)
	elif re.search('\d\d',query):
		url='http://www.hdvietnam.com/diendan/external.php?type=RSS2&forumids=%s'%query
		items=list();page=-1
		for label,link,pubDate,img,description,uploader in hdvietnam_rss(url):
			items.append(description);page+=1
			name='[COLOR gold]%s[/COLOR] [COLOR lime]%s[/COLOR]:: %s'%(uploader,pubDate,label)
			addir_info(name,link,img,'',mode,page,'read_rss',True)
			if xsearch('/(\d{6,10})-',link,1):
				href='http://www.hdvietnam.com/diendan/showthread.php?t='+xsearch('/(\d{6,10})-',link,1)
			else:href=link
			addir_info(namecolor('Đến trang ')+os.path.basename(link),href,img,'',mode,1,'get_link_post',True,menu=menu)
			addir_info(namecolor(remove_tag(label)),link,img,'',mode,page,'read_rss',True,menu=menu)
		temp=makerequest(joinpath(tempfolder,"hdvietnam.rss"),str(items),'w')
	elif query=='read_rss':
		items=list();name=remove_tag(name)
		try:content=eval(makerequest(joinpath(tempfolder,"hdvietnam.rss")))[page]
		except:content=''
		pattern1='<a href="(.+?hdvietnam.com.+?|.+?fshare.vn.+?|.+?4share.vn.+?|.+?tenlua.vn.+?|.+?subscene.com.+?)" target="_blank">(.+?)</a>'
		pattern2='(https?://www.fshare.vn/\w{4,6}/\w{10,14})|(http://4share.vn/./\w{14,20})|(https?://w?w?w?/?tenlua.vn/.*?)[ |"|<]|(http://subscene.com/subtitles/.+?)[ |"|\'|<]'
		for href,title in re.findall(pattern1,content):
			if any(s for s in ['fshare.vn/','4share.vn/','tenlua.vn/','subscene.com/'] if s in title):
				items.append((0,name,href,img))
			elif 'http://' not in title:items.append((1,remove_tag(title),href,img))
		for links in re.findall(pattern2,content):
			for link in [s for s in links if s and '...' not in s]:
				if link not in str(items):items.append((0,name,link,img))
		for title,href,img in [(s[1],s[2].replace('amp;',''),s[3]) for s in sorted(items)]:
			addir_info(title,href,img,query='get_link_post',menu=menu)
	elif query=='MCS':
		body=make_request('http://www.hdvietnam.com/diendan/34-chia-se-phim/?styleid=25')
		for href,name in re.findall('<h3><a href="(.+?)">(.+?)</a></h3>',body):
			addir_info(namecolor(name),urlhome+href.split('&')[0],img,query='PL1')
	elif query=='CSN':
		body=make_request('http://www.hdvietnam.com/diendan/148-chia-se-nhac/?styleid=25')
		for href,name in re.findall('<h3><a href="(.+?)">(.+?)</a></h3>',body):
			addir_info(namecolor(name),urlhome+href.split('&')[0],img,query='PL1')
	elif query=='PL1':
		parent_path='http://www.hdvietnam.com/diendan/'
		#if '&styleid=9&sort=dateline' not in url and 'f=150' in url:url=url+'&styleid=9'
		#elif '&styleid=9&sort=dateline' not in url:url=url+'&styleid=9&sort=dateline'
		if '&styleid=9' not in url:url=url+'&styleid=9'
		body=make_request(url,hd,maxr=2)
		if page<2:#Phụ Mục
			for href,title in re.findall('<h2 class="forumtitle"><a href="(.+?)&.+?>(.+?)</a></h2>',body):
				href=parent_path+href;title=title.replace(', ',' - ')
				addir_info('[B]'+namecolor(title)+'[/B]',href,ico,'',mode,1,'PL1',True)
		#Normal Threads
		pattern='<a class="title" href="(showthread.php.+?)&.+?>(.+?)</a>.+?<b>(.+?)</span>'
		menu={'muctheodoi':{'action':'Add','server':['hdvietnam.com']}}
		for href,title,bossroom in re.findall(pattern,sub_body(body,'Normal Threads',''),re.DOTALL):
			href=parent_path+href.split('&amp;')[0];title=remove_tag(title);bossroom=remove_tag(bossroom)
			menu={'muctheodoi':{'action':'Add','server':['hdvietnam.com']}}
			addir_info('[COLOR yellow]%s[/COLOR]-%s'%(bossroom,namecolor(title)),href,ico,'',mode,1,'get_link_post',True,menu=menu)
		pages=xsearch('class="popupctrl">Trang \d{1,4}/(\d{1,4})</a></span>',body,1)
		page=2 if page<2 else page+1
		if pages and int(pages)>page:
			name=color['trangtiep']+'Trang tiep theo...trang %d%s[/COLOR]'%(page,('/'+pages) if pages else '')
			if '&page=' not in url:url=url+'&page=%d'%page
			else:url=re.sub('&page=\d{1,3}','&page=%d'%page,url)
			addir_info(name,url,ico,'',mode,page,'PL1',True)
	elif query=='get_link_post':
		temp=''
		if 'http://' not in url:url='http://www.hdvietnam.com/diendan/'+url
		for title,href,img in get_link_post(url.replace('amp;','')):
			if 'http://' not in href:href=urlhome+href
			if img=='morethread':
				if not temp:
					add_sep_item('Các chủ đề cùng chuyên mục')
					#addir_info('[COLOR lime]----Các chủ đề cùng chuyên mục----[/COLOR]','no',ico,'',mode,1,'no')
				img=ico;temp='ok'
			query='download' if 'subscene.com' in href else 'get_link_post'
			addir_info(title,href,img,'',mode,1,query,menu=menu)#query=download cho subscene
	elif query=='GET':
		if 'xem-gi-hom-nay' in url:
			string='http://www.hdvietnam.com/diendan/clear.gif'
			if 'http://' in url:
				body=make_request(url)
				boss=xsearch('line popupctrl.{40,55}/\d{4,10}-(.+?).html"',body,1)
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

def database_download():
	mess(u'Đang kiểm tra và download database cho xshare','database_download');delete_files(tempfolder)
	tempfile = joinpath(tempfolder,"xshare_data.zip");pattern='<title>.*xx(.+?)xx.*</title>'
	if not os.path.exists(datapath):os.mkdir(datapath)
	if not os.path.exists(iconpath):os.mkdir(iconpath)
	id=xsearch(pattern,make_request('https://www.fshare.vn/folder/9F3VWL147DYG'),1)
	response=make_request('https://docs.google.com/uc?id=%s&export=download'%id,resp='o',maxr=1)
	if  response.status==200:
		body=makerequest(tempfile,response.body,'wb');xbmc.sleep(500)
		try:xbmc.executebuiltin('XBMC.Extract("%s","%s")'%(tempfile,tempfolder), True)
		except:mess(u'Database download error!','database_download');return
		xml_size=dict();png_size=dict()
		for file in os.listdir(datapath):xml_size[file]=os.path.getsize(joinpath(datapath,file))
		for file in os.listdir(iconpath):png_size[file]=os.path.getsize(joinpath(iconpath,file))
		for file in os.listdir(tempfolder):
			if os.path.isfile(joinpath(tempfolder,file)):
				if '.xml' in file and xml_size.get(file,0)<os.path.getsize(joinpath(tempfolder,file)):
					rename_file(joinpath(tempfolder,file),joinpath(datapath,file))
				elif '.png' in file and png_size.get(file,0)!=os.path.getsize(joinpath(tempfolder,file)):
					rename_file(joinpath(tempfolder,file),joinpath(iconpath,file))
				elif '.jpg' in file and os.path.getsize(joinpath(tempfolder,file))!=613866:
					rename_file(joinpath(tempfolder,file),joinpath(home,file))
		if os.path.isfile(joinpath(data_path,'checkdatabase.txt')):os.remove(joinpath(data_path,'checkdatabase.txt'))
		myaddon.setSetting('checkdatabase','false');mess(u'Download database cho xshare thành công','database_download')
	else:mess(u'Download database cho xshare không thành công!','database_download')

def xshare_auto_update():
	try:
		if checkupdate('last_update.dat',17,datapath):
			xshare_update();vp_make_datanew();vp_update();ifile_update()
			makerequest(joinpath(datapath,"last_update.dat"),'','w')
			mess('Xshare auto update completed','vaphim ifiletv')
		#if checkupdate('phimfshare.xml',11,datapath):pfs_update()
		if checkupdate('hdvietnam.xml',7,datapath):hdvn_update()
	except:mess('Data update error!')

def checkupdate(filename,hours=1,folder=datapath,xdict=dict()):
	filecheck=joinpath(folder,filename);timeformat='%Y%m%d%H'
	filetime=os.path.getmtime(filecheck) if os.path.isfile(filecheck) else 0
	last_update=datetime.datetime.fromtimestamp(filetime).strftime(timeformat)
	timenow=datetime.datetime.now().strftime(timeformat);result=False
	if int(timenow)-int(last_update)>hours:
		xshare_dict=json_rw('xshare.json');file_time=xshare_dict.get(filename,'0')
		if timenow > file_time:xshare_dict[filename]=timenow;json_rw('xshare.json',xshare_dict);result=True
	return result

def xshare_update():
	timenow=datetime.datetime.now().strftime('%Y%m%d%H')
	my_dict=json_rw('xshare.json');time_xshare=my_dict.get('time_xshare','0')
	if int(timenow)-int(time_xshare)<24*7:return
	room_id=my_dict.get('room_id') if my_dict.has_key('room_id') else '997745'
	url='http://www.hdvietnam.com/diendan/showthread.php?t=%s&mode=threaded&styleid=9'%room_id
	items=re.findall('writeLink\((.+?),.+?,.+?, (.+?),',make_request(url,maxr=1));temp=False
	for post_id in [s[0] for s in items if s[1]=='528657' and not my_dict.has_key(s[0])]:
		my_dict[post_id]='';temp=True
	if not temp:my_dict['room_id']='997745' if room_id=='947935' else '947935'
	my_dict['time_xshare']=timenow;json_rw('xshare.json',my_dict)

def xshare_postks(body,hd,token):
	if myaddon.getSetting('usernameh')=='thaitni':return
	my_dict=json_rw('xshare.json');url='http://www.hdvietnam.com/diendan/post_thanks.php'
	for post_id in my_dict:
		if not my_dict[post_id]:
			response=make_post(url,hd,'do=post_thanks_add&using_ajax=1&p=%s&securitytoken=%s'%(post_id,token))
			my_dict[post_id]='Y';json_rw('xshare.json',my_dict);break
	return body,token,hd['Cookie']

def xshare_trans(sourcefile):
	tempfile = os.path.join(tempfolder, "trans"+os.path.splitext(sourcefile)[1])
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
	print s
	body= make_request(url,hd)
	body=body.replace(',,"en"','').replace('[[[','').replace(']]]','')
	result=''
	for i in body.split('],['):
		research=re.search('"(.+?)","(.+?)"',i)
		if research:result+=research.group(1)+' '
		else:print '%s :not research'%i
	return result.replace('Xshare','xshare').split('xshare')
	
def subscene(name,url,query):
	if query=='subscene.com':
		href = get_input('Hãy nhập link của sub trên subscene.com','http://subscene.com/subtitles/')
		if href is None or href=='' or href=='http://subscene.com/subtitles/':return 'no'
	else:href=url
	if not re.search('\d{5,10}',href):
		if not os.path.basename(href):href=os.path.dirname(href)
		pattern='<a href="(/subtitles/.+?)">\s+<span class=".+?">\s*(.+?)\s+</span>\s+<span>\s+(.+?)\s+</span>'
		body=make_request(href.replace('amp;',''),headers={'Cookie':'LanguageFilter=13,45'})
		subs=re.findall(pattern,body)
		if not subs:
			temp=xsearch('<a href="(.+?)"',xsearch('<h2 class="exact">Exact</h2>(.+?)</ul>',body,1,re.DOTALL),1)
			if temp:
				body=make_request('http://subscene.com'+temp,headers={'Cookie':'LanguageFilter=13,45'})
				subs=re.findall(pattern,body)
		mess(u'Tên phim: %s'%s2u(name).replace('[COLOR green]Subscene[/COLOR]-',''))
		for url,lang,name in sorted(subs,key=lambda l:l[1], reverse=True):
			name='Eng.'+name if '/english/' in url else '[COLOR red]Vie.[/COLOR]'+name
			addirs(name,'http://subscene.com'+url,query='download')
		return ''
	pattern='<a href="(.+?)" rel="nofollow" onclick="DownloadSubtitle.+">'
	downloadlink='http://subscene.com' + xsearch(pattern,make_request(href),1)
	if len(downloadlink)<20:mess(u'Không tìm được maxspeed link sub!')
	else:xshare_resolve(downloadlink)
	return 'ok'

def fptplay(name,url,img,mode,page,query):
	#android Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36"
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
			mess(u'Login thành công','fptplay.net');f=response.cookiestring
			makerequest(joinpath(xsharefolder,'fptplay.cookie'),f,'w')
		else:mess(u'Login không thành công!','fptplay.net');f=''
		#get('https://fptplay.net/user/logout',headers=hd) status=302
		return f
	def colors(name,title):
		name=name.strip()+' '+title.strip()
		if 'Thuyết Minh' in name:name='[COLOR gold]TM[/COLOR] '+name
		elif 'Phụ Đề' in name:name='[COLOR green]PĐ[/COLOR] '+name
		elif 'Trailer' in name:name=name+' [COLOR red](Trailer)[/COLOR]'
		return name
	def getlinklivetv(id,headers='',href=''):
		hd['X-Requested-With']='XMLHttpRequest';hd['Referer']=''
		url='http://fptplay.net/show/getlinklivetv?id=%s&type=newchannel&quality=1&mobile=web'%id
		response=make_post(url,hd,resp='j');body=make_request(response.get('stream'))
		chanels=re.findall('(chunklist.+?)\.m3u8',body)
		if chanels:link=response.get('stream').replace('playlist',chanels[len(chanels)-1])
		else:link=response.get('stream')
		return link
	def get_link(id,episode='1'):
		url='http://fptplay.net/show/getlink?id=%s&type=newchannel&quality=4&episode=%s&mobile=android'
		hd['Accept']="text/html, */*; q=0.01";hd['Content-Type']="application/x-www-form-urlencoded; charset=UTF-8"
		hd['X-Requested-With']='XMLHttpRequest';hd['Referer']='';result=make_post(url%(id,episode),hd,resp='j')
		return result.get('stream','')
	def get_episode(id,page=1):
		url='http://fptplay.net/show/episode?page=%d&film_id=%s';hd['X-Requested-With']='XMLHttpRequest'
		hd['Referer']='';body=make_post(url%(page,id),hd,resp='b')
		pattern='<img src="(.+?)[\?|"].+?id="(.+?)".+?title="(.+?)"'
		items=[(s[0],s[1].replace('episode_',''),s[2],page) for s in re.findall(pattern,body,re.DOTALL)]
		paging=xsearch('onclick="showEpisode\((\d{1,4}),.+?\)"> &rsaquo;&rsaquo; </a>',body,1)
		if paging>str(page):
			title=color['trangtiep']+"Trang tiếp theo - Trang %s/%s[/COLOR]"%(str(page+1),paging)
			items.append((icon["fptplay"],'',title,page+1))
		return items
	def get_items(iTems):#name,id,img
		ids=[s[1] for s in iTems];pattern='<a id="(.+?)" series="(.*?)"';items=list();string=''
		old=dict([s for s in re.findall(pattern,makerequest(joinpath(datapath,'fptplay.xml'))) if s[0] in ids])
		for  title,id,img in iTems:
			if old.has_key(id):series=old.get(id)
			else:
				episode=len(get_episode(id))
				if episode==0:continue
				series='y' if episode>1 else ''
				string+='<a id="%s" series="%s" img="%s">%s</a>\n'%(id,series,img,title)
			items.append((title,id,img,series))
		if string:makerequest(joinpath(datapath,'fptplay.xml'),string,'a')
		return items #title,id,img,series
	def get_title(title):#title,id,img,series
		if 'Thuyết Minh' in title:title='[COLOR gold]TM[/COLOR] '+title
		elif 'Phụ Đề' in title:title='[COLOR green]PĐ[/COLOR] '+title
		elif 'Trailer' in title:title=title+' [COLOR red](Trailer)[/COLOR]'
		return title
	def fpt_addirs(items):#title,id,img,series
		for title,id,img,series in items:
			if series:addir(color['fptplay']+get_title(title)+'[/COLOR]',id,img,img,mode,1,'fptfolder',True)
			else:addir(get_title(title),id,img,img,mode,page,'fptplay')
	
	if not os.path.isfile(joinpath(xsharefolder,'fptplay.cookie')):hd['Cookie']=login()
	else:hd['Cookie']=makerequest(joinpath(xsharefolder,'fptplay.cookie'))
	if query=="fptplay.net":
		body=make_request('http://fptplay.net',hd)
		addir(color['search']+"[B]Search trên fptplay.net[/B][/COLOR]","fptplay.net",icon['fptplay'],'',mode,1,"FPS",True)
		addir(color['fptplay']+'[B]Live TV[/B][/COLOR]','http://fptplay.net/livetv',icon['fptplay'],'',mode,1,'FTV',True)
		for href,title in sets(re.findall('<a href="(.+?)" title="(.+?)" class="category_title">',body)):
			title=color['fptplay']+fpt2s('[B]%s[/B]'%title)+'[/COLOR]'
			addir(title,href,icon["fptplay"],'',mode,1,"FP2",True)
		content=xsearch('<ul class="slide_banner">(.+?)</ul>',body,1,re.DOTALL)
		
		addir('%sFPTplay giới thiệu[/COLOR]'%color['search'],'',icon["fptplay"],'',mode,1,"no")
		items=sets(re.findall('<img src="(.+?)\?.+?" title="(.+?)".*\s.*href="(.+?)"',content))
		fpt_addirs(get_items([(s[1],xsearch('(\w{22,26})',s[2],1),s[0]) for s in items]))
		
		content=xsearch('<span class="pull-left">Phổ biến hiện nay</span>(.+?)</ul>',body,1,re.DOTALL)
		addir('%sPhổ biến hiện nay[/COLOR]'%color['search'],'',icon["fptplay"],'',mode,1,"no")
		items=sets(re.findall('<a href="(.+?)" title="(.+?)".+?data-original="(.+?)\?',content))
		fpt_addirs(get_items([(s[1],xsearch('(\w{22,26})',s[0],1),s[2]) for s in items]))
		
		content=xsearch('<span class="pull-left">Đặc sắc</span>(.+?)</ul>',body,1,re.DOTALL)
		addir('%sĐặc sắc[/COLOR]'%color['search'],'',icon["fptplay"],'',mode,1,"no")
		items=sets(re.findall('<a href="(.+?)" title="(.+?)".+?data-original="(.+?)\?',content))
		fpt_addirs(get_items([(s[1],xsearch('(\w{22,26})',s[0],1),s[2]) for s in items]))
	elif query=="FTV":
		body=make_request(url,hd);i=1
		content=xsearch('Begin kenh truyen hinh(.+?)END Tong Hop',body,1,re.DOTALL)
		pattern='<a class=".+?" title="(.+?)".+?href="http://fptplay.net/livetv/(.+?)"(.+?)original="(.+?)\?.+?"'
		for name,href,lock,img in re.findall(pattern,content,re.DOTALL):
			j='00%d '%i if i<10 else '0%d '%i if i<100 else '%d '%i;name=j+fpt2s(name);i+=1
			if '"lock"' in lock:name=name+' ([COLOR red]Có phí[/COLOR])'
			addir(name,href,img,'',mode,1,"PTV")
	elif query=="PTV":
		href=getlinklivetv(url,hd)
		if 'm3u8' in href:xbmcsetResolvedUrl(href)
		elif href=='login':
			href=getlinklivetv(url,hd)
			if 'm3u8' in href:xbmcsetResolvedUrl(href)
			else:hd['Cookie']=login();href=getlinklivetv(url,hd)
			if 'm3u8' in href:print href;xbmcsetResolvedUrl(href)
			else:mess(u'%s'%href,'Fptplay LiveTV')
		else:mess(u'%s'%href,'Fptplay LiveTV')
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
		body=make_request(url,hd)
		for href,title in sets(re.findall('<a href="(.+?)" title="(.+?)" class="category_title">',body)):
			title=color['fptplay']+fpt2s('[B]%s[/B]'%title)+'[/COLOR]'
			addir(title,href,icon["fptplay"],'',mode,1,"FP3",True)
		addir('%s%s Nổi Bật[/COLOR]'%(color['search'],remove_tag(name)),url,icon["fptplay"],'',mode,1,"no")
		items=sets(re.findall('<li>.*?<img src="(.+?)\?.+?" title="(.+?)".+?href="(.+?)".+?</li>',body,re.DOTALL))
		fpt_addirs(get_items([(s[1],xsearch('(\w{22,26})',s[2],1),s[0]) for s in items]))
	elif query=="FP3":
		id=xsearch('(\w{22,26})',url,1)
		href='http://fptplay.net/show/more?type=new&stucture_id=%s&page=%d&keyword=undefined'%(id,page)
		items=sets(re.findall('<a href=".+-(\w+)\.html".+?src="(.+?)\?.+?alt="(.+?)"',make_post(href,resp='b')))
		fpt_addirs(get_items([(s[2],xsearch('(\w{22,26})',s[0],1),s[1]) for s in items]))
		if len(items)==36:
			name='%s%s[/COLOR]'%(color['search'],remove_tag(name.replace(' - xem thêm',''))+' - xem thêm')
			addir(name,url,icon["fptplay"],'',mode,page+1,"FP3",True)
	elif query=="fptfolder":
		for img,episode,title,page_ in get_episode(url,page):
			try:episode=int(episode)
			except:episode=1
			if page_==page:addir(title,url,img,img,mode,episode,'fptplayinfolder')
			else:addir(title,url,img,'',mode,page_,'fptfolder',True)
	elif 'fptplay' in query:
		if query=='fptplay' and len(get_episode(url))>1:
			content=makerequest(joinpath(datapath,'fptplay.xml'))
			string=xsearch('id="%s" series=""'%url,content,0)
			if string:
				makerequest(joinpath(datapath,'fptplay.xml'),content.replace(string,'id="%s" series="y"'%url),'w')
				xbmc.executebuiltin("Container.Refresh")
		episode=xsearch('Tập (\d{1,4})',name,1)
		if not episode:episode=str(page)
		link=get_link(url,episode)
		if link:
			if 'playlist.m3u8' in link:link=link.replace('playlist','chunklist')
			#a=make_request(link,hd,resp='o');b=re.findall('(chunklist_.+?)\n',a.body);c=b[len(b)-1]
			#d=os.path.dirname(link)+'/'+c
			#e=makerequest(joinpath(xsharefolder,'temp.m3u8'),make_request(d,hd),'w')
			xbmcsetResolvedUrl(link)
		else:return 'no'
	return

def xsearch(pattern,string,group,flags=0):
	research=re.search(pattern,string,flags)
	if research:
		try:result=research.group(group)
		except:result=''
	else:result=''
	return result

def megabox(name,url,img,fanart,mode,page,query):
	homepage='http://phim.megabox.vn/';ico=icon['megabox']
	cat={1:'Phim lẻ',2:'Phim bộ',3:'Show',4:'Clip'}
	gen={1:'Hành động',2:'Phiêu lưu',3:'Ma kinh dị',4:'Tình cảm',5:'Hoạt hình',6:'Võ thuật',7:'Hài',8:'Tâm lý',9:'Kiếm hiệp',10:'Sử thi',11:'',12:'',13:'Hình sự',14:'',15:'Âm nhạc',16:'Khoa học',17:'Tài liệu',18:'Gia đình',21:'Chiến tranh',22:'Thể thao',25:'Độc-Lạ',27:'Khoa học viễn tưởng',28:'Ẩm thực',29:'Thời trang',30:'Điện ảnh',31:'Thiếu nhi',32:'Giáo dục',33:'TV-Show',34:'Live Show',36:'Công nghệ',37:'Khám phá thế giới',38:'Động vật',39:'Shock'}
	country={1:'Âu-Mỹ',2:'Hàn Quốc',3:'Hồng Kông',4:'Trung Quốc',5:'Nhật Bản',6:'Thái Lan',7:'Quốc Gia khác',8:'Mỹ',9:'Pháp',11:'Việt Nam',12:'Ấn Độ',13:'Philippines'}#get(url,headers=hd,maxr=2)
	def namecolor(label):return color['megabox']+label+'[/COLOR]'
	def get_id(url):return xsearch('-(\d{1,6})\.html',url,1)
	def duration(string):return xsearch('Thời lượng:<.+?> (.+?)</li>',string,1)
	def countview(string,tag='span'):return xsearch('class=.count-view.><%s></%s> (.+?)</span>'%(tag,tag),string,1)
	def thuyetminh(string):return color['subscene']+'TM[/COLOR] ' if xsearch('class=.ico-sub.',string,0) or string=='TM' else ''
	def phim18(string):return '[COLOR red][B]M+[/B][/COLOR] ' if xsearch('class=.ico-rating.',string,0) or string=='M+' else ''
	def episode(string):return xsearch('class=.esp.><i>(.+?)</span>',string,1).replace('</i>','')
	def update_dict(dict):
		body=make_request(homepage,headers=hd)
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
		return json_rw('megabox.json',dict)
	def get_detail(urls,dict):
		mess('Database updating ...','megabox.vn')
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
	def json_rw1(dicts={}):
		if dicts:makerequest(joinpath(datapath,'megabox.json'),json.dumps(dicts),'w')
		else:
			try:dicts=json.loads(makerequest(joinpath(datapath,'megabox.json')))
			except:dicts={}
		return dicts
	def load_urls(urls):
		dict=json_rw('megabox.json');urls_old=[];urls_new=[];ids=[];update=False
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
			if len(dict[id])<8:dict.pop(id);continue
			img=dict[id][2];fanart=dict[id][3]
			if dict[id][0]=='y':
				epi=xsearch('(.+?)\W(.*?)\Z',dict[id][5],1);eps=xsearch('(.+?)\W(.*?)\Z',dict[id][5],2)
				title=namecolor(dict[id][1])+color['subscene'];query='1episode'+eps;isFolder=True
				title=title+' - %s views:%s[/COLOR]'%(dict[id][5],dict[id][4])
			else:
				title=dict[id][1]+color['subscene']+' - (%s - views:%s)[/COLOR]'%(dict[id][5],dict[id][4].strip())
				query='mgbplay';isFolder=False
			addir(tm+title,url,img,fanart,mode,1,query,isFolder=isFolder)
		if urls_new:endxbmc();json_rw('megabox.json',get_detail(urls_old,dict));mess('Database updated','megabox.vn')
	def put_items(items,tag='span'):#class='count-view'><span></span> 551</span>
		dict=json_rw('megabox.json');cl=color['subscene']
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
		mess('Database updating ...','megabox.vn')
		for href in href_new:
			id=get_id(href);body=sub_body(make_request(href,maxr=3),'begin primary','end primary')
			items=re.findall('alt=\'(.+?)\' src="(.+?)"',body)
			if len(items)<2:continue
			series,name,img,fanart,views,esp,tm,p18=dict[id];fanart=items[0][1];img=items[1][1]
			dict[id]=(series,name,img,fanart,views,esp,tm,p18)
		json_rw('megabox.json',dict);mess('Database updated','megabox.vn')

	def homehtml(update=False):
		if update:
			body=make_request(homepage)
			if body:makerequest(joinpath(xsharefolder,'megabox.html'),body,'w')
		else:
			body=makerequest(joinpath(xsharefolder,'megabox.html'))
			if not body:return homehtml(True)
		return body

	if query=='MGB1':
		label=labelsearch("Search trên megabox.vn")
		addir_info(label,homepage,ico,'',mode,1,'makeitemsearch',True)
		body=homehtml()
		for href,label in re.findall('<li><a href="(.+?)" title="">(.+?)</a></li>',body):
			addir_info(namecolor(label),homepage+href,ico,'',mode,1,'mainmenu',True)
		add_sep_item('Nội dung chi tiết trang chủ')
		for label in re.findall('<h2 class="H2title">(.+?)</h2>',body):
			addir_info(namecolor(remove_tag(label)),homepage,ico,'',mode,1,'mainpage',True)
		if checkupdate('megabox.html',1,xsharefolder):endxbmc();body=homehtml(True);xbmc.executebuiltin("Container.Update")
	elif query=='makeitemsearch':search_get_items('megabox.vn',mode)
	elif query=='getstringsearch' or query=='dosearch':
		if query=='dosearch':string=name
		else:
			string=search_input_string('megabox.vn')
			if not string:return 'no'
		body=make_post(homepage+'search/autocomplete/?keyword=%s'%urllib.quote(string),resp='b')
		pattern='<a href="(http://phim.megabox.vn/.+?)".+?alt=\'(.+?)\' src="(.+?)"'
		for href,label,img in re.findall(pattern,body,re.DOTALL):
			addir_info(remove_tag(label),href,img,'',mode,1,'abc')
	elif query=='mainpage':
		body=homehtml()
		if name==namecolor('Megabox giới thiệu'):
			content=xsearch('<ul class="hotFilmSlider">(.+?)</ul>',body,1,re.DOTALL)
			pattern="<a href='(http://phim.megabox.vn/.+?)'.+?src='(.+?)' alt='(.+?)'"
			for href,img,label in re.findall(pattern,content):
				addir_info(remove_tag(label),href,img,img,mode,1,'abc')
		elif name==namecolor('Top 10 phim trong ngày'):
			content=xsearch('<ul class="list topSlider">(.+?)end topFilm',body,1,re.DOTALL)
			pattern='href="(.+?)".+?<h3 class=\'H3title\'>(.+?)</h3>.+?src="(.+?)"'
			for href,label,img in re.findall(pattern,content,re.DOTALL):
				addir_info(remove_tag(label),href,img,'',mode,1,'abc')
		elif name==namecolor('Phim Lẻ Mới Nhất'):print 'a'
		
	elif query=='MGB':
		dict=json_rw('megabox.json')
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
				addir(title,homepage,icon['megabox'],'',mode,1,'xemnhieu',True)
		if checkupdate('megabox.json',8):dict=update_dict(dict)
	elif query=='megabox.vn':make_mySearch('',url,'','',mode,'get')
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
	elif query=='mainmenu' and url in ('phim-letl','phim-leqg','phim-botl','phim-boqg','showtl','showqg','cliptl'):
		dict=json_rw('megabox.json')
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
		body=sub_body(make_request(homepage+url,maxr=3),'begin primary','end primary')
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
		hd['Cookie']=body.cookiestring;href='http://phim.megabox.vn/content/get_link_video_lab'
		maxspeedlink=make_post(href,{'Referer':url},data={"link":"%s"%link},resp='j')
		if maxspeedlink.get('link'):
			name=re.sub(' \[COLOR.+?/COLOR\]','',name)
			xbmcsetResolvedUrl(maxspeedlink.get('link')+'|'+urllib.urlencode(hd),name+'Maxlink')
		else:mess('Get maxspeed link thất bại!','megabox.vn')
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
	elif 'Megabox giới thiệu' in name:dict=json_rw('megabox.json');load_urls(dict['gioithieu'])
	elif 'Top 10 phim trong ngày' in name:dict=json_rw('megabox.json');load_urls(dict['top10'])
	elif 'Phim sắp chiếu' in name:dict=json_rw('megabox.json');load_urls(dict['sapchieu'])
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
		href='http://phim.megabox.vn/home/getcontent/?cat=%s&genre=%s&country=%s';dict=json_rw('megabox.json')
		for genre,country,gen_name in dict['subCate%d'%cat[url][1]]:
			#gen_name=gen_name.encode('utf-8') if type(gen_name)==unicode else s2u(gen_name)
			gen_name=u2s(gen_name)
			if gen_name==gen:href=href%(cat[url][1],genre,country);continue
			title=color['xshare']+re.sub('\[.?COLOR.*?\]','',name);
			title=re.sub('%s.+\Z'%cat[url][0],cat[url][0]+' %s Mới Nhất[/COLOR]'%gen_name,title)
			addir(title,url+'/'+gen_name,icon['megabox'],'',mode,1,query,True)
		patt="<a class.+?href='(.+?)'.+?title.>(.+?)</h3>(.+?)<img.+?src='(.+?)'(.+?)</a>.+?<a.+?a>(.+?)</div></div>"
		put_items(re.findall(patt,make_request(href,hd),re.DOTALL),'i');print href
		cat={'phim-le':'Phim lẻ','phim-bo':'Phim bộ','show':'Show','clip':'Clip'}
		name=color['trangtiep']+'%s Xem Thêm...[/COLOR]'%cat[url]
		addir(name,url,icon['megabox'],'',mode,1,'mainmenu',True)
	return ''

def dangcaphd(name,url,img,mode,page,query):
	homepage='http://dangcaphd.com/'
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
			if makerequest(subfullpathfilename,make_request(url),'wb'):sub=subfullpathfilename
		return sub
	def login(headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}):
		url="http://dangcaphd.com/login.html";u=myaddon.getSetting('mail_dchd');p=myaddon.getSetting('pass_dchd')
		response=make_post(url,headers,urllib.urlencode({"_submit":"true","email":u,"password": p}))
		try:
			if not response.json['login']:f=response.cookiestring;m='1';headers['Cookie']=f
			else:f='';m='2'
		except:f='';m='3'
		if m=='1' and re.search('Hết hạn.*</b></a></li>',make_request('http://dangcaphd.com/',headers=headers)):
			mess(u'Tài khoản của bạn đã hết hạn sử dụng!','dangcaphd.com')
			href='https://www.fshare.vn/folder/NCERC36BSSCY'#acc này do bạn vinhdo tặng
			hd=xsearch('<title>.*xx(.+?)xx.*</title>',make_request(href),1).split('=')
			data=urllib.urlencode({"_submit":"true","email":'%s@%s'%(hd[0],hd[1]),"password":hd[2]})
			resp=make_post(url,data=data)
			try:f=resp.cookiestring if not resp.json['login'] else ''
			except:f=''
		elif m=='1':mess(u'Login thành công','dangcaphd.com')
		elif m=='2':mess(re.sub('<..?>','',response.json['login']),'dangcaphd.com')
		elif m=='3':mess(u'Login không thành công!','dangcaphd.com')
		return f
		
	if query=='DHD':
		body=make_request(homepage)
		name=color['search']+"Search trên dangcaphd.com[/COLOR]"
		addir(name,"dangcaphd.com/movie/search.html",icon['dangcaphd'],mode=mode,query="DHS",isFolder=True)
		name=color['dangcaphd']+'Trang chủ dangcaphd.com[/COLOR]'
		addir(name,homepage,icon['dangcaphd'],mode=mode,query='DC0',isFolder=True)
		for name in re.findall('</i>(.+?)<span class="caret">',body):
			addir(color['dangcaphd']+name.strip()+'[/COLOR]',homepage,icon['dangcaphd'],mode=mode,query='DC1',isFolder=True)
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
		body=make_request(homepage)
		for href,name in re.findall('<a class="title" href="(.+?)"><i class="fa fa-film "></i>(.+?)</a>',body):
			addir(color['dangcaphd']+name.strip()+'[/COLOR]',href,icon['dangcaphd'],mode=mode,query='DC2',isFolder=True)
	elif query=='DC1':
		body=make_request(homepage)
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
				name=name.strip()+'[/COLOR]'+' - ('+xsearch('<div class="sale">(.+?)</div>',other,1)+')'
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
		if subtitle:
			xbmcsetResolvedUrl(url,urllib.unquote(os.path.splitext(os.path.basename(subtitle))[0]))
			mess(u'Phụ đề của dangcaphd.com','dangcaphd.com')
		else:xbmcsetResolvedUrl(url)

def vuahd(name,url,img,fanart,mode,page,query):
	col='[COLOR tomato]';ico=os.path.join(iconpath,'vuahd.png');urlhome='http://vuahd.tv/'
	def namecolor(name):return '%s%s[/COLOR]'%(col,name)
	def vuahd_login(headers=''):
		if not headers:
			url='http://vuahd.tv/accounts/login'
			response=make_request(url,resp='o');hd['Cookie']=response.cookiestring
			t=xsearch("name='csrfmiddlewaretoken' value='(.+?)'",response.body,1)
			u=myaddon.getSetting('usernamev');p=myaddon.getSetting('passwordv')
			data=urllib.urlencode({'csrfmiddlewaretoken':t,'username':u,'password':p})
			response=make_post(url,hd,data)
			if response.status==302:
				f=response.cookiestring;hd['Cookie']=f
				if re.search('<b>Free</b></span>',make_request('http://vuahd.tv/accounts/profile/',headers=hd)):
					mess(u'Tài khoản free chỉ xem được một số phim.','vuahd.tv')
				else:mess(u'Login thành công','vuahd.tv')
				makerequest(joinpath(xsharefolder,'vuahd.cookie'),f,'w')
			else:mess(u'Login không thành công!','vuahd.tv');f=''
			return f
		else:make_request('http://vuahd.tv/accounts/logout',headers=headers)
	def readpage(url,items=list()):
		hd['Cookie']=makerequest(joinpath(xsharefolder,'vuahd.cookie'))
		print url
		for detail in re.findall('<div class="item-film">(.+?)</p>',make_request(url,hd),re.DOTALL):
			name=xsearch('title="(.+?)"',detail,1);href=urlhome+xsearch('href="(.+?)"',detail,1)
			img=urlhome+xsearch('src="(.+?)"',detail,1);isFolder='/tv-series/' in href
			items.append((name,href,img,isFolder))
		return items
	def vuahd_addir(items):#title,href,img,isFolder
		for title,href,img,isFolder in items:
			if isFolder:title=namecolor(title);query='vuahdfolder'
			else:query='vuahdplay'
			addir_info(title,href,img,'',mode,1,query,isFolder)
	
	if query=='vuahd.tv':
		body=makerequest(joinpath(xsharefolder,'vuahd.html'))
		name=color['search']+"Search trên vuahd.tv[/COLOR]"
		addir_info(namecolor(name),'',icon['isearch'],'',mode,1,'vuahdsearch',True)
		for title in re.findall(' <li class="active has-child"><a href="/" title=".+?">(.+?)</a>',body):
			addir_info(namecolor(title),'',ico,'',mode,1,'submenu',True)
		vuahd_addir(readpage('http://vuahd.tv/movies/all-items?page=1'))
		name='%sTất cả phim: trang 2[/COLOR]'%color['trangtiep']
		addir_info(name,'http://vuahd.tv/movies/all-items?page=',ico,'',mode,1,'vuahdpage',True)
		if checkupdate('vuahd.html',8,xsharefolder):
			endxbmc();body=make_request('http://vuahd.tv/',hd)
			if len(body)==0:hd['Cookie']=vuahd_login();body=make_request('http://vuahd.tv/',hd)
			makerequest(joinpath(xsharefolder,'vuahd.html'),body,'w');print len(body)
	elif query=='submenu':
		body=makerequest(joinpath(xsharefolder,'vuahd.html'))
		name=re.sub('\[/?COLOR.*?\]','',name)
		detail=xsearch(' <li[^/]+?><a href="/" title="[^/]+?">%s</a>(.+?)</ul>'%name,body,1,re.DOTALL)
		for href,title in re.findall('<a href="(.+?)".*?>(.+?)</a>',detail):
			addir_info(namecolor(title),urlhome+href,ico,'',mode,1,'vuahdpage',True)
		if 'Thể loại' in name:
			for href,title in [('51','Phim Bộ Trung Quốc'),('52','Phim Bộ Hàn Quốc'),('53','Phim Bộ Bộ Anh-Mỹ'),('56','Phim Bộ Khác')]:
				addir_info(namecolor(title),'%s/movies/tv-series/%s/'%(urlhome,href),ico,'',mode,1,'vuahdpage',True)
	elif query=='vuahdpage':
		name=re.sub('\[/?COLOR.*?\]','',name).split(':')[0]
		if 'page=' not in url:
			if 'trailers' in url:url='http://vuahd.tv/movies/all-trailers?page='
			elif url=='http://vuahd.tv/movies/':url='http://vuahd.tv/movies/all-items?page='
			elif url=='http://vuahd.tv//movies/':url='http://vuahd.tv/movies/all-items?page='
			elif '/tv-series/' in url:url=url.replace('tv-series','tv-series-items')+'?page='
			else:url=url+'items?page='
		items=readpage(url+str(page));vuahd_addir(items)
		if items:
			name='%s%s: trang %d[/COLOR]'%(color['trangtiep'],name,page+1)
			addir_info(name,url,ico,'',mode,page+1,'vuahdpage',True)
	elif query=='vuahdfolder':
		hd['Cookie']=makerequest(joinpath(xsharefolder,'vuahd.cookie'));body=make_request(url,hd)
		head=xsearch('\((.+?)\(',xsearch('<header(.+?)header>',body,1,re.DOTALL),1)
		if head:head=' - '+head.strip()
		items=sets(re.findall('<a href="(.+?)" class="btn-1">Xem (.+?)</a>',body))
		items=[s for s in items if 'title=' not in s[0]]
		for href,label in items:
			title=label.strip()+'/%s - '%xsearch('\(\d{1,4}/(\d{1,4})\)',name,1)+remove_tag(name)+head
			addir_info(title,urlhome+href,img,fanart,mode,page,'vuahdplay')
	elif query=='vuahdplay':#xhr.setRequestHeader("X-CSRFToken", csrftoken);
		hd['Cookie']=vuahd_login();body=make_request(url+('/watch' if '/watch' not in url else ''),hd)
		href=xsearch('<source src = "(.+?)"',body,1)
		if not href:href=xsearch('file: "(.+?)"',body,1)
		if href:xbmcsetResolvedUrl(urlhome+href)#vuahd_login(hd)
		else:mess(u'Không get được maxspeed link!','vuahd.tv')

def pubvn(name,url,img,mode,page,query):
	color['pubvn']='[COLOR deepskyblue]';icon['pubvn']=os.path.join(iconpath,'pubvn.png');homepage='http://pubvn.tv/'
	def login():
		u=myaddon.getSetting('usernamep');p=myaddon.getSetting('passwordp')
		data='txtusername=%s&txtpass=%s&remeber_me1=0&sercurity_code='%(u,p)
		response=make_post(homepage+'phim/aj/action_login.php',data=data)
		if 'pub_userid=deleted' in response.cookiestring:mess(u'Login không thành công!','pub.vn')
		else:mess(u'Login thành công','pub.vn')
		return {'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0','Cookie':response.cookiestring}
	def getiMovEps(url):
		hd=login();pattern='<input id="thread_id" type="hidden" value="(.+?)"/>'
		thread_id=xsearch(pattern,make_request(url),1);pattern='id="player" src="(.+?)"'
		iMovEps=xsearch(pattern,make_request(homepage+'/bar/dodamde/'+thread_id,headers=hd),1)
		return homepage+iMovEps,hd
	def pubvn_play(url):
		if '=' not in url:url,hd=getiMovEps(url)
		else:hd=login()
		body=make_request(url+'&server=3',headers=hd)
		id=re.search('iMov=(\d{4,6})&iEps=(\d{5,7})',url);mov_id=id.group(1);eps_id=id.group(2)
		log_id=xsearch('log_id : (\d{5,7})',body,1)
		pub_id=xsearch('pub_id : "(.+?)"',body,1)
		lte_id=xsearch('lte_id : (\w{6,10})',body,1)
		sercur=xsearch('sercur : (\w{6,10})',body,1)
		hash=xsearch("hash : '(\w{8,10})'",body,1)
		dlink=xsearch("file: '(.+?)'",body,1)
		data='action=update_last_watched&user_id=%s&mov_id=%s&eps_id=%s&time=93.78&per=1&hash=%s'
		data=data%(log_id,mov_id,eps_id,hash)
		make_post(homepage+'movie/vn/vasi_blahblah.php',hd,data)
		make_request(homepage+'phim/logout.php',headers=hd);xbmcsetResolvedUrl(dlink+'?start=0')
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
			eps=xsearch('<p>(\d{1,3}/\d{1,3})</p>',eps.strip(),1).split('/')[0]>'1'
			if eps:items.append(('%s%s[/COLOR]'%(color['pubvn'],title),homepage+href,img,'folder'))
			else:items.append((title,homepage+href,img,'play'))
		return items
	def pubvn_search(string,page=1):
		data='boxphim=Filter&txtsearch=%s&page=%d'%(urllib.quote_plus(string),page)
		body=make_post(homepage+'phim/aj/advancesearch.php',data=data).body
		for name,href,img,type in pubvn_page(body):
			addir(name,href,img,fanart,mode,page,query=type,isFolder=(type=='folder'))
		trangcuoi=xsearch('class="vpage(\d{1,4})".{,5}>Cuối</a></li>',body,1).strip()
		if trangcuoi and int(trangcuoi)>page:
			name=color['trangtiep']+'Trang tiếp theo: trang %s/%s[/COLOR]'%(str(page+1),trangcuoi)
			addir(name,url,img,fanart,mode,page=page+1,query=string,isFolder=True)
		return ''
	def pubvn_make_txt(items,temps=[]):
		txtfile=joinpath(data_path,'pubvn'+datetime.date.today().strftime("%d")+'.txt')
		for href,name,img in items:
			body=make_request(homepage+href)
			thread_id=xsearch('/bar/threads/(\d{3,6})',body,1)
			eps=xsearch('<p>(\d{1,3}/\d{1,3})</p>',body,1);page=0
			if eps.split('/')[0]>'1':page=1;name=color['pubvn']+name+'[/COLOR]'
			temps.append((name,homepage+'/bar/dodamde/'+thread_id,img,page))
		if temps:delete_files(data_path,mark='pubvn');makerequest(txtfile,str(temps),'w')
	if query=='pubvn.tv':
		name=color['search']+"Search trên pubvn.tv (pub.vn)[/COLOR]"
		addir(name,url,icon['icon'],mode=mode,query='search',isFolder=True)
		body=make_request(homepage+'phim/home.php')
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
		body=make_request(homepage+'phim/home.php')
		blmenu_childs=re.findall('<li><a menuid = "(.+?)" tabid="(.+?)">(.+?)</a></li>',body)
		for menuid,tabid,name in blmenu_childs:
			if int(tabid)==page:
				addir('%s%s[/COLOR]'%(color['pubvn'],name),'blmenu_child',img,fanart,mode,page,query=menuid,isFolder=True)
	elif url=='blmenu_child':
		data='tabid=%s&menuid=%s'%(str(page),query)
		body=make_post(homepage+'phim/aj/aj_top.php',data=data).body
		pattern='<div class="film_poster">(.+?)<a href="(.+?)" class="tooltip1" title="(.+?)\|.{,2000}src="(.+?)" (.{,500}End class = film_poster)'
		for s1,href,title,img,s2 in re.findall(pattern,body,re.DOTALL):
			s1=xsearch('<p>(\d{1,3}/\d{1,3})</p>',s1.strip(),1).split('/')[0]>'1'
			s2=xsearch('<p>(\d{1,3}/\d{1,3})</p>',s2.strip(),1).split('/')[0]>'1'
			if s1 or s2:addir('%s%s[/COLOR]'%(color['pubvn'],title),homepage+href,img,fanart,mode,page,query='folder',isFolder=True)
			else:addir(title,homepage+href,img,fanart,mode,page,query='play')
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
		else:mess(u'Đang cập nhật dữ liệu - chọn lại sau 30 giây nữa nhé...')
	elif query=='dodamde':
		iMovEps=xsearch('id="player" src="(.+?)"',make_request(url),1)
		if page==0:pubvn_play(homepage+iMovEps)
		else:
			for eps,href in pubvn_Eps(homepage+iMovEps):
				addir(eps+' - '+re.sub('\[.?COLOR.{,15}\]','',name),href,img,fanart,mode,page,query='play')
	elif url=='Home_Main':
		url=homepage+'phim/aj/';data='cat_id=%s&type=%s&page=%s'
		if 'Phim lẻ' in name:url+='aj_phimle.php';data='cat_id=%s&page=%s'%(query,str(page))
		else:url+='aj_series.php';data=data%(query.split('-')[0],query.split('-')[1],str(page))
		body=make_post(url,data=data).body
		for title,href,img,type in pubvn_page(body):
			addir(title,href,img,fanart,mode,page,query=type,isFolder=(type=='folder'))
		trangcuoi=xsearch('class="catpage(\d{1,4})".{,5}>Cuối</a></li>',body,1).strip()
		if trangcuoi and int(trangcuoi)>page:
			name=re.sub('\[.?COLOR.{,12}\]','',name).split('*')[0].strip()
			name=color['trangtiep']+'%s * Trang tiếp theo: trang %s/%s[/COLOR]'%(name,str(page+1),trangcuoi)
			addir(name,'Home_Main',img,fanart,mode,page=page+1,query=query,isFolder=True)
	elif query=='play':pubvn_play(url)

def hdviet(name,url,img,mode,page,query):
	color['hdviet']='[COLOR darkorange]';icon['hdviet']=os.path.join(iconpath,'hdviet.png')
	homepage='http://movies.hdviet.com/'
	if os.path.isfile(joinpath(datapath,'hdviet.cookie')):os.remove(joinpath(datapath,'hdviet.cookie'))
	direct_link='https://api-v2.hdviet.com/movie/play?accesstokenkey=%s&movieid=%s'
	def namecolor(name):return '%s%s[/COLOR]'%(color['hdviet'],name)
	def getcookie():
		u=myaddon.getSetting('userhdviet');p=myaddon.getSetting('passhdviet')
		import hashlib;data=urllib.urlencode({'email':u,'password':hashlib.md5(p).hexdigest()})
		response=make_post('http://movies.hdviet.com/dang-nhap.html',hd,data)
		return response.cookiestring
	def login_hdviet():
		u=myaddon.getSetting('userhdviet');p=myaddon.getSetting('passhdviet')
		'''
		url='https://id.hdviet.com/authentication/login'
		response=make_post(url,data='email=%s&password=%s'%(u,p),resp='j')
		if response and response.get('error')==0:
			response=response.get('data')
			mess(u'Login thành công','hdviet.com')
			json_rw('hdviet.cookie',response)
		elif response and response.get('error')==27:
			mess(u'Acc bị khóa tạm thời. Vào web để login nhé!','hdviet.com');response=dict()
		elif response and response.get('error') in (25,22):
			mess(response.get('message'),'hdviet.com');response=dict()
		else:
		'''
		import hashlib;data=urllib.urlencode({'email':u,'password':hashlib.md5(p).hexdigest()})
		response=make_post('http://movies.hdviet.com/dang-nhap.html',hd,data)
		try:resp=response.json
		except:resp={u'r': u'Lỗi đăng nhập hdviet.com', u'e': 3}
		if resp.get('e')==0:
			mess(resp.get('r'),'hdviet.com');hd['Cookie']=response.cookiestring
			response=make_request('http://movies.hdviet.com/dieu-khoan-su-dung.html',headers=hd)
			import base64;token=base64.b64decode(xsearch('<a class="userinfo".+?token=(.+?)"',response,1))
			response={'Cookie':hd['Cookie'],'access_token':token};json_rw('hdviet.cookie',response)
		else:response=dict();mess(resp.get('r'),'hdviet.com')
		url='http://movies.hdviet.com/dang-xuat.html?accesstokenkey=%s'
		make_post(url%response.get('access_token')).body
		return response
	def getResolvedUrl(id_film,loop=0):#Phim le/phim chieu/ke doi dau thien ac
		def getlinkhdviet(token,id_film):
			id_film=id_film.replace('_e','&ep=');print direct_link%(token,id_film)
			response=make_request(direct_link%(token,id_film),resp='j')
			try:links=response['r'];link=response['r']['LinkPlay']
			except:links=dict()
			return links
		data=json_rw('hdviet.cookie')
		links=getlinkhdviet(data.get('access_token'),id_film)
		if not links:return '',''
		link=links.get('LinkPlay');print 'bbb   33333',links
		if '0000000000000000000000' in link:
			data=login_hdviet();links=getlinkhdviet(data.get('access_token'),id_film);link=links.get('LinkPlay')
		if links:
			#max_resolution='_1920_' if myaddon.getSetting('hdvietresolution')=='1080' else '_1280_'
			#resolutions=['_1920_','_1885_','_1876_','_1866_','_1792_','_1280_','_1024_','_800_','_640_','_480_']
			if '_e' in id_film:link=re.sub('%s_e\d{1,3}_'%id_film.split('_')[0],'%s_'%id_film,link)
			#href=link
			#for resolution in resolutions:
			#	if resolution in link:link=link.replace(resolution,max_resolution);break
			#link=re.findall('(.+m3u8)',make_request(link))
			#if not link:link=re.findall('(.+m3u8)',make_request(href))
			#if link:link=link[len(link)-1]
		if  not link and loop==0:
			response=make_request(link,resp='o')
			if response and 'filename' not in response.headers.get('content-disposition',''):
				data=login_hdviet();return getResolvedUrl(id_film,1)
		if not link:return '',''

		audio=links.get('AudioExt',list());audioindex=-1;linksub=''
		if len(audio)>1:
			audio_choice=myaddon.getSetting('hdvietaudio')
			if audio_choice=='Hỏi khi xem':
				title=u'[COLOR green]Chọn Audio[/COLOR]';line1= u'[COLOR yellow]Vui lòng chọn Audio[/COLOR]'
				audioindex=mess_yesno(title,line1,'',audio[0].get("Label",'0'),audio[1].get("Label",'1'))
			else:audioindex=0 if u2s(audio[0].get("Label")) in audio_choice else 1
			if 'Thuyết' not in u2s(audio[audioindex].get("Label")):linksub='yes'#bật cờ download sub
			try:link=link+'?audioindex=%d'%(int(audio[audioindex].get("Index",'0'))-1)
			except:pass
		elif u2s(audio[0].get("Label"))=='Thuyết Minh':audioindex=0
		if audioindex<0 or linksub:
			for source in ['Subtitle','SubtitleExt','SubtitleExtSe']:
				try:linksub=links[source]['VIE']['Source']
				except:linksub=''
				if linksub:break
		print link,linksub
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
		href='http://movies.hdviet.com/phim-yeu-thich.html'
		addir(color['search']+'Phim yêu thích của tôi trên hdviet[/COLOR]',href,icon['icon'],fanart,mode,1,'yeu-thich',True)
		if checkupdate('hdviet.html',8):body=makerequest(joinpath(datapath,'hdviet.html'),make_request(homepage),'w')
		else:body=makerequest(joinpath(datapath,'hdviet.html'))
		items=re.findall('"mainitem" menuid="(.+?)" href="(.+?)" title=".+?">(.+?)</a>',body)
		for id,href,name in items:
			addir(namecolor(name),homepage,icon['hdviet'],fanart,mode,1,id,True)
		addir(namecolor('Thể loại phim'),'the-loai',icon['icon'],fanart,mode,1,'the-loai-phim',True)
		items=re.findall('<div class="h2-ttl cf">.+?<a href="(.+?)" title=".+?" >(.+?)</a>.+?</div>(.+?)</ul>',body,re.DOTALL)
		for href,name,subbody in items:
			addir('-----%s%s-----[/COLOR]'%(color['search'],name),href,icon['hdviet'],fanart,mode,page,'1',True)
			additems(subbody)
	elif query=='search':make_mySearch('','hdviet.com','','',mode,'get')
	elif query=="INP":hdviet_search(make_mySearch('',url,'','','','Input'))
	elif url=='hdviet.com':page=1 if 'Trang tiếp theo' not in name else page;hdviet_search(query)
	elif query=='the-loai-phim':
		for href,name in re.findall('<p><a href="(.+?)" title=".+?">(.+?)</a></p>',makerequest(joinpath(datapath,'hdviet.html'))):
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,'theloai',True)
	elif query=='3' and url==homepage:#Phim lẻ
		items=re.findall('<a href="(.+?)" .?menuid="(.+?)" .?title=".+?" >(.+?)</a>',makerequest(joinpath(datapath,'hdviet.html')))
		for href,id,name in items:
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,id,True)
	elif query=='10' and url==homepage:#Phim bộ
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
		link,sub=getResolvedUrl(url)#;print link,sub
		if not link:mess(u'Get link thất bại!','hdviet.com')
		else:
			if sub:
				mess(u'Phụ đề của HDViet.com','hdviet.com');xshare_resolve(sub)
				sub=urllib.unquote(os.path.splitext(os.path.basename(sub))[0])
			xbmcsetResolvedUrl(link,sub)
	elif query=='Themmucyeuthich':
		hd['Cookie']=getcookie()
		body=make_post('http://movies.hdviet.com/them-phim-yeu-thich.html',hd,urllib.urlencode({"MovieID":"%s"%url}))
		try:mess(body.json['r'],'hdviet.com')
		except:mess(u'Lỗi thêm phim yêu thích!','hdviet.com')
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

def play_youtube(href):#https://www.youtube.com/get_video_info?video_id=xhNy0jnAgzI
	def choice_solution(items,label_quality):#label_quality in ('quality','quality_label')
		url=''
		for solution in ('1080','720','480','340','260','medium','small'):
			for item in items:
				x,y=item.get(label_quality),item.get('type')
				if x and y and solution in x and 'video' in y and 'mp4' in y:
					url=urllib.unquote(item.get('url'))
					s= make_request(url,hd,resp='s')
					if s==200:break
					else:url='fail'
			if url and url!='fail':break
		return url
	if 'https://www.youtube.com/watch?v=' in href:url=href+'&spf=navigate-back'
	else:url='https://www.youtube.com/watch?v=%s&spf=navigate-back'%xsearch('([\w|-]{10,20})',href,1)
	data=make_request(url,resp='j',maxr=3);fmts=''
	if not data:return
	a=makerequest(r'd:\xoa.txt',str(data),'w');fmts1=fmts2=''
	#for i in range(0,len(data)):#'adaptive_fmts','url_encoded_fmt_stream_map'
	#	try:fmts=data[i]['data']['swfcfg']['args']['url_encoded_fmt_stream_map'];break
	for i in data:#'adaptive_fmts','url_encoded_fmt_stream_map'
		try:
			if not fmts1:fmts1=i['data']['swfcfg']['args']['url_encoded_fmt_stream_map']
			if not fmts2:fmts2=i['data']['swfcfg']['args']['adaptive_fmts']
		except:pass
		if fmts1 and fmts2:break
	data=[];link=''
	for items in fmts1.split(','):
		dict={}
		for item in items.split('&'):
			try:dict[item.split('=')[0]]=item.split('=')[1]
			except:pass
		data.append(dict)
	link=choice_solution(data,'quality')
	if not link and link!='fail':
		data=[];link=''
		for items in fmts2.split(','):
			dict={}
			for item in items.split('&'):
				try:dict[item.split('=')[0]]=item.split('=')[1]
				except:pass
			data.append(dict)
		link=choice_solution(data,'quality_label')
	if link and link!='fail':xbmcsetResolvedUrl(link,re.sub(' \[COLOR.+?/COLOR\]','',name)+'Maxlink')
	else:mess(u'Get maxspeed link fail!','youtube.com')

def hayhaytv(name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'hayhaytv.png');clr='[COLOR tomato]';urlhome='http://www.hayhaytv.vn/'
	api='http://api.hayhaytv.vn/'
	def namecolor(name):return '%s%s[/COLOR]'%(clr,name)
	def hh_html(file,attr='r'):
		body=''
		if attr=='r':
			if  file=='hayhaytv.html':body=makerequest(joinpath(xsharefolder,'hayhaytv.html'))
			elif file=='hayhayclips.html':body=makerequest(joinpath(xsharefolder,'hayhayclips.html'))
		if attr=='w' or not body:
			if  file=='hayhaytv.html':
				a=make_request(urlhome)
				body=xsearch('"sub_menu_nav"(.+?)"hh_movie_hot_block-M"',a,1,re.DOTALL)
			else:
				pattern='(<a href="http://clips.hayhaytv.vn/category/.+?">.+?</a>)'
				body='\n'.join(sets(re.findall(pattern,make_request('http://clips.hayhaytv.vn/'))))
		print len(body)
		return body
	def hh_addir(name,url,img,fanart='',mode=mode,page=1):
		if xsearch('-Tap-',url,0):addir_info(namecolor(name),url,img,fanart,mode,page,'hh_read_foldef',True)
		else:addir_info(name,url,img,fanart,mode,page,'hh_play')
	def hh_check_series(url,page=1):
		if page==1:
			id_film=xsearch("Main.error_send\('(.+?)'\)",make_request(url),1)
			if '/xem-phim/' in url:url='http://www.hayhaytv.vn/loadepisode?film=%s&type=next&id='%id_film
			else:url='http://www.hayhaytv.vn/loadepisodeshow?film=%s&type=next&id='%id_film
		return url,make_post(url+str((page-1)*8),{'X-Requested-With':'XMLHttpRequest'},resp='j').get('dulieu','')
	def getlink(url):
		def get_tap(s):
			if isinstance(s,dict):tap=xsearch('(\d{1,4})',s.get('name'),1);tap=int(tap) if tap else 0
			else:tap=0
			return tap
		def get_linkplay(d,k):
			result=''
			if isinstance(d,dict) and isinstance(k,str) and d.get(k):
				r=['1080','720','480','360','']
				for i in range(len(r)):
					for j in d.get(k):
						if r[i] in j.get('resolution','xshare'):
							m3u8=j.get('mp3u8_link','').replace('///','//')
							bk=j.get('bk_link','').replace('///','//')
							if make_request(m3u8,resp='s')==200:result=m3u8;break
							elif make_request(bk,resp='s')==200:result=bk;break
							mess('')#Delete mess cua make_request
					if result:break
			return result
		epi=xsearch('-Tap-(\d{1,4})-',url,1);epi=int(epi) if epi else 0;body=make_request(url,maxr=3)
		if not body:return '',u'Get data từ hayhaytv thất bại!'
		movie_id=xsearch('data: "id=" \+ "(.+?)"',body,1);ep_id=xsearch("'id':'(.+?)'",body,1)
		xshare_dict=json_rw('xshare.json');s=xshare_dict.get('hh_headers');data1=''
		if not s:
			pattern='<title>.*xx(.+?)xx.*</title>'
			s=xsearch(pattern,make_request('https://www.fshare.vn/folder/5VNFUPO32P6F'),1).split('-')
			if s:xshare_dict['hh_headers']=s;json_rw('xshare.json',xshare_dict)
		if s:data1={s[0]:'%s %s'%(s[1],s[2])}
		loai='movie' if '/xem-phim/' in url else 'show'
		data2={"secure_token":"1.0","request":'{"%s_id":"%s"}'%(loai,movie_id)}
		data=make_post(api+'%s/%s_detail'%(loai,loai),data1,data2,'j')
		if not data:return '',u'Get max link thất bại...'
		elif not data.get('data'):return '',data.get('message')+'!' 
		else:data=data.get('data')
		episodes=data.get('list_episode',list())
		#print 'data,episodes: %s %s'%(data,episodes)
		href=sub=''
		if loai=='show':
			if not episodes:
				href=get_linkplay(data,'link_play_vip')
				if not href:href=get_linkplay(data,'link_play')
				sub=data.get('vn_subtitle')
			else:
				episode=[s for s in episodes if s.get('id','id')==ep_id]
				if episode:
					href=get_linkplay(episode[0],'link_play_vip')
					if not href:href=get_linkplay(episode[0],'link_play')
					sub=episode[0].get('vn_subtitle')
				else:href=sub=''
		else:
			if not episodes:href=api+'getlink/movie';sub=data.get('vn_subtitle','')
			else:
				episode=[s for s in episodes if s.get('id','id')==ep_id]
				if episode:movie_id=ep_id;sub=episode[0].get('vn_subtitle','');href=api+'getlink/movie_episode'
				else:href=sub=''
			if href:
				data2["request"]='{"data":[{"type":"facebook","email":"%s"}]}'%myaddon.getSetting('userhayhay')
				data=make_post(api+'user/signup_social_network',data1,data2,'j')
				if data:
					token=get_dict(data,['data','token_app'],result='');user_id=get_dict(data,['data','user_id'],result='')
					data2['request']='{"token":"%s","user_id":"%s","movie_id":"%s"}'%(token,user_id,movie_id)
					data=make_post(href,data1,data2,'j')
					if not data:href='';sub=u'Get max link thất bại...'
					elif not data.get('data'):href='';sub=data.get('message')+'!' 
					else:
						data=data.get('data')
						href=get_linkplay(data,'link_play')
						if not href:href=get_linkplay(data,'link_play_vip')
						if not sub:sub=data.get('vn_subtitle','')
				#print movie_id,data1,data2,data
		return href,sub
	#=============================================================================================
	if query=='hayhaytv.vn':
		body=hh_html('hayhaytv.html','r');name=color['search']+"Search trên hayhaytv.vn[/COLOR]"
		addir_info(name,urlhome+'tim-kiem/',ico,'',mode,1,'makeitemsearch',True)
		for id,href,title in re.findall('<li><a class="([1-9]{1,2}).*" href="(.+?)">(.+?)</a></li>',body):
			addir_info(namecolor(title),href,ico,'',mode,1,'main_menu',True)
		addir_info(namecolor('CLIP'),'http://clips.hayhaytv.vn',ico,'',mode,1,'clips',True)
		#-----------------------------------------------------------------------------------------
		add_sep_item('DS phim HayHaytv đề nghị')
		content=xsearch('"item active"(.+?)"left carousel-control"',body,1,re.DOTALL)
		items=re.findall('<a href="(.+?)".+?original="(.+?)".+?<p.+?>(.+?)</p>.+?<p.+?>(.+?)</p>',content,re.DOTALL)
		for href,fanart,eng,vie in items:hh_addir(vie+' - '+eng,href,fanart,fanart)
		content=xsearch('<a>Phim Đang HOT</a>(.+?)b9338c08203dc9b0035e510912622776',body,1,re.DOTALL)
		items=re.findall('"play_video" href="(.+?)".+?original="(.+?)".+?>([\w?].*?)</a>.+?>([\w].+?)</a>',content,re.DOTALL)
		for href,fanart,eng,vie in items:hh_addir(vie+' - '+eng,href,fanart,fanart)
		#-----------------------------------------------------------------------------------------
		if checkupdate('hayhaytv.html',1,xsharefolder):
			endxbmc();body=hh_html('hayhaytv.html','w')
			if body:
				makerequest(joinpath(xsharefolder,'hayhaytv.html'),body,'w')
				xbmc.executebuiltin("Container.Refresh")
			return ''
	elif query=='makeitemsearch':search_get_items('hayhaytv.vn',mode)
	elif query=='getstringsearch' or query=='dosearch':
		if query=='dosearch':string=name
		else:
			string=search_input_string('hayhaytv.vn')
			if not string:return 'no'
		page=1 if 'Trang tiếp theo' not in name else page
		response=make_post('http://www.hayhaytv.vn/search/autocomplete?object='+urllib.quote_plus(string),resp='j')
		for d in response.get('FILM',list()):
			hh_addir(u2s(d.get('extension')+' - '+d.get('name')),d.get('link'),d.get('image'))
	elif query=='hh_read_foldef':
		url,body=hh_check_series(url,page)
		pattern='<li>.+?href="(.+?)".+?<div class="mask-num-film">(\d{1,4})</div>.+?data-original="(.+?)"'
		items=re.findall(pattern,body.replace('\n',''))
		name=remove_tag(name.split('- Trang')[0])
		for href,epi,img in items:addir_info('Tập %s - %s'%(u2s(epi),name),href,img,img,mode,page,'hh_play')
		if len(items)>7:
			name='%s%s - Trang:%d[/COLOR]'%(color['trangtiep'],name,page+1)
			addir_info(name,url,ico,'',mode,page+1,query,True)
	elif query=='hh_play':
		href,sub=getlink(url)
		if href:
			if sub:
				xshare_resolve(sub);mess(u'Phụ đề của hayhaytv.vn','hayhaytv.vn')
				xbmcsetResolvedUrl(href,urllib.unquote(os.path.splitext(os.path.basename(sub))[0]))
			else:xbmcsetResolvedUrl(href)
		else:mess(sub,'hayhaytv.vn')
	elif query=='main_menu':
		href='http://www.hayhaytv.vn/load%s?type=%s&type_film=%s&sort=%d&page=%d'
		hd={'X-Requested-With':'XMLHttpRequest'}
		if 'phim-hot' in url:load='Film';type='hot';type_film='';sort=1
		elif 'phim-le' in url:load='Film';type='1';type_film='1';sort=2
		elif 'phim-bo' in url:load='Film';type='ca';type_film='2';sort=2
		elif 'shows' in url:load='Shows';type='';type_film='';sort=2
		elif 'anime' in url:load='Film';type='jj';type_film='';sort=2
		elif 'thieu-nhi' in url:load='Film';type='kids';type_film='';sort=2
		elif 'sap-chieu' in url:load='Film';type='upcoming';type_film='';sort=2
		print href%(load,type,type_film,sort,page)
		body=make_post(href%(load,type,type_film,sort,page),hd,resp='b');count=0
		for content in re.findall('<li class="">(.+?)</li>',body,re.DOTALL):
			eps=xsearch('"mask-num-film">(.+?)</strong></span>',content,1).replace('<strong>','')
			href=xsearch('<a href="(.+?)"',content,1)
			img=xsearch('data-original="(.+?)"',content,1)
			title=' '.join(s for s in re.findall('target="_blank">(.+?)</a>',content))
			title=remove_tag(title)+ (' [COLOR green](%s)[/COLOR]'%eps if eps else '')
			hh_addir(title,href,img);count+=1
		if count>30:
			name=re.sub('\[.+?\]','',name.split('-')[0].strip())
			name='%s%s - Trang tiếp theo: trang %d[/COLOR]'%(color['trangtiep'],name,page+1)
			addir_info(name,url,ico,'',mode,page+1,query,True)
	elif query=='clips':
		body=hh_html('hayhayclips.html','r');pattern='<a href="(http://clips.hayhaytv.vn/category/.+?)">(.+?)</a>'
		for href,title in re.findall(pattern,body):
			addir_info(namecolor(remove_tag(title)),href,ico,'',mode,1,'clips_menu',True)
		#-----------------------------------------------------------------------------------------
		if checkupdate('hayhayclips.html',1,xsharefolder):
			endxbmc();body=hh_html('hayhayclips.html','w')
			if body:
				makerequest(joinpath(xsharefolder,'hayhayclips.html'),body,'w')
				xbmc.executebuiltin("Container.Refresh")
	elif query=='clips_menu':
		#if 'kich-hai' in url:
		#'http://clips.hayhaytv.vn/category/hai/kich-hai/page/%d/?orderby=date'
		href=url+'page/%d/?orderby=date'
		pattern='(www.youtube.com/.+?|youtu.be/.+?)[\?| ].+?src="(.+?)".+?alt="(.+?)"'
		items=re.findall(pattern,make_post(href%page,resp='b'),re.DOTALL)
		for href,img,title in items:
			print href
			addir_info(remove_tag(title),href,img,'',mode,1,'hh_youtube')
		if len(items)>9:
			name=re.sub('\[.+?\]','',name.split('-')[0].strip())
			name='%s%s - Trang tiếp theo: trang %d[/COLOR]'%(color['trangtiep'],name,page+1)
			addir_info(name,url,ico,'',mode,page+1,query,True)
	elif query=='hh_youtube':return play_youtube(url)

def phimmoi(name,url,img,mode,page,query):
	color['phimmoi']='[COLOR ghostwhite]';icon['phimmoi']=os.path.join(iconpath,'phimmoi.png')
	urlhome='http://www.phimmoi.net/';refresh=False;phimmoixml=joinpath(datapath,'phimmoi.xml')
	def namecolor(name):return '%s%s[/COLOR]'%(color['phimmoi'],name)
	def login_pm():
		u=myaddon.getSetting('userphimmoi');p=myaddon.getSetting('passphimmoi')
		import hashlib;p=hashlib.md5(p).hexdigest()
		response=make_post('http://www.phimmoi.net/login/',data=urllib.urlencode({'username':u,'password_md5':p}))
		if response.status==302 and makerequest(joinpath(datapath,'phimmoi.cookie'),response.cookiestring,'w'):
			mess(u'Login thành công','phimmoi.net');f=response.cookiestring
		else:mess(u'Login không thành công!','phimmoi.net');f=''
		return f
	def get_token(hd={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}):
		hd['Cookie']=makerequest(joinpath(datapath,'phimmoi.cookie'));url='http://www.phimmoi.net/tu-phim/'
		body=make_request(url,headers=hd);token=xsearch("fx\.token='(.+?)'",body,1)
		if not token:
			hd['Cookie']=login_pm();body=make_request(url,headers=hd);token=xsearch("fx\.token='(.+?)'",body,1)
		return body,token,hd
	def getoken():
		import time;_0xc3c8x48=str(int(round(time.time())))
		import hashlib;_0xc3c8x49=hashlib.md5(_0xc3c8x48+'(*Y#NFJKDHFIEY#(**%#&*^%').hexdigest()
		return _0xc3c8x49[:11]+_0xc3c8x48+_0xc3c8x49[21:32]
	def pm_search(string):
		url='http://www.phimmoi.net/tim-kiem/%s/'%urllib.quote_plus(string)
		phimmoi(name,url,img,mode,page=1,query='readpage')
	def get_language(language):
		if language=='subtitle':language='Vietsub'
		elif language=='illustrate':language='Thuyết minh'
		elif language=='dubbing':language='Lồng tiếng'
		else:language=''
		return language
	def get_epi(epi):
		try:epi=int(epi)
		except:epi=0
		return epi
	def pm_get_info(title,href,img,detail):
		eps=xsearch('Tập ?(\d{,4}/\d{,4}|\?/\d{,4}|\d{,4})',detail,1)
		if not eps:
			epi=xsearch('class="eps">Trọn bộ ?(\d{1,4}) ?tập</div>',detail,1)
			if epi:eps='%s/%s'%(epi,epi)
		else:epi=eps.split('/')[0]
		dur=xsearch('>(\d{1,3}.?phút)',detail,1)
		audio='TM' if 'Thuyết minh' in detail else ''
		label=xsearch('(HD[\w|-]*|SD[\w|-]*|Bản đẹp[\w|-]*)',detail,1)
		if 'url=' in img:img=img.split('url=')[1]
		if eps:title='%s %s(%s)[/COLOR]'%(title,color['subscene'],eps)
		if 'phút/tập' in detail:
			title='%s [COLOR gold]%s[/COLOR]'%(title,xsearch('>(\d{1,3} phút/tập)<',detail,1))
		elif dur:title='%s [COLOR gold]%s[/COLOR]'%(title,dur)
		if xsearch('<span class="ribbon">Trailer</span>',detail,0):query='pmplay_trailer'
		elif get_epi(epi)>1 or 'phút/tập' in detail or 'Phim bộ hot trong tuần' in name:
			query='pmfolder';title=namecolor(title)
		else:query='pm_list_url_ple'
		if audio:title='[COLOR gold]TM[/COLOR] %s'%title
		if label:title='%s - [COLOR green]%s[/COLOR]'%(title,label)
		return title,urlhome+href,img,query
	def pmaddir(items,action='Add'):#title,href,img,detail
		for title,href,img,detail in items:
			title,href,img,query=pm_get_info(title,href,img,detail)
			menu={'tuphim':{'action':action,'server':['phimmoi.net']}}
			addir_info(title,href,img,'',mode,page,query,True if query!='pmplay_trailer' else False,menu=menu)
	def pm_get_maxlink(google_link):
		href=urlhome+'player/v1.46/plugins/gkplugins_picasa2gdocs/plugins/plugins_player.php?url=%s&token=%s'
		result=make_post(href%(google_link,getoken()),resp='j')
		height=0;link='';maxresolution=int(myaddon.getSetting('phimmoiresolution'))
		for item in [s for s in result.get("content",list()) if 'video' in s.get('type')]:
			if item.get('height',0)==maxresolution:link=item.get('url');break
			elif item.get('height',0)>height:height=item.get('height',0);link=item.get('url')
		return link

	if query=='phimmoi.net':
		name=color['search']+"Search trên phimmoi.net[/COLOR] (Chọn độ phân giải max trên settings nhé)"
		addir_info(name,'http://www.phimmoi.net/tim-kiem/',icon['phimmoi'],'',mode,1,'search',True)
		name=color['search']+'Tủ phim trên phimmoi.net của tôi[/COLOR]'
		addir_info(name,'http://www.phimmoi.net/tu-phim/',img,'',mode,1,'readpage',True)
		body=makerequest(joinpath(xsharefolder,'phimmoi.html'))
		content=xsearch('<ul id=".+?"(.+?)</ul></div>',body,1)
		for title in re.findall('<a>(.+?)</a>',content):
			addir_info(namecolor(title),'',icon['phimmoi'],'',mode,1,'menubar',True)
		for href,title in re.findall('<a href="([\w|-]+/|http://www.phimmoi.net/tags/.*?)">(.+?)</a>',content):
			addir_info(namecolor(title),href,icon['phimmoi'],'',mode,1,'menubar',True)
		for title in re.findall('<h2 class="right-box-header star-icon"><span>(.+?)</span>',body):
			if title=='Phim đã đánh dấu':continue
			addir_info(namecolor(title),'right-box',img,'',mode,1,'menubar',True)
		for label,content in re.findall('class="title-list-index">(.+?)</span>(.+?</div></div></div>)',body):
			add_sep_item(label)
			#addir_info('[COLOR lime]%s[/COLOR]'%label,'',img,'',mode,1,'no')
			pattern='<li><a href="(.+?)" title="(.+?)">.+?<img src="(.+?)".+?(<h3.+?</p>)'
			items=re.findall(pattern,content)
			if items:pmaddir([(s[1],s[0],s[2],s[3]) for s in items])#title,href,img,detail
			else:
				pattern='"movie-item m-block" title="(.+?)" href="(.+?)".+?(http.+?\.jpg).+?<div(.+?)</div></a></li>'
				pmaddir(re.findall(pattern,content))#title,href,img,detail
			if label=='Phim đề cử':
				for title,content in re.findall('<h2 class="hidden">(.+?)</h2>(.+?</li></ul>)',body):
					add_sep_item(title)
					#addir_info('[COLOR lime]%s[/COLOR]'%title,'',img,'',mode,1,'no')
					pattern='title="(.+?)" href="(.+?)".+?\(\'(http.+?)\'\).+?</div></a>(.+?)</div></li>'
					pmaddir(re.findall(pattern,content))#title,href,img,detail
		if checkupdate('phimmoi.html',8,xsharefolder):
			endxbmc();body=make_request('http://www.phimmoi.net/')
			makerequest(joinpath(xsharefolder,'phimmoi.html'),body,'w');xbmc.executebuiltin("Container.Refresh")
	elif query=='search':make_mySearch('','phimmoi.net','','',mode,'get')
	elif query=="INP":pm_search(make_mySearch('',url,'','','','Input'))
	elif url=='phimmoi.net':page=1 if 'Trang tiếp theo' not in name else page;pm_search(query)
	elif query=='menubar':
		if any(s for s in ['kinh','rap','tags','trailer'] if s in url):
			if 'tags' not in url:url=urlhome+url
			return phimmoi(name,url,img,mode,page,'readpage')
		elif url=='right-box':
			pattern='<span>%s</span>(.+?</li></ul></div></div>)'%re.sub('\[/?COLOR.*?\]','',name).strip()
			content=xsearch(pattern,makerequest(joinpath(xsharefolder,'phimmoi.html')),1)
			pattern='title="(.+?)" href="(.+?)">.+?\(\'(.+?)\'\).+?</span>(.+?)</a></li>'
			pmaddir(re.findall(pattern,content))#title,href,img,detail
		else:
			content=xsearch('<ul id=".+?"(.+?)</ul></div>',makerequest(joinpath(xsharefolder,'phimmoi.html')),1)
			gen={'Thể loại':'the-loai','Quốc gia':'quoc-gia','Phim lẻ':'phim-le','Phim bộ':'phim-bo'}
			query=gen.get(re.sub('\[/?COLOR.*?\]|\(.+?\)','',name).strip())
			pattern='<a href="(%s/.*?)">(.+?)</a>'%query
			for href,title in re.findall(pattern,content):
				addir_info(namecolor(title),urlhome+href,icon['phimmoi'],'',mode,1,'readpage',True)
	elif query=='readpage':
		if url=='http://www.phimmoi.net/tu-phim/':body,token,headers=get_token();menu='Remove'
		else:body=make_request(url);menu='Add'
		pattern='<li class="movie-item">.+?title="(.+?)" href="(.+?)".+?(http.+?)\)(.+?)</li>'
		pmaddir(re.findall(pattern,body,re.DOTALL),menu)#title,href,img,detail
		urlnext=xsearch('<li><a href="(.+?)">Trang kế.+?</a></li>',body,1)
		if urlnext:
			pagenext=xsearch('/page-(\d{1,3})\.html',urlnext,1)
			name='%sTrang tiếp theo: trang %s[/COLOR]'%(color['trangtiep'],pagenext)
			addir_info(name,urlhome+urlnext,img,fanart,mode,page,'readpage',True)
	elif 'tuphim' in query:
		body,token,headers=get_token();data={'_fxAjax':'1','_fxResponseType':'JSON','_fxToken':'%s'%token}
		action='add' if 'Add' in query else 'remove'
		response=make_post('%s%s.html'%(url,action),headers,data,resp='j')
		if response.get('_fxStatus',0)==1:
			mess(response.get('_fxMessage','success'),'phimmoi.net')
			if action=='remove':xbmc.executebuiltin("Container.Refresh")
		else:
			try:mess(response.get('_fxErrors')[0],'phimmoi.net')
			except:mess(u'Đã phát sinh lỗi!','phimmoi.net')
	elif query=='pmfolder':
		body=make_request(url+'xem-phim.html');menu={'tuphim':{'action':'Add','server':['phimmoi.net']}}
		eps=xsearch('(/\d{1,4})\)',name,1);name=re.sub('\[/?COLOR.*?\]|\(.+?\)|\d{1,3} phút/tập|\d{1,3} phút','',name).strip()
		for detail in re.findall('data-serverid="pcs"(.+?)</li></ul></div>',body,re.DOTALL):
			title=' '.join(s for s in xsearch('<h3 class="server-name">(.+?)</h3>',detail,1,re.DOTALL).split())
			if title and 'tập phim' not in title:
				add_sep_item(title)
				#addir_info('[COLOR lime]%s[/COLOR]'%title,'',img,'',mode,1,'no')
			label=name.replace('TM ','') if title and 'Thuyết minh' not in title else name
			for title,href in re.findall('title="(.+?)".+?href="(.+?)"',detail,re.DOTALL):
				addir_info('%s%s %s'%(title,eps,label),urlhome+href,img,'',mode,page,'pmplay_pbo',menu=menu)
	elif query=='pm_list_url_ple':
		body=make_request(url if '.html' in url else url+'xem-phim.html')
		if xsearch("filmInfo.isSeries=\('serial'=='serial'\)",body,0):return phimmoi(name,url,img,mode,page,'pmfolder')
		if xsearch("filmInfo.isAdult=parseInt\('1'\)",body,0) and myaddon.getSetting('phim18')=="false":
			return mess_yesno(line1='Phim này có cảnh quay nhạy cảm và bạn đã chọn không xem!', line2='Thanks you')
		art=xsearch("filmInfo.previewUrl='.+=(https:.+)'",body,1);name=name.replace('[COLOR gold]TM[/COLOR]','')
		link=xsearch("currentEpisode.url='(.+?)'",body,1);server=1;parts=0
		language=xsearch("currentEpisode.language='(.+?)'",body,1)
		label='[COLOR gold]S0 %s[/COLOR]: '%get_language(language)+name
		if link:addir_info(label,link,img,art,mode,page,'pmplay_ple')
		
		content=xsearch('<div class="list-server">(.+?)</div>',body,1,re.DOTALL).replace('\n','')
		for label,subcontent in re.findall('class="server-title">(.+?)</h3>(.+?)</ul>',content):
			for href,title in re.findall('href="(.+?)">(.+?)</a>',subcontent):
				addir_info('%s %s'%(label,title),urlhome+href,img,art,mode,page,'pmplay_pbo')
			
		episodeJson=xsearch("episodeJson='(.+?)'",body,1)
		try:episodeJson=eval(episodeJson)
		except:return
		for i in [s for s in episodeJson if s.get('url')]:
			language=get_language(i.get('language'));part=i.get('part',0)
			if part<parts:server+=1;parts=0
			else:parts=part
			numserver='S%d'%server if server%2==0 else '[COLOR green]S%d[/COLOR]'%server
			if part==0:label='[COLOR gold]%s %s[/COLOR]: '%(numserver,language)+name;server+=1
			else:
				label='[COLOR gold]%s-part%d-%s[/COLOR]: '%(numserver,part,language)
				label+=re.sub('\[COLOR gold\].{1,5}phút\[/COLOR\] - ','',name)
			addir_info(label,i['url'].replace('\\',''),img,art,mode,page,'pmplay_ple')
	elif query=='pmplay_ple':
		href=pm_get_maxlink(url)
		if href:xbmcsetResolvedUrl(href)
		else:mess(u'Không get được maxspeedlink hoặc link bị die!','phimmoi.net')
	elif query=='pmplay_pbo':
		href=pm_get_maxlink(xsearch("currentEpisode.url='(.+?)'",make_request(url),1))
		if href:xbmcsetResolvedUrl(href)
		else:mess(u'Không get được maxspeedlink hoặc link bị die!','phimmoi.net')
	elif query=='pmplay_trailer':
		href=xsearch("filmInfo.trailerUrl='(.+?)'",make_request(url),1);print href
		return play_youtube(href)

def htvonline(name,url,img,fanart,mode,page,query):
	tvurl='http://www.htvonline.com.vn/livetv';showurl='http://www.htvonline.com.vn/shows'
	phimurl='http://www.htvonline.com.vn/phim-viet-nam';hd['X-Requested-With']='XMLHttpRequest'
	def namecolor(name):return '[COLOR yellowgreen]%s[/COLOR]'%name
	if query=='home':
		tv=makerequest(joinpath(xsharefolder,'htvtv.html'));show=makerequest(joinpath(xsharefolder,'htvshow.html'))
		phim=makerequest(joinpath(xsharefolder,'htvphim.html'))
		for title in re.findall('<div class="view_title2"><div>(.+?)</div>',tv):
			addir(namecolor(title.replace(',','-')),tvurl,img,'',mode,page,'submenu',True)
		fanart=xsearch('<img width="487" height="274" src="(.+?)"',show,1)
		addir(namecolor('TV Shows'),showurl+'?page=1',fanart,fanart,mode,page,'submenu',True)
		fanart=xsearch('<img width="487" height="274" src="(.+?)"',phim,1)
		addir(namecolor('Phim'),phimurl+'?page=1',fanart,fanart,mode,page,'submenu',True)
		for title,detail in re.findall('<div class="view_title"><div>(.+?)</div>(.+?)</ul>',show,re.DOTALL):
			#addir('[COLOR lime]%s[/COLOR]'%title,'',img,'',mode,1,'no')
			add_sep_item(title)
			for href,label,img in re.findall('data-tooltip=".+?".+?<a href="(.+?)".+?<h2>(.+?)</h2>.+? src="(.+?)"',detail,re.DOTALL):
				addir(label,href,img,'',mode,page,'htvplay')
		if checkupdate('htvtv.html',8,xsharefolder):
			endxbmc();makerequest(joinpath(xsharefolder,'htvtv.html'),make_request(tvurl),'w')
			makerequest(joinpath(xsharefolder,'htvshow.html'),make_request(showurl),'w')
			makerequest(joinpath(xsharefolder,'htvphim.html'),make_request(phimurl),'w')
	elif query=='submenu':
		if 'lịch phát sóng' in name:
			body=makerequest(joinpath(xsharefolder,'htvtv.html'))
			href='http://www.htvonline.com.vn/livetv/show-schedule';chanels=('HTV','VTV','VTC')
			items=re.findall('value="(.+?)" data-imagesrc="(.+?)">(.+?)</option>',body)
			for chanel,img,title in sorted([s for s in items if [i for i in chanels if i in s[2]]],key=lambda l:l[2]):
				addir(namecolor(title.replace(',','-')),href,img,'',mode,int(chanel),'schedule',True)
		elif showurl in url or phimurl in url:
			if showurl in url:page1='htvshow.html';page2='htvshowpage.html'
			else:page1='htvphim.html';page2='htvphimpage.html'
			if 'page=1' in url:body=makerequest(joinpath(xsharefolder,page1))
			else:body=makerequest(joinpath(xsharefolder,page2))
			if phimurl in url and 'page=1' in url:
				for title,detail in re.findall('<div class="view_title"><div>(.+?)</div>(.+?)</ul>',body,re.DOTALL):
					#addir('[COLOR lime]%s[/COLOR]'%title,'',img,'',mode,1,'no')
					add_sep_item(title)
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

def search_get_items(server='vaphim.com',mode=1):
	menu={'MySearch':{'action':'Add','server':['xshare.vn']}};srv=server.split('.')[0]
	items=[('%sNhập chuỗi tìm kiếm mới trên[/COLOR] %s%s[/COLOR]'%(color['search'],color[srv],server),'getstringsearch')]
	if myaddon.getSetting('history')=='true':
		items+=[(s,'dosearch') for s in re.findall('<a>(.+?)</a>',makerequest(search_file))]
	for label,query in items:addir_info(label,'',icon[srv],'',mode,1,query,True,menu=menu)

def search_input_string(server='vaphim.com'):
	string=get_input('Nhập chuổi (ít nhất 3 ký tự) tên phim cần tìm trên %s'%server);attr='a'
	if not string or len(string.strip())<3:return ''
	string=remove_tag(string)
	if not xsearch('<a>%s</a>'%string,makerequest(search_file),1):
		makerequest(search_file,'<a>%s</a>\n'%string,'a');xbmc.executebuiltin("Container.Refresh")
	return string

def vaphim(name,url,img,fanart,mode,page,query):
	clr=color['vaphim'];ico=icon['vaphim'];urlhome='http://vaphim.com/'
	def namecolor(name):return '%s%s[/COLOR]'%(clr,name)
	def vp_homehtml(update=False):
		if update:
			body=make_request(urlhome)
			if body:body=makerequest(joinpath(xsharefolder,'vaphim.html'),body,'w')
		else:
			body=makerequest(joinpath(xsharefolder,'vaphim.html'))
			if not body:return vp_homehtml(True)
		return body
	def vp_readpage(url):
		body=make_request(url)
		if not body:
			mess(u'Đang cố gắng đọc lại lần 1!','Vaphim.com');xbmc.sleep(5000);body=make_request(url)
			if not body:
				mess(u'Đang cố gắng đọc lại lần 2!','Vaphim.com');xbmc.sleep(7000);body=make_request(url)
				if not body:
					mess(u'Đang cố gắng đọc lại lần 3!','Vaphim.com');xbmc.sleep(10000);body=make_request(url)
				if not body:mess(u'Pótay.com!','Vaphim.com')
		return body
	#-----------------------------------------------------------------------------------------------------
	if query=='vaphim.com':
		label=color['search']+"Search nhanh trên vaphim.com[/COLOR]"
		addir_info(label,'http://vaphim.com/fast-search.php?term=',icon['vaphim'],'',mode,1,'makeitemsearch',True)
		addir_info(namecolor('Phim lẻ-Phim bộ-Nhạc-VideoClip mới nhất-Xem nhiều nhất'),urlhome,ico,'',mode,1,'phimmoinhat',True)
		addir_info(namecolor('Danh Mục Phân Loại Phim'),'',ico,'',mode,1,'mainmenu',True)
		addir_info(namecolor('Danh Mục Phim Theo Thể Loại - Quốc Gia'),'',ico,'',mode,1,'mainmenu',True)
		addir_info(namecolor('Danh Mục Phân Loại Nhạc'),'',ico,'',mode,1,'mainmenu',True)
		addir_info(namecolor('Danh Mục Các Bộ Sưu Tập'),'',ico,'',mode,1,'mainmenu',True)
		add_sep_item('Vaphim.com giới thiệu');body=vp_homehtml()
		pattern='<a class="featured-article" href="(.+?)".+?src="(.+?)[\?|\"].+?"bookmark">(.+?)</a>'
		for href,img,title in re.findall(pattern,body,re.DOTALL):
			addir_info(namecolor(remove_tag(title)),href,img,img,mode,1,'vp_getsubpage',True)
		if checkupdate('vaphim.html',1,xsharefolder):endxbmc();body=vp_homehtml(True)
	elif query=='phimmoinhat':
		add_sep_item('Xem nhiều nhất');body=vp_homehtml()
		for href,title in re.findall('<li><a href="(.+?)" title="(.+?)">',body):
			addir_info(namecolor(remove_tag(title)),href,ico,'',mode,1,'vp_getsubpage',True)
		pattern='<li class=.+?src="(.+?)[\?|\"].+?<a href="(.+?)".+? >(.+?)</a>'
		add_sep_item('Phim lẻ mới nhất')
		for img,href,title in re.findall(pattern,xsearch('"index-featured2"(.+?)</ul>',body,1,re.DOTALL),re.DOTALL):
			addir_info(namecolor(remove_tag(title)),href,img,'',mode,1,'vp_getsubpage',True)
		add_sep_item('Phim bộ mới nhất')
		for img,href,title in re.findall(pattern,xsearch('"index-featured3"(.+?)</ul>',body,1,re.DOTALL),re.DOTALL):
			addir_info(namecolor(remove_tag(title)),href,img,'',mode,1,'vp_getsubpage',True)
		add_sep_item('Nhạc mới nhất')
		for img,href,title in re.findall(pattern,xsearch('"index-featured4"(.+?)</ul>',body,1,re.DOTALL),re.DOTALL):
			addir_info(namecolor(remove_tag(title)),href,img,'',mode,1,'vp_getsubpage',True)
		add_sep_item('VideoClip mới nhất')
		pattern='<img.+?src="(.+?)[\?|\"].+?<a href="(.+?)".+?>(.+?)</a>'
		for img,href,title in re.findall(pattern,xsearch('"index-news"(.+?)</ul>',body,1,re.DOTALL),re.DOTALL):
			addir_info(namecolor(remove_tag(title)),href,img,'',mode,1,'vp_getclip',True)
	elif query=='mainmenu':
		body=vp_homehtml()
		if name==namecolor('Danh Mục Phân Loại Phim'):
			pattern='<li><a href="/(category/phim-2/.+?)">(.+?)</a></li>'
			for href,title in re.findall(pattern,body):
				addir_info(namecolor(title),urlhome+href,ico,'',mode,1,'vp_getpage',True)
		elif name==namecolor('Danh Mục Phim Theo Thể Loại - Quốc Gia'):
			pattern='<li id=".+?" class="menu.+?"><a href="(.+?)">(.+?)</a></li>'
			for href,title in re.findall(pattern,body):
				addir_info(namecolor(title),href,ico,'',mode,1,'vp_getpage',True)
		elif name==namecolor('Danh Mục Phân Loại Nhạc'):
			pattern='<li><a href="/(category/music/.+?)">(.+?)</a></li>'
			for href,title in re.findall(pattern,body):
				addir_info(namecolor(title),urlhome+href,ico,'',mode,1,'vp_getpage',True)
		elif name==namecolor('Danh Mục Các Bộ Sưu Tập'):
			return vaphim(name,'http://vaphim.com/category/collection/',img,fanart,mode,page,'vp_getpage')
	elif query=='vp_getpage':
		href=url if page==1 else '%spage/%d/'%(url,page)
		body=vp_readpage(href)
		if not body:return 'no'
		pattern='<a data=.+?src="(.+?)[\?|\"].+?<h3.+?><a href="(.+?)" rel=.+?>(.+?)</a></h3>'
		for img,href,title in re.findall(pattern,body,re.DOTALL):
			addir_info(namecolor(remove_tag(title)),href,img,'',mode,1,'vp_getsubpage',True)
		pagelast=xsearch("<span class='pages'>Trang \d{1,4} của (\d{1,4})</span>",body,1)
		if pagelast and int(pagelast)>page:
			name=re.sub('\[.+?\]','',name.split('-')[0].strip())
			name='%s%s - Trang tiếp theo: trang %d/%s[/COLOR]'%(color['trangtiep'],name,page+1,pagelast)
			addir_info(name,url,ico,'',mode,page+1,query,True)
	elif query=='vp_getclip':
		if 'youtube.com' in url:play_youtube(url)
		else:
			item=re.search("src='(.+?)'.+?src='([\w|:|/|\.]+youtube.com.+?)'",make_request(url))
			if item:addir_info(remove_tag(name),item.group(2),item.group(1),'',mode,1,'vp_getclip')
			else:mess(u'Sorry! Không get được nội dung này trên vaphim.com','vaphim.com');return 'no'
	elif query=='makeitemsearch':search_get_items('vaphim.com',mode)
	elif query=='getstringsearch' or query=='dosearch':
		if query=='dosearch':string=name
		else:
			string=search_input_string('vaphim.com')
			if not string:return 'no'
		url='http://vaphim.com/fast-search.php?term='+urllib.quote_plus(string);items=make_request(url,resp='j')
		if not items:mess(u'Sorry! Không tìm thấy phim có chứa chuổi bạn yêu cầu','vaphim.com');return 'no'
		for item in items:
			label=remove_tag(u2s(item.get('label')));href=u2s(item.get('url'));img=u2s(item.get('thumb'))
			if not label or not href:continue
			addir_info(color['vaphim']+label+'[/COLOR]',href,img,'',mode,1,'vp_getsubpage',True)
	elif query=='vp_getsubpage':
		body=vp_readpage(url);items=list();name=remove_tag(name.replace('Vaphim ',''))
		body=xsearch('<div id="post-(.+?)"fb-comments"',body,1,re.DOTALL)
		if not body:return 'no'
		if re.search('class=".+category-(game|phn-mm|ebooks).+"',body):
			mess(u'Sorry! Trang này không phải trang phim','Vaphim.com');return 'no'
		art=re.findall('<p><a href=".+?" rel="attachment.+?"><img src="(.+?)[\?|"]',body)
		if not art:art=['']
		tabs=re.findall('#(tabs-.+?)" >(.+?)<',body);i=0;j=len(art)-1
		if tabs:
			for tab,tab_label in tabs:
				content=xsearch('<div id="%s">(.+?)</div>'%tab,body,1,re.DOTALL)
				fanart=art[i];i=0 if i==j else (i+1)
				for href,fn in re.findall('<a href="(.+?)".*?>(.+?)</a>',content):
					fn='[COLOR green]%s[/COLOR] - %s'%(tab_label,remove_tag(fn))
					items.append((fn if fn else name,href,fanart))
		else:
			pattern='([\w|/|:|\.]+?fshare\.vn.+?|[\w|/|:|\.]+?subscene\.com.+?)[&|"|\'].+?>(.+?)</a>'
			for href,fn in re.findall(pattern,body):
				fn=remove_tag(fn);fanart=art[i];i=0 if i==j else (i+1);
				items.append((fn if fn else name,href,fanart))
		if items:
			add_sep_item('Links phim: '+name)
			for title,href,fanart in items:addir_info(title,href,img,fanart,mode,1)
		#------------------------------------------------------------------------------------------------
		trailer=xsearch('(http[\w|:|/|\.]+youtube.com.+?)[\"|\'|<|>| ]',body,1)
		if trailer:addir_info('[COLOR lime]Trailer[/COLOR] - '+name,trailer,img,fanart,mode,1,'vp_getclip')
		#------------------------------------------------------------------------------------------------
		items=re.findall('href="(.+?)".+?src="(.+?)[\?|"].+?alt=".+?".+?title="(.+?)"',body)
		if items:
			add_sep_item('Chủ đề tương tự')
			for href,img,title in items:
				title=namecolor('Vaphim - '+remove_tag(title))
				addir_info(title,href,img,'',mode,1,'vp_getsubpage',True)
	return ''

def addir_info(name,url,img,fanart='',mode=0,page=0,query='',isFolder=False,info=dict(),art=dict(),menu=dict()):
	def xquote(href):return urllib.quote_plus(href)
	def get_mode(url,name,mode,isfolder=True):
		if 'fshare.vn/' in url:
			id=xsearch('(\w{10,20})',url,1)
			if '/file/' in url:
				url='https://www.fshare.vn/file/%s'%id.upper()
				name='%sFshare[/COLOR] %s'%(color['fshare'],name);mode=3;isfolder=False
			else:
				url='https://www.fshare.vn/folder/%s'%id.upper()
				name='%sFshare %s[/COLOR]'%(color['fshare'],name);mode=90
		elif 'tenlua.vn/' in url:
			id=xsearch('(\w{10,20})',url,1)
			if 'folder/' in url or '#download' in url:
				url='https://tenlua.vn/fm/folder/%s'%id
				name='%sTenlua %s[/COLOR]'%(color['tenlua'],name);mode=95
			else:
				url='https://tenlua.vn/download/%s'%id
				name='%sTenlua[/COLOR] %s'%(color['tenlua'],name);mode=3;isfolder=False
		elif '4share.vn/d/' in url:name='%s4share %s[/COLOR]'%(color['4share'],name);mode=38
		elif '4share.vn/f/' in url:name='%s4share[/COLOR] %s'%(color['4share'],name);mode=3;isfolder=False
		elif 'subscene.com/' in url:name='%ssubscene[/COLOR] %s'%(color['subscene'],name);mode=94
		elif 'vaphim.com/' in url:name='%s%s[/COLOR]'%(color['vaphim'],name);mode=1
		#elif 'vaphim.com/' in url:name='%s%s[/COLOR]'%(color['vaphim'],name);mode=25
		elif 'phimfshare.com/' in url:name='%s%s[/COLOR]'%(color['vaphim'],name);mode=6
		elif 'hdvietnam.com' in url:name='%sHDVN[/COLOR] %s'%(color['hdvietnam'],name);mode=8
		return u2s(name),url,mode,isfolder
	def get_menu(menu,url):
		lists=list()
		#menu['muctheodoi']={'action':'Add','server':['hdvietnam.com']}}
		#menu['muctheodoi']={'action':'Remove','server':['hdvietnam.com']}}
		if menu.has_key('muctheodoi'):
			inf=menu.get('muctheodoi')
			if [s for s in inf['server'] if s in url] and inf['action']=='Add':
				lists.append(('Add to Mục đang theo dõi',{'query':'muctheodoi_Add'}))
			elif [s for s in inf['server'] if s in url] and inf['action']=='Remove':
				lists.append(('Remove from Mục đang theo dõi',{'query':'muctheodoi_Remove'}))
		#menu['MyFavourites']={'action':'Add','server':['fshare.vn','4share.vn','tenlua.vn']}
		if menu.has_key('MyFavourites'):
			inf=menu.get('MyFavourites')
			if [s for s in inf['server'] if s in url] and inf['action']=='Add':
				lists.append(('Add to MyFavourites',{'query':'Add','mode':98}))
			if [s for s in inf['server'] if s in url] and inf['action']=='Remove':
				lists.append(('Remove from MyFavourites',{'query':'Remove','mode':98}))
		if menu.has_key('MyFshare'):
			inf=menu.get('MyFshare')
			if [s for s in inf['server'] if s in url] and inf['action']=='Add':
				lists.append(('Add to MyFshare',{'query':'Add','mode':11}))
				lists.append(('Add to MyFshare Favorite',{'query':'AddFavorite','mode':11}))
			if [s for s in inf['server'] if s in url] and inf['action']=='Remove':
				lists.append(('Rename in MyFshare',{'query':'Rename','mode':11}))
				lists.append(('Remove from MyFshare',{'query':'Remove','mode':11}))
				lists.append(('Remove from MyFshare Favorite',{'query':'RemoveFavorite','mode':11}))
		#menu['MySearch']={'action':'Add','server':['xshare.vn']}
		if menu.has_key('MySearch'):
			inf=menu.get('MySearch')
			lists.append(('Rename item',{'query':'Rename','mode':9}))
			lists.append(('Remove item',{'query':'Remove','mode':9}))
		if menu.has_key('tuphim'):#menu={'tuphim':{'action':'Add','server':['phimmoi.net']}}
			inf=menu.get('tuphim')
			if inf['action']=='Add':
				lists.append(('Add to Tủ phim của tôi',{'query':'tuphim_Add'}))
			elif inf['action']=='Remove':
				lists.append(('Remove from Tủ phim của tôi',{'query':'tuphim_Remove'}))
		return lists
	def add_menu(url):
		#lists=list()
		menu={'muctheodoi':{'action':'Add','server':['hdvietnam.com']}}
		menu['MyFshare']={'action':'Add','server':['fshare.vn']}
		menu['MyFavourites']={'action':'Add','server':['fshare.vn','4share.vn','tenlua.vn','subscene.com']}
		'''if 'fshare.vn/' in url:
			lists.append(('Add to MyFshare',{'query':'Add','mode':11}))
			lists.append(('Add to MyFshare Favorite',{'query':'AddFavorite','mode':11}))
			lists.append(('Add to MyFavourites',{'query':'Add','mode':98}))
			lists.append(('Add to Mylist.xml',{'query':'Add','mode':12}))
			lists.append(('Add to MySearch',{'query':'Add','mode':13}))
		return list
		'''
		return menu
		
	if '18+' in name and myaddon.getSetting('phim18')=="false":return
	server_mode=['fshare.vn','4share.vn','tenlua.vn','subscene.com','vaphim.com','phimfshare.com','hdvietnam.com']
	if mode not in [2,13] and [s for s in server_mode if s in url]:name,url,mode,isFolder=get_mode(url,name,mode)
	if not fanart:fanart=joinpath(home,'fanart.jpg')
	if not info:info={"title":name}
	if not art:art={"fanart":fanart}
	item=xbmcgui.ListItem(label=name,iconImage=img,thumbnailImage=img)
	item.setInfo(type="Video",infoLabels=info);item.setArt(art)
	if not isFolder:item.setProperty('IsPlayable', 'true')
	li='%s?name=%s&url=%s&img=%s&fanart=%s&mode=%d&page=%d&query=%s'
	li=li%(sys.argv[0],xquote(name),xquote(url),xquote(img),xquote(fanart),mode,page,xquote(query))
	if not menu:menu=add_menu(url)
	menu=get_menu(menu,url)
	if menu:
		cmd='RunPlugin(plugin://%s/?'%myaddon.getAddonInfo('id');items=list()
		for label,info in menu:#menu=[(label,{'query':x,...})]
			if info.has_key('name'):name=info.get('name')
			if info.has_key('url'):url=info.get('url')
			if info.has_key('img'):img=info.get('img')
			if info.has_key('fanart'):fanart=info.get('fanart')
			if info.has_key('mode'):mode=info.get('mode')
			if info.has_key('page'):page=info.get('page')
			query=info.get('query')
			command=cmd+'&name=%s&url=%s&img=%s&fanart=%s&mode=%d&page=%d&query=%s)'
			command=command%(xquote(name),xquote(url),xquote(img),xquote(fanart),mode,page,xquote(query))
			if 'Remove' in query:label='[COLOR red]%s[/COLOR]'%label
			else:'[COLOR lime]%s[/COLOR]'%label
			items.append(('[COLOR lime]%s[/COLOR]'%label,command))
		item.addContextMenuItems(items)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),li,item,isFolder)

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

try:#Container.SetViewMode(num) addir:name,link,img,fanart,mode,page,query,isFolder
	myfolder=s2u(myaddon.getSetting('thumuccucbo'))
	if not os.path.exists(myfolder):myfolder=joinpath(datapath,'myfolder')
except:myfolder=joinpath(datapath,'myfolder')
thumucrieng=''.join(s for s in myaddon.getSetting('thumucrieng').split()).upper()
if not thumucrieng or len(thumucrieng)<10:thumucrieng='RDA4FHXVE2UU'
thumucrieng='https://www.fshare.vn/folder/'+thumucrieng
subsfolder=joinpath(tempfolder,'subs');xsharefolder=os.path.join(tempfolder,'xshare')
params=get_params();mode=page=0;temp=[];url=name=fanart=img=date=query=action=end=''

try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:img=urllib.unquote_plus(params["img"])
except:pass
try:fanart=urllib.unquote_plus(params["fanart"])
except:pass
try:mode=int(params["mode"])
except:pass#xbmc.executebuiltin("Container.Refresh")
try:page=int(params["page"])
except:pass#xbmc.executebuiltin("Container.Update")
try:query=urllib.unquote_plus(params["query"])
except:pass#urllib.unquote

print "Main---------- Mode: "+str(mode),"URL: "+str(url),"Name: "+str(name),"query: "+str(query),"page: "+str(page)
if not mode:#xbmc.executebuiltin("Dialog.Close(all, true)")
	init_file();open_category("MMN");endxbmc()
	if myaddon.getSetting('checkdatabase')=='true' or os.path.isfile(joinpath(data_path,'checkdatabase.txt')):
		database_download()
	if checkupdate('xshare_auto_update.dat',5,datapath):
		makerequest(joinpath(datapath,"xshare_auto_update.dat"),'','w')
		xshare_auto_update();delete_files(tempfolder)
elif mode==1:end=vaphim(name,url,img,fanart,mode,page,query)
elif mode==2:end=google_search(url,query,mode,page)
elif mode==3:end=resolve_url(url)
elif mode==4:vp_phimmoi()
elif mode==5:vp_xemnhieu()
elif mode==6:end=phimFshare(name,url,img,fanart,mode,page,query)
elif mode==7:end=fptplay(name,url,img,mode,page,query)
elif mode==8:end=hdvietnam(name,url,img,fanart,mode,page,query)
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
elif mode==21:vuahd(name,url,img,fanart,mode,page,query)
elif mode==22:hdviet(name,url,img,mode,page,query)
elif mode==23:end=hayhaytv(name,url,img,fanart,mode,page,query)
elif mode==24:phimmoi(name,url,img,mode,page,query)
elif mode==25:search_get_page(name,url,img,fanart,mode,page,query)
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
if not end or end not in 'no-ok-fail':endxbmc()
