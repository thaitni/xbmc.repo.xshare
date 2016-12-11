# -*- coding: utf-8 -*-
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,urllib,urllib2,re,os,unicodedata,datetime,time,random,json

myaddon=xbmcaddon.Addon()
home=xbmc.translatePath(myaddon.getAddonInfo('path'))
addonDataPath=xbmc.translatePath(myaddon.getAddonInfo('profile'))
iconpath=os.path.join(addonDataPath,'icon')
datapath=os.path.join(addonDataPath,'data')
libPath=os.path.join(home,'resources','lib')
sys.path.append(libPath);from urlfetch import get,post
search_file=os.path.join(datapath,"search.xml");data_path=os.path.join(home,'resources','data')
try:rows=int(myaddon.getSetting('sodonghienthi'))
except:rows=30
tempfolder=xbmc.translatePath('special://temp');phim18=myaddon.getSetting('phim18')
xbmcplugin.setContent(int(sys.argv[1]), 'movies');homnay=datetime.date.today().strftime("%d/%m/%Y")
from resources.lib.utils import mess,xsearch,xreadc,xrw,s2c,vnu,filetime,ls,rsl,googleItems,xcheck,xselect,siteName,xget

media_ext=['aif','iff','m3u','m3u8','m4a','mid','mp3','mpa','ra','wav','wma','3g2','3gp','asf','asx','avi','flv','mov','mp4','mpg','mkv','m4v','rm','swf','vob','wmv','bin','cue','dmg','iso','mdf','toast','vcd','ts','flac','m2ts','dtshd','nrg'];icon={}
color={'fshare':'[COLOR gold]','vaphim':'[COLOR gold]','phimfshare':'[COLOR khaki]','4share':'[COLOR blue]','tenlua':'[COLOR fuchsia]','fptplay':'[COLOR orange]','trangtiep':'[COLOR lime]','search':'[COLOR lime]','ifile':'[COLOR blue]','hdvietnam':'[COLOR red]','hdviet':'[COLOR darkorange]','xshare':'[COLOR blue]','subscene':'[COLOR green]','chiasenhac':'[COLOR orange]','phimmoi':'[COLOR ghostwhite]','megabox':'[COLOR orangered]','dangcaphd':'[COLOR yellow]','hayhaytv':'[COLOR tomato]','kenh88':'[COLOR cyan]','phimdata':'[COLOR FFDB4BDA]','phim47':'[COLOR springgreen]','phimsot':'[COLOR orangered]','hdonline':'[COLOR turquoise]','phim3s':'[COLOR lightgray]','kphim':'[COLOR lightgreen]','phimnhanh':'[COLOR chartreuse]','bilutv':'[COLOR hotpink]','pubvn':'[COLOR deepskyblue]','anime47':'[COLOR deepskyblue]','phim14':'[COLOR chartreuse]','taifile':'[COLOR cyan]','phim':'[COLOR orange]','tvhay':'[COLOR gold]','nhacdj':'[COLOR fuchsia]','phimbathu':'[COLOR lightgray]','taiphimhd':'[COLOR blue]','hdsieunhanh':'[COLOR orangered]','vuahd':'[COLOR tomato]','nhaccuatui':'[COLOR turquoise]','imovies':'[COLOR orange]','vietsubhd':'[COLOR cyan]','imax':'[COLOR chartreuse]','mphim':'[COLOR deepskyblue]','vtvgo':'[COLOR green]','youtube':'[COLOR red]','fcine':'[COLOR gold]','taiphimhdnet':'[COLOR teal]','vungtv':'[COLOR FF228B22]','biphim':'[COLOR FFBA55D3]','banhtv':'[COLOR FFF08080]'}
for hd in ['xshare','4share','dangcaphd','downsub','favorite','fptplay','fshare','gsearch','hdvietnam','icon','id','ifiletv','ifile','isearch','khophim','maxspeed','megabox','movie','msearch','myfolder','myfshare','phimfshare','serverphimkhac','setting','tenlua','vaphim','hdviet','hayhaytv','chiasenhac','kenh88','phimdata','phim47','phimsot','hdonline','phim3s','kphim','phimnhanh','bilutv','anime47','phim14','taifile','phim','tvhay','nhacdj','phimbathu','taiphimhd','hdsieunhanh','phimmoi','vuahd','pubvn','nhaccuatui','imovies','vietsubhd','imax','mphim','vtvgo','youtube','fcine','taiphimhdnet','vungtv','banhtv','biphim']:
	icon.setdefault(hd,os.path.join(iconpath,'%s.png'%hd))
hd={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/600.1.4 Gecko/20100101 Firefox/41.0'}

def log(s):xbmc.log(u2s(s))

def mess_yesno(title='[COLOR green]Xshare[/COLOR]', line1='', line2='',no='No',yes='Yes'):
	dialog=xbmcgui.Dialog()#dialog.yesno(heading, line1[, line2, line3,nolabel,yeslabel])
	return dialog.yesno(title,line1,line2,nolabel=no,yeslabel=yes)

def no_accent(s):
	s=re.sub(u'Đ','D',s2u(s));s=re.sub(u'đ','d',s)
	return unicodedata.normalize('NFKD', unicode(s)).encode('ASCII', 'ignore')

def resolu(s):
	s=s.replace('HDG','').replace('HD','1080').replace('SD','640').replace('large','640').replace('medium','480').replace('small','360')
	result=xsearch('(\d+)',s)
	return result if result else '240'

def dl(l):#Direct link
	o=make_request(l,resp='o',maxr=5);h=''
	try:s=int(o.headers.get('content-length'))
	except:s=0
	s=0 if s<10**7 else s
	if s and o.history:h=o.history[-1].headers['location']
	elif s:h=l
	return h

def test_link(urls):
	def test(url):
		try:o=urllib2.urlopen(url);link=o.geturl();o.close()
		except:link=''
		return link
	if isinstance(urls, list):
		link=''
		for href,label in urls:
			link=test(href)
			if link:break
	else:link=test(urls)
	return link

def gdl(l,link=''):
	if type(l)==list:
		for href,label in l:
			link=dl(href)
			if link:break
	else:link=l
	return link

def fptisp():
	if filetime('fptisp.txt')>240:
		try:fptISP='FPT' in json.loads(xread('http://ip-api.com/json')).get('isp')
		except:fptISP=False
		xrw('fptisp.txt','yes' if fptISP else 'no')
	return xrw('fptisp.txt')=='yes'

def s2u(s):return s.decode('utf-8') if isinstance(s,str) else s
def unescape(string):return ' '.join(re.sub('&.+;',xsearch('&(\w).+;',s),s) for s in string.split())
def u2s(s):return s.encode('utf-8') if isinstance(s,unicode) else s
def jp(mydict):print json.dumps(mydict,indent=2)
def add_sep_item(label):addir_info('[COLOR lime]%s[/COLOR]'%label,'',icon['xshare'],'',100,1,'No')
def labelsearch(label):return '%s%s[/COLOR]'%(color['search'],label)
def namecolor(name,c=''):return '[COLOR %s]%s[/COLOR]'%(c,name) if c else re.sub('\[[^\[]+?\]','',name)
def xhref(s,p=''):return xsearch('href="(.+?)"',s,result=xsearch(p,s))
def xtitle(s,p=''):return ' '.join(xsearch('title="(.+?)"',s,result=xsearch(p,s)).split())
def ximg(s,p=''):return xsearch('src="(.+?)"',s,result=xsearch(p,s))
def getHome(fn,url):return xrw(fn,xread(url)) if filetime(fn) > 1 else xrw(fn)
def getcHome(fn,url,hd={'User_Agent':'Mozilla/5.0'},data='',c=''):
	return xrw(fn,xreadc(url,hd,data,c)) if filetime(fn) > 1 else xrw(fn)
def preTitle(s,title):
	if re.search('.huyết .inh',s):title='[COLOR cyan]TM[/COLOR] '+title
	elif re.search('.ồng .iếng',s):title='[COLOR cyan]LT[/COLOR] '+title
	return title

def hideMenuItem(page):
	if page==0:s=xrw('menuhided.txt',' ')
	else:
		s=xrw('menuhided.txt')
		try:modes=[eval(i) for i in s.split(',') if re.ssearch('\d',i)]
		except:modes=[]
		xrw('menuhided.txt',str(page) if not s else '%s,%d'%(s,page))
	xbmc.executebuiltin("Container.Refresh")

def open_category(query): #category.xml
	if query=='MMN':root=True
	else:root=False
	pattern='<a server="(.+?)" category="(.+?)" mode="(\d+)" color="(.*?)" icon="(.*?)">(.+?)</a>'
	items=re.findall(pattern,makerequest(joinpath(data_path,'category.xml')))
	q='';fanart=home+'/fanart.jpg'
	haidePhim18=myaddon.getSetting('phim18')=="false"
	menuhided=[eval(i) for i in xrw('menuhided.txt').split(',') if re.search('\d',i)]
	for server,category,mode,colo,icon,name in items:
		try:mode=int(mode)
		except:mode=0
		if (server!=query) or (("18" in category) and haidePhim18) or mode in menuhided:continue
		if query=='VPH' and mode!=10:q='vaphim.xml'
		elif query=='IFI' and mode!=10:q='ifiletv.xml'
		else:q=category
		name='[COLOR '+colo+']'+name+'[/COLOR]';icon=joinpath(iconpath,icon)
		addir(name,category,icon,fanart,mode,0,q,isFolder=(mode!=16),root=root)
	if q=='vaphim.xml':
		body=makerequest(joinpath(datapath,"vp_menu.txt"));icon=joinpath(iconpath,'vaphim.png')
		if not body:mess(u'Đang update menu...','vaphim.com');return#vp_make_datanew();return
		for query,name in eval(body):
			if "18" in name and haidePhim18:continue
			addir('%s%s[/COLOR]'%(color['vaphim'],name),'vaphim.xml',icon,fanart,92,1,query,True,root=root)
	if query=='MMN' and (myaddon.getSetting('my_nas_url')!="http://buffalonas.com/"):
		addir('[COLOR lime]My NAS[/COLOR]','',os.path.join(iconpath,'csn.png'),fanart,52,1,'home',True,root=root)

def servers_list(name,url,img,fanart,mode,page,query):#88
	def make_ls(s,context=''):
		menuhided=[eval(i) for i in xrw('menuhided.txt').split(',') if re.search('\d',i)]
		i=0;l=len(s)
		for domain,MODE,color in s:#sl:server location
			mode=int(MODE)
			if mode in menuhided:continue
			title=namecolor('Kho phim trên %s'%domain,color);i+=1
			if i==1:menu={'servers_list':{'action':'Down'+context}}
			elif i<l:menu={'servers_list':{'action':'Up-Down'+context}}
			else:menu={'servers_list':{'action':'Up'+context}}
			ico=joinpath(iconpath,domain.split('.')[0]+'.png')
			addir_info(title,domain,ico,'',mode,1,domain,True,menu=menu)
	
	from resources.lib.servers import serversList;srvs=serversList()
	menu={'servers_list':{'action':'Up-Down'}}
	if query=='FRE':
		title='[COLOR lime]Search trên toàn bộ cụm "Các servers khác"[/COLOR]'
		addir_info(title,'xshare.vn',icon['xshare'],'',mode,1,'search',True)

		s=srvs.mylist();l=len(s)
		for i in range(l/10+(1 if l%10>0 else 0)):
			title=namecolor('Servers group %d'%(i+1),'blue')
			addir_info(title,str(i),icon['xshare'],'',mode,1,'group',True)
		
		add_sep_item('All servers ------------------------------------------------')
		make_ls(s,'-ShowHide')
	
	elif query=='group':
		s=srvs.mylist();i=0;l=len(s)
		def mm(i):return i+10 if i+10<len(s) else i+len(s)%10
		make_ls([[s[i] for i in range(i,mm(i))] for i in range(0,len(s),10)][int(url)])
			
	elif query=="search":url="xshare.vn";make_mySearch('',url,'','',mode,'get')
	elif url=="xshare.vn" or query=="INP":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query:return 'No'
		
		string=urllib.quote_plus('"%s"'%' '.join(query.split()))
		if 'Page next:' in name:string+='&start=%d'%((page-1)*20)
		else:page=1
		
		def labelcolor():return namecolor(domain+' '+title,c)
		def labelnocolor():return domain+' '+title
		for title,href,img in srvs.search(string):
			domain=href.split("//")[-1].split("www.")[-1].split("/")[0]
			c=srvs.color(domain)
			MODE=srvs.mode(domain)
			if (MODE==0 and 'Page next:' not in title) or not urllib2.os.path.basename(href):continue
			if domain!='phim.media':domain=domain.split('.')[0]
			
			if 'bilutv.com' in href:
				title=re.sub('Tập \d+ |tập \d+ ','',title)
				if '/tag/' in href:addir_info(labelcolor(),href,img,'',MODE,1,'page',True)
				elif 'phim/' in href:addir_info(labelcolor(),href,img,'',MODE,1,'folder',True)
				else:addir_info(labelcolor(),href,img,'',MODE,1,'eps',True)
			
			elif 'hayhaytv.vn' in href:addir_info(labelcolor(),href,img,'',MODE,1,'eps',True)
			elif 'phimbathu.com' in href:addir_info(labelcolor(),href,img,'',MODE,1,'eps',True)
			
			elif 'phim47.com' in href:
				if '/xem-online/' in href:addir_info(labelnocolor(),href,img,'',MODE,1,'p47_play')
				elif '/tag/' in href:addir_info(labelcolor(),href,img,'',MODE,1,'p47_getpage',True)
				else:addir_info(labelcolor(),href,img,'',MODE,1,"get_series",True)
				#addir_info(namecolor(domain+' '+title,'lightgray'),href,img,'',MODE,1,'episodes',True)
			
			elif 'phim14.net' in href:
				if '/tag/' in href:addir_info(labelcolor(),href,img,'',MODE,1,'p14_page',True)
				else:addir_info(labelnocolor(),href,img,'',MODE,1,'p14_eps',True)
			
			elif 'tvhay.org' in href:addir_info(labelcolor(),href,img,'',MODE,1,'eps',True)
			elif 'phim3s.net' in href:addir_info(labelcolor(),href,img,'',MODE,1,"get_server",True)
			elif 'hdonline.vn' in href:
				if '/tag1/' in href:addir_info(labelcolor(),href,img,'',MODE,1,"page",True)
				else:addir_info(labelcolor(),href,img,'',MODE,1,'eps',True)
			
			elif 'hdsieunhanh.com' in href:addir_info(labelcolor(),href,img,'',MODE,1,'play')
			elif 'fptplay.net' in href:addir_info(labelcolor(),href,img,'',MODE,1,'eps',True)
			elif 'imovies.vn' in href:
				if href.endswith('html'):addir_info(labelcolor(),href,img,'',MODE,1,'eps',True)
				else:addir_info(labelcolor(),href,img,'',MODE,1,'ajaxPage',True)
			elif 'phimnhanh.com' in href:addir_info(labelcolor(),href,img,'',MODE,1,'eps',True)
			elif 'mphim.net' in href:addir_info(labelcolor(),href,img,'',MODE,1,'eps',True)
			elif 'kenh88.com' in href:
				if '/xem-phim-online/' in href or '/phim/' in href:
					addir_info(labelcolor(),href,img,'',MODE,1,'episode',True)
				else:addir_info(labelcolor(),href,img,'',MODE,1,'k88_getpage',True)
			
			elif 'phim.media' in href:addir_info(labelcolor(),href,img,'',MODE,1,'series',True)
			elif 'kphim.tv' in href:
				q='theloai' if '/theloai/' in href else 'episode'
				addir_info(labelcolor(),href,img,'',MODE,1,q,True)
			
			elif 'phimmoi.net' in href:
				href=re.sub('/[^/]+\.html','/',href)
				addir_info(labelcolor(),href,img,'',MODE,1,'eps',True)
			
			elif 'vietsubhd.com' in href:addir_info(labelcolor(),href,img,'',MODE,1,'eps',True)
			elif 'phimdata.com' in href:addir_info(labelcolor(),href,img,'',MODE,1,'pdt_getpage',True)
			elif 'hdviet.com' in href:addir_info(labelcolor(),href,img,'',MODE,1,'eps',True)
			elif 'fcine.net' in href:
				if myaddon.getSetting('fcinefshare')=='true':
					title='[COLOR gold]Fshare[/COLOR] '+labelcolor()
					addir_info(title,href,img,'',MODE,1,'fshare',True)
				else:addir_info(labelcolor(),href,img,'',MODE,1,'play')
			elif 'vungtv.com' in href or 'biphim.com' in href or 'banhtv.com' in href:
				addir_info(labelcolor(),href,img,'',MODE,1,'eps',True)
			elif 'Page next:' in title:addir_info(title,url,icon['xshare'],'',mode,page+1,query,True)
			else:mess('Chưa xử lý link: '+href,'xshare.vn')
	
	else :step=-1 if query=='Up' else 1;srvs.move(url,step);xbmc.executebuiltin("Container.Refresh")

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

def xbmcsetResolvedUrl(url,name='',img='',sub=''):
	if 'youtube.com' in url:return play_youtube(url)
	elif img:item=xbmcgui.ListItem(path=url, iconImage=img, thumbnailImage=img)
	else:item=xbmcgui.ListItem(path=url)
	if 'Maxlink' in name:
		if name!='Maxlink':name=name.replace('Maxlink','');item.setInfo('video', {'Title':name})
		else:item.setInfo('video', {'Title':urllib.unquote(os.path.basename(url))})
		name=''
	if not url:xbmcplugin.setResolvedUrl(int(sys.argv[1]), False, item);return 'fail'
	elif sub:
		item.setSubtitles([sub])
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	else:
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
		if myaddon.getSetting('autoload_sub')=='true' and name!='xshare':
			if name:url=name
			urltitle=urllib.unquote(os.path.splitext(os.path.basename(url))[0]).lower()
			urltitle='.'+'.'.join(s for s in re.sub('_|\W+',' ',re.split('\d\d\d\d',urltitle)[0]).split())+'.'
			subfile='';items=[]
			for file in os.listdir(subsfolder):
				filefullpath=joinpath(subsfolder,file).encode('utf-8')
				filename=re.sub('vie\.|eng\.','',os.path.splitext(file)[0].lower().encode('utf-8'))
				filename=re.split('|'.join(str(i) for i in range(1930,2020)),filename)[0];count=0
				for word in re.sub('_|\W+',' ',filename).split():
					if '.%s.'%word in urltitle:count+=1
				if count:items.append((count,filefullpath))
			for item in items:
				if item[0]>=count:count=item[0];subfile=item[1]
			if subfile:
				xbmc.sleep(2000);xbmc.Player().setSubtitles(subfile)
				mess(u'%s'%s2u(os.path.basename(subfile)),'Auto load sub',5000)

def addir(name,link,img='',fanart='',mode=0,page=0,query='',isFolder=False,root=False):
	def xquote(href):return urllib.quote_plus(href)
	if '18+' in name and phim18=="false":return
	name=unescape(re.sub(',|\|.*\||\||\<.*\>','',u2s(name)))
	item=xbmcgui.ListItem(name,iconImage=img,thumbnailImage=img)

	if not root:
		label='[COLOR lime]Add to My Favourites[/COLOR]'
		q='Add-'+(query.split('?')[1] if '?' in query else query)+'-'+('F' if isFolder else '')
		cmd='RunPlugin(plugin://%s/?'%myaddon.getAddonInfo('id')#;items=list()
		cmd=cmd+'name=%s&url=%s&img=%s&fanart=%s&mode=%d&page=%d&query=%s)'
		cmd=cmd%(xquote(name),xquote(link),xquote(img),xquote(fanart),100+mode,page,xquote(q))
		command=[(label,cmd)]
	elif 'My Favourites' not in name:
		label='[COLOR lime]Hide this item[/COLOR]'
		cmd='RunPlugin(plugin://%s/?'%myaddon.getAddonInfo('id')
		cmd=cmd+'name=HideXshareMainMenuItem&page=%d)'%mode
		command=[(label,cmd)]
		label='[COLOR lime]Show all Xshare Main Menu items[/COLOR]'
		cmd='RunPlugin(plugin://%s/?'%myaddon.getAddonInfo('id')
		cmd=cmd+'name=HideXshareMainMenuItem&page=0)'
		command.append((label,cmd))
	else:command=[]
	
	query=menuContext(name,link,img,fanart,mode,query,item,command)
	item.setInfo(type="Video", infoLabels={"title":name})
	if not fanart:fanart=joinpath(home,'fanart.jpg')
	item.setProperty('Fanart_Image',fanart)
	li='%s?name=%s&url=%s&img=%s&fanart=%s&mode=%d&page=%d&query=%s'
	li=li%(sys.argv[0],xquote(name),xquote(link),xquote(img),xquote(fanart),mode,page,xquote(query))
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
	elif 'youtube.com/watch?v=' in href:
		name=namecolor('Youtube','red')+' '+namecolor(name,'deepskyblue')
		addir(name,href,img,fanart,mode=98,query=query,isFolder=False)

def menuContext(name,link,img,fanart,mode,query,item,command=[]):
	if query.split('?')[0]=='Search':
		query=query.split('?')[1]
		command+=searchContext(name,link,img,fanart,mode)
	elif query.split('?')[0]=='ID':
		query=query.split('?')[1]
		command+=searchContext(name,link,img,fanart,15)
		command+=favouritesContext(name,link,img,fanart,mode)
	elif 'fshare.vn' in link or '4share.vn' in link or 'tenlua.vn' in link:#mode in (3,38,90,95):
		command+=favouritesContext(name,link,img,fanart,mode)
	elif myfolder in s2u(link):
		command+=make_myFile(name,link,img,fanart,mode,query)
	elif query in 'hdvietfolder-hdv_play':
		command+=hdvietContext(name,link,img,fanart,mode)
	item.addContextMenuItems(command)
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
	#else:makecmd(98,'Add to MyFavourites')
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
	if url=='https://fptplay.net/livetv':searchfile=os.path.join(datapath,"channel.xml");srv='fptplay'
	else :searchfile=os.path.join(datapath,"search.xml");srv=url.split('.')[0]
	body=makerequest(searchfile)
	
	if query=='Rename':
		label=' '.join(s for s in name.split())
		string=get_input('Nhập chuổi mới',re.sub('\[.*\]-','',label)).strip()
		if not string or string==label:return
		string=' '.join(s for s in string.split())
		if url!='https://fptplay.net/livetv' and re.search('http.?://',url):
			content=re.sub('<a href="%s">.+?</a>\n'%url,'<a href="%s">%s</a>\n'%(url,string),body)
		else:content=body.replace(name,string)
		if body!=content:
			makerequest(searchfile,content,'w')
			mess(u'Sửa 1 mục thành công');xbmc.executebuiltin("Container.Refresh")
	elif query=='Remove':
		name=re.sub('\(|\)|\[|\]|\{|\}|\?|\,|\+|\*','.',name)
		content=re.sub('<a href="%s">.+?</a>\n|<a>%s</a>\n'%(url,name),'',body)
		if body!=content:
			makerequest(searchfile,content,'w')
			if img!='schedule':mess(u'Xóa 1 mục thành công');xbmc.executebuiltin("Container.Refresh")
	elif query=='Remove All':
		content=re.sub('<a href=".+?">.+?</a>\n','',body)
		if body!=content:
			makerequest(searchfile,content,'w')
			mess(u'Xóa tất cả các mục thành công');xbmc.executebuiltin("Container.Refresh")
	elif query=='Add':
		if url and not re.search(url,body):makerequest(searchfile,'<a href="%s">%s</a>\n'%(url,name),'a')
	elif query=='Input':
		if "channel.xml" in searchfile:query = get_input('Nhập chuổi tên Kênh cần tìm')
		else:query = get_input('Nhập chuổi tên phim cần tìm trên %s'%url)
		attr='a'
		if query:
			if "channel.xml" in searchfile:query= query.upper()
			query = ' '.join(s for s in query.replace('"',"'").replace('?','').split() if s!='')
			if '<a>%s</a>\n'%query not in body:
				makerequest(searchfile,'<a>%s</a>\n'%query,'a')#;xbmc.executebuiltin("Container.Refresh")
		else:query=''
	elif query=='get':
		site='Google ' if mode==2 else ''
		q=''
		if url=='chiasenhac.vn':
			q='a' if ']Tất Cả[' in name else 'v' if ']Videos[' in name else 'm'
			menu={'MyPlaylist':{'action':'Search','server':['chiasenhac.vn']}}
			label=name.split('-')[0]+'[COLOR gold]%s[/COLOR] - Nhập chuổi mới'%myaddon.getSetting('csn_s')
			addir_info(label,url,icon[srv],'',mode,1,q+'INP',True,menu=menu)
		elif "channel.xml" in searchfile and name=='channel':
			href='https://fptplay.net/livetv'
			addir_info(namecolor('Nhập tên kênh tìm kiếm','lime'),href,icon['xshare'],'',mode,1,'CHN',True)
		elif "channel.xml" in searchfile and name=='schedule':
			addir_info(namecolor('Nhập tên kênh tìm kiếm Lịch phát sóng','lime'),'i',icon['xshare'],'',mode,1,'fptSchedule',True)
			url='https://fptplay.net/livetv'
		else:
			if url=='fcine.net':q=name
			elif name=='searchFollow':
				name='[COLOR lime]Search trên [COLOR gold]Fshare Following[/COLOR][/COLOR][COLOR cyan] Nhập chuỗi tìm kiếm mới[/COLOR]'
			else:
				name='%s%sSearch[/COLOR] trên %s%s[/COLOR] Nhập chuỗi tìm kiếm mới'
				name=name%(color['search'],site,color[srv],url)
			addir_info(name,url,icon[srv],'',mode,1,q+'INP',True)
		menu={'MySearch':{'action':'Add','server':['xshare.vn'],'url':url}}
		if myaddon.getSetting('history')=='true':
			if "channel.xml" in searchfile and name=='schedule':url='getSchedule'
			for s in re.findall('<a>(.+?)</a>',body):addir_info(s,url,icon[srv],'',mode,4,q+s,True,menu=menu)
	return query

def make_myFshare(name,url,img,fanart,mode,query):#11
	def nameClean(s):
		return ' '.join(re.sub('\[/?COLOR.*?\]|\\\|/|:|\*|\?|\<|\>|\!|,|\@|\"|--|\.\.|\#|\$|\%|\^|\|','',s).split())
	
	myFshare=myaddon.getSetting('thumucrieng')
	from resources.lib.servers import fshare
	if query=='Add':
		fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'),myFshare)
		name=nameClean(name);fs.myFshare_add(url,name);xbmc.sleep(1000)
	elif query=='Rename':
		fs=fshare();old_name=new_name='';
		new_name=get_input('Sửa tên 1 mục trong MyFshare',nameClean(name)).strip();new_name=nameClean(new_name)
		if not new_name or new_name==old_name:return
		else:new_name=url.split('/')[4].strip()+('FOLDER ' if 'folder' in url else 'FILE ')+new_name
		fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'),myFshare)
		if fs.myFshare_rename(url,new_name):xbmc.executebuiltin("Container.Refresh")
	elif query=='Remove':
		fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'),myFshare)
		if fs.myFshare_remove(url):xbmc.executebuiltin("Container.Refresh")
	elif query=='Upload':
		try:
			size=os.path.getsize(s2u(url));name=re.sub('\[/?COLOR.*?\]','',os.path.basename(url)).strip()
			if size>10*1024**2:mess(u'Add-on chưa hỗ trợ upload file>10MB!','myFshare');return
			f=open(s2u(url),'rb');content=f.read();f.close()
		except:mess(u'File read error','Fshare.vn');return
		fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'),myFshare)
		fs.myFshare_upload(name,size,content)
	elif query=='AddFavorite':
		fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'),myFshare)
		fs.Favorite_add(url)
	elif query=='RemoveFavorite':
		fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'),myFshare)
		if fs.Favorite_remove(os.path.basename(url)):xbmc.executebuiltin("Container.Refresh")
	if fs.logged:fs.logout()
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
		if maxr==0:response=get(url,headers=headers)#,timeout=2)
		else:response=get(url,headers=headers,max_redirects=maxr)#,timeout=2)
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
			link=xsearch('//(.{5,20}\.\w{2,3})',s2u(url))
			if not link:link=url
			mess(u'Lỗi kết nối tới: %s!'%xsearch('//(.{5,20}\.\w{2,3})',s2u(url)),'make_request')
		print 'Lỗi kết nối tới: %s!'%u2s(url);
	return resp#unicode:body=response.text

def make_post(url,headers=hd,data='',resp='o'):
	try:
		if data:response=post(url=url,headers=headers,data=data,timeout=10)
		else:response=post(url=url,headers=headers,timeout=10)
		if resp=='b':response=response.body
		elif resp=='j':response=response.json
	except:
		mess(u'Post link error: %s!'%s2u(url),'make_post');print 'Post link error: %s'%u2s(url)
		response={} if resp=='j' else ''
	return response

def xread(url,hd={'User-Agent':'Mozilla/5.0'},data=None):
	req=urllib2.Request(url,data,hd)
	try:res=urllib2.urlopen(req, timeout=20);b=res.read();res.close()
	except:b=''
	return b

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
	if keyboard.isConfirmed():result = keyboard.getText().strip()
	else:result = ''
	return result

def tenlua_get_detail_and_starting(id,headers=hd):
	data='[{"a":"filemanager_builddownload_getinfo","n":"%s","r":0}]'%id
	response=make_post('https://api2.tenlua.vn/',headers,data,resp='j')
	try:json=response[0]
	except:json={'type':'none'}
	return json

def resolve_url(url,xml=False,name=''):
	urltemp=url.lower()
	if 'fshare.vn' in urltemp:
		result=fshare_resolve('https://www.%s'%xsearch('(fshare.vn.+?)\Z',url),xml,name)
	elif '4share.vn' in urltemp:result=fourshare_resolve(url)
	elif 'tenlua.vn' in urltemp:result=tenlua_resolve(url,xml)
	else:result=url
	return result

def fshare_resolve(url,xml,name=''):
	from resources.lib.servers import fshare
	fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'))
	sleep=2000
	for loop in range(3):
		if loop>0:mess(u'Get link lần thứ %d'%(loop+1),'fshare.vn')
		direct_link=fs.get_maxlink(url)
		if direct_link and direct_link not in 'fail-noFile':break
		elif direct_link=='noFile':direct_link='fail';break
		else:xbmc.sleep(sleep);sleep+=1000
	
	if fs.logged:fs.logout()
	if not direct_link:mess('Sorry! Potay.com','fshare.vn');return 'fail'
	elif direct_link in 'notfound-fail':return 'fail'
	elif xml:return direct_link
	else:
		name='Maxlink' if '/www.fshare.vn/' in name else ''
		return xshare_resolve(direct_link,os.path.splitext(direct_link)[1][1:].lower(),name)

def fourshare_resolve(url):
	hd['Cookie']=login4share()
	if not hd['Cookie']:return 'fail'#login fail
	response=xread(url,hd);logout_site(hd['Cookie'],url)
	if not response:xbmc.sleep(2000);return 'fail'
	direct_link=xsearch("<a style='text-decoration:none' href='(.+?)'>",response)
	if not direct_link:
		direct_link=xsearch("Link Download.+?href='(.+?4share.vn.+?)'>",response)
		if not direct_link:
			direct_link=xsearch("'http.+\?info=.+)'",response)
			if not direct_link:
				mess(u'Không get được maxspeed link!','resolve_url');return 'fail'
	ext=os.path.splitext(xsearch('<title>(.+?)</title>',response))[1][1:].lower()
	return xshare_resolve(direct_link,ext)

def fourshare_resolve1(url):
	hd['Cookie']=login4share()
	if not hd['Cookie']:return 'fail'#login fail
	response=make_request(url,hd,resp='o');logout_site(hd['Cookie'],url)
	if not response or response.status!=200:xbmc.sleep(2000);return 'fail'
	direct_link=xsearch("<a style='text-decoration:none' href='(.+?)'>",response.body)
	if not direct_link:
		direct_link=xsearch("Link Download.+?href='(.+?4share.vn.+?)'>",response.body)
		if not direct_link:
			direct_link=xsearch("'http.+\?info=.+)'",response.body)
			if not direct_link:
				mess(u'Không get được maxspeed link!','resolve_url');return 'fail'
	ext=os.path.splitext(xsearch('<title>(.+?)</title>',response.body))[1][1:].lower()
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
	response=make_request(dlink,hd,resp='o');logout_site(hd['Cookie'],url)
	if response and response.status==302:return xshare_resolve(response.headers['location'],ext)
	else:mess(u'Không get được max speed link!','resolve_url');return 'fail'

def xshare_resolve(direct_link,ext='',filmlabel=''):
	def get_detail_maxlink(direct_link):
		response=make_request(direct_link,{'User-Agent':'xshare'},resp='o',maxr=3)
		if not response:return 'fail'
		detail=response.headers
		size=int(detail.get('content-length',0))
		filename=detail.get('content-disposition','').split('=')
		if len(filename)>1:filename=filename[1].replace('"','').replace("'","")
		else:filename=os.path.basename(direct_link)
		ext=os.path.splitext(filename)[1][1:].lower()
		return response,size,filename,ext
	
	if ext in media_ext:xbmcsetResolvedUrl(direct_link,filmlabel);return ''
	
	response,size,filename,ext=get_detail_maxlink(direct_link)
	if ext in 'xml':result=doc_list_xml(direct_link,'list_xml')
	elif ext in media_ext or filmlabel:xbmcsetResolvedUrl(direct_link,filmlabel);result=''
	elif ext in ['rar','zip','srt','sub','txt','smi','ssa','ass','nfo']:
		result=xshare_download(response,size,filename,ext)
	elif not ext:mess('sorry! this is not a media file','Check media extention');result='fail'
	else:xbmcsetResolvedUrl(direct_link);result=''
	#mess('sorry! this is not a media file','xshare resolve');result='fail'
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
					filetemp=xshare_trans(filefullpath,filefullpath)
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

def xshare_trans(fs,fd):
	def trans(s):
		try:s=s.decode('unicode_escape') if '\\' in s else s.decode('utf-8')
		except:pass
		return s

	f=open(fs);b=f.read();f.close();s='';S=''
	u='https://translate.googleapis.com/translate_a/single?ie=UTF-8&oe=UTF-8&client=gtx&sl=en&tl=vi&dt=t&q=%s'
	list_1=b.splitlines();list_2=[];rows=len(list_1);row=0
	hd={'Referer':'https://translate.google.com/','User-Agent':'Mozilla/5.0 (Windows NT 6.3) Chrome/49.0.2623.112 Safari/537.36','Cookie':''}
	for i in list_1:
		row+=1
		if re.search('[a-zA-Z]',i):s=s+' '+i+' xshare';list_2.append('xshare')
		else:list_2.append(i.strip())
		if len(s)>1000 or row==rows:
			mess(u'Google đã dịch %d %%'%(row*100/rows), timeShown=1500)
			s=' '.join(i for i in s.split())
			tran=make_request(u%urllib.quote(s),headers=hd,resp='o')
			if not hd['Cookie']:hd['Cookie']=tran.cookiestring
			xbmc.sleep(1000)#;print tran.body
			try:
				l=eval(tran.body.replace(',,,',',').replace(',,"en"',''))
				S=S+' '.join(i[0] for i in l[0])
			except:xbmc.executebuiltin("Dialog.Close(all, true)");return ''
			s=''
	s=' '.join(trans(i) for i in S.split())
	list_3=s.split('xshare');d=0;f=open(fd,'w')
	f.write('0\n00:00:00,000 --> 00:01:30,000\n[COLOR gold]Xshare dich Anh-->Viet bang Google translate[/COLOR]\n\n')
	for i in list_2:
		try:
			if i=='xshare':f.write(list_3[d].strip().encode('utf-8')+'\n');d+=1
			else:f.write(i+'\n')
		except:pass
	f.close();xbmc.executebuiltin("Dialog.Close(all, true)")
	return fd

def logout_site(cookie,url):
	def logout(cookie,url,site):
		hd['Cookie']=cookie
		mess(u'Logout %s %sthành công'%(site,'' if make_request(url,hd,resp='s')==302 else u'không '))
	if cookie and myaddon.getSetting('logoutf')=="true":
		if 'fshare.vn' in url.lower():logout(cookie,'https://www.fshare.vn/logout','Fshare.vn')
		elif '4share.vn' in url.lower():logout(cookie,'http://4share.vn/default/index/logout','4share.vn')
		elif 'dangcaphd.com' in url.lower():logout(cookie,'http://dangcaphd.com/logout.html','dangcaphd.com')
		elif 'tenlua.vn' in url.lower():logouttenlua(cookie)

def login4share(headers=hd):
	form_fields = {"username":myaddon.getSetting('username4'),"password":myaddon.getSetting('password4')}
	response=make_post('http://up.4share.vn/index/login',headers,form_fields)
	if response and response.status==302:mess(u'Login thành công','4share.vn');f=response.cookiestring
	else:mess(u'Login không thành công!','4share.vn');f=''
	return f

def logintenlua(headers=hd):
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

def google_search(url,query,mode,page,items=[]):
	srv=url.split('.')[0]
	if page==0:make_mySearch('',url,'','',mode,'get');return
	elif page==1:
		query=make_mySearch('',url,'','','','Input');page=2
		if query is None or not query.strip():return 'no'
	query=no_accent(query)
	
	from resources.lib.servers import googlesearch;ggs=googlesearch()
	if url in ('fshare.vn','vaphim.com'):
		if '*#*' in query:start=query.split('*#*')[1];query=query.split('*#*')[0]
		else:start='0'
		for title,href,img in ggs.content('009789051051551375973:xekpkwarjri',start,query):
			if 'Page next:' in title:
				page=img;start=href;query=query+'*#*'+start
				addir_info(title,url,icon['fshare'],'',mode,page,query,True)
			elif 'fcine.net' in href:
				menu={'fcine':{'name':title,'action':'fcinefshare','mode':mode}}
				title='[COLOR orangered]fcine[/COLOR] '+title
				addir_info(title,href,img,'',25,1,'fshare',True,menu=menu)			
			elif 'taiphimhd.net' in href:
				title='[COLOR FF1E90FF]taiphimhd[/COLOR] '+title
				addir_info(title,href,img,img,34,1,'link',True)
			else:
				if 'fshare.vn' in href:img=icon['fshare']
				addir_info(title,href,img,'',1,1,'vp_getsubpage')
	
	elif url in ('4share.vn','ifile.tv'):
		if '*#*' in query:start=query.split('*#*')[1];query=query.split('*#*')[0]
		else:start='0'
		for title,href,img in ggs.content('009789051051551375973:a1qafjesmlc',start,query):
			if 'Page next:' in title:
				page=img;start=href;query=query+'*#*'+start
				addir_info(title,url,icon['4share'],'',mode,page,query,True)
			else:addir_info(title,href,icon['4share'])
	
	elif url=='hdvietnam.com':
		if '*#*' in query:start=query.split('*#*')[1];query=query.split('*#*')[0]
		else:start='0'
		for title,href,img in ggs.content('009789051051551375973:hzgiaiqusl0',start,query):
			if 'Page next:' in title:
				page=img;start=href;query=query+'*#*'+start
				addir_info(title,url,icon['hdvietnam'],'',mode,page,query,True)
			else:
				if 'taiphimhd.com' in href:q='page';m=53;title=namecolor('TPHD '+remove_tag(title),'blue')
				elif 'i-max.vn' in href:
					m=49;title=namecolor('i-max '+remove_tag(title),'chartreuse')
					if xsearch('t=(\d+)',href):
						href='http://i-max.vn/forum/showthread.php?t='+xsearch('t=(\d+)',href);q='thread'
					elif xsearch('f=(\d+)',href):
						href='http://i-max.vn/forum/forumdisplay.php?f='+xsearch('f=(\d+)',href);q='category'
					elif xsearch('p=(\d+)',href):
						href='http://i-max.vn/forum/showthread.php?p='+xsearch('p=(\d+)',href);q='thread'
					else:print 'i-max link other------------------'+href;continue
				else:
					if '/threads/' in href or 'showthread.php' in href:q='threads';m=1
					else:q='forums';m=1
				addir_info(title,href,icon['hdvietnam'],'',m,1,q,True)
	
	elif url=='tenlua.vn':
		if '*#*' in query:start=query.split('*#*')[1];query=query.split('*#*')[0]
		else:start='0'
		for title,href,img in ggs.content('009789051051551375973:sg3wi6kqhay',start,query):
			if 'Page next:' in title:
				page=img;start=href;query=query+'*#*'+start
				addir_info(title,url,icon['tenlua'],'',mode,page,query,True)
			else:addir_info(title,href,icon['tenlua'])
	else:print url

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
	hd['Cookie']=makerequest(joinpath(xsharefolder,'vaphim.cookie'))
	pattern='<li class="post-(\d{4,6})(.+?)">.+?src="(.+?)".+?<h3 class="entry-title">'
	pattern+='<a href="(.+?)" rel="bookmark" >(.+?)</a>';items=[]
	if not body:body=xread(url,hd)
	for id,category,img,href,name in re.findall(pattern,body,re.DOTALL):
		category=' '.join(s.replace('category-','') for s in category.split() if 'category-' in s)
		if [s for s in ['game','video-clip','phn-mm','ebooks'] if s in category]:continue
		name=' '.join(s for s in re.sub('<.+?>|&.+?; ?','',name).split())
		items.append((id,name,href,img,category))
	return items

def vp_2fshare(url):#id,title,href,img,fanart,category
	hd['Cookie']=makerequest(joinpath(xsharefolder,'vaphim.cookie'))
	body=xread(url,hd)
	if not body:
		body=xread(url,hd)
		if not body:return list()
	
	items=list();id=xsearch("href='http://vaphim.com/\?p=(.+?)'",body)
	temp=xsearch('<div id=".+?" class="post-(.+?)">',body)
	category=' '.join(s.replace('category-','') for s in temp.split() if 'category-' in s)
	if not id or [s for s in category.split() if s in 'game video-clip phn-mm ebooks']:return items
	temp=xsearch('<title>(.+?)</title>',body)
	name=' '.join(s for s in re.sub('<.+?>|&.+?; ?|\||VaPhim.com','',temp).split())
	image=xsearch('meta property="og:image" content="(.+?)"',body)
	pattern='<a \w{4,6}=".*?(fshare.vn/f.l.?e?r?/.+?|http://subscene.+?)".{,18}>(.+?)</a><'
	if 'collection' not in category:
		content=xsearch('id="attachment_(.+?)"cf5_wpts_cl"',body,1,re.DOTALL)
		if not name:
			temp=xsearch('class="wp-caption-text">(.+?)<',content)
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
			title=xsearch('<strong>(.+?)</strong>(</span></p>|</p>|<br />)',content)
			if not title:title=xsearch('"wp-caption-text">(.+?)<',content)
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
	hd['Cookie']=makerequest(joinpath(xsharefolder,'vaphim.cookie'))
	body=xread('http://vaphim.com/huong-dan-lay-rss-cua-vaphim-com/',hd)
	names=re.findall('<li><a href=".+?" title=".+?">(.+?)<',body)
	if names:makerequest(joinpath(datapath,'vp_xemnhieu.txt'),str(names),'w')
	items=re.findall('<li><a href="/category.+?/([\w-]+?)/">(.+?)</a></li>',body)
	if items:makerequest(joinpath(datapath,"vp_menu.txt"),str(items),'w')
	body=xread('http://vaphim.com/',hd)
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

def doc_Trang4share(url,temp=[]):#38
	if '4share.vn/d/' in url:
		response=xread(url)
		if '[Empty Folder]' in response:mess('Folder is empty','4share.vn');return temp
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
		try:filenames=os.listdir(url)
		except:mess(u'Không đọc được tên file/folder tiếng Việt');return
		for filename in filenames:
			asa=joinpath(url, filename)
			filenamefullpath = u2s(joinpath(url, filename));filename=u2s(filename)
			try:size=os.path.getsize(joinpath(url, filename))/1024
			except:mess(u'Không đọc được tên file/folder tiếng Việt');continue
			if size>1024:size='%dMB'%(size/1024)
			else:size='%dKB'%size
			label=filename+' - %s'%size
			if os.path.isfile(joinpath(url, filename)):
				file_ext=os.path.splitext(filenamefullpath)[1][1:].lower()
				if file_ext in media_ext:
					item = xbmcgui.ListItem(label, iconImage=icon['khophim'])
					query=menuContext(label,filenamefullpath,'','',mode,query,item)
					xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=asa,listitem=item)
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
	token=xsearch('"(.+?)"',urllib.unquote(response.cookiestring))
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

def fsharePage(name,url,img,fanart,query=''):
	from resources.lib.servers import fshare
	if (not url and query=='searchFollow') or url==query=='fshare.vn':
		make_mySearch('searchFollow','fshare.vn','','',mode,'get')
	
	elif query=="INP" or url=='fshare.vn':
		if query=="INP":query=make_mySearch('',url,'','','','Input')
		if not query.strip():return
		elif 'Page next:' not in name:page=1
		fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'))
		q='+'.join(query.split())
		for title,href in fs.searchFollow(q):addir_info(title,href,img,'',mode,1,'')
	
	elif query=='searchFollow':
		title=namecolor('Search trên Fshare Following','lime')
		title+=namecolor(' (Có thể dùng dấu "." giữa các từ)','cyan')
		addir_info(title,'',img,'',mode,1,'searchFollow',True)
		fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'))
		for title,href in fs.searchFollow(''):addir_info(title,href,img,'',mode,1,'')
	
	else:
		if 'https://www.fshare.vn/files/' in url:
			fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'))
		else:fs=fshare()
		folder_detail=fs.get_folder(url)
		
		for title,href,iD,size,date in sorted(folder_detail.get('items'), key=lambda k: k[0]):
			if 'file' in href and len(size)>3:title+=' - size:%s'%size
			addirs(title,href,img,fanart,query+'xml' if '.xml' in title.lower() else query)
		if fs.logged:fs.logout()
		return folder_detail['pagename'] if folder_detail['items'] else 'no'

def id_2url(name,url,img,mode,page,query):
	def getInfo(link):
		def checker(link):
			href='http://vnz-leech.com/checker/check.php?links=%s'
			headers={'Referer':'http://vnz-leech.com/checker/','User-Agent':'xshare'}
			b=xread(href%urllib.quote_plus(link),headers)
			try:j=json.loads(b.replace('(','').replace(')',''))
			except:j={}
			def geti(j,i):return j.get(i,'').encode('utf-8')
			result='',''
			if j.get('status','')=='good_link':
				title='%s (%s)'%(geti(j,'filename'),geti(j,'filesize'))
				href=geti(j,'link')
				if title and href:result=title,href
			return result
		
		mess('link/ID %s Checking ...'%link)
		id=xsearch('(\w{10,20})',''.join(s for s in link.split()).upper())
		l=link.lower();result='',''
		if 'fshare.vn/file' in l:result=checker('https://www.fshare.vn/file/%s'%id)
		elif 'fshare.vn/folder' in l:
			b=xread('https://www.fshare.vn/folder/%s'%id)
			if 'class="filename"' in b:
				title=xsearch('<title>(.+?)</title>',b).replace('Fshare - ','')
			if title:result=title,'https://www.fshare.vn/folder/%s'%id
		elif '4share.vn/f/' in l:result=checker('http://4share.vn/f/%s/'%id)
		elif '4share.vn/d/' in l:
			b=xread('http://4share.vn/d/%s/'%id)
			title=xsearch("<title>(.+?)</title>",b).replace('4Share.vn - ','')
			if title:result=title,'http://4share.vn/d/%s/'%id
		elif 'tenlua.vn' in l:
			response=tenlua_get_detail_and_starting(id);title='';img=icon['tenlua']
			if response["type"]=="file":title=response['n'];href="https://www.tenlua.vn/download/"+id
			elif response["type"]=="folder":
				title=response["folder_name"];href="https://www.tenlua.vn/fm/folder/"+id
			if title:result=title,href
		elif 'subscene.com' in l:subscene(name,''.join(s for s in l.split()),'subscene.com')
		else:# idf chi la ID
			result=checker('https://www.fshare.vn/file/%s'%id)
			if not result[0]:
				b=xread('https://www.fshare.vn/folder/%s'%id)
				if 'class="filename"' in b:
					title=xsearch('<title>(.+?)</title>',b).replace('Fshare - ','')
					if title:result=title,'https://www.fshare.vn/folder/%s'%id
				if not result[0] and len(id)>14:
					result=checker('http://4share.vn/f/%s/'%id)
					if not result[0]:
						b=xread('http://4share.vn/d/%s/'%id)
						title=xsearch("<title>(.+?)</title>",b).replace('4Share.vn - ','')
						if title:result=title,'http://4share.vn/d/%s/'%id
						else:
							result=checker('https://tenlua.vn/download/%s'%id)
							if not result[0]:
								response=tenlua_get_detail_and_starting(id);title='';img=icon['tenlua']
								if response["type"]=="file":title=response['n'];href="https://www.tenlua.vn/download/"+id
								elif response["type"]=="folder":
									title=response["folder_name"]
									href="https://www.tenlua.vn/fm/folder/"+id
								if title:result=title,href
		return result
	
	if query=='MyFshare' or query==thumucrieng or page==4:
		title=namecolor('Search trên [COLOR gold]Fshare[/COLOR] Following','lime')
		title+=namecolor(' (Có thể dùng dấu "." giữa các từ)','cyan')
		addir_info(title,'',img,'',90,1,'searchFollow',True)
		title=namecolor('Mục Fshare Following HOT','lime')
		addir_info(title,'https://www.fshare.vn/files/searchFollow?key=',img,'',90,1,'searchFollow',True)
		title=namecolor('Link yêu thích của tôi trên Fshare (MyFshare favorite)','lime')
		addir_info(title,'https://www.fshare.vn/files/favorite',img,'',90,1,'favorite',True)
		title=namecolor('Thư mục theo dõi của tôi trên Fshare (MyFshare Follow folder)','lime')
		addir_info(title,'https://www.fshare.vn/files/following',img,'',90,1,'following',True)
		fsharePage(name,thumucrieng,iconpath+'fshare.png','')
	
	elif page==0:
		name=color['search']+'Nhập ID/link:[/COLOR] %sFshare-Fsend[/COLOR]/%s4share[/COLOR]/%stenlua[/COLOR]/%ssubscene[/COLOR]/[COLOR orangered]link bất kỳ[/COLOR]'%(color['fshare'],color['4share'],color['tenlua'],color['subscene'])
		addir(name,url,icon['icon'],mode=mode,query=query,page=1,isFolder=True)
		for href,name in re.findall('<a href="(.+?)">(.+?)</a>',makerequest(search_file)):
			q='ID?xml' if '.xml' in name else 'ID?'+query
			addirs(name,href,icon['id'],query=q)
	elif page == 1:#Nhập ID mới BIDXFYDOZMWF
		idf = get_input('Hãy nhập chuỗi ID (hoặc fulllink) của Fshare-Fsend-Fcine/4share/tenlua/subscene')
		if not idf or not idf.strip():return 'no'
		else:idf=idf.strip()
		
		def linkMe(link):return [i for i in ('fshare.vn','4share.vn','tenlua.vn','subscene.com') if i in link]
		def makeDir(id):
			title,href=getInfo(id)
			if title:
				make_mySearch(title,href,'','',mode,'Add')
				addirs(title,href,'')
				return True
			else:return False
		kq=''
		if 'subscene.com' in idf:return subscene(name,''.join(s for s in idf.split()),'subscene.com')
		elif (idf.startswith("http:") or idf.startswith("https:")) and not linkMe(idf):
			if 'fcine.net' in idf:
				from resources.lib.servers import fcinenet;fci=fcinenet()
				b=xread(idf,{'cookie':fci.cookie})
			else:b=xread(idf)
			if not b:mess(u'Không tìm thấy trang ...!');return 'no'
			for i in list(set(i for i in re.findall('(https?://[\w|\.|/|-]+)',b) if linkMe(i))):
				kq=makeDir(i)
		else:kq=makeDir(idf)
		if not kq:mess(u'Không tìm thấy thông tin bạn yêu cầu!','xhsare.vn');return 'no'
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
		category+=xsearch('phim/(.+?)\.\d{,6}',c)+' '
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
		query,trang,p=trang_search(query);hd['Cookie']=makerequest(joinpath(xsharefolder,'vaphim.cookie'))
		url_search='http://vaphim.com/page/%s/?s=%s'%(trang,urllib.quote_plus(query))
		#body=make_request(url_search,hd)
		body=xread(url_search,hd)
		items=vp_page(url_search,body)#id,name,href,img,category
		if not items:mess(u'Không tìm được tên phim phù hợp!','vaphim.com search');return 'no'
		for id,name,href,img,category in items:
			addir_info(name,href,img,query='vp_getsubpage')
		page_tag=re.search("class='pages'>(.+?)<.+span><a href='(.+?)' class='page larger'>(\d{,3})</a>",body)
		if page_tag:
			trang=str(int(trang)+1)
			name=color['trangtiep']+'Tiep theo %s...trang %s[/COLOR]'%(page_tag.group(1),page_tag.group(3))
			addir_info(name,url,icon[url.split('.')[0]],'',mode,4,'%s?%s?%s'%(query,trang,p),True)
	
	elif url=='hdvietnam.com':
		#https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=10&hl=en&prettyPrint=false&source=gcsc&gss=.com&sig=8bdfc79787aa2b2b1ac464140255872c&cx=012570864823441480940:ui9zm9vpdyq&q=phap%20su&googlehost=www.google.com&callback=google.search.Search.apiary6840&nocache=1472952908361
		from resources.lib.servers import googlesearch;ggs=googlesearch()
		if '*#*' in query:start=query.split('*#*')[1];query=query.split('*#*')[0]
		else:start='0'
		for title,href,img in ggs.content('012570864823441480940:ui9zm9vpdyq',start,query):
			if 'Page next:' in title:
				page=img;start=href;query=query+'*#*'+start
				addir_info(title,url,icon['hdvietnam'],'',mode,page,query,True)
			else:
				if '/threads/' in href or 'showthread.php' in href or '/diendan/' in href:q='threads';m=1
				else:q='forums';m=1
				addir_info(title,href,icon['hdvietnam'],'',m,1,q,True)
	
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
		body=xread(url);items=[s for s in re.findall(pattern,body) if ext_media(s[0])]
		if not items:mess(u'Không tìm thấy dữ liệu yêu cầu!','xshare_search');return 'no'
		for href,title in items:addir_info(title,href.split()[0],icon['4share'])
		next=xsearch("<a href='([^<]+?)'> Next</a>",body)
		if next:
			title=color['trangtiep']+'Trang tiep theo...trang %s[/COLOR]'%xsearch('\?page=(\d{1,3})&',next)
			addir_info(title,'http://4share.vn'+next.replace(' ','+'),icon['4share'],'',mode,4,'',True)
	
	elif url=='ifile.tv':
		query,trang,p=trang_search(query)	
		url_search = 'http://ifile.tv/search?search_module=phim&search_name=1&'
		url_search += 'search_content=1&time_sort=new&search_string="%s"'%urllib.quote_plus(query)
		items = []
		for content in re.findall("<td>(.*?)</b>",xread(url_search)):
			items+=re.findall("<a.+href='(.+?)'.+src='(.+?)'.+(\d{5}).+>(.+?)</a>",content)
		if not items:mess(u'Không tìm được tên phim phù hợp!','Ifile.tv search');return 'no'
		items_xml,id_xml = read_all_filexml(fn="ifiletv.xml");temp=[]
		for href,img,id_htm,name in items:
			if id_htm in id_xml:
				index = id_xml.index(id_htm)
				try:
					while id_xml[index] == id_htm:
						temp.append((items_xml[index]));index +=1 
				except:pass
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

	elif 'taifile.net' in url:
		def taifile_search(url):
			q=xread(url);vp=[]
			for s in re.findall('(<div class="bgframe">.+?</a></div></div>)',q):
				if not 'fshare.vn' in s:continue
				title=xtitle(s)
				size=xsearch('Size: <b>(.+?)</b>',s)
				title='[COLOR gold]Fshare[/COLOR] '+title.replace('Download ','')+ ' - '+size
				href='http://www.taifile.net'+xsearch('href="(/x.php\?id=.+?)"',q)
				link=xsearch('href="(http://vaphim.com[^<]+?)"',s)
				label=xsearch('title="([^"]+?)" target',s)
				addir_info(title,href,icon['taifile'],'',mode,4,'play')
				if link and link not in str(vp):vp.append((link,label))

			for link,label in vp:
				addir_info('[COLOR gold]'+label+'[/COLOR]',link,icon['vaphim'],'',1,1,'vp_getsubpage',True)

			pn=re.search('<a class="active" href="[^<]+?">\d+?</a><a href="([^<]+?)">(\d+?)</a>',q)
			if pn:
				href=pn.group(1).replace('amp;','').replace('/search.php?q=','')
				href='http://www.taifile.net/search.php?q='+'%20'.join(s for s in href.split())
				title=color['trangtiep']+' Trang tiep theo...trang %s[/COLOR]'%pn.group(2)
				addir_info(title,href,icon['taifile'],'',mode,4,'search',True)
		
		if query=='search':taifile_search(url)
		elif query=='play':
			b=make_request(url,resp='o')
			if b and b.getheader('location'):resolve_url(b.getheader('location'))
		else:
			b=make_post('http://www.taifile.net/suggest.php',data={'q':query},resp='j')
			if not b or len(b)<2:
				href='http://www.taifile.net/search.php?&host=fshare&q='+urllib.quote_plus(query)
				taifile_search(href)
			else:
				if '/search.php?q='+query not in b:b[query]=query
				for i in b:
					title='[COLOR lime]Search on:[/COLOR] '+' '.join(s for s in re.sub('<.*?>|\[.*?\]|\(.*?\)','',b.get(i)).split())
					href='http://www.taifile.net/search.php?&host=fshare&q='+urllib.quote(i.replace('/search.php?q=',''))
					addir_info(title,href,icon['taifile'],'',mode,4,'search',True)
	return ''

def subtitle_of_year(title):
	string=re.split('20\d\d|19\d\d',title)[0]
	string=re.sub(xsearch('multi ',string,0,re.IGNORECASE),'',string)
	return string if string else title

def correct_link(url):
	if 'tenlua.vn' in url:idf=xsearch('(\w{16,20})',url)
	elif 'subscene.com' in url and '...' not in url:idf='ok'
	else:idf=xsearch('(\w{10,20})',url)
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

def hdvietnam(name,url,img,fanart,mode,page,query):
	ico=icon['hdvietnam'];tempfolder=xbmc.translatePath('special://temp')
	urlhome='http://www.hdvietnam.com/';c='orangered'
	from resources.lib.servers import hdVietnamn;hdvn=hdVietnamn()
	menu={'MyFshare':{'action':'Add','server':['fshare.vn']},
		'MyFavourites':{'action':'Add','server':['fshare.vn','4share.vn','tenlua.vn','subscene.com']}}
	
	def menuXML(url):
		b=xread(url)
		for href in [i for i in re.findall('href="(.+?\d/index.rss)"',b)]:
			if href.replace('/index.rss','') in url:continue
			title='[COLOR blue]RSS [COLOR gold]%s[/COLOR] %s[/COLOR]'%(homnay,xsearch('/(.+?)/',href))
			addir_info(title,urlhome+href,ico,'',mode,1,'RSS',True)
	
	if query=='HDV':
		items=	[('[COLOR crimson][COLOR blue]Mục CHIA SẺ PHIM[/COLOR] của hdvietnam.com[/COLOR]','chiase'),
				('[COLOR crimson][COLOR green]Mục CHIA SẺ NHẠC[/COLOR] của hdvietnam.com[/COLOR]','chiase')]
		fanart=joinpath(home,'fanart.jpg')
		for title,query in items:
			addir_info(title,'',ico,fanart,mode,1,query,True)
		
		menuXML('http://www.hdvietnam.com/categories/chia-se-phim.34/')
	
	elif query=='chiase':
		if 'CHIA SẺ PHIM' in name:url='http://www.hdvietnam.com/categories/chia-se-phim.34'
		else:url='http://www.hdvietnam.com/categories/chia-se-nhac.148/'
		for href,title in hdvn.getpage(url):
			addir_info(namecolor(title,c),href,img,query='forums')

	elif query=='forums':
		for id,title,href in hdvn.forums(url):
			if id=='nodeList':addir_info(namecolor(title,c),href,img,query='forums') if page==1 else ''
			elif id=='pageNext':addir_info(title,href,img,'',mode,page+1,'forums',True)
			else:addir_info(namecolor(title,c),href,img,query='threads')
	
	elif query=='threads' and 'xem-gi-hom-nay' in url:
		b=re.findall('(<li id="post.+?/li>)',xread(url),re.S)
		for s in [i for i in b if 'data-author="BuiAn"' in i]:
			for m in ['<abc>'+i for i in s.split('<span style="font-size: 18px">') if '"internalLink"' in i]: 
				label=xsearch('<abc>(.+?)</span>',m).strip()
				img=xsearch('\[td\] <a href="(http://www.hdvietnam.com/diendan/attachment.php.+?)"',m)
				for n in [i for i in re.findall('(\[td\].+?\[/td\])',m,re.S) if '"internalLink"' in i]:
					for o in re.findall('(<br /.+?/>)',n,re.S):
						t=xsearch('<b>(.+?)</b>:',o).strip()
						if t:t=t+' '
						items=re.findall('<a href="(.+?)" class="internalLink">(.+?)</a>',o)
						if items and label:add_sep_item('%s ----------------------------'%s2c(label))
						for href,title in items:
							addir_info(t+title.strip(),href,img,query='threads')
	elif query=='F4mProxy':
		xrw('hdvn.refresh','Detail');xbmc.executebuiltin("Container.Refresh")#;return 'ok'
	elif query=='threads':
		sep=False
		add_sep_item('Phim: '+xsearch('\[/COLOR\]([^\[]+?)\[/COLOR\]',name).strip())
		refresh=xrw('hdvn.refresh')=='Detail'
		if refresh:xrw('hdvn.refresh','No')
		else:
			title=namecolor('Show thông tin đầy đủ hơn cho item','orangered')
			addir_info(title,'',img,'',mode,1,'F4mProxy')
		for title,href,img in hdvn.threads(url,refresh):
			if 'www.hdvietnam.com' not in href:
				if not title:title=namecolor(re.sub('.+\[/COLOR\]\[/COLOR\]','',name))
				addir_info(title,href,img,query='threads')
			else:
				if not sep:add_sep_item('Các chủ đề cùng chuyên mục');sep=True
				addir_info(namecolor(title,c),href,img,query='threads')
	
	elif query=='RSS':
		import xml.etree.ElementTree as ET
		try:root=ET.fromstring(xread(url).replace('dc:creator','creator').replace('content:encoded','content'))
		except:root=None
		if root:
			nodes=root.getiterator('item')
			if nodes:
				for i in nodes:
					link=i.findtext('link')
					creator=i.findtext('creator')
					title='[COLOR gold]%s[/COLOR] '%creator+i.findtext('title')
					content=i.findtext('content')
					if urlhome not in link:link=urlhome+link
					addir_info(title,link,ico,'',mode,1,'threads',True)
			else:menuXML(url.replace('/index.rss',''))

def database_download():
	mess(u'Đang kiểm tra và download database cho xshare','database_download');delete_files(tempfolder)
	tempfile = joinpath(tempfolder,"xshare_data.zip");pattern='<title>.*xx(.+?)xx.*</title>'
	if not os.path.exists(datapath):os.mkdir(datapath)
	if not os.path.exists(iconpath):os.mkdir(iconpath)
	id=xsearch(pattern,make_request('https://www.fshare.vn/folder/9F3VWL147DYG'))
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
				if '.xml' in file:
					a=makerequest(joinpath(tempfolder,file));s=a.splitlines()
					a=makerequest(joinpath(datapath,file));d=a.splitlines();w=False
					for i in s:
						if i not in d:d.append(i);w=True
					if w:a='';makerequest(joinpath(datapath,file),'\n'.join(i for i in d),'w')
				elif '.xml' in file and xml_size.get(file,0)<os.path.getsize(joinpath(tempfolder,file)):
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
			vp_make_datanew();vp_update();ifile_update()
			makerequest(joinpath(datapath,"last_update.dat"),'','w')
			mess('Xshare auto update completed','vaphim ifiletv')
	except:mess('Data update error!')

def checkupdate(filename,hours=1,folder=datapath,xdict=dict()):
	filecheck=joinpath(folder,filename);timeformat='%Y%m%d%H'
	filetime=os.path.getmtime(filecheck) if os.path.isfile(filecheck) else 0
	last_update=datetime.datetime.fromtimestamp(filetime).strftime(timeformat)
	timenow=datetime.datetime.now().strftime(timeformat)
	return (int(timenow)-int(last_update))>hours

def xshare_postks(body,hd,token):
	if myaddon.getSetting('usernameh')=='thaitni':return body,token,hd['Cookie']
	my_dict=json_rw('xshare.json');url='http://www.hdvietnam.com/diendan/post_thanks.php'
	for post_id in my_dict:
		if not my_dict[post_id]:
			response=make_post(url,hd,'do=post_thanks_add&using_ajax=1&p=%s&securitytoken=%s'%(post_id,token))
			my_dict[post_id]='Y';json_rw('xshare.json',my_dict);break
	return body,token,hd['Cookie']

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
	body= xread(url,hd)
	body=body.replace(',,"en"','').replace('[[[','').replace(']]]','')
	result=''
	for i in body.split('],['):
		research=re.search('"(.+?)","(.+?)"',i)
		if research:result+=research.group(1)+' '
		else:print '%s :not research'%i
	return result.replace('Xshare','xshare').split('xshare')

def subscene(name,href,query):
	if 'phudeviet.org' in href:#http://phudeviet.org/film/Gotham-Season-2/7396.html
		b=xread(href)
		label=xsearch('<span class="title1".+?>([^>]+?)</p>',b)
		if not label:label=xsearch('<title>(.+?)</title>',b).replace('PHỤ ĐỀ VIỆT - ','')
		label='.'.join(label.split())
		s=xread(xsearch('<a href="(http://phudeviet.org/download/.+?)">',b))
		if s:
			id="rar" if s[0]=='R' else "zip" if s[0]=='P' else "srt"
			fn=os.path.join(tempfolder,"sub."+id)
			f=open(fn, "wb");f.write(s);f.close()
			if id in "rar-zip":
				try:
					xbmc.sleep(500)
					xbmc.executebuiltin(('XBMC.Extract("%s","%s")' % (fn,subsfolder,)).encode('utf-8'), True)
					mess(u'Đã download sub vào XshareSub folder')
				except:pass
			return 'ok'
		else:
			for href,title in re.findall('<a href="(.+?)">(.+?)</a></div></td>',b):
				addir_info(title,href,img,'',mode,1,'')
			return
	
	elif not re.search('\d{5,10}',href):
		if not os.path.basename(href):href=os.path.dirname(href)
		pattern='<a href="(/subtitles/.+?)">\s+<span class=".+?">\s*(.+?)\s+</span>\s+<span>\s+(.+?)\s+</span>'
		hd={'User-Agent':'Mozilla/5.0','Cookie':'LanguageFilter=13,45'}
		body=xread(href.replace('amp;',''),hd)
		subs=re.findall(pattern,body)
		if not subs:
			temp=xsearch('<a href="(.+?)"',xsearch('<h2 class="exact">Exact</h2>(.+?)</ul>',body,1,re.DOTALL))
			if temp:
				body=make_request('http://subscene.com'+temp,headers={'Cookie':'LanguageFilter=13,45'})
				subs=re.findall(pattern,body)
		mess(u'Tên phim: %s'%s2u(name).replace('[COLOR green]Subscene[/COLOR]-',''))
		for url,lang,name in sorted(subs,key=lambda l:l[1], reverse=True):
			name='Eng.'+name if '/english/' in url else '[COLOR red]Vie.[/COLOR]'+name
			addirs(name,'http://subscene.com'+url,query='download')
		return ''
	pattern='<a href="(.+?)" rel="nofollow" onclick="DownloadSubtitle.+">'
	downloadlink='http://subscene.com' + xsearch(pattern,xread(href))
	if len(downloadlink)<20:mess(u'Không tìm được maxspeed link sub!')
	else:xshare_resolve(downloadlink)
	return 'ok'

def megabox(name,url,img,fanart,mode,page,query):
	homepage='http://phim.megabox.vn/';ico=icon['megabox']
	cat={1:'Phim lẻ',2:'Phim bộ',3:'Show',4:'Clip'}
	gen={1:'Hành động',2:'Phiêu lưu',3:'Ma kinh dị',4:'Tình cảm',5:'Hoạt hình',6:'Võ thuật',7:'Hài',8:'Tâm lý',9:'Kiếm hiệp',10:'Sử thi',11:'',12:'',13:'Hình sự',14:'',15:'Âm nhạc',16:'Khoa học',17:'Tài liệu',18:'Gia đình',21:'Chiến tranh',22:'Thể thao',25:'Độc-Lạ',27:'Khoa học viễn tưởng',28:'Ẩm thực',29:'Thời trang',30:'Điện ảnh',31:'Thiếu nhi',32:'Giáo dục',33:'TV-Show',34:'Live Show',36:'Công nghệ',37:'Khám phá thế giới',38:'Động vật',39:'Shock'}
	country={1:'Âu-Mỹ',2:'Hàn Quốc',3:'Hồng Kông',4:'Trung Quốc',5:'Nhật Bản',6:'Thái Lan',7:'Quốc Gia khác',8:'Mỹ',9:'Pháp',11:'Việt Nam',12:'Ấn Độ',13:'Philippines'}#get(url,headers=hd,maxr=2)
	def namecolor(label):return color['megabox']+label+'[/COLOR]'
	def get_id(url):return xsearch('-(\d{1,6})\.html',url)
	def duration(string):return xsearch('Thời lượng:<.+?> (.+?)</li>',string)
	def countview(string,tag='span'):return xsearch('class=.count-view.><%s></%s> (.+?)</span>'%(tag,tag),string)
	def thuyetminh(string):return color['subscene']+'TM[/COLOR] ' if xsearch('class=.ico-sub.',string,0) or string=='TM' else ''
	def phim18(string):return '[COLOR red][B]M+[/B][/COLOR] ' if xsearch('class=.ico-rating.',string,0) or string=='M+' else ''
	def episode(string):return xsearch('class=.esp.><i>(.+?)</span>',string).replace('</i>','')
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
			views=countview(body);esp=xsearch('Số tập <i>(.+?)</i>',body);p18='M+' if phim18(body) else ''
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
				epi=xsearch('(.+?)\W(.*?)\Z',dict[id][5]);eps=xsearch('(.+?)\W(.*?)\Z',dict[id][5],2)
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
			tm=thuyetminh(esp)+phim18(esp);esp=episode(esp);eps=xsearch('\W(.*)\Z',esp)
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

	if url=='megabox.vn':
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
			addir_info(remove_tag(label),href,img,'',mode,1,'mgbplay')
	
	elif query=='mainpage':
		body=homehtml()
		if name==namecolor('Megabox giới thiệu'):
			content=xsearch('<ul class="hotFilmSlider">(.+?)</ul>',body,1,re.DOTALL)
			pattern="<a href='(http://phim.megabox.vn/.+?)'.+?src='(.+?)' alt='(.+?)'"
			for href,img,label in re.findall(pattern,content):
				addir_info(remove_tag(label),href,img,img,mode,1,'mgbplay')
		elif name==namecolor('Top 10 phim trong ngày'):
			content=xsearch('<ul class="list topSlider">(.+?)end topFilm',body,1,re.DOTALL)
			pattern='href="(.+?)".+?<h3 class=\'H3title\'>(.+?)</h3>.+?src="(.+?)"'
			for href,label,img in re.findall(pattern,content,re.DOTALL):
				addir_info(remove_tag(label),href,img,'',mode,1,'mgbplay')
		elif 'xem nhiều' in name:#lẻ-bộ-show-clip xem nhiều
			cats={'lẻ':1,'bộ':2,'show':3,'clip':4};cat=[cats[s] for s in cats if s in name][0]
			link='http://phim.megabox.vn/mostviewed/ajax/?cat=%d&period=%d'
			period=['ngày','tuần','tháng']#;per=[s[0] for s in period if s[0] in name][0]
			for i in range(1,4):
				add_sep_item(re.sub('\[.+?\]','',name)+' '+period[i-1])
				body=make_request(link%(cat,i))
				for b in re.findall('<li class="item">(.+?)</li>',body,re.DOTALL):
					href=xsearch('href="(.+?)"',b)
					img=xsearch('src="(.+?)"',b)
					title=xsearch("alt='(.+?)'",b).replace('Phim ','')
					tm=thuyetminh(b)+phim18(b)
					views=xsearch('</i>(.+?)</span>',b)
					if 'phim lẻ' in name:query='mgbplay';isFolder=False
					else:title=namecolor(title);query='1episode';isFolder=True
					title=tm+title+' %sviews: %s[/COLOR]'%(color['subscene'],views)
					addir(title,href,img,'',mode,1,query,isFolder)
		elif [s for s in ('Phim Lẻ','Phim Bộ','Chiếu Rạp') if s in name]:
			temp='Phim Lẻ Mới Nhất' if 'Lẻ' in name else 'Phim Bộ Mới Nhất' if 'Bộ' in name else 'Phim Chiếu Rạp'
			content=xsearch('>%s</a>(.+?)>Xem thêm</a>'%temp,body,1,re.DOTALL)
			patt="href='(.+?)'.+?title.>(.+?)</h3>(.+?)<img.+?src='(.+?)'(.+?)</a>.+?<a.+?a>(.+?)</div></div>"
			put_items(re.findall(patt,content),'i')
		
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
		if not dict.get(url):dict=update_dict(dict)
		for title,href in dict[url]:
			title=color['megabox']+title.replace('Phim ','')+'[/COLOR]'
			addir(title,href,icon['megabox'],'',mode,1,'mainmenu',True)
	
	elif query=='mainmenu':#url:(phim-le,phim-bo,show,clip)
		label=os.path.basename(url)
		submenu={'phim-le':'Phim lẻ','phim-bo':'Phim bộ','show':'Show','clip':'Clip'}
		if label=='clip':
			title=color['xshare']+submenu[label]+' theo thể loại[/COLOR]'
			addir(title,label+'tl',icon['megabox'],'',mode,1,query,True)
		elif label in ('phim-le','phim-bo','show'):
			title=color['xshare']+submenu[label]+' theo thể loại[/COLOR]'
			addir(title,label+'tl',icon['megabox'],'',mode,1,query,True)
			title=color['xshare']+submenu[label]+' theo quốc gia[/COLOR]'
			addir(title,label+'qg',icon['megabox'],'',mode,1,query,True)
		pattern='<a class.+?href="(.+?)".+?title.>(.+?)</h3>(.+?)<img.+?src="(.+?)">(.+?)</a>.+?<a.+?a>(.+?)</div><'
		body=sub_body(make_request(homepage+url,maxr=3),'begin primary','end primary')
		href_new,dict=put_items(re.findall(pattern,body,re.DOTALL),'i')
		url_next=xsearch('<li class="next"><a href="(.+?)">',body)
		if url_next:
			page_end=xsearch('<span></span>Trang.{1,10}/(\d{1,3})</div>',body)
			page_next=xsearch('trang-(.+)\Z',url_next)
			name=color['trangtiep']+'Trang tiếp theo: trang %s/%s[/COLOR]'%(page_next,page_end)
			addir(name,url_next,icon['megabox'],'',mode,1,query,True)
		if href_new:endxbmc();update_href_new(href_new,dict)
	
	elif query=='mgbplay':
		url='/'.join((os.path.dirname(url),urllib.quote(os.path.basename(url))))
		body=make_request(url,resp='o',maxr=5);link=xsearch("changeStreamUrl\('(.+?)'\)",body.body)
		if not link:play_youtube(xsearch("\'(https://www.youtube.com/watch\?v=.+?)\'",body.body));return
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
		#print 'http://phim.megabox.vn/content/ajax_episode?id=%s&start=%s'%(id,start)
		j=make_request('http://phim.megabox.vn/content/ajax_episode?id=%s&start=%s'%(id,start),resp='j')
		if j==False:addir(name.replace('orangered','grey'),url,img,'',mode,1,'mgbplay');return
		for epi in j:
			name=epi['name'];href='%s/%s-%s.html'%(href,epi['cat_id'],epi['content_id'])
			if not art:fanart='http://img.phim.megabox.vn/300x168'+epi['image_banner']
			else:fanart=art+epi['image_banner']
			addir(name,href,img,fanart,mode,1,'mgbplay')
		
		if make_request('http://phim.megabox.vn/content/ajax_episode?id=%s&start=%d'%(id,int(start)+30))!='false':
			name=color['trangtiep']+u'Các tập tiếp theo: %d-%s[/COLOR]'%(int(start)+30,eps)
			addir(name,url,img,fanart,mode,1,'%depisode%s'%(int(start)+30,eps),True)
	
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
		page_end=xsearch('<li class="last"><a href="t/phim-chieu-rap-29/phim-le/trang-(.+?)">',body)
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
		put_items(re.findall(patt,make_request(href,hd),re.DOTALL),'i')
		cat={'phim-le':'Phim lẻ','phim-bo':'Phim bộ','show':'Show','clip':'Clip'}
		name=color['trangtiep']+'%s Xem Thêm...[/COLOR]'%cat[url]
		addir(name,url,icon['megabox'],'',mode,1,'mainmenu',True)
	return ''

def get_home_page(fn,url='',update=False,hd=hd):
	def make_cookie_file(url,cookie):
		if 'vaphim.com' in url:makerequest(joinpath(xsharefolder,'vaphim.cookie'),cookie,'w')
		elif fn=='hayhaytv.html':makerequest(joinpath(xsharefolder,'hayhaytv.cookie'),cookie,'w')
			
	fullfilename=joinpath(xsharefolder,fn);body=''
	if not update and os.path.isfile(fullfilename):body=makerequest(joinpath(xsharefolder,fn))
	elif not update and url:
		response=make_request(url,hd,resp='o')
		if response:
			body=response.body;content=makerequest(fullfilename,re.sub('<script.+?/script>','',body),'w')
			if response.cookiestring:make_cookie_file(url,response.cookiestring)
	elif update and url and checkupdate(fn,folder=xsharefolder):
		response=make_request(url,hd,resp='o')
		if response:
			endxbmc();body=response.body;content=makerequest(fullfilename,re.sub('<script.+?/script>','',body),'w')
			if response.cookiestring:make_cookie_file(url,response.cookiestring)
	return body

def fptplay(name,url,img,fanart,mode,page,query,text=''):
	ico=icon['fptplay'];c=xsearch('([a-z]+)',color['fptplay'])
	
	def itemsDIR(b):
		s=xsearch('(<div id="wrap_content".+?"footer box">)',b,1,re.S,result=b)
		items=re.findall('(<a.+?/a>)',s,re.S)
		for s in items:itemDIR(s)
		return len(items)
	
	def itemDIR(s):
		if '"https://fptplay.net/epl_img/lockepl.png"' in s:return
		title=xsearch('title="([^"]+?)"',s,result=xsearch('alt="([^"]+?)"',s))
		href=xsearch('href="([^"]+?)"',s,result=xsearch('data-href="(.+?)"',s))
		if not title or not href or 'javascript' in href:return
		if re.search('.huyết .inh',title.lower()):title='[COLOR blue]TM[/COLOR] '+title
		label=[re.sub('<.+?>','',i) for i in re.findall('(<p.+?/p>)',s)]
		label=' '.join(i for i in label if i not in title)
		if label:title=title+' [COLOR green]%s[/COLOR]'%label
		img=xsearch('src="(.+?\.jpg)',s,result=xsearch('original="([^"]+?\.jpg)',s))
		if not img:img=xsearch('original="([^"]+?\.png)',s)
		addir_info(vnu(title),href,img,img,mode,1,'eps',True)
		
	if query=="fptplay.net":
		b=getHome('fptplay.html','https://fptplay.net')
		title=color['search']+"Search trên fptplay.net[/COLOR]"
		addir_info(title,'fptplay.net',ico,'',mode,1,'search',True)
		
		s=xsearch('(<ul class="top_menu".+?/ul>)',b,1,re.DOTALL)
		def abc(i):return '"dropdown"' not in i and '"login"' not in i
		for s in [i for i in re.findall('(<a.+?/a>)',s) if abc(i)]:
			title=re.sub('<.+?>','',s)
			href=xhref(s)
			addir_info(namecolor(title,c),href,ico,'',mode,1,"category",True)
		
		add_sep_item('FPT Play giới thiệu -----------------------------------------')
		s=xsearch('(<ul class="slide_banner".+?/ul>)',b,1,re.S)
		for m in re.findall('(<li.+?/li>)',s,re.S):itemDIR(m)
		
		s=re.findall('(<section>.+?</section>)',b,re.S)
		def abc(i):return 'parent=' in i and '"time_remain"' not in i and 'lockepl.png' not in i
		for s in [i for i in s if abc(i)]:
			i=re.sub('<.+?>','',xsearch('<span class="pull-left">(.+?)</span>',s))
			add_sep_item('%s -----------------------------------------'%vnu(i))
			for m in re.findall('(<li.+?/li>)',s,re.S):itemDIR(m)
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP" or url=="fptplay.net":
		if query=="INP":query=make_mySearch('',url,'','','','Input')
		if not query.strip():return
		elif 'Page next:' not in name:page=1
		
		b=xread('https://fptplay.net/tim-kiem/%s'%urllib.quote(query))
		for m in [i for i in b.split('list_img') if '<div class="title">' in i]:itemDIR(m)
		
		pn=xsearch('id="paging_(.+?)_',b)
		if pn:
			pn='type=search&stucture_id=search&page=2&keyword='+query
			addir_info('[COLOR lime]Page next: %d[/COLOR]'%(page+1),pn,ico,'',mode,page+1,"pageNext",True)
	
	elif url=='https://fptplay.net/livetv':
		from resources.lib.servers import fptPlay;fpt=fptPlay()
		hd=fpt.hd
		if query=='category':
			addir_info(namecolor('Tìm kênh','lime'),url,img,'',mode,1,'getSearch',True)
			for title,href,img in fpt.liveChannels():
				if title=='Lịch Phát Sóng':
					addir_info(namecolor('Lịch Phát Sóng',c),'1',ico,'',mode,1,'fptSchedule',True)
				elif 'sep' in href:add_sep_item('%s -----------------------------------------'%title)
				else:addir_info(namecolor(title,c),os.path.basename(href),img,'',mode,1,'playTV')
		elif query=='getSearch':make_mySearch('channel',url,'','',mode,'get')
		else:
			if query=='CHN':
				query=make_mySearch('channel',url,'','','','Input')
				if not query.strip():return 'no'
			q = ' '.join(query.split()).lower()
			for title,href,img in [i for i in fpt.liveChannels() if q in i[0].lower() or q in ''.join(j[0].lower() for j  in i[0].split())]:
				addir_info(namecolor(title,c),os.path.basename(href),img,'',mode,1,'playTV')
			
	elif query=='fptSchedule' or (name==query and url=='getSchedule'):
		if url=='getSchedule' or url=='i':
			if url=='i':query=make_mySearch('schedule','https://fptplay.net/livetv','','','','Input')
			if not query.strip():return 'no'
			items=re.findall('<li rel="(\D.+?)".+?>([^<]+?)</span>',xrw('fptschedule.txt'))
			q=query.lower()
			items=[i for i in items if q in i[1].lower() or q in ''.join(j[0].lower() for j  in i[1].split())]
			if not items:
				make_mySearch(q.upper(),'https://fptplay.net/livetv','schedule','',mode,'Remove')
				mess(u'Không tìm thấy kênh %s'%q.upper(),'fptplay.net')
				return 'no'
			for i in items:addir_info(namecolor(vnu(i[1]),c),i[0],img,'',mode,1,'fptSchedule',True)
		elif url=='0':make_mySearch('schedule','https://fptplay.net/livetv','','',mode,'get')
		elif url=='1':
			from resources.lib.servers import fptPlay;fpt=fptPlay()
			hd=fpt.hd
			items=fpt.schedule()
			day=[i[1] for i in items if i[0]=='day']
			addir_info(namecolor('Tìm kênh','lime'),'0',img,'',mode,1,'fptSchedule',True)
			url=str([day[i] for i in range(len(day)) if i>(len(day)-5)])
			addir_info(namecolor('Chọn ngày xem lịch phát sóng',c),url,img,'',mode,1,'fptSchedule',True)
			add_sep_item('Lịch Phát Sóng Hôm Nay [COLOR gold]%s[/COLOR]-------'%time.strftime("%d/%m/%Y"))
			for i in [i for i in items if i[0]!='day']:
				addir_info(namecolor(vnu(i[1]),c),i[0],img,'',mode,1,'fptSchedule',True)
		elif 'Chọn ngày xem lịch phát sóng' in name:
			for i in eval(url):
				addir_info(namecolor(i,c),'2',img,'',mode,1,'fptSchedule',True)
		elif url=='2':
			from resources.lib.servers import fptPlay;fpt=fptPlay()
			hd=fpt.hd
			name=xsearch('\](.+?)\[',name)
			items=fpt.schedule()
			for i in [i for i in items if i[0]!='day']:
				addir_info(namecolor(vnu(i[1]),c),i[0]+':'+name,img,'',mode,1,'fptSchedule',True)
		else:
			if ':' in url:t=url.split(':')[1];url=url.split(':')[0];all=True
			else:t=time.strftime("%d-%m-%Y");all=False
			b=xread('https://fptplay.net/show/schedule?channel=%s&date=%s&channel_now='%(url,t))
			b=re.findall('(<li.+?/li>)',b,re.S)
			if not b or (len(b)==1 and not xsearch('<p>(\d.+?)</p>',b[0])):
				mess(u'Chưa có dữ liệu','fptplay.net')
				return 'no'
			
			if fptisp():urls={'thvl1':'udp://@225.1.1.155:30120','vinh-long-2':'udp://@225.1.1.154:30120','htv7-hd':'udp://@225.1.1.191:30120','htv9-hd':'udp://@225.1.1.190:30120','vtv3-hd':'udp://@225.1.2.247:30120','vtv6-hd':'udp://@225.1.2.244:30120','vtv1-hd':'udp://@225.1.2.249:30120'}
			else:urls={}
			
			t0=t1=s1=time.strftime("%H:%M")
			add_sep_item('Lịch Phát Sóng Ngày [COLOR gold]%s[/COLOR] kênh %s -------'%(t,name))
			for s in b:
				t=xsearch('<p>(\d.+?)</p>',s)
				t=xsearch('id="(.+?)"',s).replace('_',':')
				i=vnu(xsearch('<p class="program_live">(.+?)</p>',s))
				j=vnu(xsearch('<p class="program_name Regular">(.+?)</p>',s))
				s=vnu(xsearch('<p class="program_type">(.+?)</p>',s))
				if i:s='[COLOR red]%s[/COLOR] [COLOR cyan]%s[/COLOR]'%(i,s)
				if j:s='%s [COLOR cyan]%s[/COLOR]'%(s,j)
				if all:addir_info('[COLOR gold]%s[/COLOR] %s'%(t,s),url,ico,'',mode,1,'playTV')
				elif t and t<t0:t1=t;s1=s;continue
				elif not t and t1:s1+=' - %s'%(s);continue
				else:
					if urls.has_key(url):url=urls.get(url)
					if t1:
						addir_info('[COLOR gold]%s[/COLOR] %s'%(t1,vnu(s1)),url,ico,'',mode,1,'playTV')
						t1=''
					addir_info('[COLOR gold]%s[/COLOR] %s'%(t,vnu(s)),url,ico,'',mode,1,'playTV')
		
	elif query=='playTV':
		from resources.lib.servers import fptPlay;fpt=fptPlay()
		hd=fpt.hd
		link=fpt.liveLink(url) if 'udp:' not in url else url
		if link:xbmcsetResolvedUrl(link)
		else:mess('Get channel link fail!') 
	
	elif query=='fpt_page':
		if url.startswith('http'):data='type=new&stucture_id=%s&page=1'%xsearch("/(\w+)/",url)
		else:data=url
		b=xread('https://fptplay.net/show/more',data=data)
		if itemsDIR(b) > 29:
			page+=1;data=re.sub('page=\d+','page=%d'%page,data)
			name=namecolor(name).split(' ... trang:')[0]
			title=namecolor(name+' ... trang: %d'%page,'lime')
			addir_info(title,data,ico,'',mode,page,"fpt_page",True)
		
	elif query=='xem_nhieu':
		data='type=view&slider=1&stucture_id=%s'%xsearch("/(\w+)/",url)
		itemsDIR(xread('https://fptplay.net/show/tab',data=data))
	
	elif query=='tabdanet':
		href='https://fptplay.net/show/tabdanet'
		b=xread(href,data='id=%s'%url)
		for s in re.findall('(<a.+?/a>)',b,re.S):itemDIR(s)
	
	elif query=='category':
		def banner(b):
			items=re.findall('(<li class="banner".+?/li>)',b,re.S)
			if items:
				add_sep_item('FPT Play giới thiệu ------------------')
				for s in items:itemDIR(s)
		
		b=xread(url)
		s=xsearch('(<ul class="Regular".+?/ul>)',b,1,re.S)
		if s:#DANET
			label=''
			for s in re.findall('(<li.+?/li>)',s):
				title=vnu(re.sub('<.+?>','',s))
				if 'class=active' in s:label=title;continue
				href=xsearch("'(.+?)'",s)
				addir_info(namecolor(title,c),href,ico,'',mode,1,"tabdanet",True)
			
			banner(b)
			
			if label:add_sep_item(label);itemsDIR(b)
			return
		
		#Submenu
		for s in re.findall('(<a class="box_header Regular".+?/a>)',b):
			title=vnu(re.sub('<.+?>','',s))
			href=xhref(s)
			addir_info(namecolor(title,c),href,ico,'',mode,1,"fpt_page",True)
		
		banner(b)
		
		#Detail
		for s in re.findall('(<section.+?/section>)',b,re.S):
			m=xsearch('(<a class="box_header Regular".+?/a>)',s)
			title=re.sub('<.+?>','',m)
			title=namecolor(vnu(title+' Mới nhất / Xem nhiều nhất'),c)
			addir_info(title,xhref(m),ico,'',mode,1,"xem_nhieu",True)
			itemsDIR(s)
		
		schedule=xsearch('(<div class="calendar".+?class="footer">)',b,1,re.S)#Lịch Ngoai hang Anh
		if schedule:
			add_sep_item('Lịch thi đấu - Kết quả ====================================')
			s=[i for i in schedule.split('<div class="list-match">') if 'href=' in i]
			for i in s:
				date=re.sub('<.+?>','',xsearch('<p class="date">(.+?)</p>',i))#.decode('utf-8')
				if date:add_sep_item('------------------------------ %s'%date)
				for j in re.findall('(<a.+?/a>)',i,re.S):
					title=xsearch('<p>(.+?)</p>',j)
					if not title:continue
					title='[COLOR gold]%s[/COLOR]'%title
					if '-' in title:title='[COLOR green]%s[/COLOR]'%('  <%s>  '%title).join(re.findall('alt="(.+?)"',j))
					else:title=title+'  '+'[COLOR orange]%s[/COLOR]'%'  <->  '.join(re.findall('alt="(.+?)"',j))
					add_sep_item(title)
				
	elif query=='eps':
		data='film_id=%s&page=%d'%(xsearch('(\w{20,30})',url),page)
		hd={'User_Agent':'Mozilla/5.0','X-Requested-With':'XMLHttpRequest','referer':'','X-KEY':'play1game'}
		b=xread('https://fptplay.net/show/episode',hd,data)
		items=[i for i in re.findall('(<li.+?/li>)',b,re.S) if '"title_items"' in i]
		for s in items:
			title=xtitle(s)
			epi=xsearch('<p class="title_items">(.+?)</p>',s)
			if epi and epi not in title:title=epi+'-'+title
			if 'phụđề' in title.replace(' ','').lower():title='[COLOR green]PĐ[/COLOR] '+title
			elif 'thuyếtminh' in title.replace(' ','').lower():title='[COLOR blue]TM[/COLOR] '+title
			href=xsearch('(\w{20,30})',xsearch('href="(.+?)"',s))+'?'+xsearch('id="episode_(\d{1,4})"',s)
			addir_info(vnu(title),href,img,img,mode,1,'play')
		
		if not items:addir_info(namecolor(name),url,img,img,mode,1,'play')
		if '&rsaquo;&rsaquo;' in b:
			title=namecolor('Các tập tiếp theo ...','lime')
			addir_info(title,url,ico,'',mode,page+1,"eps",True)
	
	elif query=='play':
		from resources.lib.servers import fptPlay;fpt=fptPlay()
		xbmcsetResolvedUrl(fpt.playLink(url))

def dangcaphd(name,url,img,mode,page,query):
	ico=os.path.join(iconpath,'phim3s.png');homepage='http://dangcaphd.com/movie/movies.html'
	
	def namecolor(name):return '%s%s[/COLOR]'%(color['dangcaphd'],name)
	def dangcaphd_get_link(url,loop=True):
		hd['Cookie']=makerequest(joinpath(xsharefolder,'dchd.cookie'))
		body=make_request(url.replace('/movie-','/watch-'),headers=hd)
		if not body or re.search('class="f20 mb10"',body):
			if loop:login();dangcaphd_get_link(url,loop=False)
			else:mess(u'Hiện tại - Bạn chỉ có thể xem bản Demo của dangcaphd.com','dangcaphd.com')
		return re.findall('"(\d{,3})" _link="(.+?)" _sub="(.*?)"',body)
	
	def dangcaphd_download_sub(url):
		if myaddon.getSetting('autodel_sub')=='true':delete_files(subsfolder)
		subfullpathfilename=joinpath(subsfolder,'vie.%s'%os.path.basename(url));sub=''
		if os.path.splitext(subfullpathfilename)[1] in [".srt", ".sub", ".txt", ".smi", ".ssa", ".ass"]:
			if makerequest(subfullpathfilename,make_request(url),'wb'):sub=subfullpathfilename
		return sub
		
	def dchd_dir(s):
		href=xhref(s)
		title=xtitle(s)
		res=xsearch('"Chất lượng (.+?)"',s)
		if res:title=title+' [COLOR gold]%s[/COLOR]'%res
		img=ximg(s)
		eps=xsearch('class="bxitem-episodes"><span>(.+?)</span></span>',s).replace('<br>',' ')
		if eps:title=namecolor(title)+' - [COLOR green](%s)[/COLOR]'%eps;dir=True;query='episodes'
		else:dir=False;query='dchd_play'
		addir_info(title,href,img,'',mode,1,query,dir)
	
	def login():
		def input_captcha(tempfile):
			mywindow = xbmcgui.Window();image = xbmcgui.ControlImage(0, 0, 200,100,tempfile)
			mywindow.addControl(image);mywindow.show()
			captcha = get_input('Để login dangcaphd.com, hãy nhập chuổi bạn nhìn thấy màn hình')
			mywindow.close()
			return captcha
			
		url="http://dangcaphd.com/login.html";result='No'
		mail_dchd=myaddon.getSetting('mail_dchd');pass_dchd=myaddon.getSetting('pass_dchd')
		if not mail_dchd:
			mail_dchd='1@kodi.com';pass_dchd='123456'
			mess(u'Bạn đang dùng acc test của xshare!','xshare.vn');xbmc.sleep(5000)
		response=make_request(url,resp='o')
		if not response:return result
		hd['Cookie']=response.cookiestring
		captcha=xsearch('_captcha="(.+?)"',response.body)
		response=make_request(captcha,headers=hd)
		if not response:return result
		tempfile = joinpath(tempfolder,"temp.jpg");makerequest(tempfile,response,"wb")
		captcha=input_captcha(tempfile)
		data={'remember':'on', 'email':mail_dchd,'password': pass_dchd,'_submit': 'true','security_code':captcha}
		response=make_post(url,hd,data)
		if not response.cookies.get('user_password'):mess(u'Login không thành công!','dangcaphd.com')
		else:
			mess(u'Login thành công','dangcaphd.com')
			result='user_email=%s;user_password=%s'%(response.cookies.get('user_email'),response.cookies.get('user_password'))
			makerequest(joinpath(xsharefolder,'dchd.cookie'),result,'w')
			logout_site(result,'http://dangcaphd.com/logout.html')
		
		return result
	
	if query=='dangcaphd.com':
		body=get_home_page('dchd.html','http://dangcaphd.com/movie/top_view.html')
		name=color['search']+"Search trên dangcaphd.com[/COLOR]"
		addir(name,"dangcaphd.com",icon['dangcaphd'],mode=mode,query="search",isFolder=True)
		for i in ('Thể loại','PHIM LẺ','PHIM BỘ','QUỐC GIA','Xem nhiều (từ trang 2)','Phim chiếu rạp'):
			addir_info(namecolor(i),'',ico,'',mode,1,i,True)
		add_sep_item('----------Xem nhiều (trang 1)-----------')
		p='(<div class="tn-bxitem">.+?<div class="tn-contentdecs mb10">)'
		for s in re.findall(p,body,re.DOTALL):dchd_dir(s)
		
		if get_home_page('dchd.html','http://dangcaphd.com/movie/top_view.html',True):
			xbmc.executebuiltin("Container.Refresh")
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return dangcaphd(name,url,img,mode,page,query)
		else:return 'no'
	elif url=="dangcaphd.com":
		search_string = urllib.quote_plus(query)
		url='http://dangcaphd.com/movie/search.html?key=%s&search_movie=1'%search_string
		return dangcaphd(name,url,img,mode,1,query='page')
	
	elif query=='Thể loại':
		body=get_home_page('dchd.html','http://dangcaphd.com/movie/top_view.html')
		for href,name in re.findall('<a href="(http://dangcaphd.com/cat.+?)" title="(.+?)">',body):
			addir_info(namecolor(name),href,ico,'',mode,1,'page',True)
		
	elif query=='QUỐC GIA':
		body=get_home_page('dchd.html','http://dangcaphd.com/movie/top_view.html')
		for href,name in re.findall('<a href="(http://dangcaphd.com/country.+?)" title="(.+?)">',body):
			addir_info(namecolor(name),href,ico,'',mode,1,'page',True)
	
	elif query in ('page','PHIM LẺ','PHIM BỘ','Xem nhiều (từ trang 2)','Phim chiếu rạp'):
		if query =='PHIM LẺ':url='http://dangcaphd.com/movie/movies.html'
		elif query =='PHIM BỘ':url='http://dangcaphd.com/movie/series.html'
		elif query =='Xem nhiều (từ trang 2)':url='http://dangcaphd.com/movie/top_view.html?&per_page=35';page=2
		elif query =='Phim chiếu rạp':url='http://dangcaphd.com/movie/cinema.html'
		body=make_request(url)
		S=xsearch('<div class="tn-main-full">(.+?)<footer class="tn-footer-full">',body,1,re.DOTALL)
		for s in re.findall('(<li class=.+?</strong></span>)',S,re.DOTALL):dchd_dir(s)
			
		pn=xsearch('<a href="([^<]+?)">&gt;</a>',S).replace('amp;','')
		if pn:
			pl=xsearch('page=(\d+?)">&gt;&gt;</a>',S)
			pl=str(int(pl)/35) if pl else ''
			title=color['trangtiep']+'Trang tiếp theo: trang %d/%s[/COLOR]'%(page+1,pl)
			addir_info(title,pn,ico,'',mode,page+1,'page',True)
		
	elif query=='episodes':
		for epi,href,sub in dangcaphd_get_link(url):
			href=href.replace(' ','%20').strip()+'xshare'+sub.replace(' ','%20').strip()
			title='Tập %s - '%epi+re.sub(' - \(.+?\)','',re.sub('\[/?COLOR.*?\]','',name))
			addir_info(title,href,img,'',mode,1,'dchd_play')
		
	elif query=='dchd_play':
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
			t=xsearch("name='csrfmiddlewaretoken' value='(.+?)'",response.body)
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
		for detail in re.findall('<div class="item-film">(.+?)</p>',make_request(url,hd),re.DOTALL):
			name=xsearch('title="(.+?)"',detail);href=urlhome+xsearch('href="(.+?)"',detail)
			img=urlhome+xsearch('src="(.+?)"',detail);isFolder='/tv-series/' in href
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
			makerequest(joinpath(xsharefolder,'vuahd.html'),body,'w')
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
		head=xsearch('\((.+?)\(',xsearch('<header(.+?)header>',body,1,re.DOTALL))
		if head:head=' - '+head.strip()
		items=sets(re.findall('<a href="(.+?)" class="btn-1">Xem (.+?)</a>',body))
		items=[s for s in items if 'title=' not in s[0]]
		for href,label in items:
			title=label.strip()+'/%s - '%xsearch('\(\d{1,4}/(\d{1,4})\)',name)+remove_tag(name)+head
			addir_info(title,urlhome+href,img,fanart,mode,page,'vuahdplay')
	elif query=='vuahdplay':#xhr.setRequestHeader("X-CSRFToken", csrftoken);
		hd['Cookie']=vuahd_login();body=make_request(url+('/watch' if '/watch' not in url else ''),hd)
		href=xsearch('<source src = "(.+?)"',body)
		if not href:href=xsearch('file: "(.+?)"',body)
		if href:xbmcsetResolvedUrl(urlhome+href)#vuahd_login(hd)
		else:mess(u'Không get được maxspeed link!','vuahd.tv')

def pubvn(name,url,img,fanart,mode,page,query):
	color['pubvn']='[COLOR deepskyblue]';ico=icon['pubvn']=os.path.join(iconpath,'pubvn.png')
	urlHome='http://pubvn.net/';c='deepskyblue'
	txtfile=joinpath(xsharefolder,'pubvn'+datetime.date.today().strftime("%d")+'.txt')
	
	def login():
		if filetime('pubvntv.cookie') < 1:
			return {'User-Agent':'Mozilla/5.0','Cookie':xrw('pubvntv.cookie')}
		u=myaddon.getSetting('usernamep');p=myaddon.getSetting('passwordp')
		data=urllib.urlencode({'txtusername':u,'txtpass':p,'remeber_me1':0,'sercurity_code':''})
		b=xreadc('http://pubvn.net/phim/aj/action_login.php',{'User-Agent':'Mozilla/5.0'},data)
		mes=xsearch('"mes":"(.+?)"',b)
		if mes:
			cookie=''
			try:mess(mes.decode('unicode_escape'),'pubvn.net')
			except:mess('Sai tên đăng nhập hoặc mật khẩu.','pubvn.net')
		else:
			cookie=b.split('xshare')[1];xrw('pubvntv.cookie',cookie)
			mess(u'Login thành công','pub.vn')
		return {'User-Agent':'Mozilla/5.0','Cookie':cookie}
	
	def getiMovEps(url):
		hd=login()
		thread_id=xsearch('<input id="thread_id.+?"(\d+?)"',xread(url))
		iMovEps=xsearch('id="player" src="(.+?)"',xread(fixUrl('/bar/dodamde/'+thread_id),hd))
		return fixUrl(iMovEps),hd
	
	def pubvn_play(url):
		if '=' not in url:url,hd=getiMovEps(url)
		else:hd=login()
		"""
		id=re.search('iMov=(\d{4,6})&iEps=(\d{5,7})',url)
		if id:mov_id=id.group(1);eps_id=id.group(2)
		else:mov_id='';eps_id=''
		b=xread(url+'&server=3',hd)
		log_id=xsearch('log_id : (\d{5,7})',b)
		pub_id=xsearch('pub_id : "(.+?)"',b)
		lte_id=xsearch('lte_id : (\w{6,10})',b)
		sercur=xsearch('sercur : (\w{6,10})',b)
		hash=xsearch("hash : '(\w{8,10})'",b)
		dlink=xsearch("file: *'(.+?)'",b)
		#log(str(dlink))
		#dlink=dlink[0]
		data='action=update_last_watched&user_id=%s&mov_id=%s&eps_id=%s&time=93.78&per=1&hash=%s'
		data=data%(log_id,mov_id,eps_id,hash);log(data)
		#b=xread(fixUrl('movie/vn/vasi_blahblah.php'),hd,data)
		#xbmcsetResolvedUrl(dlink+'?start=0')
		log_id=xsearch('log_id *: *(\d+)',b)
		mov_id=xsearch('mov_id *: *(\d+)',b)
		pub_id=xsearch('pub_id *: *"(\w+)"',b)

		data='log_id=%s&mov_id=%s&pub_id=%s'%(log_id,mov_id,pub_id)
		b=xread('http://pubvn.net/movie/vn/vasibanip.php',hd,data)
		log(data);log(b)
		j=json.loads(b)
		data='lte_id=%s&mov_id=%s&eps_id=%s&log_id=%s&type=0&sercur=%s'%(j.get('pub1'),mov_id,eps_id,log_id,j.get('pub2'))
		b=xread('http://pubvn.net/movie/vn/vasibanip.php',hd,data)
		log(data);log(b)#{"pub1":"20579615","pub2":"e7ae3c5eeb36896abdfbe4938ccb67d6","success":1}
		"""
		body=xread(url+'&server=3',hd)
		dlink=xsearch("file: *'(.+?)'",body)
		if dlink:xbmcsetResolvedUrl(dlink)
		else:mess('Get link fail!','pubvn.net')
		#xbmc.sleep(2000)
	
	def pubvn_Eps(url):
		body=xread(url+'&server=3');temp=[];items=[]
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
			eps=xsearch('<p>(\d{1,3}/\d{1,3})</p>',eps.strip()).split('/')[0]>'1'
			if eps:items.append(('%s%s[/COLOR]'%(color['pubvn'],title),fixUrl(href),img,'folder'))
			else:items.append((title,fixUrl(href),img,'play'))
		return items
	def pubvn_search(string,page=1):
		data='boxphim=Filter&txtsearch=%s&page=%d'%(urllib.quote_plus(string),page)
		body=make_post(fixUrl('phim/aj/advancesearch.php'),data=data).body
		for name,href,img,type in pubvn_page(body):
			addir(name,href,img,fanart,mode,page,query=type,isFolder=(type=='folder'))
		trangcuoi=xsearch('class="vpage(\d{1,4})".{,5}>Cuối</a></li>',body).strip()
		if trangcuoi and int(trangcuoi)>page:
			name=color['trangtiep']+'Trang tiếp theo: trang %s/%s[/COLOR]'%(str(page+1),trangcuoi)
			addir(name,url,img,fanart,mode,page=page+1,query=string,isFolder=True)
		return ''
	def pubvn_make_txt(items,temps=[]):
		for href,name,img in items:
			body=make_request(fixUrl(href))
			thread_id=xsearch('/bar/threads/(\d{3,6})',body)
			eps=xsearch('<p>(\d{1,3}/\d{1,3})</p>',body);page=0
			if eps.split('/')[0]>'1':page=1;name=color['pubvn']+name+'[/COLOR]'
			temps.append((name,fixUrl('/bar/dodamde/'+thread_id),img,page))
		if temps:delete_files(data_path,mark='pubvn');makerequest(txtfile,str(temps),'w')
	
	def fixUrl(url):
		if url.startswith('http'):return url
		elif url.startswith('/'):return urlHome+url[1:]
		else:return urlHome+url
	
	def itemDIR(s):
		title=xsearch('alt="(.+?)"',s,result=xsearch('title="(.+?)\|',s)).strip()
		href=fixUrl(xsearch('href="(.+?)" class="tool',s))
		if not title or not href:return
		img=fixUrl(ximg(s))
		if '"film_series"' in s:
			dir=True;q='eps'
			label=xsearch('<p>(\d+/\d+)</p>',s)
			title=namecolor(title,c)+' [COLOR gold]%s[/COLOR]'%label
		else:dir=False;q='play'
		label=' '.join([re.sub('<.+?>','',i).strip() for i in re.findall('(</span[^/]+?/p>)',s)])
		title=title+' '+namecolor(' '.join(label.split()),'green')
		addir_info(title.replace('nbsp;',''),href,img,'',mode,1,q,dir)
	
	if query=='pubvn.tv':
		b=getHome('pubvn.html',fixUrl('phim/home.php'))
		name=color['search']+"Search trên pubvn.tv (pub.vn)[/COLOR]"
		addir(name,url,icon['icon'],mode=mode,query='search',isFolder=True)
		
		addir_info(namecolor('Phim TOP',c),'',ico,'',mode,1,'top',True)
		
		for s in re.findall('(<div class="home_.+?/a>)',b,re.S):
			title=xsearch('<a>(.+?)</a>',s)
			loai=xsearch('class="(home_.+?)"',s)
			if 'Ple' in loai:href='http://pubvn.net/phim/phim-le/32-1-2/trang1.html'
			elif 'PboEuro' in loai:href='http://pubvn.net/phim/PboEuro/60-1-2/trang1.html'
			elif 'PboAsia' in loai:href='http://pubvn.net/phim/PboAsia/60-1-2/trang1.html'
			else:return
			addir_info(namecolor(title,c),href,img,'',mode,1,'page',True)
		
		add_sep_item('------------- PHIM HOT --------------')
		for s in [i for i in re.findall('(<a.+?/a>)',b,re.S) if 'tooltipPHot' in i]:itemDIR(s)
		#"""
		for name in re.findall('<a class="Title_menu">(.+?)</a>',b):
			page+=1;name='%s%s[/COLOR]'%(color['pubvn'],name)
			addir(name,'Title_menu',img,fanart,mode,page,query='blmenu_childs',isFolder=True)
		b=b[b.find('Phim Hot'):b.find('<a>Phim lẻ</a>')]
		phimhots=re.findall('<a href="(.+?)" class=".+?" title="(.+?)\|.{,2000}src="(.+?)"',b,re.DOTALL)
		name='%sPhim HOT[/COLOR]'%color['pubvn']
		addir(name,'Phim_Hot',img,fanart,mode,page,query=query,isFolder=True)
		temp=[('Phim lẻ','32','126'),('Phim bộ Âu - Mỹ','60-1','126-1'),('Phim bộ Châu Á','60-2','126-2')]
		for name,cat_id,type in temp:
			addir('%s%s[/COLOR]'%(color['pubvn'],name),'Home_Main',img,fanart,mode,page=1,query=cat_id,isFolder=True)
			if myaddon.getSetting('phim18')=="true":
				name='%s%s[/COLOR]'%(color['pubvn'],name+' - 18+')
				addir(name,'Home_Main',img,fanart,mode,page=1,query=type,isFolder=True)
		endxbmc();pubvn_make_txt(phimhots)
		#"""
	
	elif query=='page':
		b=xread(url)
		for s in [i for i in b.split('<div class="film"') if '"film_poster"' in i]:itemDIR(s)
		
		s=xsearch('(<nav class= main_pager.+?/nav>)',b,1,re.S)
		href=xsearch('<a href="(.+?\.html)" *>Cuối</a>',s)#trangxx.html
		pages=xsearch('(\d+)',href,result='0')
		if href and int(pages) > page+1:
			title=namecolor('Page next ...%d/%s'%(page+1,pages),'lime')
			href=xsearch('href="(.+?)" *>%d</a>'%(page+1),s)
			href=url.rsplit('/',1)[0]+'/'+href
			addir_info(title,href,img,'',mode,page+1,'page',True)
	
	elif query=='top':
		b=getHome('pubvn.html',fixUrl('phim/home.php'))
		s=xsearch('(<div class="Menu_top".+?End Menu_top)',b,1,re.S)
		for s in re.findall('(<a class="Title_menu".+?/ul>)',s,re.S):
			title=xsearch('<a class="Title_menu">(.+?)</a>',s)
			addir_info(namecolor(title,c),s,ico,'',mode,1,'topMenu',True)
		
	elif query=='topMenu':
		for menuid,tabid,title in re.findall('<a menuid *= *"(.+?)" tabid="(.+?)">(.+?)</a>',url):
			addir_info(namecolor(title,c),menuid+' '+tabid,ico,'',mode,1,'topDetail',True)
	
	elif query=='topDetail':
		menuid,tabid=url.split()
		b=xread('http://pubvn.net/phim/aj/aj_top.php',data='menuid=%s&tabid=%s'%(menuid,tabid))
		for s in b.split('class="filmtop"'):itemDIR(s)
	
	elif query=='search':make_mySearch('',url,'','',mode,'get')
	elif query=="INP":pubvn_search(make_mySearch('',url,'','','','Input'))
	elif url=='pubvn.tv':page=1 if 'Trang tiếp theo' not in name else page;pubvn_search(query,page)
	elif url=='Title_menu':
		body=make_request(fixUrl('phim/home.php'))
		blmenu_childs=re.findall('<li><a menuid = "(.+?)" tabid="(.+?)">(.+?)</a></li>',body)
		for menuid,tabid,name in blmenu_childs:
			if int(tabid)==page:
				addir('%s%s[/COLOR]'%(color['pubvn'],name),'blmenu_child',img,fanart,mode,page,query=menuid,isFolder=True)
	
	elif url=='blmenu_child':
		data='tabid=%s&menuid=%s'%(str(page),query)
		body=make_post(fixUrl('phim/aj/aj_top.php'),data=data).body
		pattern='<div class="film_poster">(.+?)<a href="(.+?)" class="tooltip1" title="(.+?)\|.{,2000}src="(.+?)" (.{,500}End class = film_poster)'
		for s1,href,title,img,s2 in re.findall(pattern,body,re.DOTALL):
			s1=xsearch('<p>(\d{1,3}/\d{1,3})</p>',s1.strip()).split('/')[0]>'1'
			s2=xsearch('<p>(\d{1,3}/\d{1,3})</p>',s2.strip()).split('/')[0]>'1'
			if s1 or s2:addir('%s%s[/COLOR]'%(color['pubvn'],title),fixUrl(href),img,fanart,mode,page,query='folder',isFolder=True)
			else:addir(title,fixUrl(href),img,fanart,mode,page,query='play')
	
	elif query=='eps':
		url,hd=getiMovEps(url)
		items=pubvn_Eps(url)
		if not items:addir_info(namecolor(name),url,img,'',mode,1,'play')
		else:
			label=namecolor(name)
			for eps,href in items:
				title=eps+' - '+label
				addir(title,href,img,fanart,mode,page,query='play')
	
	elif url=='Phim_Hot':
		if not os.path.isfile(txtfile):
			for file in os.listdir(xsharefolder):
				if 'pubvn' in file:txtfile=joinpath(xsharefolder,file);break
		try:items=eval(makerequest(txtfile))
		except:items=[]
		if items:
			for name,href,img,page in items:
				addir(name,href,img,fanart,mode,page=page,query='dodamde',isFolder=(page==1))
		else:mess(u'Đang cập nhật dữ liệu - chọn lại sau 30 giây nữa nhé...')
	elif query=='dodamde':
		iMovEps=xsearch('id="player" src="(.+?)"',make_request(url))
		if page==0:pubvn_play(fixUrl(iMovEps))
		else:
			for eps,href in pubvn_Eps(fixUrl(iMovEps)):
				addir(eps+' - '+re.sub('\[.?COLOR.{,15}\]','',name),href,img,fanart,mode,page,query='play')
	elif url=='Home_Main':
		url=fixUrl('phim/aj/');data='cat_id=%s&type=%s&page=%s'
		if 'Phim lẻ' in name:url+='aj_phimle.php';data='cat_id=%s&page=%s'%(query,str(page))
		else:url+='aj_series.php';data=data%(query.split('-')[0],query.split('-')[1],str(page))
		body=make_post(url,data=data).body
		for title,href,img,type in pubvn_page(body):
			addir(title,href,img,fanart,mode,page,query=type,isFolder=(type=='folder'))
		trangcuoi=xsearch('class="catpage(\d{1,4})".{,5}>Cuối</a></li>',body).strip()
		if trangcuoi and int(trangcuoi)>page:
			name=re.sub('\[.?COLOR.{,12}\]','',name).split('*')[0].strip()
			name=color['trangtiep']+'%s * Trang tiếp theo: trang %s/%s[/COLOR]'%(name,str(page+1),trangcuoi)
			addir(name,'Home_Main',img,fanart,mode,page=page+1,query=query,isFolder=True)
	
	elif query=='play':pubvn_play(url)

def hdviet(name,url,img,mode,page,query):
	color['hdviet']='[COLOR darkorange]';ico=icon['hdviet']=os.path.join(iconpath,'hdviet.png')
	urlhome='http://movies.hdviet.com/';c='darkorange'
	if os.path.isfile(joinpath(datapath,'hdviet.cookie')):os.remove(joinpath(datapath,'hdviet.cookie'))
	direct_link='https://api-v2.hdviet.com/movie/play?accesstokenkey=%s&movieid=%s'
	
	def getcookie():
		u=myaddon.getSetting('userhdviet');p=myaddon.getSetting('passhdviet')
		import hashlib;data=urllib.urlencode({'email':u,'password':hashlib.md5(p).hexdigest()})
		response=make_post('http://movies.hdviet.com/dang-nhap.html',hd,data)
		return response.cookiestring
	
	def login_hdviet():
		u=myaddon.getSetting('userhdviet');p=myaddon.getSetting('passhdviet')
		import hashlib;data=urllib.urlencode({'email':u,'password':hashlib.md5(p).hexdigest()})
		response=make_post('http://movies.hdviet.com/dang-nhap.html',hd,data)
		try:resp=response.json#;print resp
		except:resp={u'r': u'Lỗi đăng nhập hdviet.com', u'e': 3}
		if resp.get('e')==0:
			mess(resp.get('r'),'hdviet.com');hd['Cookie']=response.cookiestring
			response=make_request('http://movies.hdviet.com/dieu-khoan-su-dung.html',headers=hd)
			import base64;token=base64.b64decode(xsearch('<a class="userinfo".+?token=(.+?)"',response))
			response={'Cookie':hd['Cookie'],'access_token':token};json_rw('hdviet.cookie',response)
		else:response=dict();mess(resp.get('r'),'hdviet.com')
		url='http://movies.hdviet.com/dang-xuat.html?accesstokenkey=%s'
		make_post(url%response.get('access_token')).body
		return response
	
	def getResolvedUrl(id_film,loop=0):#Phim le/phim chieu/ke doi dau thien ac
		def getlinkhdviet(token,id_film):
			id_film=id_film.replace('_e','&ep=')
			href=direct_link%(token,id_film)
			try:links=json.loads(xread(href)).get('r','')
			except:links={}
			#print json.dumps(links,indent=2,ensure_ascii=True)
			return links
		
		data=json_rw('hdviet.cookie')
		links=getlinkhdviet(data.get('access_token',''),id_film)
		link=links.get('LinkPlay')
		
		if not link:return '',''
		elif '0000000000000000000000' in link:
			data=login_hdviet();links=getlinkhdviet(data.get('access_token'),id_film)
			link=links.get('LinkPlay','')
		
		if link:
			max_resolution='_1920_' if myaddon.getSetting('hdvietresolution')=='1080' else '_1280_'
			resolutions=['_1920_','_1885_','_1876_','_1866_','_1792_','_1280_','_1024_','_800_','_640_','_480_']
			if '_e' in id_film:link=re.sub('%s_e\d{1,3}_'%id_film.split('_')[0],'%s_'%id_film,link)
			
			r=''.join([s for s in resolutions if s in link]);response=''
			if r:
				href=link[:link.rfind(r)]+link[link.rfind(r):].replace(r,'%s')
				for i in resolutions:
					if i>max_resolution:continue
					response=xread(href%i)
					if len(response)>0:link=href%i;break
			else:
				href=link.replace('playlist.m3u8','playlist_h.m3u8')
				response=xread(href)
				if '#EXT' not in response:
					for s in range(1,6):
						#print re.sub('http://n0\d.vn-hd.com','http://n0%d.vn-hd.com'%s,href)
						if 'http://n0%d'%s in href:continue
						elif re.search('http://n0\d.vn-hd.com',href):
							response=xread(re.sub('http://n0\d.vn-hd.com','http://n0%d.vn-hd.com'%s,href))
						if '#EXT' in response:break
				if not response:response=xread(link)
			
			if '#EXT' in response:
				items=re.findall('RESOLUTION=(\d+?)x.*\s(.+m3u8)',response)
				if items:
					res=0;hr=''
					for r,h in items:
						#print r,h
						if int(r)>res:res=int(r);hr=h
					if hr and 'http://' in hr:link=hr
					else:link=os.path.dirname(link)+'/'+hr
				else:
					items=re.findall('(.+m3u8)',response)
					if items and 'http://' in items[0]:link=items[len(items)-1]#;print items[0]
					elif items:link=os.path.dirname(link)+'/'+items[0]
				
			else:link=''
		
		if not link:return '',''
		
		audio=links.get('AudioExt',list());audioindex=-1;linksub=''
		if len(audio)==1 and 'inh' in audio[0].get("Label",''):audioindex=0
		elif len(audio)>1:
			mess(u'Chọn audio track: "Audio and subtitle settings" (hình cái loa)',timeShown=10000)
			#audio_choice=myaddon.getSetting('hdvietaudio')
			#if audio_choice=='Hỏi khi xem':
			#	title=u'[COLOR green]Chọn Audio[/COLOR]';line1= u'[COLOR yellow]Vui lòng chọn Audio[/COLOR]'
			#	audioindex=mess_yesno(title,line1,'',audio[0].get("Label",'0'),audio[1].get("Label",'1'))
			#else:audioindex=0 if u2s(audio[0].get("Label")) in audio_choice else 1
			#if 'inh' not in audio[audioindex].get("Label",''):linksub='yes'#bật cờ download sub
			#try:link=link+'?audioindex=%d'%(int(audio[audioindex].get("Index",'0'))-1)
			#try:link=link+'?audioindex=3'
			#except:pass
		
		if audioindex<0 or linksub:
			for source in ['Subtitle','SubtitleExt','SubtitleExtSe']:
				try:linksub=links[source]['VIE']['Source']
				except:linksub=''
				if linksub:break
		#print 'getResolvedUrl: %s - %s'%(link,linksub)
		return link,linksub
	
	def itemsDIR(m):
		title=xtitle(m).replace('Phim ','');href=xsearch('data-id="(.+?)"',m);img=ximg(m)
		if not title or not href:return
		label=xsearch('id="fillprofile" class="icon-(.+?)11">',m)
		if label:title+=' [COLOR green]%s[/COLOR]'%label
		label=xsearch('<label class="vl-children11">([^<]+?)</label>',m)
		if label:title='[COLOR red]%s[/COLOR] %s'%(label,title)
		label=xsearch('id="fillaudio" class="icon-(.+?)">',m)
		if label:title='[COLOR gold]TM[/COLOR] '+title
		eps=xsearch('<span class="labelchap2">(.+?)</span>',m)
		if eps:title=namecolor('%s [COLOR cyan](%s)[/COLOR]'%(title,eps),c);dir=True;q='eps'
		else:dir=False;q='hdv_play'
		addir_info(vnu(title),href,img,'',mode,1,q,dir)
	
	def hdv_page(url):
		b=xread(url)
		s=xsearch('(<h1 class="h2-ttlpage2".+?/h1>)',b)
		if s:add_sep_item(' '.join(re.split('<.+?>',s)))
		
		s=xsearch('(<[^>]+?box-movie-list.+?)<div class="box[^"]+?">',b,1,re.S)
		for s in re.findall('(<li.+?/li>)',s,re.S):itemsDIR(s)
		
		s=xsearch('(<ul class="paginglist.+?/ul>)',b,1,re.S)
		href=xhref(xsearch('(class="active".+?/ul>)',s,1,re.S))
		if href:
			pages=xsearch('>(\d+)<.+?/ul>',s)
			title=namecolor('Trang tiếp theo: %d/%s'%(page+1,pages),'lime')
			addir(title,href,img,fanart,mode,page+1,query,True)
	
	if query=='hdviet.com':
		b=getHome('hdviet.html',urlhome)
		if len(b)<1000:
			b=xsearch('<h3>(.+?)</h3>',b)
			mess(s2u(b))
		name=namecolor('Search trên hdviet.com','lime')
		addir(name,'http://movies.hdviet.com/tim-kiem.html',ico,fanart,mode,1,'search',True)
		
		s=re.findall('(<a class="mainitem".+?</a>)',b,re.S)
		for s in [i for i in s if [j for j in ('phim-le','phim-bo','tv-show') if j in i]]:
			href=xhref(s);title=xtitle(s)
			if 'menuid' in s:addir_info(namecolor(title,c),href,ico,fanart,mode,1,'submenu',True)
			else:addir_info(namecolor(title,c),href,ico,fanart,mode,1,'hdv_page',True)
		
		S=re.findall('(<div class="h2-ttl cf".+?/ul>)',b,re.S)
		m=[]
		for s in S:
			for i in re.findall('(<li.+?/li>)',s,re.S):m.append(i)
		
		add_sep_item('HDViet giới thiệu ---------------')
		s=xsearch('(<div class="homebanner".+?/ul>)',b,1,re.S)
		for href,img,title in re.findall('<li><a href="(.+?)"><img src="(.+?)" title="(.+?)"',s):
			s='\n'.join(i for i in m if href in i)
			if s:itemsDIR(s)
			else:addir_info(namecolor(vnu(title.replace('Phim ','')),c),href,ico,fanart,mode,1,'eps',True)
		
		for s in S:
			m=xsearch('(<a.+?Xem tất cả...</a>)',s,1,re.S)
			href=xhref(m)
			title=' (click) '.join(i for i in re.split('<.+?>',m) if i)+ ''
			addir_info(namecolor(vnu(title),'lime'),href,ico,fanart,mode,1,'hdv_page',True)
			for m in re.findall('(<li.+?/li>)',s,re.S):itemsDIR(m)
	
	elif query=='search':make_mySearch('','hdviet.com','','',mode,'get')
	elif url=='hdviet.com' or query=="INP":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			page=1
			if not query:return
		
		b=xread('http://movies.hdviet.com/tim-kiem-nhanh.html?keyword=%s'%urllib.quote_plus(query))
		try:j=json.loads(b).get('Title')
		except:j={}
		if j:
			add_sep_item('Kết quả tìm nhanh ------------')
			for i in j:
				i=j.get(i);href=i.get('MovieID');img=i.get('Backdrop').replace(' ','')
				title=namecolor(u2s(i.get('KnownAs')+' - '+i.get('MovieName')),c)
				addir_info(title,href,img,img,mode,1,"eps",True)
		
		hdv_page('http://movies.hdviet.com/tim-kiem.html?keyword=%s'%urllib.quote(query))
	
	elif query=='submenu':
		b=xrw('hdviet.html')
		s=''.join([i for i in b.split('class="mainitem"') if url in i and 'menuid=' in i])
		label=''
		addir_info(name,url,ico,fanart,mode,1,'hdv_page',True)
		for s in re.findall('(<a.+?/a>)',s,re.S):
			title=xsearch('>([^<]+?)</a>',s,1,re.S).strip()
			href=xsearch('href="(.+?)"',s)
			if '"childparentlia"' in s or '"childparentlib"' in s:label=title
			else:title=label+' '+title
			addir_info(namecolor(title.strip(),c),href,ico,fanart,mode,1,'hdv_page',True)
	
	elif query=='eps':
		if url.startswith('http'):url=xsearch('mid: *(\d+)',xread(url))
		href='http://movies.hdviet.com/lay-danh-sach-tap-phim.html?id=%s'%url
		try:j=json.loads(xread(href))
		except:j={}
		if not j or j.get("Sequence","0")=="0":
			addir_info(namecolor(name),url,img,fanart,mode,page,'hdv_play')
			return
		
		label=namecolor(name)
		for epi in range(1,int(j.get("Sequence"))+1):
			title='%d %s'%(epi,label)
			addir_info(title,'%s_e%d'%(url,epi),img,fanart,mode,page,'hdv_play')
	
	elif query=='hdv_page':hdv_page(url)
	
	elif query=='hdv_play':
		link,sub=getResolvedUrl(url)
		if link:
			if sub:
				sub=xget(sub)
				if sub:sub=sub.geturl();mess(u'Phụ đề của HDViet.com','hdviet.com')
				else:sub=''
			xbmcsetResolvedUrl(link,sub=sub)
		else:mess(u'Get link thất bại!','hdviet.com')

def hayhaytv(name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'hayhaytv.png');c='tomato';urlhome='http://www.hayhaytv.vn/'
	api='http://api.hayhaytv.vn/'
	hd={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/54.0.2840.99 Safari/537.36',
		'Cookie':xrw('hayhaytv.cookie')}
	
	def detail(s):
		title=xsearch('alt="(.+?)"',s)
		href=xhref(s)
		img=ximg(s)
		if not href or not title:return
		eps=re.sub('<strong>','',xsearch('<span class="label-range">(.+?)</strong>',s).strip())
		#if not eps:addir_info(title,href,img,'',mode,1,'play')
		#else:addir_info(namecolor(title,c)+' [COLOR blue]%s[/COLOR]'%eps,href,img,'',mode,page,'eps',True)
		title=namecolor(title,c)+' [COLOR blue]%s[/COLOR]'%eps
		addir_info(title,href,img,'',mode,page,'eps',True)
	
	if query=='hayhaytv.vn':
		if filetime('hayhaytv.html') > 1:
			body=xreadc(urlhome,hd)
			xrw('hayhaytv.html',body)
			xrw('hayhaytv.cookie',body.split('xshare')[1])
		else:body=xrw('hayhaytv.html')
			
		body=re.sub('>\s*<','><',body)
		title=color['search']+"Search trên hayhaytv.vn (director/film/actor/show)[/COLOR]"
		addir_info(title,'hayhaytv.vn',ico,'',mode,1,'search',True)
		
		for href,title in [("phim-le.html",'PHIM LẺ'),("phim-bo.html","PHIM BỘ"),("show.html","SHOW"),("","THỂ LOẠI"),("","QUỐC GIA"),("","NĂM PHÁT HÀNH")]:
			if href:href='http://www.hayhaytv.vn/'+href;query='page'
			else:query='menu'
			addir_info(namecolor(title,c),href,ico,'',mode,1,query,True)
		
		S=body.split('<div class="group-title-bg">')
		t=''.join(i for i in S if '>XEM NHIỀU</a>' in i)
		s=[i for i in t.split('id="content_') if '<h3>' in i]
		
		for s in s:
			add_sep_item('-----------%s-----------'%xsearch('<h3>(.+?)</h3>',s))
			for s in re.findall('(<li.+?/li>)',s):detail(s)
			
		for s in S:
			label=re.search('<span class="title\d+"><a href="([^"]+)">([^<]+)</a>',s)
			if label:
				title='[COLOR lime]-----------%s-----------[/COLOR]'%label.group(2)
				href=label.group(1)
				if 'http' not in href:href='http://www.hayhaytv.vn'+href
				addir_info(title,href,ico,'',mode,page,'page',True)
				
				s=xsearch('(<ul.+?/ul>)',s,1,re.DOTALL)
				t=('<div class="block-base movie">','<div class="block-base movie clearfix">','<div class="block-base movie clearfix">','class="ntipse"')
				for i in t:
					if i in s:s=s.split(i);t='';break
				if t:return	
				
				for s in s:detail(s)
					
			elif '<div id="main-banner">' in s:
				add_sep_item('-----------Hayhaytv giới thiệu-----------')
				for href,t1,t2 in re.findall('<a href="([^"]+)"><[^<]+>([^<]+)<.+?>([^<]+)</span>',s):
					title=t1+' - '+t2
					img=xsearch('<a href="%s"><img[^<]+src="([^"]+)"'%href,s)
					addir_info(namecolor(title,c),href,img,img,mode,1,'eps',True)

	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="hayhaytv.vn":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query or not query.strip():return
		search_string = urllib.quote_plus(query)
		url='http://www.hayhaytv.vn/tim-kiem.html?term='+search_string
		hd={'User-Agent':'Mozilla/5.0','X-Requested-With':'XMLHttpRequest'}
		try:j=json.loads(xread(url,hd))
		except:j={}

		for s in ('phim','show'):
			for i in j.get(s,{}):
				eps=i.get('total_episode','')
				try:Eps=int(eps)
				except:Eps=0
				epi=i.get('last_episode','')
				title=i.get('name','')+' '+i.get('extension','')
				if Eps>1:dir=True;eps='%s/%s '%(epi,eps);q='eps';title=namecolor(title,c)
				else:dir=False;q='play';eps=''
				href=i.get('link','')
				img=i.get('image','')
				nokey=('total_episode','last_episode','name','link','image','type_show','type_film')
				label=' '.join(i.get(m) for m in i.keys() if m not in nokey and i.get(m))
				title=title+' [COLOR green]%s[/COLOR]'%(eps+label)
				addir_info(u2s(title),href,img,'',mode,page,q,dir)

	elif query=="menu":
		b=re.sub('>\s*<','><',getHome('hayhaytv.html',urlhome))
		S=' '.join(i for i in b.split('class="tnico-') if namecolor(name) in i)
		for href,title in re.findall('href="([^"]+?)".*?>([^"]+?)</a>',S):
			if 'http' not in href:href='http://www.hayhaytv.vn'+href
			addir_info(namecolor(title,c),href,ico,'',mode,page,'page',True)
		
	elif query=="page":
		b=re.sub('>\s*<','><',xread(url,hd))
		p1='<div class="group-title">';p2='<div class="block-base movie">'
		S=' '.join(i for i in b.split(p1) if p2 in i)
		for s in S.split(p2):detail(s)
		
		pn=xsearch('<a href="([^"]+?)">Sau</a>',S)
		if pn:
			pages=xsearch('<a href="[^"]+page=(\d+)">Cuối</a>',S)
			name=re.sub('\[COLOR %s.+/COLOR\]'%color['trangtiep'],'',name)
			title=name+color['trangtiep']+' Trang tiep theo...trang %d/%s[/COLOR]'%(page+1,pages)
			if 'http' not in pn:pn='http://www.hayhaytv.vn'+pn
			addir_info(title,pn,ico,'',mode,page+1,query,True)

	elif query=="eps":
		b=re.sub('>\s*<','><',xread(url,hd))
		s=re.findall('<a class="ep-link.+?href="(.+?)">(.+?)</a>',b)
		if not s:
			addir_info(namecolor(name),url,img,'',mode,1,'play')
		else:
			for href,title in s:
				addir_info(title+' '+namecolor(name),href,img,'',mode,1,'play')
	
	elif query=="play":
		from resources.lib.servers import hayhayvn;hh=hayhayvn(c);link=''
		link=hh.getLink(url)
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','hayhaytv.vn') 
	
	elif query=="play1":
		b=xread(url)
		s=re.findall("file:'([^']+?)',label:'([^']+?)'",b)
		link=''
		if s:
			L=list(set([(i[0],resolu(i[1])) for i in s]))#;print L
			L=sorted(L, key=lambda k: int(k[1]),reverse=True if myaddon.getSetting('resolut')=='Max' else False)
			#print href,L
			for href,r in L:
				link=dl(href)#;print 'a',link,'b',href
				if link:break
		else:
			s=list(set(re.findall("file:.?'([^']+)'",b)))#;print s
			for href in s:
				if 'm3u8' in href:link=href;break
			if not link:
				for href in s:
					if 'youtube.com' in href:link=href;break
		if 'youtube.com' in link:play_youtube(link)
		elif link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','phimbathu.com') 

def phimmoi(name,url,img,mode,page,query):
	c='ghostwhite';ico=os.path.join(iconpath,'phimmoi.png')
	urlhome='http://www.phimmoi.net/';refresh=False
	
	def fixURL(href):
		if not href.startswith('http'):href=urlhome+href
		return href
	
	def itemDIR(s):
		title=xtitle(s,'(<h.+?)<span');href=xhref(s)
		title=' '.join(re.sub('<.+?>',' ',title).split())
		if not title or not href:return
		label=re.findall('(<span.+?/span>)',s)
		def abc(s):return [i for i in ('title-1','title-2','item-en','item-vn') if i in s]
		label=''.join(i for i in label if not abc(i))
		label=' '.join(re.sub('<.+?>',' ',label).split())
		label='[COLOR green]%s[/COLOR]'%label
		if re.search('.huyết .inh',label):title='[COLOR gold]TM[/COLOR] '+title
		title=title+' '+label
		img=ximg(s,"url\('?(.+?)'?\)")
		addir_info(s2c(title),fixURL(href),img,'',mode,1,'eps',True)
	
	def pm_getPage(url):
		b=xread(url)
		for s in re.findall('(<li class="movie-item">.+?</li>)',b,re.DOTALL):itemDIR(s)
		href=xsearch('<li><a href="(.+?)">Trang kế.+?</a></li>',b)
		if href:
			title=namecolor('Trang kế ...%d'%(page+1),'lime')
			addir_info(title,fixURL(href),ico,'',mode,page+1,'pm_page',True)
	
	if query=='phimmoi.net':
		b=getHome('phimmoi.html',urlhome)
		name=color['search']+"Search trên phimmoi.net[/COLOR]"
		addir_info(name,'http://www.phimmoi.net/tim-kiem/',ico,'',mode,1,'search',True)
		
		s=xsearch('<ul id=".+?"(.+?)</ul></div>',b)
		
		for title in re.findall('<a>(.+?)</a>',s):
			addir_info(namecolor(title,c),'',ico,'',mode,1,'menubar',True)
		
		p='<a href="([\w|-]+/|http://www.phimmoi.net/tags/.*?)">(.+?)</a>'
		for href,title in re.findall(p,s):
			addir_info(namecolor(title,c),href,ico,'',mode,1,'menubar',True)
		
		p='<h2 class="right-box-header star-icon"><span>(.+?)</span>'
		for title in re.findall(p,b):
			if title=='Phim đã đánh dấu':continue
			addir_info(namecolor(title,c),'right-box',img,'',mode,1,'menubar',True)
		
		p='class="title-list-index">(.+?)</span>(.+?</div></div></div>)'
		for s in re.findall('(<h2 class="header.+?/ul>)',b):
			m=xsearch('(<h2.+?/h2>)',s)
			if 'href=' in m:
				title=re.search('title="(.+?)">(.+?)</a>',m)
				if title:
					title='%s - %s'%(title.group(1),title.group(2))
					href='http://www.phimmoi.net/'+xsearch('href="(.+?)"',m)
					addir_info(namecolor(title,'gold'),href,ico,'',mode,1,'pm_page',True)
			else:add_sep_item(xsearch('<span class="title-list-index">(.+?)</span>',m))
			
			s in xsearch('(<ul.+?/ul>)',s)
			for s in re.findall('(<li.+?/li>)',s):itemDIR(s)
	
	elif query=='search':make_mySearch('','phimmoi.net','','',mode,'get')
	elif url=='phimmoi.net' or query=="INP":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			page=1
		pm_getPage('http://www.phimmoi.net/tim-kiem/%s/'%urllib.quote_plus(query))
	
	elif query=='menubar':
		if any(s for s in ['kinh','rap','tags','trailer'] if s in url):
			if 'tags' not in url:url=urlhome+url
			return phimmoi(name,url,img,mode,page,'pm_page')
		elif url=='right-box':
			name=namecolor(name)
			b=xrw('phimmoi.html')
			s=re.findall('(<div class="right-box top-film-week".+?/ul>)',b,re.S)
			items=re.findall('(<li.+?/li>)',''.join(i for i in s if name in i))
			for s in items:itemDIR(s)
		else:
			content=xsearch('<ul id=".+?"(.+?)</ul></div>',xrw('phimmoi.html'))
			gen={'Thể loại':'the-loai','Quốc gia':'quoc-gia','Phim lẻ':'phim-le','Phim bộ':'phim-bo'}
			query=gen.get(re.sub('\[/?COLOR.*?\]|\(.+?\)','',name).strip())
			p='<a href="(%s/.*?)">(.+?)</a>'%query
			for href,title in re.findall(p,content):
				addir_info(namecolor(title,c),urlhome+href,ico,'',mode,1,'pm_page',True)
	
	elif query=='pm_page':pm_getPage(url)
	
	elif query=='eps':
		if url.endswith('/'):href=url+'xem-phim.html'
		else:href=url
		b=xread(href)
		if not b and url.endswith('/'):#Trailer
			href=url+'trailer.html'
		
		label=xsearch('<title>(.+?)</title>',b,1,re.S).replace('Xem phim ','')
		name=label if label else name
		p='(<div class="movie-list-index related-box".+?class="clear">)'
		cungchude=xsearch(p,b,1,re.S)
		chude='Mục các phim cùng chủ đề'
		
		servers=xsearch('(<div class="list-server".+?class="clear">)',b,1,re.S)
		if not servers:
			addir_info(name,href,img,fanart,mode,1,'play')
			s=re.findall('(<li.+?/li>)',cungchude)
			if s:
				add_sep_item(chude)
				for s in s:itemDIR(s)
		
		else:
			if cungchude:
				addir_info(namecolor(chude,'gold'),cungchude,ico,'',mode,1,'cungchude',True)
			servers=re.findall('(<h3.+?/ul>)',servers,re.S)
			for s in servers:
				if len(servers)>1:
					server=xsearch('(<h3.+?/h3>)',s,1,re.S)
					server=' '.join(re.sub('<.+?>','',server).split())
					add_sep_item(server)
				for href,title in re.findall('href="(.+?)">(.+?)</a>',s.replace('\n','')):
					title='%s %s'%(title.strip(),name)
					addir_info(title,fixURL(href),img,fanart,mode,1,'play')
	
	elif query=='cungchude':
		for s in re.findall('(<li.+?/li>)',url):itemDIR(s)
	
	elif query=='play':
		if 'trailer.html' in url:link=xsearch("trailerUrl='(.+?)'",xread(url))
		else:
			from resources.lib.servers import phimoinet;pm=phimoinet()
			link=pm.getLink(url)
		if link:xbmcsetResolvedUrl(link)

def phim3s(name,url,img,mode,page,query):
	ico=os.path.join(iconpath,'phim3s.png');urlhome='http://phim3s.net/'
	if not os.path.isfile(ico):
		try:urllib.urlretrieve('https://static-s.aa-cdn.net/img/ios/888227595/8efccc86a2a835c412ab46cbf99c3e15',ico)
		except:pass
	
	def namecolor(name):return '%s%s[/COLOR]'%(color['phim3s'],name)
	def namenocolor(n):return xsearch('%s(.+?)\['%color['phim3s'].replace('[','\[').replace(']','\]'),n)
	def login(u='xshare',p='xsharethaitni'):
		hd['X-Requested-With']='XMLHttpRequest';data={'username':u,'password':p}
		try:l=make_post('http://phim3s.net/member/login/',hd,data);cookie=l.cookiestring;l=l.json
		except:l={};cookie=''
		mess(u'%s'%l.get('message',['Login to phim3s.net fail !',''])[0],'Login to Phim3s.net');hd['Cookie']=cookie
		return hd
	
	def clip_getdetail(body):	
		for s in re.findall('(<div class="box">.+?</div>)',body,re.DOTALL):
			href=xhref(s)
			title=xtitle(s)
			img=xsearch('lsrc="(.+?)"',s)
			dur=xsearch('<span class="video-time">(.+?)</span>',s)
			addir_info(title,href,img,img,mode,1,"clip_play")
		pagination=re.search('<a href="[^<]+?">(\d+?)</a></li><li><a href="([^<]+?)">&gt;</a>',body)
		if pagination:
			name=color['trangtiep']+'Trang tiếp theo: trang %d/%s[/COLOR]'%(page+1,pagination.group(1))
			addir_info(name,pagination.group(2),img,'',mode,page+1,'clip_items',True)
	
	if query=='phim3s.net':
		body=get_home_page('phim3s.html',urlhome)
		title=color['search']+"Search trên phim3s.net[/COLOR]"
		addir_info(title,'phim3s.net',ico,'',mode,1,'search',True)
		title=color['search']+"Hộp phim của tôi trên phim3s.net[/COLOR]"
		addir_info(title,'http://phim3s.net/ajax/member/get_bookmarks',ico,'',mode,1,'get_bookmark',True)
		
		S=xsearch('(<ul class="container menu">.+?</ul></div>)',body)
		for title in re.findall('<a>(.+?)</a><ul class="sub-menu"',S):
			addir_info(namecolor(title),'',img,img,mode,1,"p3s_menu",True)
		
		i=re.findall('</ul></li><li><h3><a href="(.+?)" title=".*?">(\D+?)</a></h3><ul class="sub-menu"',S)
		for href,title in i:addir_info(namecolor(title),href,img,img,mode,1,"p3s_menu",True)
		i=re.findall('<a href="([^<]+?)" title="[^<]+?">([^<]+?)</a>',S)
		try:
			s=i[len(i)-2];addir_info(namecolor(s[1]),s[0],img,img,mode,1,"p3s_page",True)
			s=i[len(i)-1];addir_info(namecolor(s[1]),s[0],img,img,mode,1,"p3s_page",True)
		except:pass
		
		add_sep_item("------------------------------------")
		addir_info(namecolor('Xem nhiều nhất Ngày/Tuần/Tháng'),'tuan',img,img,mode,1,"xemnhieu",True)
		S=xsearch('(<ul class="tab topviewday">.+?</ul>)',body)
		i=re.findall('<a href="(.+?)" title=".+?">(.+?)</a>',S);menu={'bookmark':{'action':'Add'}}
		for href,title in i:
			addir_info(namecolor(title),urlhome+href,img,img,mode,1,"get_server",True,menu=menu)
		
		add_sep_item("------------------------------------")
		addir_info('Phim bộ đã hoàn thành','',img,img,mode,1,"")
		S=xsearch('(<ul class="list tab phim-bo-full.+?</ul>)',body)
		i=re.findall('<a href="(.+?)" title=".+?">(.+?)</a>',S)
		
		for href,title in i:
			addir_info(namecolor(title),urlhome+href,img,img,mode,1,"get_server",True,menu=menu)
		
		if get_home_page('phim3s.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
		
	elif query=="xemnhieu":
		body=get_home_page('phim3s.html')
		if url=='tuan':
			addir_info(namecolor('Xem nhiều nhất Tháng'),'thang',img,img,mode,1,"xemnhieu",True)
			S=xsearch('(<ul class="tab topviewweek.+?</ul>)',body)
		else:S=xsearch('(<ul class="tab topviewmonth.+?</ul>)',body)
		i=re.findall('<a href="(.+?)" title=".+?">(.+?)</a>',S);menu={'bookmark':{'action':'Add'}}
		for href,title in i:
			addir_info(namecolor(title),urlhome+href,img,img,mode,1,"get_server",True,menu=menu)
	
	elif query=="p3s_menu":
		body=get_home_page('phim3s.html');name=namenocolor(name)
		if not url:
			S=xsearch('(<a>%s</a><ul class="sub-menu".+?</a></li></ul></li>)'%name,body)
			i=re.findall('<a href="(.+?)" title=".+?">(.+?)</a>',S)
			for href,title in [s for s in i if url in s[0]]:
				addir_info(namecolor(title),urlhome+href,img,img,mode,1,"p3s_page",True)
		else:
			S=xsearch('</ul></li><li><h3><a href="%s"(.+?</li></ul>)'%url,body)
			for href,title in re.findall('href="(.+?)" title=".+?">(.+?)</a>',S):
				addir_info(namecolor(title),urlhome+href,img,img,mode,1,"p3s_page",True)
			phim3s(name,url,img,mode,page,'p3s_page')
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return phim3s(name,url,img,mode,page,query)
		else:return 'no'
	elif url=="phim3s.net":
		search_string = urllib.quote_plus(query)
		url='http://phim3s.net/search/%s'%search_string
		return phim3s(name,url,img,mode,1,query='p3s_page')
	
	elif query=='clip_getpage':
		body=get_home_page('phim3s_clip.html','http://m-viet.com/');c='[COLOR orange]'
		addir_info(c+'Clip[/COLOR]','http://m-viet.com/popular/',img,img,mode,0,"clip_items",True)
		addir_info(c+'Danh mục[/COLOR]','http://m-viet.com/category/tin-tuc',img,img,mode,0,"clip_items",True)
		clip_getdetail(body)
		if get_home_page('phim3s_clip.html','http://m-viet.com/',True):xbmc.executebuiltin("Container.Refresh")
	
	elif query=='clip_items':
		body=make_request(url);name=xsearch('\](.+?)\[',name)
		if page==0:
			page==1
			if '/category/' in url:
				s=xsearch('(>%s</a>.+?</ul>)'%name,body,1,re.DOTALL)
				p='href="(.+?)" title=".+?">(.+?)</a>'
			else:
				s=xsearch('(<li><a title=".+?" href="%s">.+?</ul>)'%url,body,1,re.DOTALL)
				p='href="(.+?)">(.+?)</a>'
			for href,title in re.findall(p,s):
				if href==url:continue
				addir_info('[COLOR orange]'+title+'[/COLOR]',href,img,img,mode,1,"clip_items",True)
		clip_getdetail(body)
		
	elif query=="clip_play":
		body=make_request(url)
		link=xsearch('src="(http://www.youtube.com/.+?)"',body)
		if link:play_youtube(link)
		
	elif query=='p3s_page':
		if '/m-viet.com/' in url:return phim3s(name,'http://m-viet.com/',img,mode,1,query='clip_getpage')
		if 'http://' not in url:url=urlhome+url
		body=xsearch('(<ul class="list-film">.+?</span></div></div></div></div>)',make_request(url),1,re.DOTALL)
		i=re.findall('<a href="(.+?)".+?img src="(.+?)".+?title="(.+?)".+?class="status">(.+?)</div>',body)
		if not i:
			i=re.findall('href="([^"]+?)" title="([^"]+?)"><img src="([^"]+?)"',body)
			if i:i=[(j[0],j[2],j[1],'') for j in i]
		menu={'bookmark':{'action':'Add'}}
		for href,img,title,res in i:
			title=namecolor(title)
			if res:title+=' [COLOR gold]'+res+'[/COLOR]'
			addir_info(namecolor(title),href,img,img,mode,1,"get_server",True,menu=menu)
			
		i=re.search('<a href="[^<]+?">(\d+?)</a></span><span class="item"><a href="([^<]+?)">Next</a></span>',body)
		if i:
			name=color['trangtiep']+'Trang tiếp theo: trang %d/%s[/COLOR]'%(page+1,i.group(1))
			addir_info(name,i.group(2),img,'',mode,page+1,'p3s_page',True)
			
	elif query=='get_server':
		if 'http://' not in url:url=urlhome+url
		if '/tag/' in url or '/search/' in url:return phim3s(name,url,img,mode,page,'p3s_page')
		elif '/xem-phim/' not in url:url=url+'xem-phim/'
		body=make_request(url);menu={'bookmark':{'action':'Add'}};result=False
		for s in re.findall('(<div class="server">.+?</ul></div>)',body,re.DOTALL):
			server=xsearch('</i>(.+?)</div>',s)
			if server:addir_info(color['trangtiep']+server+'[/COLOR]','',ico,'',mode,1,"");result=True
			for id,href,title in re.findall('data-episode-id="(.+?)" href="(.+?)" title="(.+?)"',s):
				result=True
				addir_info(re.sub('Server V.I.P.+?- ','',title)+' '+name,urlhome+href,img,'',mode,1,"p3s_play",menu=menu)
	
	elif query=='get_bookmark':
		from resources.lib.servers import phim3s_net
		p3s=phim3s_net(myaddon.getSetting('p3s_u'),myaddon.getSetting('p3s_p'))
		bookmark=p3s.get_bookmark();menu={'bookmark':{'action':'Remove'}}
		for i in bookmark.get('json'):
			bm=bookmark.get('json')[i];href=bm.get('link');img=bm.get('thumb_url')
			title=u2s(bm.get('short_title')+' - '+bm.get('short_title_o'))
			text=bm.get('pagetext');fanart=xsearch('"(http.+?\.jpg)',text)
			if not fanart:fanart=img
			addir_info(namecolor(title),href,img,fanart,mode,1,"get_server",True,menu=menu)
			
	elif query=='add_bookmark' or query=='remove_bookmark':
		from resources.lib.servers import phim3s_net
		p3s=phim3s_net(myaddon.getSetting('p3s_u'),myaddon.getSetting('p3s_p'))
		p3s.action_bookmark(url,query)
		if query=='remove_bookmark':xbmc.executebuiltin("Container.Refresh")

	elif query=='p3s_play':
		import time;hd['X-Requested-With']='XMLHttpRequest';id=xsearch('/(\d+)',url);max_link=''
		href='http://phim3s.net/ajax/episode/embed/?episode_id=%s&_=%d'%(id,int(time.time()*1000))
		j=make_request(href,hd,resp='j')
		#makerequest(r'd:\xoa.html',str(j)+href+str(hd),'w')
		href=j.get('grabber')+'?link='+urllib.quote_plus(j.get('video_url_hash'))+'&json=1'#&s=19'
		l=make_request(href,resp='j')
		if not l:print 'swapping..............';l=make_request(re.sub('http://sub.\.','http://sub4.',href),resp='j')
		
		if l:
			#print json.dumps(l,indent=2,ensure_ascii=True)
			L=[(s.get('file'),resolu(s.get('label'))) for s in l]
			#print L
			L=sorted(L, key=lambda k: int(k[1]),reverse=True if myaddon.getSetting('resolut')=='Max' else False)
			for href,label in L:
				max_link=dl(href)
				if max_link:break
		
		if not max_link:
			videoUrl=xsearch("videoUrl = '(.+?)'",make_request(url))
			if videoUrl:max_link=dl(href)
		
		if max_link:xbmcsetResolvedUrl(max_link)
		else:mess('No playable source found!','phim3s.net')
	
def kenh88(name,url,img,fanart,mode,page,query,text=''):
	color['kenh88']='[COLOR cyan]';ico=os.path.join(iconpath,'kenh88.png')
	urlhome='http://www.kenh88.com/';c=re.sub('\[COLOR |\]','',color['kenh88'])
	if not os.path.isfile(ico):
		try:urllib.urlretrieve('http://www.kenh88.com/images/logo_kenh88.png',ico)
		except:pass
	
	def getpage(url,name):
		name=xsearch(']([^\[]+)',name)
		for tap,href,title,img in k88.getPage(url):
			if title=='pageNext':
				title=namecolor(name,'gold')+namecolor(' Trang tiep theo...trang %d/%s'%(page+1,tap),'lime')
				addir_info(title,href,ico,'',mode,page+1,query,True)
			else:addir_info(namecolor(title,c),href,img,img,mode,1,"episode",True)
	
	from resources.lib.servers import k88com;k88=k88com(c)
	if query=='kenh88.com':
		body=get_home_page('kenh88.html',urlhome)
		title=color['search']+"Search trên kenh88.com[/COLOR]"
		addir_info(title,'kenh88.com',ico,'',mode,1,'search',True)
		addir_info(namecolor('Xem nhiều nhất',c),'',img,img,mode,1,"xemnhieu",True)
		menu=re.findall('<a title="(.+?)"[\s| ].*?href="(.+?)"[\s| ].+?class=".+?">',body)
		for title,href in menu:
			if title=='Home':continue
			elif 'javascript' in href:
				addir_info(namecolor(title,c),'',img,img,mode,1,"k88_menu",True)
			else:
				href=urlhome+href.replace('/','')
				addir_info(namecolor(title,c),href,img,img,mode,1,"k88_getpage",True)
		
		add_sep_item('-----------------------------------------------')
		for S in re.findall("(<div class=''.+?/h2>)",body,re.DOTALL):
			tap,href,title,img=k88.getDetail(S)
			addir_info(namecolor(title,c),href,img,img,mode,1,"episode",True)
		if get_home_page('kenh88.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="kenh88.com":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query:return 'no'
		getpage('http://www.kenh88.com/film/search?keyword=%s'%urllib.quote_plus(query),name)
	
	elif query=='k88_menu':
		loai=xsearch('\](.+?)\[',name)
		S=xsearch('(<a title="%s".+?/ul>)'%loai,get_home_page('kenh88.html'),1,re.DOTALL)
		for href,title in re.findall('href="/(.+?)">(.+?)</a>',S):
			addir_info(namecolor(title,c),urlhome+href,img,img,mode,1,"k88_getpage",True)
	
	elif query=='episode':
		name=namecolor(name)
		d=k88.episode(url);items=[]
		if len(d)>1:
			for i in sorted(list(d)):
				if len(d[i])>10 and not items:items=d[i];j='[COLOR gold]%s (Default)[/COLOR]'%i
				else:j=i
				if items:
					text=str([(m[0],'%s - %s'%(m[1],name)) for m in d[i]])
					addir_info(namecolor(j,c),'',img,'',mode,1,"list_episode",True,text=text)
				else:
					add_sep_item('List episode of %s ---------------------------'%i)
					for href,title in d[i]:
						addir_info('%s - %s'%(title,name),href,img,'',mode,1,"k88_play")
			if items:
				add_sep_item('List episode of default Server ---------------------------')
				for href,title in items:
					addir_info('%s - %s'%(title,name),href,img,'',mode,1,"k88_play")
		else:
			for i in d:
				for href,title in d[i]:
					addir_info('%s - %s'%(title,name),href,img,'',mode,1,"k88_play")
	
	elif query=='list_episode':
		for href,title in eval(text):
			addir_info('%s - %s'%(title,namecolor(name)),href,img,'',mode,1,"k88_play")
	
	elif query=='k88_getpage':getpage(url,name)
	
	elif query=='xemnhieu':		
		body=get_home_page('kenh88.html');top={'1':'TOP Ngày','2':'TOP Tuần','3':'TOP Tháng'}
		for S in re.findall('("sidebarlist-(\d)">.+?div id)',body,re.DOTALL):
			addir_info(color['trangtiep']+top.get(S[1])+'[/COLOR]','',img,img,mode,1,"")
			for href,title,img in re.findall('<a href="/(.+?)"><img alt="(.+?)" src="/(.+?)"',S[0]):
				href='%sxem-phim-online/%s'%(urlhome,os.path.basename(href))
				addir_info(namecolor(title,c),href,urlhome+img,urlhome+img,mode,1,"episode",True)
	
	elif query=='k88_play':
		link=k88.getLink(url)
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','Kenh88.com')

def phimdata(name,url,img,mode,page,query):
	ico=os.path.join(iconpath,'phimdata.png');urlhome='http://www.phimdata.com/';c='FFDB4BDA'
	if not os.path.isfile(ico):
		try:urllib.urlretrieve('http://www.phimdata.com/images/logo_kenh88.png',ico)
		except:pass
	
	def get_detail(s):
		tap=xsearch('class="process">Tập <p>(.+?)</p></span>',s)
		if not tap:tap=xsearch('class="process_r">(.+?)</span>',s)
		res=xsearch('<span class="status">(.+?)</span>',s)
		href='%scoi-phim-online/%s'%(urlhome,os.path.basename(xsearch('href="/(.+?)"',s)))
		title=xsearch('href=".+?">([^<].+?)</a>',s)+'-'+xsearch('href=".+?">.+?</a>(.+?)</h2>',s)
		title=' '.join(title.split())
		if res:title+='[COLOR blue]-%s[/COLOR]'%res
		if tap:title+='[COLOR gold]-%s[/COLOR]'%tap
		img=urlhome+xsearch('src="/(.+?)"',s)
		return tap,href,title,img
	
	def get_maxlink(body):
		link=xsearch('proxy.link=(.+?)&',body);max_link='';width=0
		if 'dailymotion' in link:
			body=make_request(link)
			data=xsearch('"qualities"\:(.+?\}\]\}),',body)
			try:data=json.loads(data)
			except:data={}
			for d in data:
				try:
					detail=data.get(d)[0]
					if 'video' in detail.get('type') and int(d)>width:
						width=int(d);max_link=detail.get('url')
				except:pass
		elif 'www.youtube.com' in link:max_link=link
		elif 'phimhub.com' in link:max_link=link
		elif 'drive.google.com' in link:
			link=link.split('*')[0]
			body=make_request(link,maxr=3)
			urls_encoded=xsearch('(\["url_encoded_fmt_stream_map",".+?\])',body)
			try:urls_encoded=urllib.unquote(eval(urls_encoded)[1])+','
			except:urls_encoded=''
			for href,q in re.findall('(https.+?)\\\(.+?quality.+?),',urls_encoded):
				if 'video' in q:
					if '1080' in q:max_link=href;width=1
					elif '720' in q and not width:max_link=href;width=1
					elif not width:max_link=href
		else:
			data=make_post('http://www.phimdata.com/media/plugins/plugins_player.php',data={'url':link})
			try:data=json.loads(xsearch('(\[.+?\])',data.body))
			except:data={}
			for d in data:
				try:
					if 'video' in d.get('type') and int(d.get('width'))>width:
						width=int(d.get('width'));max_link=d.get('url')
				except:pass
		return max_link

	if query=='phimdata.com':
		body=get_home_page('phimdata.html',urlhome)
		title=color['search']+"Search trên phimdata.com[/COLOR]"
		addir_info(title,'phimdata.com',ico,'',mode,1,'search',True)
		addir_info(namecolor('Xem nhiều nhất',c),'',img,img,mode,1,"xemnhieu",True)
		menu=re.findall('<a title="(.+?)"[\s| ].*?href="(.+?)"[\s| ].+?class=".+?">',body)
		for title,href in menu:
			if title=='Home':continue
			elif 'javascript' in href:
				addir_info(namecolor(title,c),'',img,img,mode,1,"pdt_menu",True)
			else:
				href=urlhome+href.replace('/','')
				addir_info(namecolor(title,c),href,img,img,mode,1,"pdt_getpage",True)
		addir_info('%s%s[/COLOR]'%(color['trangtiep'],'-----------------------------'),'',img,img,mode,1,"")
		for S in re.findall("(<div class=''.+?/h2>)",body,re.DOTALL):
			tap,href,title,img=get_detail(S)
			addir_info(namecolor(title,c),href,img,img,mode,1,"pdt_getpage",True)
		if get_home_page('phimdata.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return phimdata(name,url,img,mode,page,query)
		else:return 'no'
	elif url=="phimdata.com":
		search_string = urllib.quote_plus(query)
		url='http://www.phimdata.com/film/search?keyword=%s'%search_string
		return phimdata(name,url,img,mode,1,query='pdt_getpage')
	elif query=='pdt_menu':
		loai=xsearch('\](.+?)\[',name)
		S=xsearch('(<a title="%s".+?/ul>)'%loai,get_home_page('phimdata.html'),1,re.DOTALL)
		for href,title in re.findall('href="/(.+?)">(.+?)</a>',S):
			addir_info(namecolor(title,c),urlhome+href,img,img,mode,1,"pdt_getpage",True)
	
	elif query=='pdt_getpage':
		body=make_request(url);name=xsearch('\](.+?)\[',name)
		items=re.findall('(class="server".+?</ul>)',body,re.DOTALL)
		if items:
			for S in items:
				s=xsearch('</i>(.+?)</div>',S)
				if s:addir_info('%s%s[/COLOR]'%(color['trangtiep'],s),'',img,img,mode,1,"")
				for  href,title in re.findall('<a href="/(.+?)"\s.+?>(.+?)</a>',S):
					addir_info('Tập %s - %s'%(title,name),urlhome+href,img,'',mode,1,"pdt_play")
		else:
			items=re.findall("(<div class=''.+?/h2>)",body,re.S)
			for s in items:
				tap,href,title,img=get_detail(s)
				addir_info(namecolor(title,c),href,img,img,mode,1,"pdt_getpage",True)
		
		href=xsearch('class="next" href="/(.+?)\?',body)
		if href:
			pages=xsearch('>(\d{,4})</a></li><li><span>',body)
			title=namecolor(name,c)+color['trangtiep']+' Trang tiep theo...trang %d/%s[/COLOR]'%(page+1,pages)
			addir_info(title,urlhome+href,ico,'',mode,page+1,query,True)
	
	elif query=='xemnhieu':		
		body=get_home_page('phimdata.html');top={'1':'TOP Ngày','2':'TOP Tuần','3':'TOP Tháng'}
		for S in re.findall('("sidebarlist-(\d)">.+?div id)',body,re.DOTALL):
			addir_info(color['trangtiep']+top.get(S[1])+'[/COLOR]','',img,img,mode,1,"")
			for href,title,img in re.findall('<a href="/(.+?)"><img alt="(.+?)" src="/(.+?)"',S[0]):
				href='%scoi-phim-online/%s'%(urlhome,os.path.basename(href))
				addir_info(namecolor(title,c),href,urlhome+img,urlhome+img,mode,1,"pdt_getpage",True)
	elif query=='pdt_play':
		response=make_request(url)
		max_link=get_maxlink(response)
		if max_link and  'www.youtube.com' in max_link:play_youtube(max_link)
		elif max_link:xbmcsetResolvedUrl(max_link)
		else:
			link=xsearch('\{link:.*"(.+?)"\}',response)
			if len(link)>20:
				jp=make_post('http://www.phimdata.com/gkphp/plugins/gkpluginsphp.php',data={'link':link},resp='j')
				label=0;link='';j=jp.get('link')
				if isinstance(j,dict):
					for l in j.get('link'):
						l1=int(xsearch('(\d+)',l.get('label'),result=0))
						if l1>label:label=l1;link=l.get('link')
				if isinstance(j,list):
					for l in j:
						l1=int(xsearch('(\d+)',l.get('label'),result=0))
						if l1>label:label=l1;link=l.get('link')
				elif isinstance(j,unicode):link=j
				elif jp.get('error'): mess(jp.get('error'),'phimdata.com')
				if link:
					s=make_request(link,resp='o',maxr=3)
					try:link=s.history[-1].headers['location']
					except:pass#link=''
					if link:xbmcsetResolvedUrl(link)
					else:mess('File invalid or deleted!','phimdata.com') 
			elif xsearch('src="(.+?docid=.+?)"',response):
				docid=xsearch('docid=(.+?)&',response)
				if docid:
					link='https://docs.google.com/get_video_info?authuser=&eurl=%s&docid=%s'
					link=link%(urllib.quote_plus(url),docid)
					response=make_request(link)
					link=xsearch('url_encoded_fmt_stream_map(.+?)\Z',response)
					link=xsearch('url=(.+?)&type=',urllib.unquote(urllib.unquote(link)))
					xbmcsetResolvedUrl(link)
			else:mess('No playable sources found !','phimdata.com')

def phimsot(name,url,img,mode,page,query):
	ico=os.path.join(iconpath,'phimsot.png');urlhome='http://phimsot.com/'
	if not os.path.isfile(ico):
		try:urllib.urlretrieve('http://phimsot.com/default/template/img/icon_200x200.png',ico)
		except:pass
	def namecolor(name):return '%s%s[/COLOR]'%(color['phimsot'],name)
	def get_detail(s):
		title=xtitle(s,'alt="(.+?)"')
		href=xhref(s)
		#title=' '.join(title.split())
		res=xsearch('<br>Chất lượng: <b>(.+?)</b>',s)
		tap=xsearch('class="process"><span>(.+?)</span>',s)
		sub=xsearch('<br>Chuyển ngữ: <b>(.+?)</b>',s)
		if res:title+='[COLOR blue]-%s[/COLOR]'%res
		if tap:title+='[COLOR gold]-%s[/COLOR]'%tap
		if sub:title+='[COLOR blue]-%s[/COLOR]'%sub
		img=ximg(s)
		return tap,href,title,img
	
	def get_maxlink(url,loop=False):
		body=make_request(url);quality=0;max_link=picasa=sub='';found=False;srvs=[]
		for url in re.findall('href="(http://phimsot.com/xem-online.+?)"',body):
			if url in srvs:continue
			else:srvs.append(url)
			content=make_request(url)
			for link in re.findall("'playlist': '(.+?)'",content):
				response=make_request(link)
				for href,q in re.findall('file="(.+?)" label="(\d.+?)"',response):
					if int(xsearch('(\d{,4})',q))>quality:quality=int(xsearch('(\d{,4})',q));picasa=href
				if picasa:
					sub=xsearch('file="(.+?)" label=".+?" kind="captions"',response)
					s=make_request(picasa,resp='o',maxr=3)
					try:max_link=s.history[-1].headers['location'];break
					except:pass
			if max_link:break
		if not max_link and not loop:
			loop=True
			for srv in [s for s in re.findall('class="left server_name">.+?<a href="(.+?)"',content) if s not in srvs]:
				max_link,sub=get_maxlink(srv,True)
				if max_link:break
			return max_link,sub
		return max_link,sub
	
	def ps_getpage(body):
		for S in re.findall('(<div class="film_short">.+?class="subname".+?</div>)',body,re.DOTALL):
			tap,href,title,img=get_detail(S)
			if 'Info' in tap or 'trailer' in tap:continue
			if tap:title+=' [COLOR gold]%s[/COLOR]'%tap
			addir_info(namecolor(title),href,img,img,mode,1,'get_series',True)
		S=xsearch('(<div class="paging">.+?</div>)',body,1,re.DOTALL)
		next=xsearch('(class="ajax_select paging_active" href=".+?">.+?</a>\s\s.+?<a class="ajax_select" href=".+?">.+?</a>)',S)
		#print S,next
		if S and next:
			page_next=xsearch('class="ajax_select" href=".+?">(.+?)</a>',next)
			href_next=xsearch('class="ajax_select" href="(.+?)">.+?</a>',next)
			title=namecolor(xsearch('\](.+?)\[',name))
			title=title+color['trangtiep']+' Trang tiep theo...trang %s[/COLOR]'%page_next
			addir_info(title,href_next,ico,'',mode,int(page_next),'ps_getpage',True)

	if query=='phimsot.com':
		body=get_home_page('phimsot.html',urlhome)
		title=color['search']+"Search trên phimsot.com[/COLOR]"
		addir_info(title,'phimsot.com',ico,'',mode,1,'search',True)
		addir_info(namecolor('Top 1 Movie'),'http://vi.top1movie.com',img,img,mode,1,"top1movie",True)
		for href,title in re.findall('<li>\s.+?<a.+?href="(.+?)" title=".+?">([^<].+?)</a>',body):
			addir_info(namecolor(title),'',img,img,mode,1,"ps_menu",True)
		addir_info('%s%s[/COLOR]'%(color['trangtiep'],'-----------------------------'),'',img,img,mode,1,"")
		ps_getpage(body)
		if get_home_page('phimsot.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return phimsot(name,url,img,mode,page,query)
		else:return 'no'
	elif url=="phimsot.com":
		search_string = urllib.quote_plus(query)
		url='http://phimsot.com/phim-hay-p1/?keyword=%s'%search_string
		return phimsot(name,url,img,mode,1,query='ps_getpage')
	
	elif query=='ps_menu':
		loai=xsearch('\](.+?)\[',name)
		S=xsearch('(title="%s">%s</a>.+?</ul>)'%(loai,loai),get_home_page('phimsot.html'),1,re.DOTALL)
		for href,title in re.findall('<a class=".+?" href="(.+?)" title=".+?">(.+?)</a>',S):
			addir_info(namecolor(title),href,img,img,mode,1,"ps_getpage",True)
	
	elif query=='top1movie':	
		def detail(s):
			href=xhref(s)
			img=ximg(s)
			title=xsearch('alt="(.+?)"',s)
			alert=xsearch('"alert alert-warning comment">(.+?)</div>',s)
			epi=xsearch('>(.{,4})</a>/.{,10}</strong></span>',s)
			eps=xsearch('>.{,4}</a>/(.{,10})</strong></span>',s)
			return title,href,img,epi,eps,alert
		
		b=xread(url)
		s=xsearch('<div class="col-md-6">(.+?)<ul class="pagination">',b,1,re.S)
		for s in s.split('<div class="col-md-6">'):
			title,href,img,epi,eps,alert=detail(s)
			if epi or eps:title+=' [COLOR gold]%s/%s[/COLOR]'%(epi,eps)
			if alert:title+=' [COLOR green]%s[/COLOR]'%alert
			addir_info(namecolor(title),href,img,img,mode,1,"top1movie_series",True)
	
	elif query=='top1movie_series':
		body=make_request(url);fanart=xsearch('<meta property="og:image" content="(.+?)"',body)
		s=xsearch('(<ul class="dropdown-menu scrollable-select".+?</ul>)',body,1,re.DOTALL)
		for href,title in reversed(re.findall('<a href="(.+?)">(.+?)</a>',s)):
			addir_info(title,href,img,fanart,mode,1,'top1movie_play')
	
	elif query=='top1movie_play':
		body=make_request(url+'&quality=HD');max_link=''
		link=xsearch('<source src="(.+?)"',body)
		try:max_link=make_request(link,resp='o',maxr=3);max_link= max_link.history[-1].headers['location']
		except:pass
		if max_link:
			sub=xsearch('<track src="(.+?)" kind="subtitles" srclang="vi"',body)
			if not sub:sub=xsearch('<track src="(.+?)" kind="subtitles" srclang="en"',body)
		xbmcsetResolvedUrl(max_link)
		if sub:xbmc.sleep(1000);xbmc.Player().setSubtitles(sub)
		
	elif query=='ps_getpage':ps_getpage(make_request(url))
	elif query=='get_series':
		name=xsearch('\](.+?)\[',name);url=os.path.dirname(url)+os.path.basename(url)+'e0'
		body=make_request(url.replace('/phim/','/xem-phim/'))
		#body=make_request(xsearch('class="button button_20px" href="(.+?)"',body))
		S=xsearch('(<h4 class="server_name">.+?<div class="clear">)',body,1,re.DOTALL)
		for s in S.splitlines():
			title=xsearch('<h4 class="server_name">(.+?)</h4>',s)
			if title:addir_info('%s%s[/COLOR]'%(color['trangtiep'],title),'',img,'',mode,1,"");continue
			if ' <a class=' in s:
				href=xhref(s)
				title=xtitle(s)
				tap=xsearch('>(.+?)</a>',s)
				addir_info(tap+' - '+title,href,img,'',mode,1,'ps_play')
	
	elif query=='ps_play':
		body=make_request(url);quality=''
		for href,q in re.findall('<a class="go_episode" href="(.+?)" download title="Download .+?">(.+?)</a>',body):
			if q>quality:quality=q;link=href
		if quality:
			link=make_request(link,resp='o',maxr=3)
			try:link=link.history[-1].headers['location'];xbmcsetResolvedUrl(link)
			except:link=''
		else:
			link=xsearch('id="mainPayler".+?\s.+?\s.+?src="(.+?)"',body)
			if 'youtube.com' in link:play_youtube(link)
			elif link:
				link=make_request(link,resp='o',maxr=3)
				try:link=link.history[-1].headers['location'];xbmcsetResolvedUrl(link)
				except:pass
			#if sub:xbmc.sleep(1000);xbmc.Player().setSubtitles(sub)
			else:mess('File invalid or deleted!','phimsot.com') 

def phim47(name,url,img,fanart,mode,page,query,text=''):
	ico=os.path.join(iconpath,'phim47.png');urlhome='http://phim47.com/';c='springgreen'
	if not os.path.isfile(ico):
		try:urllib.urlretrieve('http://tailieuhot.vn/images/danh-ba-web/phim-47.jpg',ico)
		except:pass
	
	def get_detail(s):
		tm=xsearch('(<span class="thuyetminh">)',s) or xsearch('(title="Audio Việt")',s)
		series=xsearch('class="bo">(.*?)</span>',s)
		views=xsearch('"viewshow">(.*?)</span>',s)
		href=xsearch('<a href="(.+?)"',s)
		title=xsearch('alt="(.+?)"',s)
		img=ximg(s)
		return title,href,img,tm,series,views
	
	def get_items(content):
		from resources.lib.servers import phim47com;p47=phim47com(c)
		for title,href,img in p47.getItems(body):
			addir_info(namecolor(title,'darkseagreen'),href,img,img,mode,1,'get_series',True)
	
	if query=='phim47.com':
		body=get_home_page('phim47.html',urlhome)
		title=color['search']+"Search trên phim47.com[/COLOR]"
		addir_info(title,'phim47.com',ico,'',mode,1,'search',True)
		addir_info(namecolor('Xem nhiều nhất',c),'',img,img,mode,1,"xemnhieu",True)
		for s,title in re.findall('<li class="downmenu"><span><a(.+?)>(.+?)</a></span>',body):
			if 'javascript' in s:addir_info(namecolor(title,c),'',img,img,mode,1,"p47_menu",True)
			else:addir_info(namecolor(title,c),xhref(s),img,img,mode,1,"p47_getpage",True)

		add_sep_item('--------------------------------------------------')
		get_items(body)
		#from resources.lib.servers import phim47com;p47=phim47com(c)
		#for title,href,img in p47.getItems(body):
		#	addir_info(namecolor(title,'darkseagreen'),href,img,img,mode,1,'get_series',True)
		if get_home_page('phim47.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="phim47.com" or query=="INP":
		if query=="INP":query=make_mySearch('',url,'','','','Input')
		if not query:return 'no'
		url='http://phim47.com/tim-kiem/%s.html'%urllib.quote_plus(query)
		return phim47(name,url,img,fanart,mode,1,query='p47_getpage')
	
	elif query=='p47_menu':
		loai=xsearch('\](.+?)\[',name)
		S=xsearch('((>%s</a></span><ul class="shownav">.+?</ul></li>))'%loai,get_home_page('phim47.html'),1,re.DOTALL)
		for href,title in re.findall('<a href="(.+?)" title=".+?">(.+?)</a>',S):
			addir_info(namecolor(title,c),href,img,img,mode,1,"p47_getpage",True)
	
	elif query=='xemnhieu':
		from resources.lib.servers import phim47com;p47=phim47com(c)
		for title,href,img in p47.xemnhieu(get_home_page('phim47.html')):
			addir_info(title,href,img,img,mode,1,"get_series",True)
	
	elif query=='xemnhieu':		
		body=get_home_page('phim47.html')
		items=re.findall('<li class="zitem">.+?src="(.+?)".+?<a href="(.+?)".+?>(.+?)</a>',body,re.DOTALL)
		for img,href,title in items:
			addir_info(title,href,img,img,mode,1,"p47_play")
	
	elif query=='p47_getpage':
		body=make_request(url);name=xsearch('\](.+?)\[',name)
		get_items(body)
		pages=xsearch('class=page_text>Page(.+?)</span>',body)
		if pages:
			pages=pages.split('/')
			page_current=int(pages[0].strip());page_last=int(pages[1].strip()) if len(pages)>1 else 0
			href=xsearch('<span class="click">.+?</span><span class="giua[^"]*?"><a href="(.+?)">',body)
			if href:
				title=namecolor(name,c)+color['trangtiep']+' Trang tiep theo...trang %d/%d[/COLOR]'%(page+1,page_last)
				addir_info(title,urlhome+href,ico,'',mode,page+1,query,True)
	
	elif query=='get_series':
		name=namecolor(name)
		b=xread(url)
		fanart=xsearch('<link rel="image_src" href="(.+?)"',b);count=0
		tm=xsearch('(Thuyết minh)</span>',b)
		if tm:name='[COLOR blue]TM[/COLOR] '+name
		listDefault=[]
		
		for url in re.findall('id="xemphimus" href="(http://phim47.com.+?)"',b):
			b=xread(url);count+=1
			list_episode=re.findall('("list_episode".+?"clear_span")',b,re.S)
			for s in list_episode:
				label=xsearch('"name_server">([^<]+?)</span>',s).replace('+','').replace(':','')
				if label:label='Cụm server %d: %s'%(count,label)
				tap1=xsearch('class="current">([^<]+?)</',s)#Link tap 1 not in href list
				items=[(url,'Tập 1')] if tap1 else []
				items+=re.findall('<a href="(.+?)" title="(.+?)">',s)
				#	addir_info('Tập 1'+' '+name,url,img,fanart,mode,1,'p47_play')
				#for href,title in re.findall('<a href="(.+?)" title="(.+?)">',s):
				#	addir_info(title+' '+name,href,img,fanart,mode,1,'p47_play')
				if len(items)<10:
					add_sep_item('%s---------------------------------------'%label)
					for href,title in items:addir_info(title+' '+name,href,img,fanart,mode,1,'p47_play')
				else:
					if not listDefault:
						listDefault=items;label=namecolor(label+' (default)','gold')
						addir_info(label,url,img,fanart,mode,1,'list_episode',True,text=str(items))
					else:addir_info(namecolor(label,c),url,img,fanart,mode,1,'list_episode',True,text=str(items))
		
		if listDefault:
			add_sep_item('List episode default --------------------------------')
			for href,title in listDefault:addir_info(title+' '+name,href,img,fanart,mode,1,'p47_play')
	
	elif query=='list_episode':
		items=eval(text)
		for href,title in items:addir_info(title+' '+namecolor(name),href,img,fanart,mode,1,'p47_play')
	
	elif query=='get_series':
		name=xsearch('\](.+?)\[',name)
		body=make_request(url)
		url=xsearch('href="(http://phim47.com/xem-online[^"]+?)"',body);print url
		fanart=xsearch('<link rel="image_src" href="(.+?)"',body)
		body=make_request(xsearch('href="(http://phim47.com/xem-online[^"]+?)"',body))
		for s in re.findall('("list_episode".+?"clear_span")',body,re.DOTALL):
			title=xsearch('"name_server">([^<]+?)</span>',s)
			if title:addir_info('%s%s[/COLOR]'%(color['trangtiep'],title),'',img,fanart,mode,1,"")
			tap1=xsearch('class="current">([^<]+?)</',s)
			if tap1:addir_info('Tập %s'%tap1+' '+name,url,img,fanart,mode,1,'p47_play')
			for href,title in re.findall('<a href="(.+?)" title="(.+?)">',s):
				addir_info(title+' '+name,href,img,fanart,mode,1,'p47_play')
	
	elif query=='p47_play':
		from resources.lib.servers import phim47com;p47=phim47com(c)
		link,sub=p47.getLink(url)
		if link and 'youtube.com' not in link:
			if sub:
				s=xread(sub)
				sub=joinpath(subsfolder,'phim47-Vie.sub')
				makerequest(sub,s,'wb')
			xbmcsetResolvedUrl(link,sub)
		elif link:play_youtube(link)
		else:mess('File invalid or deleted!','phim47.com') 
		
	elif query=='p47_play':
		items=[];link=sub='';items=[];url=url.replace('xem-phim-','xem-online/')
		print url
		from resources.lib.servers import phim47com;p47=phim47com(c)
		for link in re.findall("playlist':.?'(.+?)'",xread(url)):
			l,sub=p47.maxLink(link)
			link=dl(l[0][0])
			if link:break
			else:items+=[i for i in l if link not in i]
		
		if not link:#test all
			mess('Checking all ...','phim47.com')
			if myaddon.getSetting('resolut')=='Max':
				items=sorted(list(set([(i[0],resolu(i[1])) for i in items])), key=lambda k: int(k[1]),reverse=True)
			else:items=sorted(list(set([(i[0],resolu(i[1])) for i in items])), key=lambda k: int(k[1]))
			for href,label in items:
				link=dl(href)
				if link:break
		
		if link:
			xbmcsetResolvedUrl(link)
			if sub:xbmc.sleep(2000);xbmc.Player().setSubtitles(sub);mess(u'Sub của phim47.com')
		else:mess('File invalid or deleted!','phim47.com') 

def hdonline(name,url,img,fanart,mode,page,query,bakName,bakData):
	ico=os.path.join(iconpath,'hdonline.png');urlhome='http://hdonline.vn'
	c=xsearch('\[COLOR (\w+)\]',color['hdonline'])
	if not os.path.isfile(ico):
		try:
			link='http://hdonline.vn/template/frontend/images/facebooksharehomepage.png'
			f=open(ico,'wb');f.write(make_request(link));f.close()
		except:pass
	
	def url_fix(url):return url if 'http://' in url else urlhome+url
	def login():
		url='http://id.hdonline.vn/dang-nhap.html'
		primaryKey=xsearch('value="(.+?)" id="primaryKey"',xread(url))
		u=myaddon.getSetting('hdo_u');p=myaddon.getSetting('hdo_p')
		data={'username':u,'password':p,'primaryKey':primaryKey}
		response=make_post(url,data=data)
		if response and response.status==302:
			cookie=response.cookiestring;mess(u'Login to hdonline.vn success')
			hd={'User-Agent':'Mozilla/5.0','Cookie':cookie,'Referer': 'http://hdonline.vn'}
			body=make_request('http://id.hdonline.vn/thong-tin.html',hd)
			userID='; userID=%s'%xsearch('<span class="upgradeVip"><strong>(.+?)</strong>',body)
			makerequest(joinpath(xsharefolder,'hdonline.cookie'),cookie+userID,'w')
		else:cookie='';mess(u'Login to hdonline.vn Fail !')
		return cookie
	
	def page_detail(url):
		items=[]
		for title,href,img,q,dir in hdo.page(url):
			if 'Trang tiep theo...' not in title:
				addir_info(title,href,img,'',mode,1,q,dir,menu=menu)
				items.append((title,href,img,'',mode,1,q,dir,menu))
			else:
				addir_info(title.replace('page',str(page+1)),href,ico,'',mode,page+1,query,True)
				items.append((title.replace('page',str(page+1)),href,ico,'',mode,page+1,query,True,{}))
		return items

	def tag(url):
		b=xread(url)
		for s in [i for i in b.split('class="tn-bxitem"') if 'class="bxitem-txt"' in i]:
			title=xsearch('class="bxitem-txt">([^<]+?)<',s)
			href=xsearch('href="([^"]+?)"',s)
			if not title or not href:continue
			if 'http://' not in href:href='http://hdonline.vn'+href
			img=xsearch('src="([^"]+?)"',s)
			addir_info(namecolor(title,c),href,ico,'',mode,1,"eps",True)
	
	if checkupdate('hdonline.cookie',hours=100,folder=xsharefolder):login()
	from resources.lib.servers import hdonline;hdo=hdonline(c)
	hd=hdo.hd;menu={'hdonline':{'action':'Add'}}
	
	if query=='hdonline.vn':
		body=get_home_page('hdonline.html','http://m.hdonline.vn/danh-sach/phim-moi.html',False,hd)
		title=color['search']+"Search trên hdonline.vn[/COLOR]"
		addir_info(title,'hdonline.vn',ico,'',mode,1,'search',True)
		title=color['search']+"Mục Yêu thích của tôi[/COLOR]"
		href='http://hdonline.vn/frontend/user/ajax?page=1&type=like&user=%s'%hdo.userID
		addir_info(title,href,ico,'',mode,1,'like',True)
		
		S=xsearch('(<a href="[^"]+?"><i class="fa fa-film">.+?class="nav")',body,1,re.DOTALL)
		for href,title in re.findall('<a href="([^"]+?)".+class="fa fa-.+>([^<]+?)</a>',S):
			addir_info(namecolor(title,c),href,ico,'',mode,1,"menu",True)
		
		add_sep_item('-------------Phim Mới Cập Nhật--------------')
		query='page'
		page_detail(body)
		
		if get_home_page('hdonline.html','http://m.hdonline.vn/danh-sach/phim-moi.html',True):
			xbmc.executebuiltin("Container.Refresh")
	
	elif query=='Add':
		id_film=xsearch('-(\d+?)\.html',url)
		body=make_request('http://hdonline.vn/frontend/user/ajax?page=1&type=like&user=%s'%hdo.userID,hdo.hd)
		if xsearch('("#phim-like-%s")'%id_film,body):
			mess(u'Phim này đã có trong Danh sách Phim yêu thích của bạn !')
		else:hdo.like_film('http://hdonline.vn/episode/like?film=%s&_=%d'%(id_film,int(time.time())*1000))
	
	elif query=='Remove':
		id_film=xsearch('-(\d+?)\.html',url)
		url='http://hdonline.vn/episode/like?film=%s&_=%d'%(id_film,int(time.time())*1000)
		hdo.like_film(url);xbmc.executebuiltin("Container.Refresh")
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="hdonline.vn" or query=="INP":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query:return 'No'
		search_string = '-'.join(query.split());page=1;query='page'
		url='http://m.hdonline.vn/tim-kiem/%s/trang-1.html'%search_string;page_detail(url)
	
	elif query=='like':
		b=xread(url);menu={'hdonline':{'action':'Remove'}}
		items=re.findall('(<div class="tn-bxitem">.+?</div>\W</div>)',b,re.S)
		for s in items:
			title,href,img,q,dir=hdo.getDetail(s)
			addir_info(title,url_fix(href),img,'',mode,1,'play',menu=menu)
	
	elif query=='hdo_folder0':#http://hdonline.vn/frontend/video/morevideo?film=12331&_=1465175662582
		from resources.lib.servers import hdonline;hdo=hdonline(c)
		for epi,id in hdo.eps(url):
			print id
			title='Tập %s %s'%(epi,namecolor(name))
			addir_info(title,id,img,'',mode,1,'play')

	elif query=="menu":
		b=xread(url)
		if [s for s in ['Mới','Lẻ','Bộ'] if s in name]:
			s=xsearch('(<a href="%s".+?</ul>)'%url,b,1,re.DOTALL)
			for href,title in re.findall('<a href="(.+?)" title=.+?</i>(.+?)</a>',s):
				addir_info(namecolor(title,c),href,ico,'',mode,1,"page",True)
			add_sep_item('---------------------------------------')
		
		page_detail(b)
	
	elif query=='eps':
		if 'Các tập tiếp theo' in  name:name= url.split('.html')[1];url= url.split('.html')[0]+'.html'
		else:name=namecolor(name).replace('hdonline Xem phim','').strip()
		id=xsearch('-(\d+)\.html',url)
		items=hdo.eps(id,page);l=len(items)
		for href,epi in items:
			if 'Các tập tiếp theo' in href:addir_info(href,url+name,img,'',mode,page+1,query,True)
			else:
				title='Tập-'+epi+' '+name if l>1 else name
				addir_info(title,href,img,'',mode,1,'play',menu=menu)
		if not items:tag(url)
	
	elif query=='eps':
		for title,href,img in hdo.eps(url):
			title=u2s(title)+' '+namecolor(name)
			addir_info(title,href,img,'',mode,1,'play',menu=menu)
			bakData[bakName].append((title,href,img,'',mode,1,'play',False,menu))
		if bakData.get(bakName):xrw('sysmenu.dat',json.dumps(bakData));mess('buff list ok',timeShown=100)
	
	elif query=="page":
		bakData[bakName]=page_detail(url)
		if bakData.get(bakName):xrw('sysmenu.dat',json.dumps(bakData));mess('buff list ok',timeShown=100)
	
	elif query=='play':
		epi=xsearch('Tập-(\d+) ',name,result='1')
		from resources.lib.servers import hdonline;hdo=hdonline(c)
		items,sub,img=hdo.getLink(url,epi)
		if img and myaddon.getSetting('chonserver')=='Không':
			link=img.rsplit('/',2)[0]+'/playlist.m3u8'
			link=xget(link)
			if link:
				link=link.geturl()
				#mess(u'Chọn audio track: "Audio and subtitle settings" (hình cái loa)',timeShown=10000)
			else:link=gdl(items)
		else:link=gdl(items)
		if img and myaddon.getSetting('chonserver')!='Không' and not link:
			link=img.rsplit('/',2)[0]+'/playlist.m3u8'
			link=xget(link)
			if link:link=link.geturl()
		if link:
			xbmcsetResolvedUrl(link)
			if sub:
				if 'hdonline.vn' in sub:
					if not sub.startswith('http'):sub='http://data.hdonline.vn/api/vsub.php?url=%s'%sub
					s=xread('http://data.hdonline.vn/api/vsub.php?url='+sub)
					subname=joinpath(subsfolder,os.path.basename(sub).split('?')[0]+'-Vie.sub')
					makerequest(subname,s,'wb')
				else:subname=sub
				xbmc.sleep(1000);xbmc.Player().setSubtitles(subname);mess(u'Sub của HDOnline.vn')
		else:mess('File invalid or deleted!','hdonline.vn') 

	elif query=='play':
		epi=xsearch('Tập-(\d+) ',name)
		if not epi:epi='1'
		from resources.lib.servers import hdonline;hdo=hdonline(c)
		j=hdo.getLink(url,epi)
		link=''
		if j:
			L=sorted(j, key=lambda k: k[1],reverse=True if myaddon.getSetting('resolut')=='Max' else False)
			#print href,L
			for href,r in L:
				link=dl(href)#;print 'a',link,'b',href
				if link:break
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','hdonline.vn') 

	elif query=='play':
		from resources.lib.servers import hdonline;hdo=hdonline(c)
		hdo.getLink(url)
		if 'http://hdonline.vn/frontend/episode/xmlplay' not in url:
			l=hdo.eps(url)
			if l:url=l[0][1]
		items,sub=hdo.maxLink(url+'&format=json&_x=%s'%str(random.random()))
		link=gdl(items)
		if link:
			xbmcsetResolvedUrl(link)
			if sub:
				if 'hdonline.vn' in sub:
					if not sub.startswith('http'):sub='http://data.hdonline.vn/api/vsub.php?url=%s'%sub
					s=xread('http://data.hdonline.vn/api/vsub.php?url='+sub)
					subname=joinpath(subsfolder,os.path.basename(sub).split('?')[0]+'-Vie.sub')
					makerequest(subname,s,'wb')
				else:subname=sub
				xbmc.sleep(1000);xbmc.Player().setSubtitles(subname);mess(u'Sub của HDOnline.vn')
		else:mess('File invalid or deleted!','hdonline.vn') 

def kphim(name,url,img,mode,page,query):
	hd={'User-Agent':'Mozilla/5.0'};c='lightgreen'
	color['kphim']='[COLOR lightgreen]'
	ico=os.path.join(iconpath,'kphim.png');urlhome='http://kphim.tv/'
	if not os.path.isfile(ico):
		try:makerequest(ico,get('http://kphim.tv/resources/images/logo.png').body,'wb')
		except:pass
		
	from resources.lib.servers import kPhim;kph=kPhim(c)
	if  query=='kphim.tv':
		a=xread(urlhome)
		title=color['search']+"Search trên kphim.tv[/COLOR]"
		addir_info(title,'kphim.tv',ico,'',mode,1,'search',True)
		
		for title in re.findall('<div class="title-tab">.*?\s(.+?)\s.*?</div>',a):
			addir_info(namecolor(title.strip(),c),urlhome,ico,'',mode,1,'new',True)
		
		b=xsearch('(<nav id="footer-nav">.+?</ul>)',a,1,re.S)
		for href,title in re.findall('<li><a href="(.+?)">(.+?)</a></li>',b):
			if 'theloai' in href:addir_info(namecolor(title,c),href,img,'',mode,1,'theloai',True)
			else:addir_info(namecolor(title,c),href,img,'',mode,1,'episode',True)
			
		title='PHIM TRUYỀN HÌNH HÀN QUỐC'
		href='http://kphim.tv/theloai/phim-truyen-hinh-han-quoc-z1.html'
		addir_info('[COLOR lime]'+title+'[/COLOR]',href,img,'',mode,1,'theloai',True)
		l=re.findall('(<div class="kdrama-item.+?</div>)',a,re.S)
		for title,href,img in kph.detail(l):
			addir_info(namecolor(title,c),href,img,'',mode,1,'episode',True)
		
		title='TV SHOW, TRUYỀN HÌNH THỰC TẾ'
		href='http://kphim.tv/theloai/truyen-hinh-thuc-te-z2.html'
		addir_info('[COLOR lime]'+title+'[/COLOR]',href,img,'',mode,1,'theloai',True)
		l=re.findall('(<div class="kshow-item.+?</div>)',a,re.S)
		for title,href,img in kph.detail(l):
			addir_info(namecolor(title,c),href,img,'',mode,1,'episode',True)

	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="kphim.tv":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query:return
		
		search_string = urllib.quote_plus(query)
		url='http://kphim.tv/search/?keyword=%s'%search_string
		for title,href,img in kph.genre(url):
			addir_info(namecolor(title,c),href,img,'',mode,1,'episode',True)
	
	elif query=='new':
		if 'TOP' in name:s=xsearch('(%s.+?<script>)'%namecolor(name),make_request(urlhome),1,re.DOTALL)
		else:s=xsearch('(%s.+?</ul>)'%namecolor(name),make_request(urlhome),1,re.DOTALL)
		for href,title,label in set(re.findall('href="(.+?)" title="(.+?)".+?> ([^>]+?)</span>',s)):
			addir_info(namecolor(title+' - '+label,c),href,img,'',mode,1,'episode',True)

	elif query=='theloai':
		for title,href,img in kph.genre(url):
			addir_info(namecolor(title,c),href,img,'',mode,1,'episode',True)
	
	elif query=='episode':
		name=' '.join(re.sub('\([^\(]+\)|Ep \d+|ep \d+|EP \d+','',name).split())
		for href,title in kph.eps(url):
			addir_info('Tập %s - '%title+namecolor(name),href,img,'',mode,1,'play')
	
	else:
		link=kph.getLink(url)
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','kphim.tv') 

def phimnhanh(name,url,img,mode,page,query):
	ico=os.path.join(iconpath,'phimnhanh.png');urlhome='http://phimnhanh.com/';c='FF1277C1'
	if not os.path.isfile(ico):
		try:makerequest(ico,get('http://cdn.phimnhanh.com/assets/images/logo.png').body,'wb')
		except:pass
	
	def fixURL(href):
		if not href.startswith('http'):href='http://phimnhanh.com'+href
		return href
	
	def makeDir(s):
		title=xtitle(s)
		href=xhref(s)
		if not title or not href:return
		img=xsearch('original="(.+?)"',s)
		label=[re.sub('<.+?>','',i) for i in re.findall('(<span.+?/span>)',s) if 'title' not in i]
		label=' '.join(i.strip() for i in label)
		if re.search('.huyết .inh',label):title='[COLOR gold]TM[/COLOR] '+title
		title+=' [COLOR green]%s[/COLOR]'%label
		if 'Trailer' in title:
			title=title.replace('Trailer','[COLOR gold]Trailer[/COLOR]')
			addir_info(title,fixURL(href),img,'',mode,1,'play')
		else:addir_info(namecolor(title,c),fixURL(href),img,'',mode,1,'eps',True)
	
	def detail(body):
		for  s in re.findall('(class="serial".+?/li>)',body,re.S):makeDir(s)
		np=xsearch('<a href="([^>]+?)" rel="next">',body)
		if np:
			np=np.replace('amp;','');pn=xsearch('page=(\d+?)\Z',np)
			ps=xsearch('<a href="[^>]+?">(\d+?)</a></li> <li><a href="[^>]+?" rel="next">',body)
			t=color['trangtiep']+' Trang tiep theo...trang %s/%s[/COLOR]'%(pn,ps)
			addir_info(t,np,ico,'',mode,page+1,query,True)
	
	if query=='phimnhanh.com':
		b=getHome('phimnhanh.html',urlhome)
		title=color['search']+"Search trên phimnhanh.com[/COLOR]"
		addir_info(title,'phimnhanh.com',ico,'',mode,1,'search',True)
		
		for s in re.findall('(<li data-id=".+?/li>)',b,re.S):
			title=re.sub('<.+?>','',xsearch('(<span.+?/a>)',s))
			href=xhref(s)
			addir_info(namecolor(title,c),fixURL(href),ico,'',mode,1,'page',True)
		
		for s in re.findall('(<span class="arr-d".+?/ul>)',b,re.S):
			title=xsearch('<p>(.+?)</p>',s)
			if title:
				href=xsearch('(<ul.+?/ul)',s,1,re.S)
				addir_info(namecolor(title,c),fixURL(href),ico,'',mode,1,'submenu',True)
		
		for s in re.findall('(<section class="cat-gr.+?/section>)',b,re.S):
			label=xsearch('(<h2.+?/h2>)',s)
			if label:
				title=xsearch('>([^>]+?)</a>',label)+' (clik to expand) -------------'
				href=xsearch('href="(.+?)"',label)
				addir_info(namecolor(title,'gold'),fixURL(href),ico,'',mode,1,'page',True)
			for s in [i for i in re.findall('(<h2.+?/h2>)',s,re.S) if 'src=' in i]:makeDir(s)
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return kphim(name,url,img,mode,page,query)
		else:return 'no'
	elif url=="phimnhanh.com":
		url='http://phimnhanh.com/danh-sach-phim/?s='+urllib.quote_plus(query)
		query='page'#xu ly pagenext
		detail(xread(url))
	
	elif query=='submenu':
		for href,title in re.findall('href="(.+?)" title="(.+?)"',url):
			addir_info(namecolor(title,c),fixURL(href),ico,'',mode,1,'page',True)

	elif query=='page':detail(xread(url))
			
	elif query=='eps':
		b=xread(url)
		name=xsearch('<title>(.+?)</title>',b)
		s=xsearch('(<p class="epi">.+?</p>)',b,1,re.DOTALL)
		items=re.findall('href="(.+?)" title=".+?">(.+?)</a>',s)
		for href,title in items:
			addir_info('Tập %s '%title+name,fixURL(href),img,'',mode,1,'play')
	
	else:
		b=xread(url.replace('/phim/','/xem-phim/'));link=''
		if not b:link=xsearch('file: "(..+?)"',xread(url))
		
		elif xsearch('(video.ready.+?/script>)',b,1,re.S):
			s=xsearch('(video.ready.+?/script>)',b,1,re.S)
			b=xread(xsearch("url: *'(.+?)'",s))
			try:
				j=json.loads(b).get('data',{}).get('sources',[])
				link=googleItems(j,link='src',label='label')
			except:link=''
		
		else:
			s=xsearch('(<div id="iframe-player".+?/div>)',b,1,re.S)
			link=ximg(s)
			if 'drive.google.com' in link:
				b=xread(link)
				s=xsearch('"url_encoded_fmt_stream_map"."(.+?)"',b)
				qsl=urllib2.urlparse.parse_qsl
				items=[dict(qsl(i)) for i in s.decode('unicode_escape').split(',')]
				for href,quality in ls([(i.get('url'),rsl(i.get('quality'))) for i in items]):
					link=xget(href)
					if link:link=href;break
			else:
				try:import YDStreamExtractor;vid=True
				except:vid=False;mess(u'Cài đặt module youtube.dl để sử dụng youtube tốt hơn')
				if vid:
					vid=YDStreamExtractor.getVideoInfo(url)
					if vid:
						link=vid.streamURL()
						if link:
							xbmcsetResolvedUrl(link)
							mess('Xshare play Youtube by Youtube.dl module','Notification')
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','phimnhanh.com')

def htvonline(name,url,img,fanart,mode,page,query):
	tvurl='http://www.htvonline.com.vn/livetv';showurl='http://www.htvonline.com.vn/shows'
	phimurl='http://www.htvonline.com.vn/phim-viet-nam';hd['X-Requested-With']='XMLHttpRequest'
	def namecolor(name):return '[COLOR yellowgreen]%s[/COLOR]'%name
	if query=='home':
		tv=makerequest(joinpath(xsharefolder,'htvtv.html'));show=makerequest(joinpath(xsharefolder,'htvshow.html'))
		phim=makerequest(joinpath(xsharefolder,'htvphim.html'))
		for title in re.findall('<div class="view_title2"><div>(.+?)</div>',tv):
			addir(namecolor(title.replace(',','-')),tvurl,img,'',mode,page,'submenu',True)
		fanart=xsearch('<img width="487" height="274" src="(.+?)"',show)
		addir(namecolor('TV Shows'),showurl+'?page=1',fanart,fanart,mode,page,'submenu',True)
		fanart=xsearch('<img width="487" height="274" src="(.+?)"',phim)
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
			href_next=xsearch('<a class="btn_channel_next page_hr" href="(.+?)"></a>',body)
			if href_next:
				page_next=xsearch('page=(\d{1,3})\Z',href_next)
				page_end=xsearch('\?page=(\d{1,3})"><span aria-hidden="true">',body)
				label='%sTrang tiếp theo: trang %s/%s[/COLOR]'%(color['trangtiep'],page_next,page_end)
				addir(label,href_next,img,'',mode,page,query,True)
				endxbmc();hd['X-Requested-With']='XMLHttpRequest';body=make_post(href_next,headers=hd,resp='b')
				makerequest(joinpath(datapath,page2),body,'w')
		else:
			body=makerequest(joinpath(datapath,'htvtv.html'))
			for title,detail in re.findall('<div class="view_title2"><div>(.+?)</div>.+?<ul class="listtv group small livetvDetail">(.+?)</ul>',body,re.DOTALL):
				if title.replace(',','-') in name:
					for hplus,href,img in re.findall('href="(.+?)" data-original="(.+?)">.+?src="(.+?)"></a>',detail):
						addir(xsearch('/([\w|-]+)-\d',hplus).upper(),href,img,'',mode,page,'htvplay')
	elif query=='episode_show':
		p='<a data-tooltip=.+?href="(.+?)".*?>([ |\d|\w|-]+?)</'
		label=re.sub('\[.+?\]','',name);items=re.findall(p,make_request(url),re.DOTALL)
		for href,adate in items:
			addir('%s %s'%(label,adate),href,img,'',mode,page,'htvplay')
		if not items:addir(label,url,img,'',mode,page,'htvplay')
	elif query=='htvplay':
		body=make_request(url);maxlink=xsearch('"(http:.+?\.m3u8\?.+?)"',body)
		if '/xem-show/' in url and not xsearch('\d{1,2}-\d{1,2}-\d{4}',name,0):
			p='<a data-tooltip=".+?".+?href="%s".*\s.*>(.+?)</span></a>'%url
			adate=xsearch(p,body)
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
	if not xsearch('<a>%s</a>'%string,makerequest(search_file)):
		makerequest(search_file,'<a>%s</a>\n'%string,'a');xbmc.executebuiltin("Container.Refresh")
	return string

def vaphim(name,url,img,fanart,mode,page,query):
	colo=xsearch('\[COLOR (.+?)\]',color['vaphim']);ico=icon['vaphim'];urlhome='http://vaphim.com/'
	hd['Cookie']=makerequest(joinpath(xsharefolder,'vaphim.cookie'))
	def home_page(fn,url='',update=False):
		fullfilename=joinpath(xsharefolder,fn);body=''
		if not update and os.path.isfile(fullfilename):body=makerequest(joinpath(xsharefolder,fn))
		elif not update and url:body=xread(url)
		elif update and url and checkupdate(fn,folder=xsharefolder):
			body=xread(url)
			if body:endxbmc();content=makerequest(fullfilename,body,'w')
		return body

	if query=='vaphim.com':
		body=home_page('vaphim.html',urlhome)
		label=color['search']+"Search trên vaphim.com[/COLOR]"
		addir_info(label,'vaphim.com',ico,'',mode,1,'search',True)
		addir_info(namecolor('Phim lẻ-Phim bộ-Nhạc-VideoClip mới nhất-Xem nhiều nhất',colo),urlhome,ico,'',mode,1,'phimmoinhat',True)
		addir_info(namecolor('Danh Mục Phân Loại Phim',colo),'',ico,'',mode,1,'mainmenu',True)
		addir_info(namecolor('Danh Mục Phim Theo Thể Loại - Quốc Gia',colo),'',ico,'',mode,1,'mainmenu',True)
		addir_info(namecolor('Danh Mục Phân Loại Nhạc',colo),'',ico,'',mode,1,'mainmenu',True)
		addir_info(namecolor('Danh Mục Các Bộ Sưu Tập',colo),'',ico,'',mode,1,'mainmenu',True)
		add_sep_item('Vaphim.com giới thiệu')
		pattern='<a class="featured-article" href="(.+?)".+?src="(.+?)[\?|\"].+?"bookmark">(.+?)</a>'
		for href,img,title in re.findall(pattern,body,re.DOTALL):
			addir_info(namecolor(remove_tag(title),colo),href,img,img,mode,1,'vp_getsubpage',True)
		if home_page('vaphim.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
	
	elif query=='phimmoinhat':
		def dirAll(id,p):
			s=xsearch('%s(.+?)</ul>'%id,body,1,re.S)
			title=namecolor(remove_tag(xtitle(s)),'orangered')
			href=xhref(s)
			addir_info(title,href,img,'',mode,1,'vp_getpage',True)
			for image,href,title in re.findall(p,s,re.S):
				addir_info(namecolor(remove_tag(title),colo),href,image,'',mode,1,'vp_getsubpage',True)
		
		body=home_page('vaphim.html')
		add_sep_item('Xem nhiều nhất')
		for href,title in re.findall('<li><a href="(.+?)" title="(.+?)">',body):
			addir_info(namecolor(remove_tag(title),colo),href,ico,'',mode,1,'vp_getsubpage',True)
		
		add_sep_item('Phim lẻ mới nhất')
		dirAll('"index-featured2"','<li class=.+?src="(.+?)[\?|\"].+?<a href="(.+?)".+? >(.+?)</a>')
		
		add_sep_item('Phim bộ mới nhất')
		dirAll('"index-featured3"','<li class=.+?src="(.+?)[\?|\"].+?<a href="(.+?)".+? >(.+?)</a>')
		
		add_sep_item('Nhạc mới nhất')
		dirAll('"index-featured4"','<li class=.+?src="(.+?)[\?|\"].+?<a href="(.+?)".+? >(.+?)</a>')
		
		add_sep_item('VideoClip mới nhất')
		s=xsearch('"index-news"(.+?)</ul>',body,1,re.DOTALL)
		title=namecolor(remove_tag(xtitle(s)),'orangered')
		href=xhref(s)
		addir_info(title,href,img,'',mode,1,'vp_getpage',True)
		for s in re.findall('(<a data.+?/h3>)',s,re.S):
			id=xsearch('<a data="(.+?)"',s)
			title=' '.join(re.sub('<.+?>','',xsearch('(<h3.+?/h3>)',s)).split())
			addir_info(s2c(title),id,img,'',mode,1,'vp_getclip',False)
	
	elif query=='mainmenu':
		body=home_page('vaphim.html')
		if name==namecolor('Danh Mục Phân Loại Phim',colo):
			pattern='<li><a href="/(category/phim-2/.+?)">(.+?)</a></li>'
			for href,title in re.findall(pattern,body):
				addir_info(namecolor(title,colo),urlhome+href,ico,'',mode,1,'vp_getpage',True)
		elif name==namecolor('Danh Mục Phim Theo Thể Loại - Quốc Gia',colo):
			url='http://vaphim.com/?cat=%s'
			for href,title in re.findall('<option value="(\d.+?)">(.+?)</option>',body):
				addir_info(namecolor(title,colo),url%href,ico,'',mode,1,'vp_getpage',True)
		elif name==namecolor('Danh Mục Phân Loại Nhạc',colo):
			pattern='<li><a href="/(category/music/.+?)">(.+?)</a></li>'
			for href,title in re.findall(pattern,body):
				addir_info(namecolor(title,colo),urlhome+href,ico,'',mode,1,'vp_getpage',True)
		elif name==namecolor('Danh Mục Các Bộ Sưu Tập',colo):
			return vaphim(name,'http://vaphim.com/category/collection/',img,fanart,mode,page,'vp_getpage')
	
	elif query=='vp_getpage':
		href=url.split('?')[0] if page==1 else '%spage/%d/'%(url.split('?')[0],page)
		if len(url.split('?'))>1:href=href+'?'+url.split('?')[1]
		
		b=xread(href)
		if re.search('<div class="search-home-title">Danh sách đề xuất</div>',b):
			mess(u'Xin lỗi! không tìm thấy kết quả dựa trên truy vấn của bạn.','Vaphim search',10000)
			add_sep_item('-----Không tìm thấy kết quả--->Danh sách đề xuất----')
		for s in re.findall('(<a data=.+?/li>)',b,re.S):
			title=' '.join(re.sub('<.+?>','',xsearch('(<h3.+?/h3>)',s)).split())
			title+=' [COLOR cyan]%s[/COLOR]'%xsearch('<span class="entry-comments">(.+?)</span>',s)
			if '/video-clip/' in url:c='';href=xsearch('data="(.+?)"',s);q='vp_getclip';dir=False
			else:href=xhref(s);c=colo;q='vp_getsubpage';dir=True
			img=ximg(s)
			addir_info(namecolor(s2c(title),c),href,img,'',mode,1,q,dir)

		pagelast=xsearch("<span class='pages'>Trang \d{1,4} của (\d{1,4})</span>",b)
		if pagelast and int(pagelast)>page:
			name=re.sub('\[.+?\]','',name.split('-')[0].strip())
			name='%s%s - Trang tiếp theo: trang %d/%s[/COLOR]'%(color['trangtiep'],name,page+1,pagelast)
			addir_info(name,url,ico,'',mode,page+1,query,True)
	
	elif query=='vp_getclip':
		if 'youtube.com' in url:play_youtube(url)
		elif 'vaphim.com' not in url:
			url='http://vaphim.com/?p='+url
			play_youtube(xsearch('src="(http.+?youtube.com.+?)"',xread(url)))
		else:
			item=xsearch('src="(http.+?youtube.com.+?)"',xread(url))
			if item:addir_info(remove_tag(name),item,img,fanart,mode,1,'vp_getclip')
			else:mess(u'Sorry! Không get được nội dung này trên vaphim.com','vaphim.com');return 'no'

	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return vaphim(name,url,img,fanart,mode,page,query)
		else:return 'no'
	elif url=="vaphim.com":
		url='http://vaphim.com/?s='+urllib.quote_plus(query);query='vp_getpage'
		return vaphim(name,url,img,fanart,mode,1,'vp_getpage')
	
	elif query=='vp_getsubpage':
		if '/tag/' in url:url=xsearch('class="entry-title"><a href="([^"]+?)"',xread(url))
		body=xread(url);items=list();name=remove_tag(name.replace('Vaphim ',''))
		body=xsearch('<div id="post-(.+?)"fb-comments"',body,1,re.S)
		if not body:return 'no'
		if re.search('class=".+category-(game|phn-mm|ebooks).+"',body):
			mess(u'Sorry! Trang này không phải trang phim','Vaphim.com');return 'no'
		art=re.findall('<img class=".+?" src="(.+?)"',body)
		if not art:art=['']
		tabs=re.findall('#(tabs-.+?)" >(.+?)<',body);i=0;j=len(art)-1
		if tabs:
			for tab,tab_label in tabs:
				content=xsearch('<div id="%s">(.+?)</div>'%tab,body,1,re.DOTALL)
				fanart=art[i];i=0 if i==j else (i+1)
				for href,fn in re.findall('<a href="(.+?)".*?>(.+?)</a>',content):
					if '/goo.gl/' in href or href=='https://subscene.com/':continue
					fn='[COLOR green]%s[/COLOR] - %s'%(tab_label.replace('Download',''),remove_tag(fn))
					items.append((fn if fn else name,href,fanart))
		else:
			pattern='([\w|/|:|\.]+?fshare\.vn.+?|[\w|/|:|\.]+?subscene\.com.+?)[&|"|\'].+?>(.+?)</a>'
			for href,fn in re.findall(pattern,body):
				fn=remove_tag(fn);fanart=art[i];i=0 if i==j else (i+1);
				items.append((fn if fn else name,href,fanart))
		if items:
			add_sep_item('Links phim: '+name)
			for title,href,fanart in items:addir_info(title,href,img,fanart,mode,1,query)
		#------------------------------------------------------------------------------------------------
		trailer=xsearch('(http[\w|:|/|\.]+youtube.com.+?)[\"|\'|<|>| ]',body)
		if trailer:addir_info('[COLOR lime]Trailer[/COLOR] - '+name,trailer,img,fanart,mode,1,'vp_getclip')
		#------------------------------------------------------------------------------------------------
	return ''

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

def music(name,url,img,fanart,mode,page,query):
	title='[COLOR gold]chiasenhac.vn[/COLOR]'
	addir_info(title,'http://chiasenhac.vn/',os.path.join(iconpath,'chiasenhac.png'),'',45,1,'Home',True)
	
	title='[COLOR blue]nhaccuatui.com[/COLOR]'
	addir_info(title,'nhaccuatui.com',os.path.join(iconpath,'nhaccuatui.png'),'',46,1,'Home',True)
	
	title='[COLOR fuchsia]nhacdj.vn[/COLOR] (Dành cho lũ trẻ - U40 không nên vào!)'
	addir_info(title,'nhacdj.vn',os.path.join(iconpath,'nhacdj.png'),'',42,1,'Home',True)
		
def nhacdj(name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'nhacdj.png');urlhome='http://nhacdj.vn/';c='fuchsia'
	if not os.path.isfile(ico):
		try:urllib.urlretrieve('https://lh6.ggpht.com/gIx3RPsUEMcNbDA2hkM2OA6-MxONAJ9BtZBOwbCpOhU71pO601kxFWgdhkYfk7B2vA8=w300',ico)
		except:pass
	def detail(b):
		for s in re.findall('(class="song-name".+?</div>\s*</div>)',b,re.DOTALL):
			href=xsearch('href="([^"]+?)"',s)
			title=xsearch('title="([^"]+?)"',s)
			views=xsearch('class="song-listen">([^"]+?)</div>',s)
			if views:title+=' - [COLOR gold]%s[/COLOR]'%views
			upload=xsearch('title="[^"]+?">([^"]+?)</a>.?<i class="icon-caret-right">',s)
			if upload:title+=' - [COLOR blue]%s[/COLOR]'%upload
			addir_info(title,href,ico,'',mode,1,'play')
		
		p=xsearch('(<div class="pagination">.+?</div)',b,1,re.DOTALL).replace('\n','')
		if p:
			pn=xsearch('class="page active"[^"]+?href="([^"]+?)"',p)
			pages=xsearch('page=(\d+?)"[^<]+?>Cuối</a>',p)
			title=color['trangtiep']+'Page next: %d/%s[/COLOR]'%(page+1,pages)
			addir_info(title,pn,ico,'',mode,page+1,'djpage',True)

	if not os.path.isfile(ico):
		try:urllib.urlretrieve('http://nhacdj.vn/images/misc/logo-dj.png',ico)
		except:pass
	if query=='Home':
		body=get_home_page('nhacdj.html',urlhome)
		title=color['search']+"Search trên nhacdj.vn[/COLOR]"
		#addir_info(title,'nhacdj.vn',ico,'',mode,1,'search',True)
		
		s=xsearch('(<ul class="navbar">.+?</ul>)',body,1,re.DOTALL)
		for href,title in re.findall('<a href="(.+?)" title="(.+?)">',s):
			addir_info(namecolor(title,c),href,ico,'',mode,1,'djpage',True)
		
		s=xsearch('(class="left-box-home".+?</div></div></div></div>)',body,1,re.DOTALL)
		label=xsearch('>([^<]+?)</h4>',s)
		if label:add_sep_item('%s'%label)
		for href,title in re.findall('href="(.+?)">(.+?)</a>',s):
			addir_info(title,href,ico,'',mode,1,'play')
		
		if get_home_page('nhacdj.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
		
	elif query=='vdjpage':
		b=make_request(url)
		s=xsearch('(id="list-video-cat".+?class="[^<]+?">Cuối</a>)',b,1,re.DOTALL)
		for href,title,img in re.findall('href="(.+?)" title="(.+?)"><img src="(.+?)"',s):
			addir_info(title,href,img,'',mode,1,'vplay')
		
		p=xsearch('(<div class="pagination">.+?>Cuối</a>)',s,1,re.DOTALL).replace('\n','')
		if p:
			pn=xsearch('class="page active"[^"]+?href="([^"]+?)"',p)
			pages=xsearch('page=(\d+?)"[^<]+?>Cuối</a>',p)
			title=color['trangtiep']+'Page next: %d/%s[/COLOR]'%(page+1,pages)
			addir_info(title,pn,ico,'',mode,page+1,'vdjpage',True)
		
	elif query=='djpage':
		b=make_request(url)
		if url=='http://nhacdj.vn/Video-cat2.html': 
			s=xsearch('("child-cat-list".+?</ul>)',b,1,re.DOTALL)
			for href,title in re.findall('href="(.+?)">(.+?)</a>',s):
				addir_info(namecolor(title,c),href,ico,'',mode,1,'vdjpage',True)
			s=xsearch('(id="top-video-data".+?Xem thêm</a>)',b)#,1,re.DOTALL):
			for href,img,title in re.findall('href="([^<]+?)"><[^<]+?src="([^<]+?)"[^<]+?title="([^<]+?)"',s):
				addir_info(title,href,img,'',mode,1,'vplay')
		else:detail(b)
	
	elif query=='vplay':
		b=make_request(url)
		link=xsearch('(youtube.com/[^"]+?)&',b)
		if link:play_youtube('https://www.'+link)
		
	elif query=='play':# http://nhacdj.vn/category.xml http://nhacdj.vn/Nhac-San-Dam-Cuoi-alb828.xml http://nhacdj.vn/artist1.xml
		b=make_request(url);link=''
		link=xsearch('flashvars="file=(.+?)"',b);print link
		if link:link=dl(link)
		if link:xbmcsetResolvedUrl(link)
		else:
			link_=xsearch("file:.?'(.+?)'",b);print link
			if link_:link=dl(link_)
			if link:xbmcsetResolvedUrl(link)
			else:xbmcsetResolvedUrl(link_)#mess('File invalid or deleted!','nhacdj.vn') 

def nhaccuatui(name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'nhaccuatui.png');urlhome='http://www.nhaccuatui.com/';c='turquoise'
	if not os.path.isfile(ico):
		try:urllib.urlretrieve('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTKOJ_A9ybSZxzDgfG_cChKX84xkOjnCCkM36ptKxBNHxHOOCjc',ico)
		except:pass
		
	def nct_play(url,inf='Video'):
		if not url:xbmcplugin.setResolvedUrl(int(sys.argv[1]), False, None)
		else:
			item=xbmcgui.ListItem(path=url)
			item.setInfo(inf, {'Title':name})
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	
	from resources.lib.servers import nhaccuatui;nct=nhaccuatui()
	if query=='Home':
		b=xread(urlhome);counter_pl=nct.getCounter_pl(b);counter_sg=nct.getCounter_sg(b)
		title=namecolor('Search trên nhaccuatui.com','lime')
		addir_info(title,'nhaccuatui.com',ico,'',mode,1,'search',True)
		for href,title in re.findall('<a rel="follow" href="([^"]+?)"[^<]+?>([^<]+?)</a>',b):
			if 'nghe-si' in href:q='nghe-si'
			elif 'su-kien' in href:q='su-kien'
			elif 'playlist-hero' in href:q='hero'
			else:q='menu'
			addir_info(namecolor(title,c),href,ico,'',mode,1,q,True)
		
		add_sep_item('-----Playlist mới------')
		for s in [i for i in re.findall('(<li.+?/li>)',b,re.DOTALL) if '"box-left-album"' in i]:
			title,href,img=nct.getDetail_pl(s,counter_pl)
			addir_info(namecolor(title,c),href,img,'',mode,1,'playlist',True)
	
		add_sep_item('-----Bài hát mới------')
		for s in [i for i in re.findall('(<li.+?/li>)',b,re.DOTALL) if '"box-content-music-list"' in i]:
			title,href,img=nct.getDetail_sg(s,counter_sg)
			addir_info(title,href,img,'',mode,1,'play')
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="nhaccuatui.com" or query=="INP" or query=="search-in":
		def make_list(i):
			tt,title,href,img=i
			if 'Page next:' in title:
				addir_info(title.replace('page',str(page+1)),href,img,'',mode,page+1,query,True)
			elif '/bai-hat/' in href:addir_info(title,href,img,'',mode,1,'play')
			elif '/playlist/' in href:addir_info(namecolor(title,c),href,img,'',mode,1,'playlist',True)
			elif '/video/' in href:addir_info(title,href,img,'',mode,1,'playvideo')
			elif '/nghe-si-' in href:
				title=namecolor('Nghệ sĩ '+title,c)
				addir_info(title,href.replace('.html','.bai-hat.html'),img,'',mode,1,'page',True)
			elif '/tim-kiem?q=' in href:
				title=namecolor('Tìm kiếm theo cụm từ [COLOR gold]%s[/COLOR]'%title,c)
				addir_info(title,href,img,'',mode,1,'search-in',True)
			elif tt=='1':addir_info(namecolor(title,'blue'),href,img,'',mode,1,'search-in',True)
		
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query:return 'No'
		
		items=nct.search(urllib.quote(query),url)
		
		j=[j for j in items if j[0]=='0']
		if j:
			add_sep_item('-----Kết quả tìm nhanh------')
			for i in j:make_list(i)
			add_sep_item('-----Kết quả được đề xuất bởi NhacCuaTui------')
		for i in [j for j in items if j[0]!='0']:make_list(i)
	
	elif query=='menu':
		b=xread(urlhome)
		s=''.join([i for i in re.findall('(<a rel="follow".+?/ul>)',b,re.DOTALL) if  url in i]).replace('\\','')
		s=xsearch('(<ul.+?/ul>)',s)
		#f=open(r'd:\xoa1.html','w');f.write(s);f.close()
		for href,title in re.findall('href="([^"]+?)"[^<]+?>([^<]+?)</a>',s):
			if 'http' not in href:href='http://www.nhaccuatui.com'+href
			addir_info(namecolor(title,c),href,ico,'',mode,1,'BXH' if 'BXH' in name else 'page',True)
		
		if 'BXH' in name:
			for title,href,img in nct.getBXH(url):
				if not img:img=ico
				if 'COLOR lime' not in title:addir_info(title,href,img,'',mode,1,'play')
				else:addir_info(title,href,img,'',100,page+1,query)
	
	elif query=='hero':
		add_sep_item('-----PLAYLIST MỚI THAM GIA TUẦN NÀY------')
		for title,href,img in nct.getPage_hero(url):
			if 'Page next:' not in title:addir_info(namecolor(title,c),href,img,'',mode,1,'playlist',True)
			else:addir_info(title.replace('page',str(page+1)),href,ico,'',mode,page+1,query,True)
		
		href='http://www.nhaccuatui.com/playlist-hero-top-10.html'
		addir_info(namecolor('CÁC CHỦ ĐỀ TRƯỚC','blue'),href,img,'',mode,1,'hero-10',True)
	
	elif query=='hero-10':
		for title,href,img in nct.getPage_hero_10(url):
			addir_info(namecolor(title,c),href,img,'',mode,1,'playlist',True)

	elif query=='nghe-si':
		for title,href,img in nct.getNghesi(url):
			addir_info(namecolor(title,c),href,ico,'',mode,1,'page',True)
		
	elif query=='su-kien':
		for title,href,img,fanart in nct.getSukien(url):
			if not fanart:fanart=img
			addir_info(title,'http://event.nhaccuatui.com/'+os.path.basename(href),img,fanart,mode,1,'listSK',True)
		
	elif query=='listSK':
		for title,href,img in nct.listSukien(url):
			addir_info(title,href,img,fanart,mode,1,'playvideo')
	
	elif query=='BXH':
		for title,href,img in nct.getBXH(url):
			if not img:img=ico
			if 'COLOR lime' not in title:addir_info(title,href,img,'',mode,1,'play')
			else:addir_info(title,href,img,'',100,page+1,query)
		
	elif query=='page' and 'bai-hat' in url:
		if 'nghe-si' in url and page==1:
			title='[COLOR gold]Playlist[/COLOR] - '+name
			addir_info(title,url.replace('.bai-hat.html','.playlist.html'),ico,'',mode,1,'playlist',True)
			title='[COLOR gold]Video[/COLOR] - '+name
			addir_info(title,url.replace('.bai-hat.html','.mv.html'),ico,'',mode,1,'page',True)
			add_sep_item('-----Bài Hát %s ------'%namecolor(name))
		
		for title,href,img in nct.getPage_sg(url):
			if not img:img=ico
			if 'Page next:' not in title:addir_info(title,href,img,'',mode,1,'play')
			else:addir_info(title.replace('page',str(page+1)),href,img,'',mode,page+1,query,True)

	elif query=='page' and 'playlist' in url:
		for title,href,img in nct.getPage_pl(url):
			if 'Page next:' not in title:addir_info(namecolor(title,c),href,img,'',mode,1,'playlist',True)
			else:addir_info(title.replace('page',str(page+1)),href,ico,'',mode,page+1,query,True)
	
	elif query=='page'  and ('video-' in url or '.mv.' in url):
		for title,href,img in nct.getPage_video(url):
			if 'video' not in href and 'page' not in img:continue
			elif img=='link':addir_info(title,href,ico,'',mode,1,query,True)
			elif img=='page':addir_info(title.replace('page',str(page+1)),href,ico,'',mode,page+1,query,True)
			else:addir_info(title,href,img,'',mode,1,'playvideo')
	
	elif query=='playlist' or 'chu-de' in url:
		for title,href,img in nct.getPlayList(url):
			if not title:continue
			elif '/playlist/' in href:addir_info(namecolor(title,c),href,img,'',mode,1,'playlist',True)
			elif img=='page':addir_info(title.replace('page',str(page+1)),href,ico,'',mode,page+1,query,True)
			else:addir_info(title,href,img,'',mode,1,'playPL')
	
	elif query=='playPL':nct_play(url,inf='Music')
	elif query=='play':nct_play(nct.getLink(xsearch('\.(\w+)\.html',url)),inf='Music')
	elif query=='playvideo':
		id=xsearch('\.(\w+)\.html',url)
		if not id:id=xsearch('src="http://www.nhaccuatui.com/vh/auto/(\w+)\?',xread(url,nct.headers))
		nct_play(nct.getLink(id,'video'),inf='video')

def chiasenhac(name,url,img,fanart,mode,page,query):
	hd={'User_Agent':'Mozilla/5.0 (Android 4.4; Mobile; rv:42.0) Gecko/41.0 Firefox/42.0'}
	if myaddon.getSetting('resolut')=='Max':hd['Cookie']='vq=i%3A1080%3B; mq=i%3A500%3B'
	else:hd['Cookie']='vq=i%3A720%3B; mq=i%3A500%3B'
	ico=os.path.join(iconpath,'chiasenhac.png');icodj=os.path.join(iconpath,'nhacdj.png');urlhome='http://chiasenhac.vn/'
	if not os.path.isfile(ico):
		try:urllib.urlretrieve('http://chiasenhac.vn/templates/light2012/images/logo.jpg',ico)
		except:pass
	#url=url.replace('.com','.vn')
	def csn_url(url):return urlhome+url if 'http://' not in url else url
	
	def csn_get_dir(s,art=dict(),isFolder=False):
		result=re.search('<a href="(.+?)" title="(.+?) - (.+?)"',s)
		if not result:result=re.search('<a href="(.+?)".+?"_top">(.+?)</a>.*[\n|](.+?)[\n|].*</span>',s)
		if not result:result=re.search('<a href="(.+?)".+?>(.+?)</a><br />\s+?(\S.+?)\n',s)
		if result:
			href=csn_url(result.group(1))
			t1=result.group(2).strip();t2=result.group(3).strip()
			img=art.get(href,xsearch('<img src="(.+?)"',s,result=ico))
			res=xsearch('<span style=".+?">(.+?)</span>',s)
			p1='<p class="middle">([\d|\.]+?)</p>';p2='<span class="gen">([\d|\.]+?)</span><br />'
			d1=xsearch(p1,s,result=xsearch(p2,s))
			p1='<span>([\d|\.|\:]+?)</span>';p2='<p>([\d|\.|\:]+?)</p>'
			p3='<span class="gensmall">([\d|\.|\:]+?)<br />'
			d2=xsearch(p1,s,result=xsearch(p2,s,result=xsearch(p3,s)))
			title='[COLOR red]%s[/COLOR] [COLOR yellow]%s[/COLOR] [COLOR green]%s[/COLOR]'%(res,d2,d1)
			if isFolder:
				title='[COLOR green]%s[/COLOR] [COLOR yellowgreen]%s[/COLOR] %s'%(t1,t2,title)
				addir_info(title,href,img,'',mode,1,'get_album',True,menu=menu)
			else:
				title='%s [COLOR yellowgreen]%s[/COLOR] %s'%(t1,t2,title)
				addir_info(title,href,img,'',mode,1,'csn_play',menu=menu)

	def csn_get_album(body):
		img=xsearch('"image_src" href="(.+?)"',body,result=ico)
		for s in re.findall('(<tr id=.playlist.+?</tr>)',body,re.DOTALL):
			result=re.search('<a href="(.+?)" class="musictitle".*?>([^<>].+?)</.+?>([^<>]+?)</span>',s)
			if result:
				href=csn_url(result.group(1))
				t1=result.group(2).replace('amp;','');t2=result.group(3).replace('-','').replace('amp;','').strip()
				label='%s [COLOR yellowgreen]%s[/COLOR]'%(t1,t2)
				addir_info(label,href,img,'',mode,1,'csn_play',menu=menu)

	def csn_video_main_page(body):
		subbody=xsearch('(<div class="h-main3".+?<div class="t2">)',body,1,re.DOTALL)
		result=re.search('<a href=".+?">(.+?)</a>.+?href="(.+?)"',subbody,re.DOTALL)
		if result:
			title='[COLOR lime]Playlist %s (Full)[/COLOR]'%result.group(1)
			addir_info(title,csn_url(result.group(2)),ico,'',mode,1,'get_album',True)
			pattern='<div class="gensmall"(.+?)class="info"'
			for s in re.findall(pattern,subbody,re.DOTALL):csn_get_dir(s)
		bodys=re.findall('(<div class="h-main3".+?</ul></div>)',body[body.find('class="t2"'):],re.DOTALL)
		for subbody in bodys:
			result=xsearch('class="cattitle">(.+?)</p>',subbody)
			if result:#Mới chia sẻ, Download mới nhất
				npage=xsearch('class="active_page"><a .+?><a href="(.+?)"',subbody)
				if npage:
					title='[COLOR lime]Video Clip/%s: Xem thêm[/COLOR]'%result
					addir_info(title,csn_url(npage),ico,'',mode,1,'get_video_page',True)
				else:
					title='[COLOR gold]Video Clip/%s  -----------------[/COLOR]'%result
					addir_info(title,'',ico,'',mode)
				for s in re.findall('<div class="gensmall"(.+?)class="info"',subbody,re.DOTALL):
					csn_get_dir(s)

	def csn_mp3_main_page(body):
		subbody=xsearch('(<th class="catLeft".+?</table>)',body,1,re.DOTALL)
		label=xsearch('\](.+?)[\:|\[]',name).replace('BXH','').strip()
		if subbody:
			if 'Bảng xếp hạng' in name:#Album mới chia sẻ
				result=re.search('"absmiddle"> <a href="(.+?)">(.+?)</a>',subbody)
				title='[COLOR lime]%s/%s: Xem thêm...[/COLOR]'%(label,result.group(2))
				href=result.group(1)
				if href:addir_info(title,csn_url(href),ico,'',mode,1,'get_album_page',True)
			else:
				result=re.search('"absmiddle"> (.+?)</span>.+?<a href="(.+?)">',subbody,re.DOTALL)
				if result:
					title='[COLOR lime]%s/%s: Xem thêm...[/COLOR]'%(label,result.group(1))
					href=result.group(2)
					if href:addir_info(title,csn_url(href),ico,'',mode,1,'get_album_page',True)
			art=dict(re.findall('<a href="(.+?)"><img src="(.+?)"',body))
			for s in re.findall('(<td title.+?</span></td>)',subbody,re.DOTALL):csn_get_dir(s,art,True)
		for subbody in re.findall('(class="ht-c".+?class="t2")',body,re.DOTALL):
			result=xsearch('<p style="float.+?">([^<].+?)</a>',subbody)
			if result:#Việt Nam, US-UK, Playback
				title='[COLOR lime]%s - Playlist (Full)[/COLOR]'%result
				href=xsearch('<a href="(.+?)" class="xt">',subbody)
				if href:addir_info(title,csn_url(href),ico,'',mode,1,'get_album',True)
				for s in re.findall('("li-3".+?href=.+?</span></p>)',subbody,re.DOTALL):csn_get_dir(s)
			else:#Mới chia sẻ, Download mới nhất
				result=xsearch('<p style="float.+?">([^<].+?)</p>',subbody)
				if result:
					title='[COLOR lime]%s/%s: Xem thêm...[/COLOR]'%(label,result)
					href=xsearch('<a href="(.+?)" class="xt">',subbody)
					if href:addir_info(title,csn_url(href),ico,'',mode,1,'get_mp3_page',True)
					for s in re.findall('("text2".+?</span></p>)',subbody,re.DOTALL):csn_get_dir(s)
	
	def csn_get_album_page(body):
		art=dict(re.findall('<a href="(.+?)"><img src="(.+?)"',body))
		for subbody in re.findall('(class="catLeft".+?class="xt">.+?</a>)',body,re.DOTALL):
			result=re.search('<a href="(.+?)">(.+?)</a></span></th>',subbody)
			if result:
				title='[COLOR lime]%s[/COLOR]'%result.group(2)
				addir_info(title,csn_url(result.group(1)),ico,'',mode,1,'get_album_page',True)
			elif not result:
				label=xsearch('"absmiddle"> (.+?)</span></th>',subbody)
				result=re.search('<a href="(.+?)".+?class="xt">(.+?)</a>',subbody)
				if label and result:
					if 'Quay về' not in result.group(2):
						title='[COLOR lime]%s: %s - %s[/COLOR]'%(xsearch('\](.+?)[\:|\[]',name),label,result.group(2))
						addir_info(title,csn_url(result.group(1)),ico,'',mode,1,'get_album_page',True)
					else:
						title='[COLOR lime]%s: %s[/COLOR]'%(xsearch('\](.+?)[\:|\[]',name),label)
						addir_info(title,'',ico,'',mode,1,'')
			for s in re.findall('class="gen"(.+?)</span></td>',subbody,re.DOTALL):csn_get_dir(s,art,True)
	
	def csn_search(url,string):
		if 'changeSettings' in string:string=string.replace('changeSettings','')
		if '?' not in url and string:
			setting={'None':'Tên bài hát/Ca sĩ','artist':'Ca sĩ',
					'composer':'Sáng tác','album':'Tên Album','lyric':'Lời bài hát'}
			search_set=myaddon.getSetting('csn_s')
			m=''.join(s for s in setting if  setting.get(s)==search_set and s!='None')
			c='video' if string[0]=='v' else 'music' if string[0]=='m' else ''
			href='http://search.chiasenhac.vn/search.php?s=%s&mode=%s&cat=%s'
			href=href%(urllib.quote_plus(string[1:]),m,c)
		else:m=xsearch('mode=(.+?)\W',url+'&');href=url
		body=xread(href)
		
		if m=='album':
			csn_get_album_page(body)
			next=xsearch('<a href="(.+?)" class="xt">Xem thêm...</a>',body)
			if next:
				title='[COLOR lime]Search: Xem thêm...[/COLOR]'
				addir_info(title,next.replace('amp;',''),ico,'',mode,1,query,True)
		else:
			title='Ẩn' if myaddon.getSetting('csn_l')=='true' else 'Hiện'
			title=namecolor('%s Playlisst trong kết quả tìm kiếm'%title,'lime')
			addir_info(title,url,ico,'',mode,1,'changeSettings'+string,True)
			imgs=dict(re.findall('<a href="(.+?)"><img src="(.+?)"',body))
			for s in re.findall('(<tr.+?/tr>)',body,re.DOTALL):
				href=xhref(s);t1=xsearch('target=".+?">(.+?)</a>',s)
				if not href or not t1:continue
				t2=xsearch('<p>([^<]+?)</p>\s+</div>',s)
				d1=xsearch('<span class="gen">(.+?)<br />',s)
				d2=xsearch('style="color: .+?">(.+?)</span>',s)
				d3=xsearch('<td nowrap="nowrap" align="center">\s+<p>(.+?)<p>',s)
				title='%s [COLOR yellowgreen]%s[/COLOR] [COLOR red]%s[/COLOR] [COLOR yellow]%s[/COLOR] [COLOR green]%s[/COLOR]'%(t1,t2,d2,d1,d3)
				href=csn_url(href);img=imgs.get(href,ico)
				addir_info(title,href,img,'',mode,1,'csn_play',menu=menu)
				if myaddon.getSetting('csn_l')=='false':result=''
				else:result=re.search('<p>(.*?)<a href="(.+?)" title="(.+?)">.+?alt="Listen Album"',s)
				if result:#Playlist item
					t1=result.group(3).replace('Nghe playlist:','Playlist:')
					title='[COLOR green]%s[/COLOR] [COLOR yellowgreen]%s[/COLOR]'%(t1,result.group(1))
					addir_info(title,csn_url(result.group(2)),img,'',mode,1,'get_album',True)
			
			subbody=xsearch('(<th colspan="3" height="25">.+?</table>)',body,1,re.DOTALL)
			result=xsearch('<th colspan="3" height="25">(.+?)</th>',subbody)
			if result:#Album result
				addir_info('[COLOR gold]-----%s-----[/COLOR]'%result,'',ico,'',mode,1,'No')
				for i in re.findall('<a href="(.+?)" title="(.+?)".+?</a>(.*?)<br />\s.*\s.*<span style.+?>(.+?)</span>',subbody):
					img=imgs.get(i[0],ico)
					title='[COLOR green]%s[/COLOR] [COLOR yellowgreen]%s[/COLOR] [COLOR red]%s[/COLOR]'%(i[1],i[2],i[3])
					addir_info(title,csn_url(i[0]),img,'',mode,1,'get_album',True)
		
			npage=re.search('class="active_page"><a .+?><a href="(.+?)" class="npage">(.+?)</a>',body)
			if npage:
				title='[COLOR lime]Search: [COLOR yellow]%s[/COLOR]- Trang %s[/COLOR]'%(string,npage.group(2))
				addir_info(title,csn_url(npage.group(1).replace('amp;','')),img,'',mode,1,string,True)
	
	menu={'MyPlaylist':{'action':'Add','server':['chiasenhac.vn']}}
	if query not in 'search-csnSearch-INF' and 'csn_Search_' not in query and 'changeSettings' not in query:
		body=make_request(urlhome) if query=='Home' else make_request(url,headers=hd)
	
	if query=='csnSearch':
		menu={'MyPlaylist':{'action':'Search','server':['chiasenhac.vn']}}
		title='[COLOR lime]CSN Search[/COLOR] [COLOR blue]Tất Cả[/COLOR] theo - [COLOR gold]%s[/COLOR] - Phím Func tìm khác'%myaddon.getSetting('csn_s')
		addir_info(title,'chiasenhac.vn',ico,'',mode,1,'search',True,menu=menu)
		title='[COLOR lime]CSN Search[/COLOR] [COLOR blue]Videos[/COLOR] theo - [COLOR gold]%s[/COLOR] - Phím Func tìm khác'%myaddon.getSetting('csn_s')
		addir_info(title,'chiasenhac.vn',ico,'',mode,1,'search',True,menu=menu)
		title='[COLOR lime]CSN Search[/COLOR] [COLOR blue]Nhạc[/COLOR] theo - [COLOR gold]%s[/COLOR] - Phím Func tìm khác'%myaddon.getSetting('csn_s')
		addir_info(title,'chiasenhac.vn',ico,'',mode,1,'search',True,menu=menu)
		
	elif query=='Home':
		menu={'MyPlaylist':{'action':'Search','server':['chiasenhac.vn']}}
		title='[COLOR lime]CSN Search ...[/COLOR]'
		addir_info(title,'chiasenhac.vn',ico,'',mode,1,'csnSearch',True,menu=menu)
		
		menu={'MyPlaylist':{'action':'Add','server':['chiasenhac.vn']}}
		title='[COLOR lime]My playlist - Tên Album[/COLOR]'
		addir_info(title,'http://chiasenhac.vn/mp3/favourite',ico,'',mode,1,'myplaylist_album',True)
		
		title='[COLOR lime]My playlist - Tên Bài hát[/COLOR]'
		addir_info(title,'http://chiasenhac.vn/mp3/favourite',ico,'',mode,1,'myplaylist_baihat',True)
		
		for i in re.findall('style="white-space.+href="(.*?)" title="(.+?)"',body):#Main menu
			href=csn_url(i[0])
			addir_info('[COLOR green]%s[/COLOR]'%i[1],href,ico,'',mode,1,'submenu',True)
			
		for i in re.findall('<div class="[v|h]t[3|-][1|c]">(.+?)<div class=".2">',body,re.DOTALL):#Detail hompage
			result=re.search('<a href="(.+?)" class="cattitle">(.+?)</a>',i)
			if result:#BXH Video Clip, BXH Nhạc Việt Nam, BXH Nhạc US-UK
				title='[COLOR lime]%s[/COLOR]'%result.group(2)
				addir_info(title,csn_url(result.group(1)),ico,'',mode,1,'main_page',True)
			else:
				result=re.search('<a href="(.+?)">(.+?)</a></span></th>',i)
				if result:#Album mới chia sẻ
					title='[COLOR lime]%s[/COLOR]'%result.group(2)
					addir_info(title,csn_url(result.group(1)),ico,'',mode,1,'get_album_page',True)
				else:
					result=xsearch('<a href="(.+?)"',i);title=xsearch('>(.+?)</p>',i)
					if result and title:#Download mới nhất, Mới chia sẻ
						addir_info('[COLOR lime]%s[/COLOR]'%title,csn_url(result),ico,'',mode,1,'get_mp3_page',True)
					else:continue
			
			if 'Album' in title:
				art=dict(re.findall('<a href="(.+?)"><img src="(.+?)"',body))
				items=re.findall('(<td title.+?</span></td>)',i,re.DOTALL)
				for subbody in items:csn_get_dir(subbody,art,True)
			else:
				if 'Video' in title:items=re.findall('<div class="gensmall"(.+?)class="info"',i,re.DOTALL)
				elif 'Download' in title or 'chia' in title:items=re.findall('class="text2"(.+?</span></p>)',i,re.DOTALL)
				elif 'Cảm' in title:items=re.findall('class="info"(.+?)lass="tip"',i,re.DOTALL)
				else:items=re.findall('class="texte1x"(.+?</span></p>)',i,re.DOTALL)
				for subbody in items:csn_get_dir(subbody)
	
	elif query=='search':make_mySearch(name,'chiasenhac.vn','','',mode,'get')
	elif 'csn_Search_' in query:#thay doi cach tim
		query=query.replace('csn_Search_','')
		setting={'None':'Tên bài hát/Ca sĩ','artist':'Ca sĩ',
			'composer':'Sáng tác','album':'Tên Album','lyric':'Lời bài hát'}
		myaddon.setSetting('csn_s',setting.get(query));xbmc.executebuiltin("Container.Refresh")
	
	elif 'changeSettings' not in query and ("INP" in query or 'search.php' in url or url=='chiasenhac.vn'):
		if "INP" in query:
			q=query.replace('INP','')
			query=make_mySearch('',url,'','','','Input')
			if not query:return 'no'
			query=q+query
		csn_search(url,query)
	
	elif query=='submenu':
		title=xsearch('\](.+?)\[',name)
		subbody=xsearch('title="%s"(.+?)</ul>'%title,body,1,re.DOTALL)
		for href,title in re.findall('<a href="(.+?)" title="(.+?)"',subbody):#sub menu
			if 'Playlist' in name:
				addir_info('[COLOR green]%s[/COLOR]'%title,csn_url(href),ico,'',mode,1,'get_album',True)
			else:addir_info('[COLOR green]%s[/COLOR]'%title,csn_url(href),ico,'',mode,1,'main_page',True)
				
		if 'Playlist' in name:csn_get_album(body)
		elif 'Video Clip' in name:csn_video_main_page(body)
		else:csn_mp3_main_page(body)

	elif query=='main_page':
		if 'Video' in name:csn_video_main_page(body)
		elif 'BXH' in name and url!='http://chiasenhac.vn/mp3/vietnam/':
			body=make_request(url)
			for i in re.findall('(<a href=".+?" class="cattitle">(.+?)</a>)',body):
				add_sep_item(i[1])
				subbody=xsearch('%s(.+?)</table>'%i[0],body,1,re.DOTALL)
				for s in re.findall('(<tr.+?/tr>)',subbody,re.DOTALL):csn_get_dir(s)
		else:csn_mp3_main_page(body)
				
	elif query=='get_video_page':
		for s in re.findall('"gensmall"(.+?)"info"',body,re.DOTALL):csn_get_dir(s)
		npage=re.search('class="active_page"><a .+?><a href="(.+?)" class="npage">(.+?)</a>',body)
		if npage:
			title='[COLOR lime]%s: Trang tiếp theo - Trang %s[/COLOR]'%(xsearch('\](.+?):',name),npage.group(2))
			addir_info(title,csn_url(npage.group(1)),ico,'',mode,1,'get_video_page',True)
		
	elif query=='get_mp3_page':#Download mới nhất, Mới chia sẻ, Cảm nhận mới
		for s in re.findall('<tr class="\d{,4}(.+?)</tr>',body,re.DOTALL):csn_get_dir(s)
		npage=re.search('class="active_page"><a .+?><a href="(.+?)" class="npage">(.+?)</a>',body)
		if npage:
			title='[COLOR lime]%s: Xem thêm - Trang %s[/COLOR]'%(xsearch('\](.+?)[\:|\[]',name),npage.group(2))
			addir_info(title,csn_url(npage.group(1)),ico,'',mode,1,'get_mp3_page',True)

	elif query=='get_album_page':csn_get_album_page(body)
	
	elif query=='get_album':csn_get_album(body)
	
	elif 'myplaylist' in query:
		menu={'MyPlaylist':{'action':'Remove','server':['chiasenhac.vn']}}
		from resources.lib.servers import chiaseNhac
		csn=chiaseNhac(myaddon.getSetting('csn_u'),myaddon.getSetting('csn_p'));
		body=csn.get_favourite();csn.logout()
		imgs=re.findall('<a href="(.+?)" title=".+?"><img src="(.+?)"',body)
		for s in re.findall('(<tr class.+?/tr>)',body,re.DOTALL):
			result=re.search('<span class="musictitle"><a href="(.+?)" class="musictitle">(.+?)</a>',s)
			if result:
				href=csn_url(result.group(1))
				d1=result.group(2)
				d2=xsearch('<br /> <span class="gen">(.+?)</span>',s)
				d3=xsearch('<span style="color.+?">(.+?)</span>',s)
				d4=xsearch('<div style="position.+?">(.+?)<br />',s)
				d5=xsearch('<span class="postdetails">(.+?)</span>',s)
				#img=imgs.get(href,ico)
				img=[i[1] for i in imgs if os.path.basename(href) in i[0]]
				img=img[0] if img else ico
				title='%s [COLOR yellowgreen]%s[/COLOR] [COLOR red]%s[/COLOR] [COLOR yellow]%s[/COLOR] [COLOR green]%s[/COLOR]'%(d1,d2,d3,d4,d5)
				if query=='myplaylist_baihat':addir_info(title,href,img,'',mode,1,'csn_play',menu=menu)
				else:
					title='[COLOR green]%s[/COLOR]'%title;href=href.replace('/favourite/','/nghe-album/')
					addir_info(title,href,ico,'',mode,1,'get_album',True,menu=menu)

	elif query=='playlist_Add':
		from resources.lib.servers import chiaseNhac
		csn=chiaseNhac(myaddon.getSetting('csn_u'),myaddon.getSetting('csn_p'));csn.favourite(url);csn.logout()
	
	elif query=='playlist_Remove':
		from resources.lib.servers import chiaseNhac
		csn=chiaseNhac(myaddon.getSetting('csn_u'),myaddon.getSetting('csn_p'))
		csn.favourite(url,'remove');csn.logout();xbmc.executebuiltin("Container.Refresh")
	
	elif query=='playlist_RemoveAll':
		if mess_yesno('xshare cảnh báo','Delete all in My Playlist? (Trừ bài hát cuối cùng - hehehe)'):
			from resources.lib.servers import chiaseNhac
			csn=chiaseNhac(myaddon.getSetting('csn_u'),myaddon.getSetting('csn_p'));body=csn.get_favourite()
			for href in re.findall('<span class="musictitle"><a href="(.+?)" class="musictitle">.+?</a>',body):
				csn.favourite(csn_url(href),'remove')
			csn.favourite(csn_url(href));csn.logout();xbmc.executebuiltin("Container.Refresh")
	
	elif query=='csn_play':
		href=xsearch('"(http.+?\.csn)"',body);print href
		if 'http://' not in href:href=urllib.unquote(href)
		if '/m4a/' in href and '.m4a.' in href:href=href.replace('/m4a/','/flac/').replace('.m4a.','.flac.')
		xbmcsetResolvedUrl(href,img=xsearch('rel="image_src" href="(.+?)"',body))
	
	elif 'changeSettings' in query:
		if myaddon.getSetting('csn_l')=='false':myaddon.setSetting('csn_l','true')
		else:myaddon.setSetting('csn_l','false')
		csn_search(url,query)

def myNAS(name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'mynas.png');urlhome=myaddon.getSetting('my_nas_url')
	username=myaddon.getSetting('my_nas_up')
	if not username or not username.split('/')[0].strip():username=''
	else:hd['Cookie']=makerequest(joinpath(xsharefolder,'mynas.cookie'))
	if not os.path.isfile(ico):
		try:urllib.urlretrieve('http://www.buffalo-asia.com/uploads/product/1299/ws5200d589.png',ico)
		except:pass
	
	def nas_login():
		if not username:return ''
		elif '/' not in username:mess(u'Hãy set username/password đúng quy ước cho acc NAS !','My NAS');return ''
		try:url_login=make_request(urlhome,resp='o').headers.get('location')+'rpc/login'
		except:return ''
		response=make_post(url_login,data={'user':username.split('/')[0],'password':username.split('/')[1]})
		if not response or response.status>302:mess('Login to NAS fail !','My NAS');return ''
		cookie=response.cookiestring
		f=open(joinpath(xsharefolder,'mynas.cookie'),'w');f.write(cookie);f.close()
		return cookie
	
	def nas_items(url,cookie='',loop=True):
		if cookie:hd['Cookie']=cookie
		js=make_request(url,hd,resp='j')
		i=[s for s in js if s.get('name')!='.' and s.get('name')!='..' and s.get('name')!='/' and s.get('name')!='.webaxs']
		if not i and loop:i=nas_items(url,nas_login(),False)
		return i
	
	if query=='home':
		response=make_request(urlhome,resp='o')
		if not response or response.status!=302:return
		url=response.headers.get('location')+'rpc/ls/';query=''
	
	elif query=='nas_play':
		direct_link=url.replace('/ls/','/download/')
		if username:direct_link+='|Cookie='+makerequest(joinpath(xsharefolder,'mynas.cookie'))
		return xshare_resolve(direct_link,os.path.splitext(direct_link)[1][1:].lower())
	
	detail=nas_items(url+urllib.quote(query))
	for title,href,dir in  [(s.get('name'),s.get('path'),s.get('directory')) for s in detail]:
		href=u2s(href);title=u2s(title)
		if str(dir) in 'True-true':addir_info('[COLOR gold]'+title+'[/COLOR]',url,ico,'',mode,page,href,True)
		else:addir_info(title,url+urllib.quote(href),ico,'',mode,page,'nas_play')

def bilutv(name,url,img,mode,page,query):
	hd={'User-Agent':'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}
	ico=os.path.join(iconpath,'bilutv.png');urlhome='http://bilutv.com/';c='hotpink'
	if not os.path.isfile(ico):
		try:makerequest(ico,get('http://bilutv.com/images/logo.png').body,'wb')
		except:pass
		
	def page_items(body,cl='film-item'):
		for s in re.findall('(<li class="%s.+?</li>)'%cl,body,re.DOTALL):
			href=xsearch('href="/(.+?)"',s)
			img=xsearch('original="(.+?)"',s,result=ximg(s))
			title=xsearch('<p class="name">(.+?)</p>',s)
			label=xsearch('<p class="real-name">(.+?)</p>',s)
			title='%s - [COLOR green]%s[/COLOR]'%(title,label)
			quality=xsearch('<span class="label-quality">(.+?)</span>',s)
			label=xsearch('<label class="current-status">(.+?)</label>',s)
			if re.search('Tập \d+|\d+/|/\d+|\+',label):
				title=namecolor(title,c)+' (%s%s)'%('' if not quality else quality+' ',label)
				dir=True;query='folder'
			else:
				title=title+' (%s%s)'%('' if not quality else quality+' ',label)
				dir=False;query='play'
			if 'Thuyết Minh' in label:title='[COLOR blue]TM[/COLOR] '+title
			addir_info(title,urlhome+href,img,'',mode,1,query,dir)
	
	def get_eps(body):
		s=xsearch('(<ul class="list-episode".+?/ul>)',body,1,re.S)
		title=' '.join(s for s in re.sub('\[.+?\]','',name).split())
		items=re.findall('href="(.+?)">(.+?)</a>',s)
		for href,tap in items:
			addir_info('Tập '+tap+' - '+title,href,img,'',mode,1,'play')
		return items
	
	if query=='bilutv.com':
		b=getHome('bilutv.html',urlhome)
		title=color['search']+"Search trên bilutv.com[/COLOR]"
		addir_info(title,'bilutv.com',ico,'',mode,1,'search',True)
		s=xsearch('(<a href="/the-loai.+?"main-content")',b,1,re.DOTALL)
		for href,title in re.findall('<a href="/(.+?)" title="(.*?)">',s):
			if not title:title=xsearch('<a href="/%s".+?</i><span>(.+?)</span>'%href,s)
			if [i for i in ('hoat-hinh','xem-nhieu','chieu-rap') if i in href]:
				addir_info(namecolor(title,c),urlhome+href,ico,'',mode,1,'page',True)
			else:addir_info(namecolor(title,c),href,ico,'',mode,1,'menu',True)
		
		add_sep_item('--------------Top--------------')
		s=xsearch('(<ul id="top-slide".+?/ul>)',b,1,re.DOTALL)
		for title,href,img in re.findall('<a title="(.+?)" href="/(.+?)".+?src="(.+?)"',s):
			addir_info(title,urlhome+href,img,'',mode,1,'folder',True)
		
		add_sep_item('--------------Hot--------------')#;page_items(b)
		page_items(xsearch('(<ul id="film-hot".+?/ul>)',b,1,re.S))
		
		for s in re.findall('(<h2 class="caption".+?/ul>)',b,re.S):
			title=xsearch('<a class="view-all" title="(.+?)" href="/(.+?)">',s,1)
			href=xsearch('<a class="view-all" title="(.+?)" href="/(.+?)">',s,2)
			if title and href:
				addir_info(namecolor(title,'cyan'),urlhome+href,ico,'',mode,1,'page',True)
			page_items(xsearch('(<ul class="list-film".+?/ul>)',s,1,re.S))
		
		if "/cdn-cgi/l/chk_jschl" in b:mess('DDoS protection by CloudFlare','bilutv.com')
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return bilutv(name,url,img,mode,page,query)
		else:return 'no'
	elif url=="bilutv.com":
		search_string = urllib.quote_plus(query)
		url='http://bilutv.com/tim-kiem.html?q=%s'%search_string
		return bilutv(name,url,img,mode,1,'page')

	elif query=='menu':
		body=get_home_page('bilutv.html',urlhome)
		s=xsearch('(<a href="/%s".+?/ul>)'%url,body,1,re.DOTALL)
		if 'phim-le' in url:
			url='http://bilutv.com/danh-sach/phim-le.html'
			addir_info(namecolor('Phim lẻ - Tất cả',c),url,ico,'',mode,1,'page',True)
		elif 'phim-bo' in url:
			url='http://bilutv.com/danh-sach/phim-bo.html'
			addir_info(namecolor('Phim bộ - Tất cả',c),url,ico,'',mode,1,'page',True)
		elif 'quoc-gia' in url:
			url='http://bilutv.com/quoc-gia'
			addir_info(namecolor('Tất cả quốc gia',c),url,ico,'',mode,1,'page',True)
		
		for href,title in re.findall('<a title=".+?" href="/(.+?)">(.+?)</a>',s):
			addir_info(namecolor(title,c),urlhome+href,ico,'',mode,1,'page',True)
				
	elif query=='page':
		body=xread(url)
		page_items(body,'film-item ')
		
		pn=re.search('<a href="/[^<]+?" >(\d+)</a></li><li><a href="/([^<]+?)" class="navigation next" rel="next">',body)
		if pn:
			href=urlhome+pn.group(2);pages=pn.group(1)
			title=color['trangtiep']+'Trang tiếp theo: trang %d/%s[/COLOR]'%(page+1,pages)
			addir_info(title,href,ico,'',mode,page+1,'page',True)
		else:
			pn=re.search('<a href="[^<]+?" >(\d+)</a></li><li><a href="([^<]+?)" class="navigation next" rel="next">',body)
			if pn:
				href=url.split('?')[0]+pn.group(2);pages=pn.group(1)
				title=color['trangtiep']+'Trang tiếp theo: trang %d/%s[/COLOR]'%(page+1,pages)
				addir_info(title,href,ico,'',mode,page+1,'page',True)

	elif query=='eps':get_eps(xread(url))

	elif query=='folder':
		fanart=''
		if '/xem-phim/' not in url:
			body=make_request(url)
			fanart=xsearch('<img alt=".*?" src="(.+?)"',body)
			url=xsearch('<a href="(.*?/xem-phim/.+?)">',body)
			if urlhome not in url:url='http://bilutv.com'+url
		body=make_request(url)
		s=xsearch('(<ul class="choose-server">.+?/ul>)',body,1,re.DOTALL)
		name=' '.join(re.sub('bilutv|Phim|phim|Xem|xem','',namecolor(name)).split())
		if s and re.search('class="list-episode"',body):
			for href,title in re.findall('<a href="/(.+?)".*>([^<]+?)</a>',s):
				addir_info(title+' '+name,urlhome+href,img,fanart,mode,1,'eps',True)
			current=xsearch('<div class="playing"></div>(.+?)</a>',body)
			add_sep_item('--------------List of server: %s--------------'%current)
			get_eps(body)
		elif s:
			for href,title in re.findall('<a href="/(.+?)".*>([^<]+?)</a>',s):
				addir_info(title+' '+name,urlhome+href,img,fanart,mode,1,'play')
		else:
			s=get_eps(body)
			if not s:
				s=re.findall('"(.+www.youtube.com.+)"',body);i=1
				for href in s:
					addir_info('Link %d '%i+name,href,img,fanart,mode,1,'play_yt');i+=1
				if not s:addir_info(name,url,img,fanart,mode,1,'play')

	elif query=='play_yt':play_youtube(url)
	elif query=='play':
		from resources.lib.servers import gibberishAES;keyAES='bilutv.com4590481877'
		if '/xem-phim/' not in url:
			url=xsearch('<a class="btn-see btn btn-danger" href="/(.+?)"',xread(url))
			if urlhome not in url:url=urlhome+url
		
		b=xread(url)
		if "/cdn-cgi/l/chk_jschl" in b:mess('DDoS protection by CloudFlare','bilutv.com');return
		elif 'Vì lý do bản quyền' in b:mess(u'Vì lý do bản quyền! BiluTV không cập nhật phim này nữa');return
		
		link='';max=myaddon.getSetting('resolut')=='Max'
		try:
			L=re.findall("decodeLink\('(.+?)', *(\d+?)\)[^}]+?label: *'(.+?)'",b,re.S)
			if L:L=[(urllib.unquote(gibberishAES(i, keyAES+j)),resolu(l)) for i,j,l in L]
			else:
				j=json.loads(xsearch('playerSetting[^{]+({.+?});',b))
				modelId=j.get('modelId','')
				def abc(i):return urllib.unquote(gibberishAES(i.get('file',''), keyAES+modelId))
				L=[(abc(i),resolu(i.get('label',''))) for i in j.get('sources')]
			L=sorted(L, key=lambda k: int(k[1]),reverse=True if max else False)
			for href,label in L:
				link=test_link(href)
				if link:break
		except:pass
		'''
		xbmcsetResolvedUrl(link)
	
		try:c=urllib.unquote(gibberishAES(b))
		except:c=''
		for h in re.findall('"(/episode/getlinkbackup/.+?)"',c):
			try:
				j=json.loads(xread('http://bilutv.com'+h))
				L=[(s.get('file'),resolu(s.get('label'))) for s in j]
			except:L=[]
			L=sorted(L, key=lambda k: int(k[1]),reverse=True if max else False)
			#print L
			for href,label in L:
				link=test_link(href)
				if link:break
			if link:break

		if not link:
			L=[]
			for s in re.findall('(\{file:decodeLink.+?\})',c):
				L.append((xsearch("\('(.+?)'",s),xsearch("\('.+?',(\d+)\)",s),resolu(xsearch("label:'(.+?)'",s))))
			L=sorted(L, key=lambda k: int(k[2]),reverse=True if max else False)
			#print L
			if L:
				for href,id,label in L:
					try:href=urllib.unquote(gibberishAES(href, "bilutv.com454657883435677%s"%id))
					except:continue
					link=test_link(href)
					if link:break
		'''
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','bilutv.com') 

def anime47(name,url,img,mode,page,query):
	ico=os.path.join(iconpath,'anime47.png');urlhome='http://anime47.com/';c='deepskyblue'
	hd['Cookie']='location.href=1';gkplugins='http://dll.anime47.com/gkphp/plugins/gkpluginsphp.php'
	if not os.path.isfile(ico) or filetime(ico)>2000:
		try:makerequest(ico,xread('http://anime47.com/skin/tatcasau/img/logo.png'),'wb')
		except:pass
	
	def get_item(s):
		title=xsearch('alt="(.+?)"',s,result=xsearch('(<h3.+?/h3>)',s,1,re.S,result=xsearch('(<h1.+?/h1>)',s,1,re.S)))
		title=' '.join(re.sub('<.+?>','',title).split())
		href=urlhome+xsearch('href="./(.+?)"',s,result=xsearch('href="/(.+?)"',s))
		if not title or not href:return
		img=ximg(s)
		year=xsearch(' <div class="year">([^<]+?)</div>',s,1,re.S,result=xsearch('<p>Năm.* (\d+?)</p>',s)).strip()
		if year:title+=' [COLOR gold]%s[/COLOR]'%year
		eps=xsearch('<div class="episode">([^<]+?)</div>',s,1,re.S,result=xsearch('<p>Tập.* (\d.+?)</p>',s)).strip()
		if eps:title+=' [COLOR blue]%s[/COLOR]'%eps
		v=xsearch('<p>View.* (\d+?)</p>',s)
		views=xsearch('<span class="view-left">([^<]+?)</span>',s,1,re.S,result=v).strip()
		if views:title+=' [COLOR orange]%s[/COLOR]'%views
		addir_info(namecolor(title,c),href,img,'',mode,1,'episodes',True)
		
	if query=='anime47.com':
		b=get_home_page('anime47.html',urlhome)
		title=color['search']+"Search trên anime47.com[/COLOR]"
		addir_info(title,'anime47.com',ico,'',mode,1,'search',True)
		title=namecolor('Phân theo Thể loại/Năm Sản Xuất/Lượt xem',c)
		addir_info(title,'menu',ico,'',mode,1,'menu',True)
		href='http://anime47.com/the-loai/cartoon-34/1.html'
		addir_info(namecolor('Cartoon',c),href,ico,'',mode,1,'page',True)
		href='http://anime47.com/tim-nang-cao/?keyword=&nam=&season=&status=complete&sapxep=1'
		addir_info(namecolor('Hoàn thành',c),href,ico,'',mode,1,'page',True)
		href='http://anime47.com/listanime.html'
		addir_info(namecolor('List ANIME',c),href,ico,'',mode,1,'list',True)
		
			
		add_sep_item('-------Phim Đề Cử--------')
		s=xsearch('(<section.+?/section>)',b,1,re.S)
		for s in [i for i in s.split('<div class="item">') if '"big img"' in i]:
			get_item(s)
		
		href='http://anime47.com/danh-sach/phim-moi.html'
		addir_info(namecolor('Phim mới','cyan'),href,ico,'',mode,1,'page',True)
		for s in [i for i in re.findall('(<li.+?/li>)',b,re.S) if '"decaption"' in i]:get_item(s)

		if get_home_page('anime47.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP" or url=="anime47.com":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query:return 'no'
		
		search_string = urllib.quote_plus(query)
		url='http://anime47.com/tim-kiem.php?keyword=%s'%search_string
		try:j=json.loads(xread(url,hd)[4:])
		except:j={}
		print j
		for key in j:
			i=j.get(key,{})
			try:
				title=u2s(i.get('title',''))
				href=i.get('url','')
				img=i.get('img','')
			except:continue
			if not title or not href:continue
			addir_info(namecolor(title,c),href,img,'',mode,1,'episodes',True)

	elif query=="list":
		if page==1:b=xread(url,hd).split('class="content"')[-1];xrw('anime47.txt',b)
		else:b=xrw('anime47.txt')
		items=re.findall('href=/(.+?)>(.+?)<',b)
		rows=len(items);row=25
		if rows>page*row:items=items[(page-1)*row:page*row];next=True
		else:items=items[(page-1)*row:len(items)];next=False
			
		for href,title in items:
			addir_info(namecolor(title.strip(),c),urlhome+href,ico,'',mode,1,'episodes',True)
		
		if next:
			pages=(rows-1)/row+1
			title=namecolor('Trang tiếp theo: trang %d/%d'%(page+1,pages),'lime')
			addir_info(title,url,ico,'',mode,page+1,'list',True)
	
	elif query=="page":
		b=xread(url,hd)
		for s in [i for i in re.findall('(<li.+?/li>)',b,re.S) if '"decaption"' in i]:get_item(s)
		
		s=xsearch('(<div class="pagination".+?/div)',b,1,re.S)
		try:pages=max(int(i) for i in re.findall('/(\d+)\.html',s))
		except:pages=0
		if pages and pages > page:
			title=namecolor('Trang tiếp theo: trang %d/%d'%(page+1,pages),'lime')
			href=re.sub('/\d+\.html','/%d.html'%(page+1),url)
			addir_info(title,href,ico,'',mode,page+1,query,True)
	
	elif query=="menu":
		b=get_home_page('anime47.html',urlhome)
		if url=='menu':
			addir_info(namecolor('Năm Sản Xuất','cyan'),'namsx',ico,'',mode,1,'menu',True)
			addir_info(namecolor('Lượt xem','cyan'),'luotxem',ico,'',mode,1,'menu',True)
			for href,title in re.findall('<li><a href="./(the-loai/.+?)">(.+?)</a>',b):
				addir_info(namecolor(title.strip(),c),urlhome+href,img,'',mode,1,'page',True)
		elif url=='namsx':
			p='<li><a href="(http://anime47.com/tim-nang-cao/\?keyword=&nam.+?)">(.+?)</a>'
			for href,title in re.findall(p,b):
				addir_info(namecolor(title,c),href,img,'',mode,1,'page',True)
		elif url=='luotxem':
			p='<li><a href="(http://anime47.com/danh-sach/.+?)">(.+?)</a>'
			for href,title in re.findall(p,b):
				addir_info(namecolor(title,c),href,img,'',mode,1,'page',True)
	
	elif query=='episodes':
		b=xread(xsearch('<a class="play_info" href="(.+?)"',xread(url,hd)).replace(' ','%20'),hd)
		s=xsearch('(<ul><span class="server".+?/ul>)',b)
		for s in [i for i in s.split('<span class="server">') if '<li>' in i]:
			server=xsearch('<img src=style/icon_server.png>(.+?)<',s).strip()
			if server:add_sep_item('Server: %s ------------'%server)
			for m in re.findall('(<li.+?/li>)',s):
				title=xsearch('title="(.+?)"',m)
				eps=xsearch('data-episode-tap="(.+?)"',m)
				if eps:title='Tập %s %s'%(eps,title)
				if 'class="active"' in m:href=xsearch('link:[^"]*"(.+?)"',b)
				else:href=xsearch('href="(.+?)"',m)
				addir_info(title,href,img,'',mode,1,'play')
	
	elif query=='play':
		if 'anime47.com' in url:
			b=xread(url,hd)
			url=xsearch('link:[^"]*"(.+?)"',b)
		link=''
		if url:
			j=make_post(gkplugins,hd,{'link':url.replace('&','%26')},'j')
			#print j
			l=j.get('link',list)
			if l and isinstance(l, unicode):link=l
			elif l and isinstance(l, list):
				try:L=[(s.get('link'),resolu(s.get('label'))) for s in l]
				except:L=[]
				L=sorted(L, key=lambda k: int(k[1]),reverse=True if myaddon.getSetting('resolut')=='Max' else False)
				for href,label in L:
					link=dl(href)
					if link:break
		if link:xbmcsetResolvedUrl(link)
		elif not link:mess(u'Xin lỗi! Link bạn muốn xem có thể đã bị hỏng')

def phimmedia(name,url,img,mode,page,query):
	ico=os.path.join(iconpath,'phim.png');urlhome='http://www.phim.media/'
	if not os.path.isfile(ico):
		b=make_request('http://www.phim.media/templates/themes/phim/images/phimmedia-s.png')
		if b:makerequest(ico,b,'wb')
	def namecolor(name):return '[COLOR orange]'+name+'[/COLOR]'
	def detail(s):
		href=xhref(s)
		title=xsearch('<div class="name"><a[^<]+?>(.+?)</div>',s,1,re.DOTALL)
		title=' '.join(s for s in re.sub('<[^<]+?>','',title).split())
		name2=' '.join(s for s in xsearch('"name2">([^<]+?)</div>',s,1,re.DOTALL).split())
		if name2:title=title+' - '+name2
		img=ximg(s)
		name3=' '.join(s for s in xsearch('class="status">([^<]+?)</div>',s,1,re.DOTALL).split())
		if name3:title=title+' - [COLOR gold]%s[/COLOR]'%name3
		if re.search('\d/\d',name3):addir_info(namecolor(title),href,img,'',mode,1,'series',True)
		else:addir_info(title,href,img,'',mode,1,'play')
	
	if query=='phim.media':
		body=get_home_page('phimmedia.html',urlhome)
		title=color['search']+"Search trên phim.media[/COLOR]"
		addir_info(title,'phim.media',ico,'',mode,1,'search',True)
		
		addir_info(namecolor('Phim mới'),'http://www.phim.media/phim-moi/',ico,'',mode,1,'page',True)
		for title in re.findall('href="">([^<]+?)<span class="caret"',body):
			addir_info(namecolor(title),'',ico,'',mode,1,'menu1',True)
			
		add_sep_item('----------Movie-hot----------')
		for s in re.findall('(<div class="item">.+?</span></a>)',body,re.DOTALL):detail(s)
		
		S=xsearch('(id="tab_done" class="data-tab">.+?</li>\s*</ul>\s*</div>\s*</div>)',body,1,re.DOTALL)
		for s in re.findall('(<span class="data-tab-wrap-title">.+?</ul>)',S,re.DOTALL):
			label=xsearch('<span class="data-tab-wrap-title">(.+?)</span>',s)
			add_sep_item('----------Mới Hoàn Thành %s----------'%label)
			for j in re.findall('(<li>.+?</li>)',s,re.DOTALL):
				href=xsearch('href="(.+?)"',j)
				title=xsearch('title="(.+?)"',j)
				addir_info(namecolor(title),href,ico,'',mode,1,'series',True)

		top={'id="topviewday"':'Ngày','id="topviewweek"':'Tuần','id="topviewmonth"':'Tháng'}
		tops=('id="topviewday"','id="topviewweek"','id="topviewmonth"')
		for i in tops:
			add_sep_item('----------Top Phim Xem Nhiều: %s----------'%top[i])
			s=xsearch('(%s.+?</ul>)'%i,body,1,re.DOTALL)
			for j in re.findall('(<li>.+?</li>)',s,re.DOTALL):
				href=xsearch('href="(.+?)"',j)
				title=re.sub('<[^"]+?>','',xsearch('>([^"]+?)</p>',j))
				name2=' '.join(s for s in xsearch('<p>([^"]+?)</p>',j).split())
				if name2:title=title+' - '+name2
				addir_info(namecolor(title),href,ico,'',mode,1,'series',True)
		
		
		if get_home_page('phimmedia.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
		mess(u'Các bạn hãy like fanpage: https://www.facebook.com/PhimMedia nhé')  
	
	elif query=="menu1":
		name=re.sub('\[.+?\]','',name)
		body=get_home_page('phimmedia.html',urlhome)
		s=xsearch('(href="">%s<span class="caret".+?</ul>)'%name,body,1,re.DOTALL)
		for href,title in re.findall('<a href="(.+?)">(.+?)</a>',s):
			href=os.path.dirname(href)+'/'+urllib.quote(os.path.basename(href))
			addir_info(namecolor(title),href,ico,'',mode,1,'page',True)
		
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return phimmedia(name,url,img,mode,page,query)
		else:return 'no'
	elif url=="phim.media":
		search_string = urllib.quote_plus(query)
		url='http://www.phim.media/index.php?keyword=%s&do=phim&act=search'%search_string
		return phimmedia(name,url,img,mode,page,'page')
			
	elif query=='page':
		body=make_request(url)
		S=xsearch('(<ul class="list-film">.+?</ul>)',body,1,re.DOTALL)
		for s in re.findall('(<li>.+?</li>)',S,re.DOTALL):detail(s)
		pn=xsearch('<a href="([^<]+?)" class="NextBtn">Next</a>',body)
		if pn:
			pl=xsearch('<a href="([^<]+?)" class="NextBtn">Last</a>',body)
			p01=xsearch('page-(\d+)',pn)
			p02=xsearch('page-(\d+)',pl)
			p02='/'+p02 if p02 else ''
			title=color['trangtiep']+'Page next: %s%s[/COLOR]'%(p01,p02)
			addir_info(title,pn,ico,'',mode,page+1,'page',True)
			
	elif query=='series':
		name=re.sub('\[.+?\]','',name)
		body=make_request(url+'tap-1.html');fanart=''
		if not body:
			body=make_request(url)
			fanart=xsearch('<img alt=[^<]+?src="(.+?)"',body)
			link=xsearch('class="btn-watch" href="(.+?)"',body)
			if not link:return
			body=make_request(link)
		items=re.findall('(<h4>Server.+?</ul>)',body,re.DOTALL);result=False
		for s in items:
			if len(items)>1:add_sep_item('---------- %s ----------'%xsearch('<h4>(.+?)</h4>',s))
			for href,title in re.findall('href="(.+?)" title="(.+?)"',s):
				addir_info(title+' '+name,href,img,fanart,mode,1,'play');result=True
		if not result:#search all server
			return phimmedia(name,xsearch('class="btn-watch" href="([^"]+?)"',body),img,mode,page,'series')
	
	elif query=='play':
		from resources.lib.servers import phimMedia;pmd=phimMedia();link=''
		for href,label in pmd.maxLink(url if url.endswith('.html') else url+'xem-online.html'):
			link=dl(href)
			if link:break
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','phim.media') 

def phimbathu(name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'phimbathu.png');urlhome='http://phimbathu.com/';c='lightgray'
	film_id=xsearch('-(\d+)[.|_]',url)
	if not os.path.isfile(ico):
		href='https://docs.google.com/uc?id=0B5y3DO2sHt1LeVZsMUQxbkUxWk0&export=download'
		response=make_request(href,resp='o',maxr=3)
		if  response.status==200:makerequest(ico,response.body,'wb')
	
	def detail(b):
		s=xsearch('(id="content".+?class="right-content")',b,1,re.DOTALL)
		for i in re.findall('(<li class="item.+?/li>)',s,re.DOTALL):
			title=xsearch('title="(.+?)"',i)
			label=xsearch('class="name-real">(.+?)</span>',i,1,re.DOTALL).replace('<span>','')
			label=' '.join(label.split())
			if label:title=title+' '+label
			label=xsearch('"label">(.+?)<',i)
			if label:title=title+' '+label
			if re.search('.huyết .inh',i):title='[COLOR blue]TM[/COLOR] '+title
			href=xsearch('href="(.+?)"',i)
			if '//' not in href:href='http://phimbathu.com'+href
			img=xsearch('src="(.+?)"',i,result=xsearch('data-original="(.+?)"',i))
			addir_info(namecolor(title,c),href,img,'',mode,1,'eps',True)
		pn=xsearch('<a href="([^<]+?)" class="navigation next"',s)
		if pn:
			pages=xsearch('>(\d+?)</a></li><li><a href="[^<]+?" class="navigation next"',s)
			title=color['trangtiep']+'Page next: %d/%s[/COLOR]'%(page+1,pages)
			addir_info(title,'http://phimbathu.com'+pn,ico,'',mode,page+1,'page',True)

	
	if query=='phimbathu.com':
		b=get_home_page('phimbathu.html',urlhome)
		title=color['search']+"Search trên phimbathu.com[/COLOR]"
		addir_info(title,'phimbathu.com',ico,'',mode,1,'search',True)
		title=color['search']+"Mở chế độ tự động chọn Server trên phimbathu.com[/COLOR]"
		addir_info(title,'phimbathu.com',ico,'',mode,1,'choose-server',True)
		
		s='\n'.join(re.findall('(<li class="menu-item ">.+?</ul>)',b,re.DOTALL))
		for href,title in re.findall('href="([^"]+?)".+</i>(.+?)</a>',s):
			addir_info(namecolor(title,c),'http://phimbathu.com'+href,ico,'',mode,1,'menu',True)
			
		addir_info(namecolor('PHIM QUAN TÂM',c),'http://phimbathu.com/film/AjaxView',ico,'',mode,1,'mostview',True)
		
		S=xsearch('<h2 class="title-box">(.+?End left-content)',b,1,re.DOTALL)
		for s in S.split('<h2 class="title-box">'):
			title=xsearch('>([^<]+?)</a>',s)
			add_sep_item('-------------%s--------------'%title)
			for i in re.findall('(<li.+?/li>)',s,re.DOTALL):
				title=xsearch('title="(.+?)"',i)
				href=xsearch('href="(.+?)"',i)
				if not title or not href:continue
				if '//' not in href:href='http://phimbathu.com'+href
				label=xsearch('"label">(.+?)<',i)
				if label:title=title+' '+label
				if re.search('.huyết .inh',i):title='[COLOR blue]TM[/COLOR] '+title
				img=xsearch('src="(.+?)"',i)
				addir_info(namecolor(title,c),href,img,'',mode,1,'eps',True)
		
		if get_home_page('phimbathu.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")

	elif query=="choose-server":
		label='Chọn chế độ tự động chọn Server trên phimbathu.com'
		choices=['Thuyết minh','Viet Sub','Không Chọn tự động']
		chonserver=["Thuyết minh","VietSub","Không"]
		choice=xselect(label,choices)
		if choice >= 0:
			myaddon.setSetting('chonserver',chonserver[choice])
			mess(u'Đã chọn: %s'%choices[choice].decode('utf-8'))
			xbmc.executebuiltin("Container.Refresh")
		return 'no'
	
	elif query=="menu":
		b=make_request(url)
		s=[i for i in re.findall('(<li class="menu-item ">.+?</ul>)',b,re.DOTALL) if xsearch('</i>(.+?)</a>',i) in name]
		if not s:return
		s=s[0]
		for href,title in re.findall('href="([^"]+?)">([^"]+?)</a>',s):
			addir_info(namecolor(title,c),'http://phimbathu.com'+href,ico,'',mode,1,'page',True)
			
		add_sep_item('--------------------------------------------');detail(b)

	elif query=="page":detail(make_request(url))
	elif query=="mostview":
		if url=='http://phimbathu.com/film/AjaxView':
			href=url+'?type=d'
			url='http://phimbathu.com/film/AjaxView?type=w'
			addir_info(namecolor('PHIM QUAN TÂM TRONG TUẦN',c),url,ico,'',mode,1,'mostview',True)
			url='http://phimbathu.com/film/AjaxView?type=m'
			addir_info(namecolor('PHIM QUAN TÂM TRONG THÁNG',c),url,ico,'',mode,1,'mostview',True)
			add_sep_item('-------------PHIM QUAN TÂM TRONG NGÀY-------------')
		else:href=url
		for i in re.findall('(<li.+?/li>)',make_request(href),re.DOTALL):
			title=xsearch('<span>(.+?)<',i)
			label=xsearch('"count_view">(.+?)<',i)
			if label:title=title+' [COLOR gold]%s[/COLOR]'%label
			if re.search('.huyết .inh',i):title='[COLOR blue]TM[/COLOR] '+title
			href=xsearch('href="(.+?)"',i)
			if '//' not in href:href='http://phimbathu.com'+href
			addir_info(namecolor(title,c),href,ico,'',mode,1,'eps',True)
		
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return phimbathu(name,url,img,fanart,mode,page,query)
		else:return 'no'
	elif url=="phimbathu.com":
		search_string = urllib.quote_plus(query)
		return detail(make_request('http://phimbathu.com/tim-kiem.html?q='+search_string))

	elif query=='eps':#values="Thuyết minh|VietSub|Không" 
		title="Mở chế độ tự động chọn Server trên phimbathu.com"
		menu={'phimbathu':{'name':title,'action':'choose-server','mode':mode}}
		if '/xem-phim/' not in url:
			p='"btn-see btn btn-info adspruce-streamlink" href="(.+?)"'
			url='http://phimbathu.com'+xsearch(p,xread(url))
		b=xread(url)
		name=' '.join(re.sub('phimbathu','',namecolor(name)).split())
		
		if myaddon.getSetting('chonserver')=='Không':
			s=xsearch('(<div class="list-episode".+?/div)',b,1,re.S)
			if s:
				for href,title in re.findall('href="(.+?)">(.+?)<',s):
					addir_info('Tập %s %s'%(title,name),href,img,'',mode,1,'server',True,menu=menu)
			else:addir_info(name,url,img,'',mode,1,'server',True,menu=menu)
		
		else:
			s=xsearch('(<div class="list-episode".+?/div)',b,1,re.S)
			if s:
				for href,title in re.findall('href="(.+?)">(.+?)<',s):
					addir_info('Tập %s %s'%(title,name),href,img,'',mode,1,'play',menu=menu)
			else:addir_info(name,url,img,'',mode,1,'play',menu=menu)
	
	elif query=='server':
		b=xread(url)
		server=xsearch('<ul class="choose-server">(.+?)</ul>',b,1,re.S)
		if server:
			for href,title in re.findall('<a href="([^"]+?)".*?>([^<]+?)</a>',server):
				if '//' not in href:href='http://phimbathu.com'+href
				title=namecolor(title,'gold')+' '+namecolor(re.sub('\+|TM|Vietsub|Thuyết minh','',name))
				addir_info(title,href,img,'',mode,1,'play')
		else:addir_info(name,url,img,'',mode,1,'play')
	
	elif query=='play':
		from resources.lib.servers import phimBatHu;pbh=phimBatHu()
		xbmcsetResolvedUrl(pbh.getDirectLink(url))

def phim14(name,url,img,fanart,mode,page,query,text):
	ico=os.path.join(iconpath,'phim14.png');urlhome='http://phim14.net/';c='chartreuse'
	#hd['Cookie']='location.href=1'
	if not os.path.isfile(ico):
		b=xread('https://docs.google.com/uc?id=0B5y3DO2sHt1LZnkyYXQ4ckZaeDA&export=download')
		if b:makerequest(ico,b,'wb')
	
	def p14_page(url):
		from resources.lib.servers import phim14com;p14=phim14com(c)
		b=xread(url)
		s=xsearch('(<ul class="list-film tab".+?/ul>)',b,1,re.S)
		for s in re.findall('(<li.+?/li>)',s,re.S):itemDIR(s)
		
		s=xsearch('(<div class="navpage".+?/div>)',b)
		pn=xsearch('<span class="current">\d+</span><span class="item"><a href="(.+?)"',b)
		if pn:
			pl=xsearch('<span class="current">.+<a href=".+?">(\d+)</a>',b)
			title=namecolor('Page next: %d/%s'%(page+1,pl),'lime')
			addir_info(title,pn,ico,'',mode,page+1,query,True)
	
	def itemDIR(s):
		title=re.findall('(<div class="title.+?</div>)',s,re.S)
		title=' - '.join(re.sub('<.+?>','',i) for i in title)
		if not title:
			title=xtitle(s)
			if not title:
				title=re.findall('(class="name.+?</div>)',s,re.S)
				title=' - '.join(re.sub('<.+?>','','<'+i) for i in title)
		href=xhref(s)
		if not href or not title:return
		img=ximg(s)
		p='(<span.+?/span>|<div class="stat.+?/div>|<dd>.+?</dd>)'
		label=set([re.sub('<.+?>|\s+|,',' ',i).strip() for i in re.findall(p,s,re.S)])
		label=' '.join(' '.join(i for i in label).split())
		if re.search('.huyết .inh|TM',label):title='[COLOR gold]TM[/COLOR] '+title
		title='%s [COLOR green]%s[/COLOR]'%(namecolor(title,c),label)
		addir_info(s2c(title),href,img,'',mode,1,'p14_eps',True)
	
	def eps_server(s):
		name=xsearch('property="og:title" content="(.+?)"',s)
		label=re.sub('<.+?>','',xsearch('(<strong.+?/strong>)',s))
		label='List of Server '+label.replace('Download','Server').replace(':','')
		add_sep_item('[COLOR lime]-------'+label+'-------[/COLOR]')
		for m in re.findall('(<li.+?/li>)',s,re.S):
			title='[COLOR cyan]%s[/COLOR] %s'%(xsearch('href=.+?>(.+?)</a>',m),name)
			title=title.replace('Download','')
			href=xhref(m);id=xsearch('id="(.+?)"',m)
			if 'daily' in label.lower():p='playDaily'
			elif 'youtube' in label.lower():p='playYoutube'
			elif 'fshare' in label.lower():p='playFshare'
			else:p='play'
			addir_info(title,href,img,'',mode,1,p)
	
	if query=='phim14.net':
		b=getHome('phim14.html',urlhome)
		title=color['search']+"Search trên phim14.net[/COLOR]"
		addir_info(title,'phim14.net',ico,'',mode,1,'search',True)
		
		for s in re.findall('(<li class="child">.+?/ul>)',b,re.S):
			for i in re.findall('(<li class="child">.+?</a>)',s):
				title=re.sub('<.+?>','',i)
				if 'class="sub-menu"' not in s:
					href=xsearch('href="(.+?)"',i)
					addir_info(namecolor(title,c),href,ico,'',mode,1,'p14_page',True)
				else:addir_info(namecolor(title,c),s,ico,'',mode,1,'sub-menu',True)
		
		addir_info(namecolor('Drama','cyan'),'',ico,'',mode,1,'drama',True)
		addir_info(namecolor('Kênh Hay','cyan'),'',ico,'',mode,1,'kenhhay',True)
		
		add_sep_item('----------------------------')
		addir_info(namecolor('Phim HOT','gold'),'',ico,'',mode,1,'hot',True)
		addir_info(namecolor('Phim Bộ mới','gold'),'',ico,'',mode,1,'bomoi',True)
		addir_info(namecolor('Phim mới cập nhật','gold'),'',ico,'',mode,1,'moicapnhat',True)
		
		for s in re.findall('(<div class="blockbody blockrow list_02.+?/ul)',b,re.S):
			tab='Ngày' if 'topviewday' in s else 'Tuần' if 'topviewweek' in s else 'Tháng'
			add_sep_item('-------Top %s--------'%tab)
			for s in s.split('<li>'):
				href=xhref(s)
				img=xsearch('href="%s".+?(src=".+?")'%href,b,result='src="%s"'%ico)
				itemDIR(s+' '+img)
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="phim14.net" or query=="INP":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			page=1
		search_string = urllib.quote_plus(query)
		p14_page('http://phim14.net/search/%s.html'%search_string)
	
	elif query=='drama':
		s=xsearch('<a href="#">Drama</a>(.+?/ul>)',xrw('phim14.html'),1,re.S)
		for href,title in re.findall('<a href="([^"]+?)">([^<]+?)</a>',s):
			addir_info(namecolor(title,c),href,ico,'',mode,1,'p14_page',True)
	
	elif query=='kenhhay':
		s=xsearch('<a href="#">Kênh Hay</a>(.+?/ul>)',xrw('phim14.html'),1,re.S)
		for href,title in re.findall('<a href="([^"]+?)">([^<]+?)</a>',s):
			addir_info(namecolor(title,c),href,ico,'',mode,1,'p14_page',True)
	
	elif query=='moicapnhat':
		b=xrw('phim14.html')
		s=xsearch('(<ul class="list-film tab toan-bo".+?/ul>)',b,1,re.S)
		for s in re.findall('(<li.+?/li>)',s,re.S):itemDIR(s)
	
	elif query=='bomoi':
		b=xrw('phim14.html')
		s=re.findall('(class="blockbody blockrow link_film list_01".+?/ul>)',b,re.S)
		add_sep_item('-------Đang cập nhật--------')
		m=''.join(i for i in s if '"dang-cap-nhat"' in i)
		for n in re.findall('(<li.+?/li>)',m,re.S):itemDIR(n)
		add_sep_item('-------Phim Đã Hoàn Thành--------')
		m=''.join(i for i in s if '"da-hoan-thanh"' in i)
		for n in re.findall('(<li.+?/li>)',m,re.S):itemDIR(n)
	
	elif query=='hot':
		b=xrw('phim14.html')
		s=xsearch('(<ul class="overview".+?/ul>)',b,1,re.S)
		for s in re.findall('(<li.+?/li>)',s,re.S):itemDIR(s)
	
	elif query=='sub-menu':
		for href,title in re.findall('<a href="(.+?)".*?>(.+?)</a>',url):
			addir_info(namecolor(title,c),href,ico,'',mode,1,'p14_page',True)
	
	elif query=='p14_page':p14_page(url)
	
	elif query=='phimlienquan':
		for s in re.findall('(<li.+?/li>)',url,re.S):itemDIR(s)
	
	elif query=='p14_eps':
		if '/xem-phim/' not in url:
			b=xread(url)
			href=xsearch('<a class="watch_button now" href="(.+?)"',b)
			if href:b=xread(href)
		else:b=xread(url)
		
		img=xsearch('<meta property="og:image" content="(.+?)"',b)
		p='(<div class="block".+?/ul>)'
		phimlienquan=''.join(i for i in re.findall(p,b,re.S) if 'Phim liên quan' in i)
		lienquan='Mục các phim liên quan'
		
		s=re.findall('(<li class="server_item">.+?</ul>)',b,re.S)
		title=xsearch('(property="og:title" content=".+?")',b)
		s=[title+' '+i for i in s]
		lenEPS=len(re.findall('(</li>)',''.join(s)))
		if lenEPS > 10:
			if phimlienquan:
				title=namecolor(lienquan,'gold')
				addir_info(title,phimlienquan,img,'',mode,1,'phimlienquan',True)
			
			default=s[0]
			submenu=len(s)>1
			for s in s:
				title=re.sub('<.+?>','',xsearch('(<strong.+?/strong>)',s))
				title='Server '+title.replace('Download','Server').replace(':','')
				if 'Thuyết Minh' in title:default=s
				elif submenu:addir_info(namecolor(title,'gold'),s,img,'',mode,1,'eps_server',True)
			eps_server(default)
		
		else:
			for s in s:eps_server(s)
			s=re.findall('(<li.+?/li>)',phimlienquan,re.S)
			if s:
				add_sep_item('[COLOR gold]-------'+lienquan+'-------[/COLOR]')
				for s in s:itemDIR(s)
	
	elif query=='eps_server':eps_server(url)
	
	elif query=='play':
		from resources.lib.servers import phim14com;p14=phim14com(c)
		xbmcsetResolvedUrl(p14.getLink(url))
	
	elif query=='playYoutube':
		from resources.lib.servers import phim14com;p14=phim14com(c)
		link=p14.getYoutube(url)
		if 'youtube.com' in link:link=youtubeDL(link)
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','phim14.net')
	
	elif query=='playDaily':
		from resources.lib.servers import phim14com;p14=phim14com(c)
		link=p14.getDaily(url)
		if 'dailymotion.com' in link:link=youtubeDL(link)
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','phim14.net')
	
	elif query=='playFshare':
		b=xread(url);link=''
		href=xsearch('<a.+?href="(.+?)">Download here</a>',b)
		resolve_url(href)

def hdsieunhanh(name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'hdsieunhanh.png')
	urlhome='http://www.hdsieunhanh.com/';c='orangered'
	if not os.path.isfile(ico):
		try:makerequest(ico,get('http://hdsieunhanh.com/assets/img/layout/logo.png',headers=hd).body,'wb')
		except:pass
	hd={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/54.0.2840.99 Safari/537.36',
		'Cookie':xrw('hdsieunhanh.cookie')}
	
	def menu(s):
		for href,title in re.findall('<a href="([^"]+?)">.?<span class="tnico[^"]+?"></span>([^<]+?)</a>',s):
			href='menu' if 'javascript' in href else urlhome+href;title=title.strip()
			addir_info(namecolor(title,c),href,ico,'',mode,1,'page',True)
	
	def banner(s):
		add_sep_item('-----Nổi Bật-----')
		s=xsearch('(<div id="banner">.+?<a href="/phim-hot.html">)',s)
		for i in s.split('"titinfo"'):
			href=xsearch('href="([^"]+?)"',i)
			if not 'phim-' in href:continue
			title=xsearch('(<span class=.tt_bold.>.+?class="nivo-caption-des">)',i)
			title=' '.join(re.sub('<[^<]+?>','',title).split())
			img=xsearch('href="%s"><img[^<]+?src="(.+?)"'%href,s).replace('amp;','')
			if 'Thời lượng' in title:dir=False;query='play'
			else:dir=True;query='eps';title=namecolor(title,c)
			addir_info(title,href,img,img,mode,page,query,dir)
	
	def home_detail(s):
		s=s.split('<div class="group-title-bg">')
		s=[i for i in s if 'class="viewmore"' in i or 'class="action"' in i]
		def dirHome(s):
			i=sn.item(s)
			if i:addir_info(i[0],i[1],i[2],'',mode,page,'eps' if i[3] else 'play',i[3])
		for s in s:
			i=re.search('<a href="([^"]+?)">([^<]+?)</a>',s)
			if i:
				href=i.group(1)
				href='' if 'javascript' in href else urlhome+href if 'http' not in href else href
				title=namecolor('%s (click to expand)-----'%i.group(2),'lime')
				addir_info(title,href,ico,'',mode,1,'page',True)
			for s in re.findall('(<li.+?/li>)',xsearch('(<ul.+?/ul>)',s)):
				m=s.split('<div class="block-base movie clearfix">')
				if m:[dirHome(i) for i in m if 'href=' in i]
				else:dirHome(s)
	
	from resources.lib.servers import sieunhanh;sn=sieunhanh()
	if query=='hdsieunhanh.com':
		if filetime('hdsieunhanh.html') > 1:
			b=xreadc(urlhome,hd)
			xrw('hdsieunhanh.html',b)
			xrw('hdsieunhanh.cookie',b.split('xshare')[1])
		else:b=xrw('hdsieunhanh.html')
			
		title=color['search']+"Search trên hdsieunhanh.com[/COLOR]"
		addir_info(title,'hdsieunhanh.com',ico,'',mode,1,'search',True)
		
		menu(b);banner(b);home_detail(b)
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="hdsieunhanh.com" or query=="INP":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query:return 'No'
		for title,href,img,dir in sn.search(query):
			addir_info(title,href,img.replace('amp;',''),'',mode,1,'eps' if dir else 'play',dir)

	elif url=='menu':
		#b=get_home_page('hdsieunhanh.html',urlhome)
		b=xread(urlhome)
		i=[('THỂ LOẠI','the-loai'),('QUỐC GIA','quoc-gia'),('NĂM PHÁT HÀNH','nam-phat-hanh')]
		j=''.join(m[1] for m in i if m[0] in name)
		for href,title in re.findall('<a[^<]+?href="(/%s/[^"]+?)"[^<]*?>([^<]+?)</a>'%j,b):
			addir_info(namecolor(title,c),urlhome+href,ico,'',mode,1,'page',True)
		
	elif query=='page':
		for title,href,img,dir in sn.page(url):
			img=img.replace('amp;','')
			if img!='image':addir_info(title,href,img,'',mode,page,'eps' if dir else 'play',dir)
			else:addir_info(title.replace('page',str(page+1)),href,ico,'',mode,page,'page',True)
			
	elif query=='eps':
		i=[('Tập %s %s'%(j[1],namecolor(name)),j[0]) for j in sn.eps(url)]
		if not i:i=[(namecolor(name),url)]
		for title,href in i:addir_info(title,href,img,fanart,mode,page,'play')
		
	elif query=='play':
		link=sn.maxLink(url)
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','hdsieunhanh.com') 

def tvhay(name,url,img,mode,page,query):
	ico=os.path.join(iconpath,'tvhay.png');urlhome='http://tvhay.org/';c='gold'
	if not os.path.isfile(ico):
		href='https://docs.google.com/uc?id=0B5y3DO2sHt1LcmxSUm8yZ0dram8&export=download'
		response=make_request(href,resp='o',maxr=3)
		if  response.status==200:makerequest(ico,response.body,'wb')
	
	def tvh_page(url):
		b=xread('%spage/%d'%(url,page)) if url.startswith('http') else url
		for s in re.findall('(<div class="inner">.+?</li>)',b,re.DOTALL):itemDIR(s)
		
		href=xsearch('<a class="last" href="(.+?)">',b)
		if href:
			pages=xsearch('/(\d+)/',href)
			title=color['trangtiep']+'Page next: %d/%s[/COLOR]'%(page+1,pages)
			addir_info(title,url,ico,'',mode,page+1,'tvh_page',True)
	
	def itemDIR(s,items=[]):
		title=xsearch('title="(.+?)"><span',s,result=xtitle(s))
		href=xhref(s);img=xsearch('src=".+?url=(.+?)"',s)
		if not title or not href:return
		label=re.split('<.+?>|Xem phim',s)
		label=' '.join(re.sub('.huyết .inh|.ồng .iếng','',i) for i in label if i.strip() not in title)
		label=' '.join(label.split())
		title=title.replace('Xem Phim ','')+' [COLOR green]%s[/COLOR]'%label
		if re.search('.huyết .inh',s):title='[COLOR cyan]TM[/COLOR] '+title
		elif re.search('.ồng .iếng',s):title='[COLOR cyan]LT[/COLOR] '+title
		if not img:
			s=[i[1] for i in items if i[0]==href]
			if s:img=s[0]
			else:img=ico
		addir_info(namecolor(title,c),href,img,'',mode,1,'eps',True)
	
	def eps_server(s):
		title='Server '+xsearch('<div class="label">(.+?)</div>',s).replace(':','')
		add_sep_item('List of Server %s -------------------------'%title)
		label=xsearch('<title>(.+?)</title>',s)
		for href,title in re.findall('<a.+?href="(.+?)">(.+?)</a>',s):
			title=s2c('[COLOR cyan]%s[/COLOR] %s'%(title,label))
			addir_info(title,href,img,'',mode,1,'play')
	
	hd={'User-Agent':'Mozilla/5.0'}
	if filetime('tvhay.cookie') > 10:
		b=xreadc('http://tvhay.org/gkplayer/tvt.php',hd)
		if b.split('xshare')[1]:hd['Cookie']=xrw('tvhay.cookie',b.split('xshare')[1])
		else:hd['Cookie']=xrw('tvhay.cookie')
	else:hd['Cookie']=xrw('tvhay.cookie')
	
	if query=='tvhay.org':
		hd['Cookie']=hd['Cookie']+'; _isBlogspot=true'
		b=xrw('tvhay.html',xread(url,hd)) if filetime('tvhay.html') > 10 else xrw('tvhay.html')
		if b and 'xshare' in b and not b.split('xshare')[1]:b+=hd['Cookie']
		elif b and 'xshare' not in b:b+='xshare%s'%hd['Cookie']
		elif not b:b=xreadc('http://tvhay.org');xrw('tvhay.html',b)
		
		title=color['search']+"Search trên tvhay.org[/COLOR]"
		addir_info(title,'tvhay.org',ico,'',mode,1,'search',True)
		
		title=namecolor('Phim được xem nhiều',c)
		addir_info(title,'',ico,'',mode,1,'xemnhieu',True)
		
		s=xsearch('(<div id="nav".+?id="content">)',b,1,re.S)
		def abc(i):return ('type-custom' in i or 'type-post' in i) and 'item-16' not in i
		for s in [i for i in re.findall('(<li.+?/h3>)',s,re.S) if abc(i)]:
			s=xsearch('(<a.+?/a>)',s)
			href=xhref(s);title=re.sub('<.+?>','',s)
			if href:addir_info(namecolor(title,c),href,ico,'',mode,1,'tvh_page',True)
			else:addir_info(namecolor(title,c),'',ico,'',mode,1,'tvh_submenu',True)
		
		add_sep_item('---------TVHAY đề cử---------')
		s=xsearch('(<ul class="listfilm overview".+?/ul>)',b,1,re.S)
		for s in re.findall('(<li.+?/li>)',s,re.S):itemDIR(s)
		
		add_sep_item('---------TVHAY giới thiệu---------')
		s=xsearch('(<div class="blockbody".+?/ul>)',b,1,re.S)
		for s in re.findall('(<li.+?/li>)',s,re.S):itemDIR(s)
		
		add_sep_item('---------Phim Đã hoàn thành---------')
		s=xsearch('(<ul class="list tab phim-bo-full.+?/ul>)',b,1,re.S)
		for s in re.findall('(<li.+?/li>)',s,re.S):itemDIR(s)
	
	elif query=='eps_server':eps_server(url)
	elif query=='tvh_page':tvh_page(url)
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP" or url=="tvhay.org":
		if query=="INP":query=make_mySearch('',url,'','','','Input')
		if not query.strip():return
		page=1
		tvh_page('http://tvhay.org/search/%s/'%urllib.quote_plus(query))

	elif query=='tvh_submenu':
		name=namecolor(name)
		b=getHome('tvhay.html','http://tvhay.org')
		s=xsearch('(<div id="nav">.+?id="content">)',b,1,re.S)
		s=''.join(i for i in re.findall('(<h3.+?/ul>)',s,re.S) if name in i)
		for href,title in re.findall('<a href="(.+?)">(.+?)</a>',s,re.S):
			addir_info(namecolor(title,c),href,ico,'',mode,1,'tvh_page',True)
	
	elif query=='xemnhieu':
		b=getHome('tvhay.html','http://tvhay.org')
		items=re.findall('<a href="(.+?)".+?url=(.+?\.jpg)".+?/a>',b)
		s=xsearch('(id="topview".+?class="block">)',b,1,re.S)
		for s in re.findall('(<ul.+?/ul>)',s,re.S):
			label=xsearch('class="tab (\w+)',s)
			add_sep_item('---------%s---------'%label)
			for s in re.findall('(<li>.+?</li>)',s,re.S):itemDIR(s,items)
		
	elif query=='eps':
		b=xread(url,hd)
		title=xsearch('<title>(.+?)</title>',b).replace('|','-').replace('Phim','')
		title=' '.join(title.split())
		s=xsearch('(<div class="info".+?/div>)',b,1,re.S)
		img=xsearch('src=".+?url=(.+?)"',s,result=img)
		
		b=xread(xsearch('href="([^<]+?)" class="btn-watch"',b),hd)
		s=xsearch('(<div id="servers".+?id="comment">)',b,1,re.S)
		lenEPS=s.count('data-episode-id')
		
		s=re.findall('(<div class="server".+?/ul>)',s,re.S)
		s=['<title>%s</title> %s'%(title,i) for i in s]
		SRVS=len(s)>1
			
		if lenEPS > 25:
			default=s[0]
			for s in s:
				title='Server '+xsearch('<div class="label">(.+?)</div>',s).replace(':','')
				if 'Thuyết Minh' in title:default=s
				elif SRVS:addir_info(namecolor(title,'gold'),s,img,'',mode,1,'eps_server',True)
			eps_server(default)
		else:[eps_server(s) for s in s]
	
	elif query=='play':
		from resources.lib.servers import tvhay;tvh=tvhay()
		link=tvh.getLink(url,hd)
		if link:xbmcsetResolvedUrl(link)
		else:mess('Sorry. Chưa get được link. Hãy thử lại nhé ...','tvhay.org') 

def television(name,url,img,fanart,mode,page,query,text):
	fptlive_ico=icon['fptplay'];c='orange'
	hplus_ico='http://static.hplus.com.vn/themes/front/images/logo_hplus.png';hplus='http://hplus.com.vn/'
	xemtvhd_ico='http://xemtvhd.com/logo/xemtvhd.png';xemtvhd='http://www.xemtvhd.com/'
	vtvgo_ico=os.path.join(iconpath,'vtvgo.png')
	hd['x-requested-with']='XMLHttpRequest';hd['referer']=''
	def fixs(string):return ' '.join(re.sub('&.+;',xsearch('&(\w).+;',s),s) for s in string.split())
	
	if query=='Home':#http://www.iptvsat.com/2016/09/bestiptvsport.html?m=1
		#data=urllib2.base64.b64decode('ZW1haWw9eHNoYXJlQHRoYW5odGhhaS5uZXQmcGFzc3dkPXhzaGFyZWFkZG9u')
		#o=make_post('http://hplus.com.vn/user/login/',data=data)
		#hd['Cookie']=o.cookiestring
		addir_info(namecolor('Lịch Phát Sóng','gold'),'1',fptlive_ico,'',7,1,'fptSchedule',True)
		addir_info(namecolor('Truyền hình FPTplay.net',c),'',fptlive_ico,'',mode,1,'fptlive',True)
		if fptisp():
			title='Truyền hình FPT IPTV'
			addir_info(namecolor(title,c),'',fptlive_ico,'',mode,1,'fptiptv',True)
			addir_info(namecolor(title+' BlogCongDong.Com',c),'',fptlive_ico,'',mode,1,'fptiptv0',True)
		
		addir_info(namecolor('List IPTV của Thanh Dương - Cộng Đồng KODI Việt Nam','hotpink'),'http://textuploader.com/5bls5/raw',fptlive_ico,'',mode,1,'thanhduong',True)
		addir_info(namecolor('List IPTV của Văn Hiếu BMT - Cộng Đồng KODI Việt Nam','chartreuse'),'http://textuploader.com/d53tf/raw',fptlive_ico,'',mode,1,'thanhduong',True)
		art=os.path.join(iconpath,'iptv.png')
		if not os.path.isfile(art):
			makerequest(art,xread('http://www.m3uliste.pw/files/iptv.png'),'wb')
		if myaddon.getSetting('listIPTV').split(',')[0]:
			title='List Truyền hình IPTV trên [COLOR orange]textuploader.com[/COLOR] của người dùng'
			addir_info(namecolor(title,'cyan'),'',icon['icon'],art,mode,1,'userList',True)
		
		title=namecolor('[B]IPTV M3U Stream Hunters[/B]','cyan')
		img=os.path.join(iconpath,'m3uliste.png')
		if not os.path.isfile(img):
			makerequest(img,xread('http://www.m3uliste.pw/files/.logo-lw-scaled.jpg.png'),'wb')
		addir_info(title,'http://www.m3uliste.pw/',img,art,mode,1,'hunters',True)
		
		addir_info(namecolor('Truyền hình VTVGo.vn','turquoise'),'Home',vtvgo_ico,'',56,1,'Home',True)
		b=make_request('http://hplus.com.vn/ti-vi-truc-tuyen/kenh-htv',headers=hd,resp='o')
		if b:cookie=b.cookiestring;b=b.body
		else:cookie=''
		s=xsearch('("dropdown-menu sub-left".+?</ul>)',b,1,re.DOTALL).replace('\n','')
		for href,title in re.findall('<a href="(.+?)">(.+?)</a>',s):
			title=namecolor(fixs(title.strip()),c)+' - [COLOR green](H+)[/COLOR]'
			addir_info(title,href,hplus_ico,'',mode,1,'hplus',True)
		
		#addir_info(namecolor('Truyền hình XemTVHD.com',c),xemtvhd,xemtvhd_ico,'',mode,1,'xemtvhd',True)
		add_sep_item('---------------KÊNH HTV trên Hplus (H+)----------------')
		for s in re.findall('(class="panel".+?</div>\s*</div>)',b,re.DOTALL):
			href=hplus+xhref(s)
			img=ximg(s)
			title=xsearch('<a href="[^<]+?">(.+?)</a>',s)
			addir_info(namecolor(fixs(title.strip()),c),href,img,'',mode,1,'hplus_play',text=cookie)
	
	elif query=='thanhduong':
		py=getHome('thanhduong.py','http://textuploader.com/5bls5/raw')
		try:execfile(os.path.join(xsharefolder,'iptvlist.py'))
		except:pass
	elif query=='hunters':
		def makeList(s):
			for href in [i for i in re.findall('>(http:.+?)<',s) if 'get.php' in i]:
				href=href.replace('&amp;','&')
				addir_info(namecolor(href,'cyan'),href,img,fanart,mode,1,'userList',True)
		def getDate(s):return re.sub('<[^<]+?>','',xsearch('>Update(.+?)</font>',s)).strip()
		
		if not url.startswith('http') and len(url)>20:
			for i in eval(url):
				addir_info(namecolor(i,'orange'),i,img,fanart,mode,1,'hunters',True)
			return
		elif not url.startswith('http'):
			b=xrw('hunters.txt')
			makeList(''.join([s for s in b.split('xshare') if getDate(s)==url]))
		else:
			b=getHome('hunters.html',url)
			items=re.findall('(>Update .+?</font></p></div>)',b,re.S)
			if not items:return
			day=re.sub('<[^<]+?>','',xsearch('>Update(.+?)</font>',items[0])).strip()
			dates=[i for i in [getDate(s) for s in items] if i and i!=day]
			if len(dates)>1:
				xrw('hunters.txt','\nxshare\n'.join(items))
				title=namecolor('List các ngày khác','orangered')
				addir_info(title,str(dates),img,fanart,mode,2,'hunters',True)
			if day:add_sep_item('List Update Ngày %s ---------------------------'%day)
			makeList(items[0])
		
	elif query=='userList':
		py=getHome('iptvlist.py','http://textuploader.com/d56fz/raw')
		try:execfile(os.path.join(xsharefolder,'iptvlist.py'))
		except:pass
	
	elif query=='listGroup':
		py=getHome('iptvlistgroup.py','http://textuploader.com/d56p2/raw')
		try:execfile(os.path.join(xsharefolder,'iptvlistgroup.py'))
		except:pass
	
	elif query=='F4mProxy':#http://textuploader.com/5euky/raw
		if not url:
			b=xread('http://textuploader.com/d5oqv/raw')
			for s in re.findall('(<item.+?/item>)',b,re.S):
				title=xsearch('<title>(.+?)</title>',s)
				href=xsearch('<link>(.+?)</link>',s)
				img=xsearch('<img>(.+?)</img>',s)
				addir_info(namecolor(title,'cyan'),href,img,'',mode,1,'F4mProxy')
		else:
			try:from F4mProxy import f4mProxyHelper
			except:
				xbmcplugin.setResolvedUrl(int(sys.argv[1]), False, xbmcgui.ListItem())
				s=u'Để mở được link này bạn phải cài đặt module '
				mess(s+'[COLOR cyan]script.video.F4mProxy[/COLOR]!',timeShown=20000)
				return
			player=f4mProxyHelper()
			qsl=urllib2.urlparse.parse_qsl
			p=dict(qsl(url.split('?')[-1]))
			url=p.get('url','')
			streamtype=p.get('streamtype','')
			player.playF4mLink(url,name,streamtype=streamtype,iconImage=img)
			#xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
			#player.playF4mLink('http://5.39.70.216/live/louis/louis/1031.ts','K+1 HD',streamtype='TSDOWNLOADER',iconImage='')
	
	elif query=='xemtvhd':
		body=get_home_page('xemtvhd.html',url)
		b=make_request(url)
		
		for s in re.findall("(<h2 class='title'>.+?</ul>)",b,re.DOTALL):
			label=xsearch("<h2 class='title'>(.+?)</h2>",s)
			add_sep_item('----------------%s----------------'%label)
			for i in re.findall('(<a.+?/a>)',s,re.DOTALL):
				href=xsearch("href='(.+?)'",i)
				#title=xsearch("alt='(.+?)'",i).replace('Kênh ','').replace(' Online','')
				img=xsearch("src='(.+?)'",i)
				title=xsearch('/([^/]+?).png',img).upper()
				addir_info(namecolor(title,c),href,img,'',mode,1,'xemtvhd_play')
		
		if checkupdate('xemtvhd.html',240,xsharefolder):
			response=make_request(url,hd,resp='o')
			if response:
				endxbmc();makerequest(joinpath(xsharefolder,'xemtvhd.html'),response.body,'w')
				xbmc.executebuiltin("Container.Refresh")
		
	elif query=='xemtvhd_play':
		b=make_request(url)#;f=open(r'd:\xoa.html','w');f.write(b);f.close()
		s=xsearch('(<div id="server">.+?</div>)',b,1,re.DOTALL);print s
		link=''
		for href in re.findall('href="(.+?)"',s):
			while href and not link:
				print 'href0: '+href
				b=make_request(href)
				href=[h for h in re.findall('src=[\'|\"](http.+?)[\'|\"]',b) if '.php' in h]
				if href:href=href[0];print 'href1: '+href
				else:link=xsearch('"(http.+?m3u8)"',b);print 'link:'+link,href
				if link and make_request(link):break
			print 'link..............'+link
		if link:xbmcsetResolvedUrl(link)#+'|Referer='+href)
		else:mess('Get channel link fail!') 

	elif query=='xemtvhd_play':
		name=namecolor(name).replace('HD','').lower()
		b=make_request('http://vps.tivi12h.net/vtv-go.php?id='+name)
		link=xsearch("file\": '(.+?)'",b)
		if link:xbmcsetResolvedUrl(link)
		else:mess('Get channel link fail!') 
		
	elif query=='hplus':
		b=make_request(url,headers=hd,resp='o')
		if b:cookie=b.cookiestring;b=b.body
		else:cookie=''
		for s in re.findall('(class="panel".+?</div>\s*</div>)',b,re.DOTALL):
			href=hplus+xhref(s)
			img=ximg(s)
			title=xsearch('<a href="[^<]+?">(.+?)</a>',s)
			addir_info(namecolor(fixs(title.strip()),c),href,img,'',mode,1,'hplus_play',text=cookie)
	
	elif query=='fptiptv0':
		href='http://textuploader.com/d5oi3/raw'
		for title,href in re.findall('#EXTINF:0, (.+).\s(.+).',xread(href)):
			addir_info(namecolor(title,'orange'),href,img,'',mode,1,'fptiptvPlay')
	
	elif query=='fptiptv1':
		from resources.lib.servers import fptPlay;fpt=fptPlay()
		if not url:url='https://jobdecor.vn/IPTV/FPT/MenuFPT.xml'
		for i in fpt.fptNodes(url):
			title,href,img=namecolor(i.get('title',''),c),i.get('link','').replace('amp;',''),i.get('thumbnail','')
			try:
				if os.path.splitext(href)[-1].upper()=='.XML':addir_info(u2s(title),href,img,'',mode,1,'fptiptv',True)
				elif 'rtmp' in href or 'udp:' in href:addir_info(u2s(title),href,img,'',mode,1,'fptiptvPlay')
			except:print href;pass
		
	elif query=='fptiptv':
		from resources.lib.servers import fptPlay;fpt=fptPlay()
		#if not url:url='https://jobdecor.vn/IPTV/FPT/MenuFPT.xml'
		if not url:url='http://textuploader.com/d5oes/raw'
		for i in fpt.fptNodes(url):
			title,href,img=namecolor(i.get('title',''),c),i.get('link','').replace('amp;',''),i.get('thumbnail','')
			try:
				if 'textuploader.com' in href:addir_info(u2s(title),href,img,'',mode,1,query,True)
				elif 'rtmp' in href or 'udp:' in href:addir_info(u2s(title),href,img,'',mode,1,'fptiptvPlay')
			except:pass
		
	elif query=='fptlive':fptplay('','https://fptplay.net/livetv','','',7,page,'category')
	elif query=='fptiptvPlay':xbmcsetResolvedUrl(url)
	
	elif query=='hplus_play':
		hd['Cookie']=text;hd['referer']=url
		b=make_request(url,headers=hd)
		link=xsearch('id="link-live" type="hidden" value="(.+?)"',b)
		data={'url':link,'type':'1'}
		link=post('http://hplus.com.vn/content/getlinkvideo/',data=data,headers=hd).body
		print data,link
		xbmcsetResolvedUrl(link)

def addir_info(name,url,img,fanart='',mode=0,page=1,query='',isFolder=False,
	text='',info={},art={},menu={}):
	def get_mode(url,name,mode,query,isfolder=True):
		if 'fshare.vn/' in url and '/files/' not in url:
			id=xsearch('(\w{10,20})',url)
			if '/file/' in url:
				url='https://www.fshare.vn/file/%s'%id.upper()
				name='%sFshare[/COLOR] %s'%(color['fshare'],name);mode=3;isfolder=False
			else:
				url='https://www.fshare.vn/folder/%s'%id.upper()
				name='%sFshare %s[/COLOR]'%(color['fshare'],name);mode=90
		elif 'tenlua.vn/' in url:
			id=xsearch('(\w{10,20})',url)
			if 'folder/' in url or '#download' in url:
				url='https://tenlua.vn/fm/folder/%s'%id
				name='%sTenlua %s[/COLOR]'%(color['tenlua'],name);mode=95
			else:
				url='https://tenlua.vn/download/%s'%id
				name='%sTenlua[/COLOR] %s'%(color['tenlua'],name);mode=3;isfolder=False
		elif '4share.vn/d/' in url:name='%s4share %s[/COLOR]'%(color['4share'],name);mode=38
		elif '4share.vn/f/' in url:
			name='%s4share[/COLOR] %s'%(color['4share'],name);mode=3;isfolder=False
		elif 'subscene.com/' in url:name='%ssubscene[/COLOR] %s'%(color['subscene'],name);mode=94
		elif 'phudeviet.org' in url and mode!=94:
			name='[COLOR cyan]Sub trên phudeviet.org[/COLOR]';mode=94;isfolder=True
		elif 'vaphim.com/' in url:name='%s%s[/COLOR]'%(color['vaphim'],name);mode=1
		elif 'phimfshare.com/' in url:name='%s%s[/COLOR]'%(color['vaphim'],name);mode=6
		elif 'hdvietnam.com' in url:name='%sHDVN[/COLOR] %s'%(color['hdvietnam'],name);mode=8
		elif 'taiphimhd.com' in url:name='%sTPHD[/COLOR] %s'%(color['taiphimhd'],name);mode=53
		elif 'youtube.com' in url:
			if 'watch?' in url or '/embed' in url:isfolder=False
			elif mode !=98 and mode !=1:query= 'channel'
			if mode !=98:name='[COLOR red]YT[/COLOR] %s'%(name);mode=98 if mode !=1 else mode
		return u2s(name),url,mode,query,isfolder
	
	def get_menu(menu,url):
		lists=list()
		if menu.has_key('MyFshare'):
			inf=menu.get('MyFshare')
			if [s for s in inf['server'] if s in url] and inf['action']=='Add':
				lists.append(('Add to MyFshare',{'query':'Add','mode':11}))
				lists.append(('Add to MyFshare Favorite',{'query':'AddFavorite','mode':11}))
				lists.append(('Add item name to string search',{'query':'Add','mode':13}))
			if [s for s in inf['server'] if s in url] and inf['action']=='Remove':
				lists.append(('Rename in MyFshare',{'query':'Rename','mode':11}))
				lists.append(('Remove from MyFshare',{'query':'Remove','mode':11}))
				lists.append(('Remove from MyFshare Favorite',{'query':'RemoveFavorite','mode':11}))
		
		if menu.has_key('MySearch'):
			inf=menu.get('MySearch')
			lists.append(('Rename item',{'url':inf.get('url',''),'query':'Rename','mode':9}))
			lists.append(('Remove item',{'url':inf.get('url',''),'query':'Remove','mode':9}))
		
		if menu.has_key('MyPlaylist'):
			inf=menu.get('MyPlaylist')
			if inf['action']=='Search':#cs:artist, sag tac:composer, ten alb:album, loi:lyric
				lists.append(('Tìm kiếm theo: Tên bài hát/Ca sĩ',{'query':'csn_Search_None'}))
				lists.append(('Tìm kiếm theo: Ca sĩ',{'query':'csn_Search_artist'}))
				lists.append(('Tìm kiếm theo: Sáng tác',{'query':'csn_Search_composer'}))
				lists.append(('Tìm kiếm theo: Tên Album',{'query':'csn_Search_album'}))
				lists.append(('Tìm kiếm theo: Lời bài hát',{'query':'csn_Search_lyric'}))
			elif [s for s in inf['server'] if s in url] and inf['action']=='Add':
				lists.append(('Add to My Playlist',{'query':'playlist_Add'}))
			elif [s for s in inf['server'] if s in url] and inf['action']=='Remove':
				lists.append(('Remove from My Playlist',{'query':'playlist_Remove'}))
				lists.append(('Remove all from My Playlist',{'query':'playlist_RemoveAll'}))
		elif menu.has_key('bookmark'):
			inf=menu.get('bookmark')
			if inf['action']=='Add':
				lists.append(('Thêm vào Hộp phim',{'query':'add_bookmark'}))
			elif inf['action']=='Remove':
				lists.append(('Xóa khỏi Hộp phim',{'query':'remove_bookmark'}))
		elif menu.has_key('hdonline'):
			inf=menu.get('hdonline')
			if inf['action']=='Add':
				lists.append(('Thêm vào Mục Yêu thích',{'query':'Add'}))
			elif inf['action']=='Remove':
				lists.append(('Xóa khỏi Mục Yêu thích',{'query':'Remove'}))
		elif menu.has_key('xshare'):
			inf=menu.get('xshare')
			if inf['action']=='Add':
				lists.append(('Thêm vào Mục Yêu thích',{'query':'Add'}))
			elif inf['action']=='Remove':
				lists.append(('Xóa khỏi Mục Yêu thích',{'query':'Remove'}))
		elif menu.has_key('myFavourites'):
			inf=menu.get('myFavourites')
			if 'Add' in inf['action']:
				lists.append(('Add to My Favourites',{'query':inf['action'],'mode':100+mode}))
			elif 'Remove' in inf['action']:
				lists.append(('Remove from My Favourites',{'query':inf['action'],'mode':101}))
		
		if menu.has_key('fcine'):
			inf=menu.get('fcine')
			if inf.get('action','')=='fcinefshare':
				#menu={'fcine':{'name':title,'action':'fcinefshare','mode':mode}}
				lists.append((inf['name'],{'query':'fcinefshare','mode':inf['mode']}))
		
		elif menu.has_key('servers_list'):
			inf=menu.get('servers_list')
			if 'Up' in inf['action']:
				lists.append(('MoveUp',{'url':url,'mode':88,'query':'Up'}))
			if 'Down' in inf['action']:
				lists.append(('MoveDown',{'url':url,'mode':88,'query':'Down'}))
			if 'ShowHide' in inf['action']:
				lists.append(('Hide this item',{'name':'HideXshareMainMenuItem','page':mode,}))
				lists.append(('Show all free Servers items',{'name':'HideXshareMainMenuItem','page':0}))
		
		elif menu.has_key('phimbathu'):
			#menu={'phimbathu':{'name':title,'action':'choose-server','mode':mode}}
			inf=menu.get('phimbathu')
			lists.append((inf['name'],{'query':inf['action'],'mode':inf['mode']}))
			
		elif menu.has_key('youtube'):
		#menu={'youtube':{'name':'Open this PlayList','action':'playlist','url':playlistId,'mode':mode}}
			inf=menu.get('youtube')
			if 'playlist' in inf['action']:
				lists.append((inf['name'],{'url':inf['url'],'query':'playlist','mode':inf['mode']}))
		
		return lists
	
	def add_menu(url):
		menu['MyFshare']={'action':'Add','server':['fshare.vn']}
		return menu
		
	if '18+' in name and phim18=="false":return
	server_mode=['fshare.vn','4share.vn','tenlua.vn','subscene.com','vaphim.com','phimfshare.com','hdvietnam.com','youtube.com','phudeviet.org'];li='plugin://plugin.video.xshare?'
	if mode not in [2,13] and [s for s in server_mode if s in url]:name,url,mode,query,isFolder=get_mode(url,name,mode,query)
	
	item=xbmcgui.ListItem(label=name,iconImage=img,thumbnailImage=img)
	if not fanart:
		fn=joinpath(home,'fanart.jpg')
		if os.path.isfile(fn):fanart=fn
	if not art:art={"fanart":fanart}
	item.setArt(art)
	if not isFolder:
		if query!='F4mProxy':item.setProperty('IsPlayable', 'true')
		item.setInfo(type="video",infoLabels=info)

	q={'name':name,'url':url,'img':img,'fanart':fanart,'mode':mode,'page':page,'query':query,'text':text}
	li+=urllib.urlencode(q)
	
	if not menu:menu=add_menu(url)
	if not menu.get('myFavourites'):
		menu['myFavourites']={'action':'Add-'+query+'-'+('F' if isFolder else ''),'mode':100+mode}
	menu=get_menu(menu,url)
	
	if menu:
		cmd='RunPlugin(plugin://'+myaddon.getAddonInfo('id')+'?%s)';items=list()
		for label,info in menu:#menu=[(label,{'query':x,...})]
			if info.has_key('name'):name=info.get('name')
			if info.get('url'):url=info.get('url')
			if info.has_key('img'):img=info.get('img')
			if info.has_key('fanart'):fanart=info.get('fanart')
			if info.has_key('mode'):mode=info.get('mode')
			if info.has_key('page'):page=info.get('page')
			query=info.get('query','')
			
			q={'name':name,'url':url,'img':img,'fanart':fanart,'mode':mode,'page':page,'query':query}
			command=cmd%urllib.urlencode(q)
			
			if 'Remove' in query:label='[COLOR red]%s[/COLOR]'%label
			else:label='[COLOR lime]%s[/COLOR]'%label
			items.append((label,command))
		
		item.addContextMenuItems(items)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),li,item,isFolder)

def myFavourites(name,url,img,fanart,mode,page,query):
	from resources.lib.servers import fshare;lib_imported=True
	fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'))
	if query=='Home':
		mess('myFavourites loading...','myFavourites')
		for i in fs.myFavourites_loads(page):
			if i=='Trang tiếp theo ...':
				href='https://www.fshare.vn/home/xshare_favourite?pageIndex=%d'%(page+1)
				addir_info(namecolor(i,'lime'),'',icon['xshare'],'',mode,page+1,query,True)
			else:
				try:title,href,img,fanart,m,p,q,folder,ids=i.split(',')
				except:continue
				folder=True if folder else False
				menu={'myFavourites':{'action':'Remove-%s'%ids}}
				addir_info(title,href,img,fanart,int(m),int(p),q,folder,menu=menu)
	
	elif 'Add' in query:
		mess('myFavourites adding...','myFavourites')
		mode=mode-100;q=query.split('-');folder='1' if q[2] else '';query=q[1]
		s='%s,%s,%s,%s,%d,%d,%s,%s'%(name,url,img,fanart,mode,page,query,folder)
		if fs.myFavourites_add(s):mess('Add a item to MyFavourites success')
		else:mess('Add a item to MyFavourites Fail!')
	
	elif 'Remove' in query:
		mess('myFavourites removing...','myFavourites')
		if fs.myFavourites_remove(query.replace('Remove-','')):
			mess('Remove a item from MyFavourites success')
			xbmc.executebuiltin("Container.Refresh")
		else:mess('Remove a item from MyFavourites Fail!')
	if fs.logged:fs.logout()

def imax(name,url,img,fanart,mode,page,query):
	def sc(s):
		if 'fshare' in s:n=color['fshare']+'FS[/COLOR] '
		elif '4share' in s:n=color['4share']+'4S[/COLOR] '
		elif 'tenlua' in s:n=color['tenlua']+'TL[/COLOR] '
		elif 'subscene' in s:n=color['subscene']+'SUB[/COLOR] '
		return n
		
	ico=os.path.join(iconpath,'imax.png');urlhome='http://i-max.vn/';c='chartreuse'
	if not os.path.isfile(ico):
		try:makerequest(ico,xread('https://lh3.googleusercontent.com/YQxZANBnYMTFC1DTlBlmQnfRWUUzL0j2LCbf1VQzLOfi53UH9HChEIrrAmdL6_u7KPSC=s170'),'wb')
		except:pass

	from resources.lib.servers import iMax;imx=iMax(c)
	if query=='imax.vn':
		b=xread('https://i-max.vn/forum/index.php')
		title=color['search']+"Search trên imax.vn[/COLOR]"
		addir_info(title,'imax.vn',ico,'',mode,1,'search',True)
		
		s=xsearch('(id="highqualitybox".+?/ul>)',b,1,re.S)
		href=urllib2.base64.b64encode(json.dumps(re.findall('<a href="(.+?)">(.+?)</a>',s)))
		addir_info(namecolor('High Quality Box',c),href,ico,'',mode,1,'menu',True)
		
		s=xsearch('(id="normalbox".+?/ul>)',b,1,re.S)
		href=urllib2.base64.b64encode(json.dumps(re.findall('<a href="(.+?)">(.+?)</a>',s)))
		addir_info(namecolor('Normal Quality Box',c),href,ico,'',mode,1,'menu',True)
		add_sep_item('[COLOR gold]Bài viết mới[/COLOR]-----------------------------')

		items=re.findall('(<td width="33%" align="left"><div class.+?/td>)',b)
		try:s=items[1]+items[2]
		except:s=''
		for label,href,title in re.findall("<a title='(.+?)' href='(.+?)'>(.+?)</a>",s):
			title=title+' [COLOR green]%s[/COLOR]'%label
			href='https://i-max.vn/forum/'+href
			addir_info(namecolor(s2c(title),c),href,ico,'',mode,1,'thread',True)
	
	elif query=='menu':
		for href,title in json.loads(urllib2.base64.b64decode(url)):
			addir_info(namecolor(title,c),href,ico,'',mode,1,'category',True)
		
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="imax.vn" or query=="INP":#009789051051551375973:id317tow93q
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query:return 'No'
		href='https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&'
		href+='rsz=filtered_cse&num=20&hl=en&prettyPrint=false&source=gcsc&gss=.com&'
		href+='cx=009789051051551375973:id317tow93q&googlehost=www.google.com&'
		href+='callback=google.search.Search.apiary19044&q=%s'%urllib.quote_plus('"%s"'%' '.join(query.split()))
		
		if 'Page next:' in name:href+='&start=%d'%((page-1)*20)
		else:page=1
		
		items=imx.search(href)
		for title,href,img,q in items:
			if 'Page next:' in title:addir_info(title,url,ico,'',mode,page+1,query,True)
			else:addir_info(namecolor(remove_tag(title),c),href,img,'',mode,1,q,True)

	elif query=='thread':
		for title,href,i in imx.thread(url):
			if not href:add_sep_item('[COLOR gold]%s[/COLOR]-----------------------------'%i);continue
			elif not title:title=namecolor(re.sub('\[.+\] ','',name));i=img
			else:title=namecolor(title,c)
			if 'http' not in href:href='http://i-max.vn/forum/'+href
			addir_info(title,correct_link(href),i,'',mode,1,query,True)
		
	elif query=='category':
		for title,href,i in imx.category(url):
			if not namecolor(title).strip() or not href:continue
			elif i=='pagenext' or not i:i=img;q=query
			else:q='thread';href='http://i-max.vn/forum/showthread.php?t=%s&page=1000'%xsearch('t=(\d+)',href)
			
			addir_info(namecolor(title,c),href,i,'',mode,1,q,True)
	
	elif query=='forum':
		for title,href,i in imx.category(url):
			if not namecolor(title).strip() or not href:continue
			elif i=='pagenext' or not i:i=img;q=query
			else:q='thread';href='http://i-max.vn/forum/showthread.php?t=%s&page=1000'%xsearch('t=(\d+)',href)
			
			addir_info(namecolor(title,c),href,i,'',mode,1,q,True)

def taiphimhd(name,url,img,fanart,mode,page,query):#RSS
	ico=os.path.join(iconpath,'taiphimhd.png');urlhome='http://taiphimhd.com/';c='blue'
	if not os.path.isfile(ico):
		try:makerequest(ico,get('http://taiphimhd.com/styles/default/xenforo/logo.og.png',headers=hd).body,'wb')
		except:pass

	from resources.lib.servers import taiphim;taiphim=taiphim(c)
	if query=='taiphimhd.com':
		title=color['search']+"Search trên taiphimhd.com[/COLOR]"
		addir_info(title,'taiphimhd.com',ico,'',mode,1,'search',True)
		
		addir_info(namecolor('Mục Thảo luận mới nhất',c),'http://taiphimhd.com/find-new/posts',ico,'',mode,1,'list',True)
		
		addir_info(namecolor('Mục Xem gì hôm nay',c),urlhome+'forums/xem-gi-hom-nay.18/',ico,'',mode,1,'list',True)
		items=[('Xem gì hôm nay',urlhome+'forums/xem-gi-hom-nay.18/'+'index.rss')]
		
		b=get_home_page('taiphimhd.html',urlhome)
		a=[i for i in re.findall('<h3 class="nodeTitle"><a href="(.+?)"[^<]+>(.+?)</a></h3>',b) if [j for j in ['Phim','Show','Phụ đề'] if j in i[1]] and 'Yêu cầu' not in i[1]]
		for href,title in a:
			addir_info(namecolor('Mục '+title,c),urlhome+href,ico,'',mode,1,'list',True)
			items.append((title,urlhome+href+'index.rss'))
		
		if get_home_page('taiphimhd.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
		
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="taiphimhd.com" or query=="INP":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query:return 'No'
		query=urllib.quote('+'.join(query.split()))
		for title,href,img in taiphim.search(query):
			#print u2s(title),u2s(href),u2s(img)
			addir_info(namecolor(remove_tag(title),c),href,img,'',mode,1,'page',True)

	elif query=='list':
		for title,href,img in taiphim.getLists(url):
			if img=='ico' and page==1:img=ico;q='list'
			elif img=='ico':continue
			elif img=='next':
				img=ico;q=query;page=page+1
				name=re.sub('\[COLOR %s.+/COLOR\]'%color['trangtiep'],'',name)
				title=name+color['trangtiep']+' Trang tiep theo...trang %d/%s[/COLOR]'%(page,title)
			else:q='page'
			addir_info(title,href,ico if not img else img,'',mode,page,q,True)
	
	elif query=='page':
		for title,href,img in taiphim.getPage(url):
			if title=='name':add_sep_item('--%s--'%namecolor(name));continue
			elif title=='--Có thể bạn muốn xem--':add_sep_item(title);continue
			elif not href:continue
			addir_info(title,href,img,'',mode,page,'page',True)
	
	elif query=='rss':
		b=taiphim.getRSS(url)

def imovies(name,url,img,fanart,mode,page,query):
	def fixURL(l):
		if not l.startswith('http'):l='http://imovies.vn'+l
		return l
	
	def itemDIR(s):
		title=xsearch('<span class="ti">(.+?)</span>',s,result=xsearch('<h4>(.+?)</h4>',s))
		label=xsearch('<span class="na">(.+?)</span>',s,result=xsearch('<h3>(.+?)</h3>',s))
		if not title:title=xtitle(s,p='alt="(.+?)"').replace('Xem phim ','')
		else:title='%s - %s'%(title,label)
		href=fixURL(xhref(s))
		if not title or not href:return
		label=[re.sub('<.+?>','',i).strip() for i in re.findall('(<span.+?/span>)',s)]
		label=' '.join(i for i in label if i not in title)
		title=s2c('%s [COLOR green]%s[/COLOR]'%(title,label))
		img=fixURL(ximg(s))
		fanart=xsearch('data-src="(.+?)"',s)
		addir_info(title,href,img,fanart,mode,1,'eps',True)
		
	def dirs(item):
		if not item:return
		title,href,img,fanart,dir=item
		if 'Page next:' in title:addir_info(title,href,img,fanart,mode,1,'ajaxPage',True)
		elif 'Trang tiếp' in title:addir_info(title,href,img,fanart,mode,1,'htmlPage',True)
		elif dir=='add_sep_item':add_sep_item(title)
		elif dir=='page':addir_info(title,href,ico,fanart,mode,1,'page',True)
		elif dir:addir_info(title,href,img,fanart,mode,1,'eps',True)
		else:addir_info(title,href,img,fanart,mode,1,'play')
	
	def dirs_1(b):
		for s in ['<h2>'+i for i in b.split('<h2 class="prl-d">') if 'class="mvli"' in i]:
			i=xsearch('<h2>(.+?)</h2>',s,1,re.S)
			add_sep_item('%s ---------------------'%' '.join(re.sub('<.+?>','',i).split()))
			href=xhref(i)
			if href:
				title=namecolor(xtitle(i),'orangered')
				addir_info(title,'http://imovies.vn'+href,ico,'',mode,1,'subpage',True)
			for i in re.findall('(<div class="mt".+?/a>)',s,re.S):itemDIR(i)#dirs(imv.getElement(i))
	
	def subpage(url):
		b=xread(url)
		if 'Ooops.Đã Có lỗi xảy ra!' in b:mess(u'Ooops.Đã Có lỗi xảy ra!','imovies.vn');return
		elif 'class="mo-block"' in b:
			for s in re.findall('(<div class="mo-block".+?/ul>)',b,re.S):
				add_sep_item(' '.join(re.sub('<.+?>','',xsearch('(<h3.+?/h3>)',s,1,re.S)).split()))
				for i in re.findall('(<li.+?/li>)',s,re.S):dirs(imv.getElement(i))
		elif '<h2 class="prl-d">' in b:dirs_1(b)
	
	ico=os.path.join(iconpath,'imovies.png');urlhome='http://imovies.vn/';c='orange'
	if not os.path.isfile(ico):
		try:makerequest(ico,xread('http://imovies.vn/Images/imovies_v3_1.png'),'wb')
		except:pass
	
	from resources.lib.servers import imovies;imv=imovies(c)
	if query=='imovies.vn':
		b=getHome('imovies.html',urlhome)
		title=color['search']+"Search trên imovies.vn[/COLOR]"
		addir_info(title,'imovies.vn',ico,'',mode,1,'search',True)
		"""
		s='<ul class="nl d-i-b clearfix">'
		s=''.join(i for i in b.split('<div class="c-full') if s in i)
		s=re.findall('href="(.+?)" title="(.+?)"',s)
		m=("Phim lẻ","Phim Bộ","Thể Loại","Quốc Gia")
		for href,title in [i for i in s if i[1] in m]:
			if title=="Phim Bộ":
				addir_info(namecolor(title,c),fixURL(href),ico,'',mode,1,'imv_page',True)
			else:addir_info(namecolor(title,c),'',ico,'',mode,1,'subMenu',True)
		"""
		s=xsearch('<a href="/phim-le" title="Phim lẻ">Phim Lẻ</a>(.+?)</ul>',b,1,re.S)
		href=str(re.findall('<a href="(.+?)" title=".+?">(.+?)</a>',s))
		addir_info(namecolor('Phim Lẻ',c),href,ico,'',mode,1,'mainMenu',True)
		
		addir_info(namecolor('Phim Bộ',c),[],ico,'',mode,1,'mainMenu',True)
		
		s=xsearch('<a href="#" title="Thể Loại">Thể Loại</a>(.+?)</ul>',b,1,re.S)
		href=str(re.findall('<a href="(.+?)" title=".+?">(.+?)</a>',s))
		addir_info(namecolor('Thể Loại',c),href,ico,'',mode,1,'mainMenu',True)
		
		s=xsearch('<a href="#" title="Quốc Gia">Quốc Gia</a>(.+?)</ul>',b,1,re.S)
		href=str(re.findall('<a href="(.+?)" title=".+?">(.+?)</a>',s))
		addir_info(namecolor('Quốc Gia',c),href,ico,'',mode,1,'mainMenu',True)
		
		add_sep_item('Imovies giới thiệu ---------------------')
		s=xsearch('(id="topsli".+?class="ali")',b,1,re.S)
		for s in [i for i in s.split('<div class="sli ps-r">') if '"ps-a sli-d"' in i]:
			itemDIR(s)
		
		dirs_1(b)
	
	elif query=="subMenu":
		b=getHome('imovies.html',urlhome)
		name=namecolor(name)
		s='<ul class="nl d-i-b clearfix">'
		s=''.join(i for i in b.split('<div class="c-full') if s in i)
		s=''.join(i for i in re.findall('(<li.+?/ul>)',s,re.S) if name in i)
		items=re.findall('<a href="(.+?)" title=".+?">(.+?)</a>',s)
		for href,title in items:
			if title=='Phim Bộ' or href=='#':continue
			addir_info(namecolor(s2c(title),c),fixURL(href),ico,'',mode,1,'imv_page',True)
			
		
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="imovies.vn" or query=="INP":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query:return 'No'
			page=1
		url='http://imovies.vn/tim-kiem.html?key='+urllib.quote_plus(query)
		for item in imv.htmlPage(url,2):dirs(item)

	elif query=='mainMenu':
		items=eval(url)
		if 'Phim Lẻ' in name:
			for href,title in items:
				title=namecolor(title+' (phim lẻ)',c)
				addir_info(title,'http://imovies.vn'+href,ico,'',mode,1,'page',True)
			for item in imv.htmlPage('http://imovies.vn/phim-le',1):dirs(item)
		elif 'Phim Bộ' in name:
			for item in imv.htmlPage('http://imovies.vn/phim-bo',1):dirs(item)
		else:
			for href,title in items:
				title=namecolor(s2c(title),c)
				addir_info(title,'http://imovies.vn'+href,ico,'',mode,1,'ajaxPage',True)
	
	elif query=='page':
		phimleCat={'phim-sap-chieu':5,'phim-3d':6,'phim-full-hd':7,'phim-chieu-rap':8}
		category={'hanh-dong':1,'hai':2,'khoa-hoc-vien-tuong':4,'hoat-hinh':5,'ma-kinh-di':9}
		if 'bang-xep-hang' in url and 'phim lẻ' in name:
			for item in imv.ajaxPage('http://imovies.vn/MasterGroup/GetTop?id=1','Hit'):dirs(item)
		elif 'bang-xep-hang' in url and 'phim bộ' in name:
			for item in imv.ajaxPage('http://imovies.vn/MasterGroup/GetTop?id=2','Hit'):dirs(item)
		
		elif [i for i in phimleCat.keys() if i in url]:
			id=phimleCat.get([i for i in phimleCat.keys() if i in url][0])
			url='http://imovies.vn/Movie/Search?&pageSize=25&groupId=1&pageIndex=1&cateId=%d'%id
			for item in imv.ajaxPage(url):dirs(item)
		
		elif [i for i in category.keys() if i in url]:
			id=category.get([i for i in category.keys() if i in url][0]);mess('qqqq')
			url='http://imovies.vn/Movie/Search?pageIndex=1&pageSize=25&groupId=%d'%id
			for item in imv.ajaxPage(url):dirs(item)
		
		elif 'quoc-gia' in url:
			ids={'han-quoc':7,'dai-loan':16,'hong-kong':4,'trung-quoc':3,'nhat-ban':5,'viet-nam':0,'an-do':6,'nga':17,'canada':19,'phap':10,'my':1,'au-my':21,'chau-a-khac':22,'thai-lan':11,'au':2}
			id=''.join(str(ids.get(i,'')) for i in ids if '/%s?'%i in url)
			url='http://imovies.vn/Movie/Search?pageIndex=1&pageSize=25&countryId=%s'%id
			for item in imv.ajaxPage(url):dirs(item)
		
		elif url=='http://imovies.vn/the-loai/tam-ly?CategoryId=4':
			url='http://imovies.vn/Movie/Search?pageIndex=1&pageSize=25&groupId=40'
			for item in imv.ajaxPage(url):dirs(item)
		
		elif url=='http://imovies.vn/tim-kiem.html?CategoryId=4':
			for item in imv.htmlPage(url,2):dirs(item)
		
		elif 'tim-kiem' in url:
			url='http://imovies.vn/tim-kiem.html?pageIndex=1&CategoryId=2'
			for item in imv.htmlPage(url,2):dirs(item)
				
		else:mess('Chua xu ly')
	
	elif query=='htmlPage':
		for item in imv.htmlPage(url,2):dirs(item)
	
	elif query=='ajaxPage':#$.ajax
		if 'groupId' not in url and 'countryId' not in url and not 'cateId' in url:
			try:ids=eval(xrw('imovies.json'))
			except:ids={}
			id=ids.get(url.rsplit('/',1)[1])
			if not id:
				b=xread(url)
				id=xsearch('groupId *= *(\d+)',b)
				if id:
					ids[url.rsplit('/',1)[1]]=id
					xrw('imovies.json',str(ids))
			if id and '/the-loai/' in url:
				url='http://imovies.vn/Movie/Search?pageSize=25&pageIndex=1&groupId='+id
			elif id and '/quoc-gia/' in url:
				url='http://imovies.vn/Movie/Search?pageSize=25&pageIndex=1&countryId='+id
			else:mess('GroupID not found !');return
		
		for item in imv.ajaxPage(url):dirs(item)
	
	elif query=='subpage':subpage(url)
	elif query=='eps':
		b=xread(url)
		name=s2c(xsearch('<title>(.+?)</title>',b).replace('Xem phim ',''))
		items=re.findall('class=.prm. href="(.+?)" title=".+?">(.+?)</a>',b,re.S)
		if not items:addir_info(name,url,img,fanart,mode,1,'play')
		for href,epi in items:
			if 'http' not in href:href='http://imovies.vn'+href
			epi=' '.join(epi.split())
			addir_info(epi+' '+name,href,img,fanart,mode,1,'play')

	elif query=='play':
		if ('/video/' in url or 'wobo.vn' in url):
			b=xread(url)
			id=xsearch("loadVideoById\('(.+?)'\)",b)
			return play_youtube(id)
			
		link,sub=imv.maxLink(url)
		if link and 'youtube.com' in link:play_youtube(link)
		elif link:xbmcsetResolvedUrl(link,sub=sub)
		else:xbmcplugin.setResolvedUrl(int(sys.argv[1]), False, xbmcgui.ListItem())

def vietsubhd(name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'vietsubhd.png');urlhome='http://www.vietsubhd.com/';c='springgreen'
	if not os.path.isfile(ico):
		try:makerequest(ico,xread('https://lh3.googleusercontent.com/-dQlfS9xn87g/VZlzVLNxjZI/AAAAAAAADi4/V_HB-F9rGYg/s126/logo.png'),'wb')
		except:pass
	
	def vsh_page(url):
		b=xread(url);items=[]
		if '/videos' in url:p='(<span class="video.+?/a>)'
		else:p='(<a class="poster".+?/div>)'

		for s in re.findall(p,b,re.S):itemDIR(s)
				
		pn=xsearch('class="current".+?<a href="([^"]+?)"[^<]*?>\d+<',b)
		if pn:
			pages=xsearch('-(\d+)\.html" title="Trang cuối">',b)
			title=namecolor('Page next: %d/%s'%(page+1,pages),'lime')
			addir_info(title,pn,ico,'',mode,page+1,query,True)
	
	def itemDIR(s):
		title=xsearch('title="(.+?)"',s)
		href=xsearch('href="(.+?)"',s)
		label=' '.join(i for i in re.split('<.+?>',s) if i and i not in title)
		if re.search('.huyết .inh|TM',label):title='[COLOR gold]TM[/COLOR] '+title
		title+=' [COLOR green]%s[/COLOR]'%' '.join(label.split())
		img=xsearch('url=([^<]+jpg)',s)
		img=img.replace('w35-h35','w180-h240').replace('Poster.','')
		if '/phim-sap-chieu/' in url or '/xem-video/' in href:
			addir_info(title,href,img,'',mode,1,'youtube')
		else:addir_info(title,href,img,'',mode,1,'eps',True)
	
	def itemSRV(name,server,filmID,s):
		label=re.sub('<.+?>','',xsearch('(<i class="fa fa-database"></i>.+?</div>)',s))
		add_sep_item('Server '+label+' ------------------')
		label=label.lower()
		for href,episodeID,title in re.findall('<a href="(.+?)".+?id="(.+?)".+?>(.+?)</a>',s):
			if 'zing' in server:q='zingPlay'
			elif 'youtube' in label:q='youtubePlay'
			else:q='play'
			addir_info(title+' '+name,'filmID=%s&EpisodeID=%s'%(filmID,episodeID),img,'',mode,1,q)
	
	def epsServer(server):
		s=xrw('vietsubhd.txt')
		filmID=xsearch('filmid="(.+?)"',s)
		name=xsearch('title="(.+?)"',s)
		servers=re.findall('(<div class="name.+?/ul>)',s)
		s=''.join(i for i in servers if server in i)
		itemSRV(name,server,filmID,s)
	
	if query=='vietsubhd.com':
		title=color['search']+"Search trên vietsubhd.com[/COLOR]"
		addir_info(title,'vietsubhd.com',ico,'',mode,1,'search',True)
		
		b=xread(urlhome);ec=urllib2.base64.b64encode
		for s in [i for i in b.split('<li class="item">') if '<head>' not in i]:
			title=xsearch('>([^<]+?)</a>',s)
			if 'hot' in title:href='http://www.vietsubhd.com/phim-hot/';q='page';s=''
			elif 'Shows' in title:href='http://www.vietsubhd.com/phim-tvshows/';q='page';s=''
			elif 'Anime' in title:href='http://www.vietsubhd.com/phim-anime/';q='page';s=''
			else:href='';q='menu'
			if 'http' not in href:href=urlhome+href
			addir_info(namecolor(title,c),'',ico,'',mode,1,q,True,text=ec(s))
			
		add_sep_item('------------PHIM HAY NHẤT------------')
		s=xsearch('(<div class="block-body slider">.+?<div class="block-foot">)',b,1,re.S)
		for s in re.findall('(<a class="poster".+?/a>)',s):itemDIR(s)
	
		add_sep_item('------------PHIM LẺ MỚI------------')
		s=xread('http://www.vietsubhd.com/ajaxload',data='loadfilm=1&idTab=%23phimlemoi')
		for s in re.findall('(<li.+?/li>)',s):itemDIR(s)
	
		add_sep_item('------------PHIM BỘ MỚI------------')
		s=xread('http://www.vietsubhd.com/ajaxload',data='loadfilm=1&idTab=%23phimbomoi')
		for s in re.findall('(<li.+?/li>)',s):itemDIR(s)
	
		add_sep_item('------------PHIM BỘ FULL------------')
		s=xread('http://www.vietsubhd.com/ajaxload',data='loadfilm=1&idTab=%23phimbofull')
		for s in re.findall('(<li.+?/li>)',s):itemDIR(s)
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="vietsubhd.com" or query=="INP":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			page=1
			if not query:return 'No'
		vsh_page('http://www.vietsubhd.com/tim-kiem/%s/'%urllib.quote_plus(query))

	elif query=='menu':
		b=urllib2.base64.b64decode(text)
		#if 'Thể loại' in name:
		for href,title in re.findall('<a href="(.+?)" title="(.+?)"',b):
			if 'http' not in href:href=urlhome+href
			addir_info(namecolor(title,c),href,ico,'',mode,1,'page',True)
			
	elif query=='page':
		if not url and 'Phim hot' in name:url='http://www.vietsubhd.com/phim-hot/'
		elif not url and 'TV Shows' in name:url='http://www.vietsubhd.com/phim-tvshows/'
		elif not url and 'Anime Vietsub' in name:url='http://www.vietsubhd.com/phim-anime/'
		
		vsh_page(url)
		
	elif query=='epsServer':epsServer(url)
	
	elif query=='eps':
		if 'xem-phim.html' not in url:url+='xem-phim.html'
		b=xread(url)
		filmID=xsearch('filmid="(.+?)"',b)
		label=xsearch('title="(.+?)">Xem thêm</a>',b)
		name=label if label else namecolor(name)
		s=xsearch('<div class="block servers">(.+?)<div class="block comment">',b,1,re.S)
		servers=re.findall('(<div class="name.+?/ul>)',s)
		if len(re.findall('(</a>)',b)) > 25 and len(servers) > 1:
			default_s=servers[0];default_server=''
			xrw('vietsubhd.txt','filmid="%s" title="%s" '%(filmID,name)+s)
			for s in servers:
				server=re.sub('<.+?>','',xsearch('(<i class="fa fa-database"></i>.+?</div>)',s))
				if 'class="active"' in s:default_server=server;default_s=s
				else:
					try:eps=[int(i) for i in re.findall('>(\d+)</a>',s)]
					except:eps=re.findall('>([^>]+?)</a>',s)
					try:title=namecolor('Server %s (%s-%s)'%(server,min(eps),max(eps)),'gold')
					except:title=namecolor('Server %s'%server,'gold')
					addir_info(title,server,img,'',mode,1,'epsServer',True)
			
			itemSRV(name,default_server,filmID,default_s)
		else:
			for s in servers:
				server=re.sub('<.+?>','',xsearch('(<i class="fa fa-database"></i>.+?</div>)',s))
				itemSRV(name,server,filmID,s)

				
	elif query=='youtube':
		if 'youtube.com' not in url:b=xread(url);yt=xsearch('"([^"]+youtube.com[^"]+)"',b)
		else:yt=url
		if yt:return play_youtube(xsearch('([\w|-]{10,20})',yt))
	
	elif query=='youtubePlay':
		from resources.lib.servers import vietsubhd;vsh=vietsubhd(c)
		link=vsh.getYoutube(url)
		if link:play_youtube(link)
		else:mess('File invalid or deleted!','vietsubhd.com') 
	
	elif query=='zingPlay':
		from resources.lib.servers import vietsubhd;vsh=vietsubhd(c)
		link=vsh.getZing(url)
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','vietsubhd.com') 
	
	elif query=='play':
		from resources.lib.servers import vietsubhd;vsh=vietsubhd(c)
		link=vsh.getLink(url)
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','vietsubhd.com') 

def mphim (name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'mphim.png');urlhome='http://mphim.net/';c='deepskyblue'
	if not os.path.isfile(ico):
		try:makerequest(ico,xread('https://www.baokim.vn/promote/phimhd-baokim/logo-phimhd.png'),'wb')
		except:pass
	
	def fixURL(url):return url if url.startswith('http') else 'http://mphim.net'+url
	
	def itemDIR(s):
		title=xtitle(s)
		href=xhref(s)
		if not title or not href:return
		label=' '.join(i for i in re.findall('(<span.+?/span>)',s,re.S) if 'class="title' not in i)
		label=' '.join(re.sub('<.+?>','',label).split())
		title='%s [COLOR green]%s[/COLOR]'%(title,label)
		title=preTitle(s,title)
		img=xsearch('original="(.+?)"',s)
		addir_info(namecolor(title,c),fixURL(href),img,'',mode,1,'eps',True)
			
	def mp_page(url):
		b=xread(url)
		if not b:b=xread(url+'.html')
		s=xsearch('(<ul class="list_m".+?/ul>)',b,1,re.S)
		for s in re.findall('(<li.+?/li>)',s,re.S):itemDIR(s)
		
		s=xsearch('(<ul class="pagination".+?/ul>)',b)
		href=xsearch('<a href="([^"]+?)" rel="next">',s)
		if href:
			pages=re.findall('>(\d+)</a>',s)
			if pages:pages=max(int(i) for i in pages)
			else:pages=0
			title=namecolor('Page next: %d/%d'%(page+1,pages),'lime')
			addir_info(title,href,ico,'',mode,page+1,'mp_page',True)
	
	from resources.lib.servers import mphim;mph=mphim(c)
	if query=='mphim.net':
		b=getHome('mphim.html','http://mphim.net/')
		title=color['search']+"Search trên mphim.net[/COLOR]"
		addir_info(title,'mphim.net',ico,'',mode,1,'search',True)
		
		s=xsearch('(<nav.+?/nav>)',b,1,re.S);ec=urllib2.base64.b64encode
		for m in re.findall('(<li data-id=.+?/li>)',s):
			href=xhref(m)
			title=re.sub('<.+?>','',m)
			addir_info(namecolor(title,c),href,ico,'',mode,1,'mp_page',True)
		for title in re.findall('<p>(.+?)</p>',s):
			addir_info(namecolor(title,c),title,ico,'',mode,1,'mp_submenu',True)
		
		add_sep_item('------------------------------------------------')
		for s in re.findall('(<section.+?/section>)',b,re.S):
			href=re.search('<h2><a href="(.+?)">(.+?)</a></h2>',s)
			if href:
				title=href.group(2)
				href=href.group(1)
				addir_info(namecolor(title,'gold'),fixURL(href),ico,'',mode,1,'mp_page',True)
				
			for m in [i for i in re.findall('(<li.+?/li>)',s,re.S) if '"serial"' in i]:itemDIR(m)
		
		for s in re.findall('(<h3.+?/ul>)',b,re.S):
			label=re.sub('<.+?>','',xsearch('(<h3.+?/h3>)',s))
			if label:add_sep_item(label)
			for m in re.findall('(<li.+?/li>)',s,re.S):
				title=xsearch('title="(.+?)"',m).replace('Xem phim ','')
				if not title:title=xsearch('<span class="title">(.+?)</span>',m)
				label=' '.join(re.findall('<span class=.+?>(\d[^>]+?)<',m))
				title='%s [COLOR green]%s[/COLOR]'%(title,label)
				href=href='http://mphim.net'+xsearch('href="(.+?)"',m)
				img=xsearch('data-original="(.+?)"',m,result=ico)
				addir_info(namecolor(title,c),href,img,'',mode,1,'eps',True)
	
	elif query=="mp_submenu":
		b=xrw('mphim.html')
		s=xsearch('(<p>%s.+?/ul)'%url,b,1,re.S)
		for href,title in re.findall('<a href="(.+?)" title=".+?">(.+?)</a>',s):
			addir_info(namecolor(title,c),href,ico,'',mode,1,'mp_page',True)
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="mphim.net" or query=="INP":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query:return 'No'
		if 'Page next:' not in name:page=1
		
		mp_page('http://mphim.net/danh-sach-phim/?s=%s'%'-'.join(query.split()))
	
	elif query=='mp_page':mp_page(url)
	
	elif query=='eps':
		b=xread(url)
		label=xsearch('<title>(.+?)</title>',b).replace(' — MPHIM.net','')
		href=xsearch('<a href="(.+?/tap-Fshare.html)"',b)
		if href:
			for href in [i for i in re.findall('<a href="(.+?)"',xread(href)) if '/www.fshare.vn/' in i]:
				addir_info(label,href,img,'',mode,1,'play')
		
		s=xsearch('(<div id="eps".+?/div>)',b,1,re.S)
		s=re.findall('(<p class="epi".+?/p>)',s,re.S)
		for s in [i for i in s if '/xem-phim/' in i]:
			for href,epi in re.findall('href="([^"]+?)".+?>([^<]+?)</a>',s):
				addir_info(epi+' '+label,fixURL(href),img,'',mode,1,'play')
	
	elif query=='play':
		link=''
		for href,label in mph.maxLink(url):
			if 'www.fshare.vn/file/' in href:resolve_url(href);break
			elif 'youtube.com' in href:link=href;break
			else:
				link=xget(href)
				if link:link=link.geturl();break
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','mphim.net') 

def vtvgo (name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'vtvgo.png');urlhome='http://vtvgo.vn/';c='green'
	if not os.path.isfile(ico):
		try:makerequest(ico,xread('http://vtvgo.vn/public/images/logo.png'),'wb')
		except:pass
	
	from resources.lib.servers import vtvgovn;vtv=vtvgovn(c)
	if query=='Home':
		title=color['search']+"Search trên vtvgo.vn[/COLOR]"
		addir_info(title,'vtvgo.vn',ico,'',mode,1,'search',True)
		
		menu=[("http://vtvgo.vn/tin-tuc.html","Tin tức tổng hợp","cat01"),
			("http://vtvgo.vn/kho-video.html","Gameshows","cat02"),
			("http://vtvgo.vn/an-tuong-vtv.html","VTV Awards 2016","cat03")]
		
		for href,title,cat in menu:addir_info(namecolor('[B]%s[/B]'%title,c),href,ico,'',mode,1,cat,True)
		add_sep_item('VTVgo Live TV--------------------------------------')
		[addir_info(namecolor('[B]%s[/B]'%i[0],c),i[1],i[2],'',mode,1,'live') for i in vtv.liveList()]
		
	elif query=='cat01':#Tin tức tổng hợp
		for title in re.findall('<h2>(.+?)</h2>',xread(url)):
			addir_info(namecolor(title,c),'',ico,'',mode,1,'cat1',True)
	
	elif query=='cat1':
		if 'Mới Nhất' in name:url='http://vtvgo.vn/get-data-news?keyword=new&page=%d'
		elif 'Nóng Nhất' in name:url='http://vtvgo.vn/get-data-hot-news?keyword=hot&page=%d'
		elif 'Thời Sự' in name:url='http://vtvgo.vn/get-data-news?keyword=thoi+su&page=%d'
		elif 'Kinh Tế' in name:url='http://vtvgo.vn/get-data-news?keyword=kinh+te&page=%d'
		elif 'Thể Thao' in name:url='http://vtvgo.vn/get-data-news?keyword=the+thao&page=%d'
		elif 'Giải Trí' in name:url='http://vtvgo.vn/get-data-news?keyword=giai+tri&page=%d'
		elif 'Thế Giới' in name:url='http://vtvgo.vn/get-data-news?keyword=the+gioi&page=%d'
		for title,href,img in vtv.news(url,page):addir_info(title,href,img,img,mode,1,'play')
		
	elif query=='cat02':#Gameshows
		for title,href,img in vtv.cat02(url):
			if 'sep' in href:add_sep_item('%s --------------------------------------'%title)
			else:addir_info(title,href,img,img,mode,1,'play')
	
	elif query=='cat03':
		for title,href,img in vtv.cat03(url):
			if 'sep' in href:add_sep_item('%s --------------------------------------'%title)
			else:addir_info(title,href,img,img,mode,1,'play')
	
	elif query=='cat04':
		addir_info(namecolor('[B]VTV3 - [COLOR orange]FPT[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B]',c),'http://118.69.252.4/tv2/vtv3HD/index.m3u8',ico,'',mode,1,'cat41')
		addir_info(namecolor('[B]VTV6 - [COLOR orange]FPT[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B]',c),'http://118.69.252.4/tv2/vtv6HD/index.m3u8',ico,'',mode,1,'cat41')
		add_sep_item('-----------------------------------------------')
		
		addir_info(namecolor('[B]VTV3 - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] 640x360',c),'1_ks4iwsda-01',ico,'',mode,1,'golive')
		addir_info(namecolor('[B]VTV3 - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] 854x480',c),'1_ks4iwsda-02',ico,'',mode,1,'golive')
		addir_info(namecolor('[B]VTV3 - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] 1024x576',c),'1_ks4iwsda-03',ico,'',mode,1,'golive')
		addir_info(namecolor('[B]VTV3 - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] 1280x720',c),'1_ks4iwsda-04',ico,'',mode,1,'golive')
		add_sep_item('-----------------------------------------------')
		
		addir_info(namecolor('[B]VTV6 - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] 640x360',c),'1_rhex2pfs-01',ico,'',mode,1,'golive')
		addir_info(namecolor('[B]VTV6 - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] 854x480',c),'1_rhex2pfs-02',ico,'',mode,1,'golive')
		addir_info(namecolor('[B]VTV6 - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] 1024x576',c),'1_rhex2pfs-03',ico,'',mode,1,'golive')
		addir_info(namecolor('[B]VTV6 - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] 1280x720',c),'1_rhex2pfs-04',ico,'',mode,1,'golive')
		add_sep_item('-----------------------------------------------')
		
		addir_info(namecolor('[B]VTV3 - [COLOR orange](Dự phòng)[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B]',c),'http://live.tvmienphi.biz/stream-flix/vtv3hd.php','https://static.fptplay.net/static/img/share/channels/icon_channel_vtv3-hd_145810226276.jpg','',mode,1,'cat45')
		addir_info(namecolor('[B]VTV6 - [COLOR orange](Dự phòng)[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B]',c),'http://live.tvmienphi.biz/stream-flix/vtv3hd.php','https://static.fptplay.net/static/img/share/channels/icon_channel_vtv6-hd_14567302322.jpg','',mode,1,'cat45')
		addir_info(namecolor('[B]VTV3 - [COLOR orange](Dự phòng)[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B]',c),'http://embed.sohatv.vn?__c=vtv3','https://static.fptplay.net/static/img/share/channels/icon_channel_vtv3-hd_145810226276.jpg','',mode,1,'cat45')
		addir_info(namecolor('[B]VTV6 - [COLOR orange](Dự phòng)[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B]',c),'http://embed.sohatv.vn?__c=vtv6','https://static.fptplay.net/static/img/share/channels/icon_channel_vtv6-hd_14567302322.jpg','',mode,1,'cat45')
		addir_info(namecolor('[B]VTV9 - [COLOR orange](Dự phòng)[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B]',c),'http://embed.sohatv.vn?__c=vtv9','http://vtv1.vcmedia.vn/web_images/vtv9-3.png','',mode,1,'cat45')
		add_sep_item('-----------------------------------------------')
		
		addir_info('[B][COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR] [COLOR red]Nổi Bật[/COLOR][/B]','http://vtvgo.vn/euro2016/index.html',ico,'',mode,1,'cat42',True)
		addir_info('[B][COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR] [COLOR lime]Phát Lại[/COLOR][/B]','http://vtvgo.vn/euro2016/replay.html',ico,'',mode,1,'cat43',True)

	elif query=='cat45':
		if 'stream-flix' in url:
			link=xsearch('"file":\'(.+?)\'',xread(url))
			if 'VTV6' in name:link=link.replace('vtv3','vtv6')
		else:link=xsearch('playUrl.{3,5}"(.+?)"',xread(url))+'|Referer=http://vtv.vn/truyen-hinh-truc-tuyen.htm'
		xbmcsetResolvedUrl(link)

	elif query=='cat44':
		addir_info(namecolor('[B]VTV6 live - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] Chỉ có Audio',c),'1_rhex2pfs',ico,'',mode,1,'golive_TYPE=AUDIO')
		addir_info(namecolor('[B]VTV6 live - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] 854x480',c),'1_rhex2pfs',ico,'',mode,1,'golive_854')
		addir_info(namecolor('[B]VTV6 live - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] 1024x576',c),'1_rhex2pfs',ico,'',mode,1,'golive_1024')
		addir_info(namecolor('[B]VTV6 live - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] 1280x720',c),'1_rhex2pfs',ico,'',mode,1,'golive_1280')
	
	elif query=='cat41':xbmcsetResolvedUrl(url)
	
	elif query=='golive':
		xbmcsetResolvedUrl(vtv.golive(url.split('-')[0],url.split('-')[1]))
		#xbmcsetResolvedUrl(joinpath(xsharefolder,'vtv.m3u8'))
	
	elif 'golive_' in query:
		url=vtv.golive(url)
		link=query.split('_')[1]
		base=urllib2.os.path.dirname(url)
		for i in xread(url).splitlines():
			if 'AUDIO' in link and link in i:link=xsearch('URI="(.+?)"',i);break
			elif link in i:link='OK';continue
			elif i and link=='OK':link=i;break
		link=base+'/'+link
		xbmcsetResolvedUrl(link)
	
	elif query=='cat42':
		b=xread('https://drive.google.com/folderview?id=0B5y3DO2sHt1LRzFuUzN5cUhKT28')
		url=urllib2.base64.b64decode(xsearch('<title>(.+?)</title>',b))
		[addir_info(i[0],i[1],i[2],'',mode,1,'playVOD') for i in vtv.vodList(url)]
	
	elif query=='cat43':
		b=xread('https://drive.google.com/folderview?id=0B5y3DO2sHt1LcGNoaC1QcUpldGs')
		url=urllib2.base64.b64decode(xsearch('<title>(.+?)</title>',b))
		[addir_info(i[0],i[1],i[2],'',mode,1,'playVOD') for i in vtv.vodList(url)]
		
	elif query=='playVOD':
		try:link=xbmcsetResolvedUrl(urllib2.urlopen(url).geturl()+'|Referer=http://vtvgo.vn/euro2016/live.html')
		except:mess('Get maxspeed link fail !','VTVgo.vn')
	
	elif query=='live':
		id=xsearch('-(\d+)\.html',url)
		if not id:id=xsearch('/(\d+)\.jpg',img)
		try:xbmcsetResolvedUrl(vtv.live(id))
		except:mess('Get maxspeed liveTV link fail !','VTVgo.vn')
	
	elif query=='play':
		try:xbmcsetResolvedUrl(vtv.vodLink(url))
		except:mess('Get maxspeed link fail !','VTVgo.vn')

def youtubeDL(url):
	try:import YDStreamExtractor;vid=True
	except:vid=False;mess(u'Cài đặt module youtube.dl để get link phim này')
	if vid:
		vid=YDStreamExtractor.getVideoInfo(url)
		if vid:
			link=xget(vid.streamURL().split('|')[0])
			if link:
				link=link.geturl()
				mess('Xshare get link on Youtube.dl module','Notification')
		else:link=''
	return link

def play_youtube(url):
	from resources.lib.servers import youtube;yt=youtube()
	link=yt.getDL(url,'url_encoded_fmt_stream_map')
	if link=='Video not found!':mess(link,'youtube.com')
	elif not link:
		try:link=youtubeDL(url)
		except:link=''
		if link:xbmcsetResolvedUrl(link)
		else:
			id=xsearch('([\w|-]{10,20})',url)
			url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s'%id
			item=xbmcgui.ListItem(path=url, iconImage=img, thumbnailImage=img)
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
			mess('Xshare play on Youtube Add-on','Notification')
	else:
		xbmcsetResolvedUrl(link,re.sub(' \[COLOR.+?/COLOR\]','',name)+'Maxlink')
		mess('Link Youtube playing on Xshare')

def youtube(name,url,img,fanart,mode,page,query,text=''):
	ico=os.path.join(iconpath,'youtube.png');urlhome='https://www.youtube.com/';c='red'#cyan turquoise
	if not os.path.isfile(ico):
		try:makerequest(ico,xread('https://www.youtube.com/yt/brand/media/image/YouTube-logo-full_color.png'),'wb')
		except:pass
	
	def channelPage(url,ajax=False):
		b=xread(url)
		if ajax:
			try:j=json.loads(b)
			except:j={}
			b=j.get('content_html','').encode('utf-8')
			pn=j.get('load_more_widget_html','').encode('utf-8')
			pn=xsearch('data-uix-load-more-href="(.+?)"',pn).replace('amp;','')
		else:pn=xsearch('data-uix-load-more-href="(.+?)"',b).replace('amp;','')
		
		string='<li class="channels-content-item yt-shelf-grid-item">'
		for s in [i for i in b.split(string) if 'data-context-item-id' in i]:addirVideo(s)
		
		if pn:
			title=namecolor('Page next: %d'%(page+1),'lime')
			addir_info(title,'https://www.youtube.com'+pn,ico,'',mode,page+1,'channelAjax',True)
		
	def addirVideo(s,menu={}):
		def s2s(s):#string to seconds
			def n(i):
				try:j=int(i)
				except:j=0
				return j
			s=s.split(':')
			if len(s)>2:i=n(s[0])*3600+n(s[1])*60+n(s[2])
			elif len(s)>1:i=n(s[0])*60+n(s[1])
			else:i=n(s[0])
			return i
			
		title=xsearch('dir="ltr" title="(.+?)"',s,result=xsearch('dir="ltr">([^<]+?)<',s)).strip()
		href=xsearch('<a href="(.+?)"',s).replace('amp;','')
		if not title or not href:return
		view=xsearch('<li>([\d|\.]+?) lượt xem</li>',s)
		if not view:view=xsearch('class="yt-lockup-meta-info".+>([\d|\.]+).*</li><li>',s)
		if view:title+=' [COLOR gold]%s[/COLOR]'%view
		t=xsearch('class="yt-lockup-meta-info".+?>([^<]+?)</li></ul>',s)
		if not t or 'lượt' in t:
			t=xsearch('class="yt-lockup-meta-info".+?>([^<]+?)</li></li>',s)
		if t:title='[COLOR blue]%s[/COLOR] %s'%(t,title)
		duration=s2s(xsearch('>(\d*:?\d*:\d*)</span>',s,result='0').replace('.','').strip())
		href='https://www.youtube.com'+href
		img=xsearch('thumb="(.+?\.jpg)',s,result=xsearch('src="(.+?\.jpg)',s))
		if not duration:addir_info(s2c(title),href,img,'',mode,1,'video',menu=menu)
		else:addir_info(s2c(title),href,img,'',mode,1,'video',info={'title': title,'duration':duration},menu=menu)

	def playlistItemsPage(url,cookie=''):
		b=xreadc(url,c=cookie)
		c=xsearch('xshare(.+)',b);b=b.replace('xshare'+c,'')
		if c:cookie=c
		if '/browse_ajax' in url:
			try:j=json.loads(b)
			except:j={}
			b=j.get('content_html','').encode('utf-8')
			pn=j.get('load_more_widget_html','').encode('utf-8')
			pn=xsearch('data-uix-load-more-href="(.+?)"',pn).replace('amp;','')
		else:pn=xsearch('data-uix-load-more-href="(.+?)"',b).replace('amp;','')
		
		string='<div class="feed-item-main-content">';menu={}#menu={'servers_list':{'action':'Down'}}
		strings=[i for i in b.split(string) if '"shelf-wrapper clearfix"' in i]
		playlists=[]
		for S in strings:
			s=xsearch('(<a href="/playlist\?list=.+?/a>)',S,1,re.S)
			playlistId=xsearch('<a href="/playlist\?list=(.+?)"',s)
			title=xsearch('<span class="" >(.+?)</span>',s)
			img=xsearch('thumb="(.+?\.jpg)',S,result=xsearch('src="(.+?\.jpg)',S))
			if playlistId and title:playlists.append((title,playlistId,img))
		if playlists:
			title=namecolor('Playlists ','deepskyblue')+name
			addir_info(title,'',img,'',mode,1,'lists',True,text=str(playlists))
			
		for S in strings:
			string='<div class="yt-lockup-dismissable">'
			for s in [i for i in S.split(string) if '<div class="yt-lockup-thumbnail"' in i]:
				addirVideo(s,menu)

		if pn:
			title=namecolor('Page next: %d'%(page+1),'lime')
			addir_info(title,'https://www.youtube.com'+pn,ico,'',mode,page+1,'playlistItemsPage'+cookie,True)
	
	def playlistsPage(url,cookie=''):
		b=xreadc(url,c=cookie)
		c=xsearch('xshare(.+)',b);b=b.replace('xshare'+c,'')
		if c:cookie=c
		if '/browse_ajax' in url:
			try:j=json.loads(b)
			except:j={}
			b=j.get('content_html','').encode('utf-8')
			pn=j.get('load_more_widget_html','').encode('utf-8')
			pn=xsearch('data-uix-load-more-href="(.+?)"',pn).replace('amp;','')
		else:pn=xsearch('data-uix-load-more-href="(.+?)"',b).replace('amp;','')
		
		for s in re.findall('(<h2.+?/h2>)',b,re.S):
			title=xsearch('<span class="" >(.+?)</span>',s)
			id=xsearch('href="/playlist\?list=(.+?)"',s)
			if not id or not title:continue
			addir_info(namecolor(title,'turquoise'),id,img,'',mode,1,'playlist',True)
		
		if pn:
			title=namecolor('Page next: %d'%(page+1),'lime')
			addir_info(title,'https://www.youtube.com'+pn,ico,'',mode,page+1,'playlistsPage'+cookie,True)
		
	def playlistPage(url):
		b=xread(url)
		if '/browse_ajax' in url:
			try:j=json.loads(b)
			except:j={}
			b=j.get('content_html','').encode('utf-8')
			pn=j.get('load_more_widget_html','').encode('utf-8')
			pn=xsearch('data-uix-load-more-href="(.+?)"',pn).replace('amp;','')
		else:pn=xsearch('data-uix-load-more-href="(.+?)"',b).replace('amp;','')
		
		string='<li class="channels-content-item yt-shelf-grid-item">'
		for s in [i for i in b.split(string) if '"yt-lockup-thumbnail"' in i]:
			title=xsearch('dir="ltr" title="(.+?)"',s,result=xsearch('dir="ltr">([^<]+?)<',s)).strip()
			href=xsearch('href="/playlist\?list=(.+?)"',s).replace('amp;','')
			if not title or not href:continue
			videos=xsearch('<b>(\d+)</b>',s)
			if videos:title+=' [COLOR gold]%s video(s)[/COLOR]'%videos
			img=xsearch('src="(.+?\.jpg)',s,result=xsearch('thumb="(.+?\.jpg)',s))
			addir_info(namecolor(title,'turquoise'),href,img,'',mode,1,'playlist',True)
		
		if pn:
			title=namecolor('Page next: %d'%(page+1),'lime')
			addir_info(title,'https://www.youtube.com'+pn,ico,'',mode,page+1,'playlistPage',True)
	
	def getElements(url,query):
		from resources.lib.servers import youtube;yt=youtube()
		link=re.sub('&pageToken=.*','',url)
		items=yt.getElements(url,query)
		if page==1 and query=='searchListResponse':
			title=namecolor('[B]%s Playlists Search[/B]'%url,'deepskyblue')
			addir_info(title,url,img,'',mode,1,'searchPlayLists',True)
			title=namecolor('[B]%s channels Search[/B]'%url,'gold')
			addir_info(title,url,img,'',mode,1,'searchChannels',True)
		for title,id_,img_,query_ in items:
			if not img_:img_=ico
			if title=='nextPage':
				title=namecolor('Page next: %d'%(page+1),'lime')
				addir_info(title,id_,img_,'',mode,page+1,query,True)
			elif 'duration:' in title:
				duration=title.split('duration:')[1]
				title=title.split('duration:')[0]
				addir_info(title,id_,img_,'',mode,1,query_,info={'title': title,'duration':duration})
			else:addir_info(namecolor(title,'deepskyblue'),id_,img_,'',mode,1,query_,True)
	
	if query=='Home':
		title=namecolor('Search trên www.youtube.com','lime')
		addir_info(title,'youtube.com',ico,'',mode,1,'videoSearch',True)
		title=namecolor('Search trên api.youtube.com','lime')
		addir_info(title,'youtube.com',ico,'',mode,1,'videoSearchAPI',True)
		title=namecolor('Videos Phổ biến trên YouTube - Việt Nam','gold')
		url=urlhome+'channel/UCy3AjyBptEC4ODn-JeOp4JQ/videos?lang=vi&regionCode=VN&hl=vi'
		addir_info(title,url,ico,'',mode,1,'home',True)
		title=namecolor('PlayLists Phổ biến trên YouTube - Việt Nam','gold')
		url=urlhome+'channel/UCy3AjyBptEC4ODn-JeOp4JQ/playlists?lang=vi&regionCode=VN&hl=vi'
		addir_info(title,url,ico,'',mode,1,'home',True)

		b=xread('https://www.youtube.com?lang=vi&regionCode=VN&hl=vi')
		s=re.findall('(<a class="guide-item[^<]+?>)',b,re.S)
		for s in [i for i in s if '/feed/' in i or '/channel/' in i]:
			title=xtitle(s)
			href='https://www.youtube.com'+xhref(s)
			addir_info(namecolor('[B]%s[/B]'%title,'blue'),href,ico,'',mode,1,'home',True)
		addir_info(namecolor('[B]Youtube world channels[/B]','green'),'',ico,'',mode,1,'guideCategoryListResponse',True)
			
	elif '&pageToken=' in url:getElements(url,query)
	elif query=="videoSearch":make_mySearch('',url,'','',mode,'get');xrw('ytsearch.txt','SearchWEB')
	elif query=="videoSearchAPI":make_mySearch('',url,'','',mode,'get');xrw('ytsearch.txt','SearchAPI')
	elif url=="youtube.com" or query=="INP" or url=='videoSearch':# or url=='channelSearch':
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query:return 'No'
		if url=="youtube.com":page=1
		
		if xrw('ytsearch.txt')=='SearchAPI':
			query='+'.join(query.split())
			if query:
				from resources.lib.servers import youtube;yt=youtube()
				href='https://www.youtube.com/watch?v='
				for title,id,img in yt.search(query):
					if title=='nextPageToken':
						title=namecolor('Page next...%d'%(page+1),'lime')
						addir_info(title,'videoSearch',ico,'',mode,page+1,id,True)
					else:addir_info(s2c(title),href+id,img,'',mode,1,'video')
					
			return
		if 'https://www.youtube.com' in query:href=query+'&spf=navigate'
		else:href='https://www.youtube.com/results?search_query=%s&spf=navigate'%'+'.join(query.split())
		b=xread(href)
		try:
			j=json.loads(b)
			s=j[1].get('body')
			if type(s) is str:s=j[0].get('body')
			s=s.get('content').encode('utf-8')
		except:s=''
		next=xsearch('(<a href="/results\?.+?>)Tiếp theo',s).replace('&amp;','&')
		s=xsearch('(<ol id="item-section.+?/ol>)',s,1,re.S)
		items=[]
		for s in [i for i in s.split('<div class="yt-lockup-dismissable yt-uix-tile">') if 'href=' in i]:
			title=xsearch('title="(.+?)"',xsearch('(<h3.+?/h3>)',s,1,re.S))
			href=xhref(s)
			if not title or not href:continue
			if 'http' not in href:href='https://www.youtube.com'+href
			img=xsearch('<img.+?"([^"]+?\.jpg)',s).replace('&amp;','&')
			addir_info(s2c(title),href,img,'',mode,1,'video')
		
		if next:
			title=xsearch('label="(.+?)"',next)
			href='https://www.youtube.com'+xsearch('href="(.+?)"',next)
			addir_info(namecolor(title,'lime'),url,img,'',mode,1,href,True)

	elif query=='searchPlayLists':getElements(url,query)
	elif query=='searchChannels':getElements(url,query)
	elif query=='searchResultPlaylist':getElements(url,'playlist')
	elif query=='searchResultChannel':getElements(url,'playlists')
		
	elif query=='home' and '/feed/' in url:
		b=xread(url+'?regionCode=VN&hl=vi&lang=vi')
		
		string='<li class="expanded-shelf-content-item-wrapper">'
		strings=[j for j in b.split(string) if '"expanded-shelf-content-item"' in j]
		items=[]
		for s in strings:
			i=xsearch('(<div class="yt-lockup-byline".+?/div>)',s)
			title=xsearch('>([^<]+)</a>',i)
			href=xsearch('href="(.+?)"',i)
			img=xsearch('thumb="(.+?\.jpg)',s,result=xsearch('src="(.+?\.jpg)',s))
			if title and href:items.append((title,'https://www.youtube.com'+href+'/videos',img))
		if items:
			title=namecolor('Channels ','deepskyblue')+name
			addir_info(title,'',img,'',mode,1,'lists',True,text=str(items))

		for s in strings:addirVideo(s)
	
	elif query=='home' and '/channel/' in url and '/videos' in url:
		href='https://www.youtube.com/channel/UCy3AjyBptEC4ODn-JeOp4JQ/featured'
		addir_info(namecolor('PlayLists','deepskyblue'),href,img,'',mode,1,'home',True)
		channelPage(url)
	elif query=='home' and '/channel/' in url and '/featured' in url:playlistsPage(url)
	elif query=='home' and '/user/' in url and '/videos' in url:channelPage(url)
	elif query=='home' and '/channel/' in url and '/playlists' in url:playlistPage(url)
	elif query=='home' and '/channel/' in url:playlistItemsPage(url)
	elif query=='channelAjax':channelPage(url,True)
	elif query=='playlistPage':playlistPage(url)
	elif 'playlistsPage' in query:playlistsPage(url,query.replace('playlistsPage',''))
	elif 'playlistItemsPage' in query:playlistItemsPage(url,query.replace('playlistItemsPage',''))
	elif query=='lists':
		try:l=eval(text)
		except:l=[]
		for title,url,img in l:
			if 'https:' in url:addir_info(title,url,img,'',mode,1,'home',True)
			else:addir_info(title,url,img,'',mode,1,'playlist',True)
	
	elif query and query in 'searchListResponse-guideCategoryListResponse-channel-playlists-playlistItems':
		getElements(url,query)
		
	elif query=='channels':
		for title,id,img in eval(text):
			addir_info(namecolor(title,'deepskyblue'),id,img,'',mode,1,'channel',True)
	
	elif query=='video' or query=='play' or '/watch' in url:play_youtube(url)

	else:mess('Not things')

def ifiletv(name,url,img,fanart,mode,page,query):
	urlhome='http://ifile.tv';ico=icon['ifiletv'];c='blue'
	from resources.lib.servers import ifile;ifi=ifile(c)
	def getpage(url):
		content=xread(url)
		if url==urlhome+'/phim/index':xrw('ifiletv.html',content)
		for title,href,img,epi in ifi.page(content):
			if 'Page next...' in title:
				title=namecolor(title,'lime')
				addir_info(title,href,ico,'',mode,page+1,'page',True)
			elif epi :addir_info(namecolor(title,'turquoise'),href,img,fanart,mode,1,'eps',True)
			else:addir_info(namecolor(title,'turquoise'),href,img,fanart,mode,1,'getLink',True)
	
	if query=='Home':
		addir_info(namecolor('[B]Phim theo phân loại[/B]',c),'',ico,fanart,mode,1,'category',True)
		getpage(urlhome+'/phim/index')
		
	elif query=='page':getpage(url)
	
	elif query=='category':
		content=xrw('ifiletv.html')
		s=xsearch("(<hr>.+?<hr>)",content,1,re.S)
		for href,title in re.findall("href='(.+?)'>(.+?)</a>",s):
			addir_info(namecolor(title,c),urlhome+href,ico,fanart,mode,1,'page',True)
	
	elif query=='getLink' or query=='eps':
		name=namecolor(name.split('[COLOR gold]')[0])
		b=xread(url)
		s=[i for i in b.split("<div class='arrow_news'") if 'http://4share.vn/' in i]
		s=s[0] if s else ''
		
		items=[]
		for a in s.split('<hr>'):
			title=' '.join(i.strip() for i in re.findall('<b>(.+?)</b>',a.split('</div>')[0]) if 'http' not in i)
			href=xsearch("href='(.+?)'",a)
			if title and href:
				if query=='eps':label=href.split('/')[-1]+' '+name
				else:label=name
				items.append((label,title,href))
		for label,title,href in sorted(items, key=lambda k: k[0].upper()):#,reverse=reverse)
				addir_info('%s %s'%(label,title),href,img,fanart,mode)
		
		for href in [i for i in re.findall("href='(.+?)'",s) if 'subscene.com' in i]:
			addir_info(name,href,img,fanart,mode)
			
		b=re.findall("(<div class='left_news_div_table'.+?/div>)",b,re.S)
		if b:
			add_sep_item('----------Phim Cùng thể loại---------')
			for s in b:
				href=xsearch("<a href='(.+?)'>",s)
				title=xsearch('<b><font color=.+?>([^<]+)<',s).strip()
				if not href or not title:continue
				title=' '.join(title.split())
				if 'http://ifile.tv' not in href:href='http://ifile.tv'+href
				img=xsearch("src=.?'(.+?)'",s)
				if 'http://ifile.tv' not in img:img='http://ifile.tv'+img
				addir_info(namecolor(title,'turquoise'),href,img,'',mode,1,'getLink',True)

def fcine(name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'fcine.png')
	if not os.path.isfile(ico):
		b=xread('http://fcine.net/uploads/monthly_2015_11/fcine_logo.png.27c717f766c607f8438950bbe4b3b7a0.png')
		if b:makerequest(ico,b,'wb')
	
	def makeItemsPage(url):
		from resources.lib.servers import fcinenet;fci=fcinenet()
		makeDir(fci.pageItems(url))
	
	def makeDir(items):
		title=namecolor('Dùng link %s Fcine.net'%('' if fcinefshare else 'Fshare trên '),'lime')
		menu={'fcine':{'name':title,'action':'fcinefshare','mode':mode}}
		for title,href,img in items:
			title=s2c(title)
			if 'Page next:' in title:addir_info(title,href,ico,'',mode,1,'page',True)
			elif fcinefshare:
				title='[COLOR gold]Fshare[/COLOR] '+title
				addir_info(title,href,img,'',mode,1,'fshare',True,menu=menu)
			else:addir_info(title,href,img,'',mode,1,'play',menu=menu)
	
	fcinefshare=myaddon.getSetting('fcinefshare')=='true'
	if query=='fcine.net':
		b=getHome('fcine.html','http://fcine.net/')
		title='Chuyển sang chế độ dùng link '
		if fcinefshare:
			title=namecolor(title+'của Fcine.net','orange')
			addir_info(title+'[COLOR green](phím Func)[/COLOR]','',ico,'',mode,1,'fcinefshare',True)
		else:
			title=namecolor(title+'[COLOR gold]Fshare[/COLOR] trên Fcine.net','orange')
			addir_info(title+'[COLOR green](phím Func)[/COLOR]','',ico,'',mode,1,'fcinefshare',True)
			choice=myaddon.getSetting('chonserver')
			title=namecolor('Tự động chọn Server trên Fcine.net (đang chọn: %s)'%choice,'lime')
			addir_info(title,'fcine.net',ico,'',mode,1,'choose-server',True)
		
		title=namecolor('Tìm nhanh trên fcine.net','lime')
		addir_info(title,'',ico,'',mode,1,'quicksearch',True)
		title=namecolor('Tìm đủ kết quả trên fcine.net','lime')
		addir_info(title,'',ico,'',mode,1,'fullsearch',True)
		
		for s in re.findall('(<div class="container.+?class="menuFix">)',b,re.S):
			title=xsearch('<div class="container-4 highlighted">(.+?)</div>',s)
			addir_info(namecolor(title,'orangered'),s,ico,'',mode,1,'menu',True)
		
		title=namecolor('Phim mới cập nhật','orangered')
		addir_info(title,'http://fcine.net/?listResort=1&page=1',ico,'',mode,1,'page',True)
		
		title=namecolor('Dùng link %s Fcine.net'%('' if fcinefshare else 'Fshare trên '),'lime')
		menu={'fcine':{'name':title,'action':'fcinefshare','mode':mode}}
		add_sep_item('--------- Fcine giới thiệu ---------')
		s=xsearch('(<div id="featuredvideo".+?/div>)',b,1,re.S)
		for s in re.findall('(<a.+?/a>)',s,re.S):
			title=xsearch('"#(.+?)"',s)
			href=xsearch("href='(.+?)'",s)
			img=xsearch('thumb="(.+?)"',s)
			fanart=xsearch('src="(.+?)"',s)
			s=xsearch('(<div id="%s".+?/i></a>)'%title,b,1,re.S)
			title=[re.sub('<.+?>','',i) for i in re.findall('(<div.+?/div>)',s,re.S) if "'1 lines'" in i]
			title=' '.join(i for i in ' '.join(i for i in title).split())
			label=''.join(re.findall('<strong.+?/strong>(.+?)<',s))
			title=s2c(title+' [COLOR green]%s[/COLOR]'%label)
			if fcinefshare:
				title='[COLOR gold]Fshare[/COLOR] '+title
				addir_info(title,href,img,fanart,mode,1,'fshare',True,menu=menu)
			else:addir_info(title,href,img,fanart,mode,1,'play',menu=menu)

		add_sep_item('--------- Fcine đề cử ---------')
		s=xsearch('(<ul class="bimdethuong".+?/ul>)',b,1,re.S)
		for s in re.findall('(<li.+?/li>)',s,re.S):
			title=xsearch("title='(.+?)'",s)
			href=xsearch("href='(.+?)'",s)
			img=xsearch('src="(.+?)"',s)
			if fcinefshare:
				title='[COLOR gold]Fshare[/COLOR] '+title
				addir_info(title,href,img,'',mode,1,'fshare',True,menu=menu)
			else:addir_info(title,href,img,'',mode,1,'play',menu=menu)
	
	elif query=="choose-server":
		label='Chọn chế độ tự động chọn Server trên Fcine.net'
		choices=['Thuyết minh','Viet Sub','Không Chọn tự động']
		chonserver=["Thuyết minh","VietSub","Không"]
		choice=xselect(label,choices)
		if choice >= 0:
			myaddon.setSetting('chonserver',chonserver[choice])
			mess(u'Đã chọn: %s'%choices[choice].decode('utf-8'))
			xbmc.executebuiltin("Container.Refresh")
		return 'no'
	
	elif query=="fcinefshare" and fcinefshare:
		myaddon.setSetting('fcinefshare','false')
		xbmc.executebuiltin("Container.Refresh")
		return 'no'
	elif query=="fcinefshare" and not fcinefshare:
		myaddon.setSetting('fcinefshare','true')
		xbmc.executebuiltin("Container.Refresh")
		return 'no'
	
	elif query=="quicksearch" or query=="fullsearch":
		make_mySearch(query,'fcine.net','','',mode,'get')
	elif url=="fcine.net" or "INP" in query:
		if query=="fcine.net" in query:return make_mySearch("fullsearch",'fcine.net','','',mode,'get')
		elif "INP" in query:
			q=make_mySearch('','fcine.net','','','','Input')
			if not q:return 'No'
			else:query=query.replace('INP','')+q
			page=1
		
		if 'quicksearch' in query:
			query=query='+'.join(query.replace('quicksearch','').split())
			href='http://fcine.net/?app=videobox&module=video&controller=quicksearch&do=autoSearch'
			b=xread(href,data='term=%s'%query)
			if '<!DOCTYPE html>' in b:mess(u'Không tìm thấy phim có chuổi %s!'%query);return 'no'
			from resources.lib.servers import fcinenet;fci=fcinenet()
			makeDir(fci.lisItem(b))
		
		else:
			query=query='+'.join(query.replace('fullsearch','').split())
			makeItemsPage('http://fcine.net/findContent/?listResort=1&videobox=&term=%s&page=1'%query)
	
	elif query=='menu':
		for href,title in re.findall("<a href='(.+?)'>(.+?)</a>",url):
			href+='?listResort=1&alphabet=all&page=1'
			addir_info(namecolor(title,'orangered'),href,ico,'',mode,1,'page',True)
	
	elif query=='page':makeItemsPage(url)
		
	elif query=='fshare':
		name=namecolor(name).replace('Fshare ','')
		add_sep_item('Tên Phim: '+name)
		label=siteName(url)
		query='download.'+'.'.join(label.split('-'))
		from resources.lib.servers import fcinenet;fci=fcinenet()
		for href,title in fci.getFshare(url):
			addir_info(re.sub('\xc2|\xa0|\|','',title).strip(),href,img,'',mode,1,query,True)
			
	elif 'download' in query:
		mess('Initializing Downloader ...')
		try:b=urllib2.urlopen(url)
		except:b=''
		if b:
			fn=query.replace('download.','')
			if not fn:
				fn=xsearch('filename=([\w|\.|-]+)',str(b.headers.headers))
				if not fn:
					fn=b.geturl().split('?')[0]
					if fn[-1]=='/':fn=fn[:-1]
					fn=fn.rsplit('/',1)[1]
					if not fn:fn='abc'
			b=b.read(500*1024)
		if b and len(b)<500*1024:
			try:
				xrw(joinpath(subsfolder,'Vie.%s'%fn),b.replace('\r\n', '\n'))
				mess(u'Đã download sub vào xshare subfolder')
			except:mess(u'Downloaded sub thất bại!')
		else:mess(u'Downloaded sub thất bại!')
		return 'no'
	
	elif query=='play':
		from resources.lib.servers import fcinenet;fci=fcinenet()
		link,sub=fci.getLink(url)
		if sub:mess(u'Subtitle của fcine.net','xshare')
		xbmcsetResolvedUrl(link,sub=sub)

def taiphimhdnet(name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'taiphimhdnet.png');c='FF1E90FF';urlhome='http://taiphimhd.net'
	if not os.path.isfile(ico):
		b=xread('http://taiphimhd.net/sites/all/themes/taiphimhd/logo/200x200.png')
		if b:makerequest(ico,b,'wb')
	
	def makeDir(s):
		from resources.lib.servers import taiphimhdnet;hdnet=taiphimhdnet()
		for title,href,img in hdnet.getDetail(s):addir_info(title,href,img,img,mode,1,'link',True)
		pn=hdnet.pageNext(s,page)
		if pn:addir_info(pn[0],pn[1],ico,'',mode,page+1,'page',True)
	
	def makedir(s):
		title=xsearch('title="([^"]+?)"',s)
		href=xhref(s)
		img=ximg(s)
		if title and href:
			i=xsearch('<div class="left">([^<]+?)</div>',s)
			if i:title='[COLOR gold]%s[/COLOR] '%i+title
			if urlhome not in href:href=urlhome+href
			addir_info(title,href,img,img,mode,1,'link',True)
	
	if query=='taiphimhd.net':
		b=xread(urlhome)
		title=namecolor("Search trên taiphimhd.net",'lime')
		addir_info(title,'taiphimhd.net',ico,'',mode,1,'search',True)
		
		cat=re.findall('<h2 class="megamenu-parent-title"><a href="(.+?)"',b)
		addir_info(namecolor('Phim lẻ',c),cat[0],ico,'',mode,1,'phimle',True)
		addir_info(namecolor('Phim bộ',c),cat[1],ico,'',mode,1,'phimbo',True)
		add_sep_item('Đề cử ------------------------')
		for s in re.findall('(<div class="views-rotator-item".+?/div>)',b,re.S):makedir(s)
		
		for s in re.findall('(<div class="defaultblock">.+?<div class="more-link">)',b,re.S):
			add_sep_item('%s ------------------------'%xsearch('<h2>(.+?)</h2>',s))
			for i in re.findall('(<td class=.+?/td>)',s,re.S):makedir(i)
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="taiphimhd.net" or query=="INP":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query:return 'No'
		page=1
		makeDir(xread('http://taiphimhd.net/search/content/'+'%20'.join(query.split())))
	
	elif query=='phimle':
		b=xread(url)
		m=('xem nhiều nhất ngày','xem nhiều nhất tuần','xem nhiều nhất tháng')
		for i in m:addir_info(namecolor('Phim lẻ '+i,c),'phimle',ico,'',mode,1,'xemnhieu',True)
		items=re.findall('<li id="megamenu-mlid-30[^"]+?" class=".+?"><a href="(.+?)".+?>(.+?)</a>',b)
		items=[(i[0].replace('&amp;','&'),i[1]) for i in items]
		title=namecolor('Thể Loại Phim',c)
		addir_info(title,str(items),ico,'',mode,1,'category',True)
		makeDir(b)
	
	elif query=='xemnhieu':
		from resources.lib.servers import taiphimhdnet;hdnet=taiphimhdnet()
		if 'Trang tiếp theo' in name:d=xsearch('\((.+?)\)',name)
		else:d='day' if 'ngày' in name else 'week' if 'tuần' in name else 'month'
		for title,href,img in hdnet.xemnhieu(url,d,page):
			if 'Trang tiếp theo' in title:
				addir_info(title,url,ico,'',mode,page+1,query,True)
			else:addir_info(title,href,img,img,mode,1,'link',True)
	
	elif query=='category':
		for href,title in eval(url):addir_info(namecolor(title,c),href,ico,'',mode,1,'page',True)
	
	elif query=='phimbo':
		b=xread(url)
		m=('xem nhiều nhất ngày','xem nhiều nhất tuần','xem nhiều nhất tháng')
		for i in m:addir_info(namecolor('Phim bộ '+i,c),'phimbo',ico,'',mode,1,'xemnhieu',True)
		items=re.findall('<li id="megamenu-mlid-3125[^"]+?" class=".+?"><a href="(.+?)".+?>(.+?)</a>',b)
		items=[(i[0].replace('&amp;','&'),i[1]) for i in items if 'filters=1' in i[0]]
		title=namecolor('Quốc Gia',c)
		addir_info(title,str(items),ico,'',mode,1,'category',True)
		makeDir(b)
	
	elif query=='page':makeDir(xread(url))
	elif query=='link':
		from resources.lib.servers import taiphimhdnet;hdnet=taiphimhdnet()
		label=re.sub('\[.+\]','',name).strip()
		#add_sep_item('Phim: %s'%namecolor(name))
		for title,href in hdnet.getLinks(url):
			addir_info(title+' '+label,href,img,fanart,mode,1,'phude',True)
	
	elif query=='phude':
		mess('Initializing Downloader ...')
		from resources.lib.servers import taiphimhdnet;hdnet=taiphimhdnet()
		b=hdnet.download(url)
		if len(b)<500*1024:
			try:
				xrw(joinpath(subsfolder,'Vie.%s'%url.rsplit('/',1)[1]),b.replace('\r\n', '\n'))
				mess(u'Đã download sub vào xshare subfolder')
			except:mess(u'Downloaded sub thất bại')
		else:mess(u'Downloaded sub thất bại!')
		return 'no'

def vungtv(name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'vungtv.png');c='FF00FA9A'
	if not os.path.isfile(ico):
		b=xread('http://vungtv.com/favicon.png')
		if b:makerequest(ico,b,'wb')

	def itemsDir(s):
		title=xsearch('name="(.+?)"',s,result=xsearch('class="f-name">(.+?)<',s))
		href=xhref(s)
		if not title or not href:return
		img=xsearch('(http[^"]+?\.jpg)',s)
		label=' '.join(re.sub('<.+?>','',i) for i in re.findall('(<div.+?/div>)',s))
		label=label+' '+' '.join(re.sub('<.+?>','',i) for i in re.findall('(<span.+?/span>)',s))
		label=label+' '+xsearch('country="(.+?)"',s)
		label=label+' '+xsearch('duration="(.+?)"',s)
		label=label+' '+xsearch('release="(.+?)"',s)
		label=label+' '+xsearch('category="(.+?)"',s)
		label=' '.join(label.replace('N/A','').split())
		title=title+' [COLOR gold]%s[/COLOR]'%label
		if '"f-episode"' in s:dir=True;title=namecolor(title,c);q='eps'
		else:dir=False;q='play'
		addir_info(vnu(title),href,img,'',mode,1,q,dir)
	
	def vungtv_page(url):
		b=xread(url)
		for s in [i for i in re.findall('(<a.+?/a>)',b,re.S) if '"f-name"' in i]:itemsDir(s)
		
		href=xsearch('<a href="([^"]+?)">&raquo;</a>',b)
		if href and href !='#':
			pages=xsearch('/(\d+)">Trang cuối</a>',b)
			title=namecolor('Trang tiếp theo... %d/%s'%(page+1,pages),'lime')
			addir_info(title,href,ico,'',mode,page+1,query,True)
	
	def linkPlay(url):
		b=xread(url)
		title=xsearch('<title>(.+?)</title>',b)
		title=' '.join(re.sub('Xem Phim|\|','',title).split())
		return title,xsearch('<a href="([^"]+?)"[^>]+?>Xem Phim</a>',b)
	
	if query=='vungtv.com':
		b=getHome('vungtv.html','http://vungtv.com/')

		title=namecolor("Search trên vungtv.com","lime")
		addir_info(title,'vungtv.com',ico,'',mode,1,'search',True)
		
		href='http://vungtv.com/ajax/top/'
		addir_info(namecolor('TOP Ngày',c),href+'day',ico,'',mode,1,'page',True)
		addir_info(namecolor('TOP Tuần',c),href+'week',ico,'',mode,1,'page',True)
		addir_info(namecolor('TOP Tháng',c),href+'month',ico,'',mode,1,'page',True)
		
		s=xsearch('(<div class="collapse navbar.+?/nav>)',b,1,re.S)
		m=re.findall('(<li class="dropdown".+?/ul>)',s,re.S)
		items=re.findall('<a href="([^"]+?)"([^>]+?)>([^>]+?)<',s)
		items=[i for i in items if '"button"' in i[1] and 'javascript' not in i[0]]
		for href,label,title in items:
			if href=='#':
				n=''.join(i for i in m if title in i)
				addir_info(namecolor(title,c),n,ico,'',mode,1,'menu',True)
			else:addir_info(namecolor(title,c),href,ico,'',mode,1,'page',True)
		
		add_sep_item('-------- PHIM VỪNG ĐỀ CỬ --------')
		s=xsearch('(<div class="cat-fav-slide.+?class="block-big")',b,1,re.S)
		for s in s.split('<a'):itemsDir(s+' "f-episode"')
		
		add_sep_item('-------- CHỦ ĐỀ HOT --------')
		s=xsearch('(id="slider-tuyentap".+?-->)',b,1,re.S)
		p='<a href="(.+?)".+?(http.+?\.jpg).+?>(.+?)</div>'
		for href,img,title in re.findall(p,s.replace('\n','')):
			addir_info(namecolor(title,c),href,img,'',mode,1,'page',True)
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP" or url=="vungtv.com":
		if query=="INP":query=make_mySearch('',url,'','','','Input')
		if not query.strip():return
		page=1
		vungtv_page('http://vungtv.com/tim-kiem/?q=%s'%urllib.quote_plus(query))

	elif query=='menu':
		for href,title in re.findall('<li><a href="(.+?)">(.+?)</a></li>',url):
			addir_info(namecolor(vnu(title),c),href,ico,'',mode,1,'page',True)
	
	elif query=='page':vungtv_page(url)
	
	elif query=='eps':
		name,url=linkPlay(url)
		b=xread(url)
		s=xsearch('(<div class="stream-episode".+?/div>)',b,1,re.S)
		if not s:addir_info(name,url,img,'',mode,1,'play')
		else:
			items=[i for i in re.findall('href="(.+?)">(.+?)</a>',s) if '#' not in i[0]]
			for href,epi in items:addir_info(epi+' '+name,href,img,'',mode,1,'play')
	
	elif query=='play':
		if '/xemphim/' in url:name,url=linkPlay(url)
		id=url.rsplit('-',1)[-1]
		hd={'User-Agent': 'Mozilla/5.0', 'X-Requested-With': 'XMLHttpRequest'}
		try:s=json.loads(xread('http://vungtv.com/player?id=%s&mp4='%id,hd)).get('html')
		except:s=''
		link=''
		for href in re.findall("file:'(.+?)'",s):
			link=xcheck(href)
			if link:break
		xbmcsetResolvedUrl(link)#,sub=sub)

def biphim(name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'biphim.png');c='FFBA55D3'
	if not os.path.isfile(ico):
		b=xread('http://biphim.com/data/images/logo.png')
		if b:makerequest(ico,b,'wb')

	def fixURL(url):
		return 'http://biphim.com/'+url if not url.startswith('http') else url
	
	def itemDir(s):
		title=xsearch('title="([^"]+?)">[^<]+?</a>',s)
		href=xhref(s)
		if not title or not href:return
		img=xsearch("src='(.+?)'",s)
		label=[re.sub('<.+?>','',i) for i in re.findall('(<div.+?/div>)',s)]
		label=' '.join(' '.join(i for i in label if i not in title).split())
		title=title+' [COLOR green]%s[/COLOR]'%label
		if re.search('.ồng .iếng',title):title='[COLOR gold]LT[/COLOR] '+title
		elif re.search('.huyết .inh',title):title='[COLOR gold]TM[/COLOR] '+title
		if not re.search('[T|t]ập \d+',title):dir=False;q='play'
		else:dir=True;q='eps';title=namecolor(title,c)
		addir_info(title,fixURL(href),img,'',mode,1,'eps',True)
		
	def biphimPage(url):
		if url.endswith('/'):url=url+'page-1'
		b=xread(url)
		s=xsearch('(<ul class="list-film".+?/ul>)',b)
		for s in re.findall('(<li.+?/li>)',s):itemDir(s)
		
		s=xsearch('(<span class="page_nav">.+?>Next</a>)',b)
		if s:
			pages=xsearch('>Page *\d+/ *(\d+)<',b)
			title=namecolor('Trang tiếp theo ... %d/%s'%(page+1,pages),'lime')
			url=url.rsplit('/',1)[0]+'/page-%d'%(page+1)
			addir_info(title,url,img,'',mode,page+1,query,True)
	
	if query=='biphim.com':
		b=getHome('biphim.html','http://biphim.com/')

		title=namecolor("Search trên biphim.com","lime")
		addir_info(title,'biphim.com',ico,'',mode,1,'search',True)
		
		s=xsearch('(<ul class="menu".+?javascript">)',b)
		for s in [i for i in s.split('</ul>') if '<li>' in i]:
			title=xsearch('<a>(.+?)</a>',s)
			if not title:title=re.sub('<.+?>','',xsearch('(<h3.+?/h3>)',s,1,re.S))
			addir_info(namecolor(title,c),s,ico,'',mode,1,'menu',True)

	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP" or url=="biphim.com":
		if query=="INP":query=make_mySearch('',url,'','','','Input')
		if not query.strip():return
		page=1
		biphimPage('http://biphim.com/search/%s'%urllib.quote_plus(query))

	elif query=='menu':
		p='<a[^>]+?href="([^"]+?)" title="[^"]+?">([^<]+?)</a>'
		for href,title in re.findall(p,url):
			addir_info(namecolor(title,c),fixURL(href),ico,'',mode,1,'page',True)

	elif query=='page':biphimPage(url)
	
	elif query=='eps':
		if '/xem-phim' not in url:url+='xem-phim'
		b=xread(url)
		name=xsearch('<span title="(.+?)"',b,result=namecolor(name))
		s=xsearch('(<div class="serverlist".+?id="comment">)',b)
		if not s:addir_info(name,url,img,'',mode,1,'play')
		servers=re.findall('(<div class="label".+?/ul>)',s)
		lenSRVS=len(servers)
		for s in servers:
			server=re.sub('<.+?>','',xsearch('(<div class="label".+?/div>)',s))
			add_sep_item(server)
			for href,epi in re.findall('<a[^>]+?href="(.+?)"[^>]+?>(.+?)</a>',s):
				addir_info(epi+' '+name,fixURL(href),img,'',mode,1,'play')
			
	elif query=='play':
		b=xread(url)
		try:links=eval(xsearch('sources: (\[.+?\])',b,1,re.S).replace('\\',''))
		except:links=[]
		link=googleItems(links,'file')
		if link:xbmcsetResolvedUrl(link)
		elif re.search('bị lỗi',b):mess('Tập film bị lỗi','biphim.com')
		else:mess('File invalid or deleted!','biphim.com')

def banhtvItems(url):
	from resources.lib.servers import gibberishAES
	link=''
	try:exec(xread('http://textuploader.com/d5bjl/raw'))
	except:pass
	return link
		
def banhtv(name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'banhtv.png');c='FFBA55D3'
	if not os.path.isfile(ico):
		b=xread('http://banhtv.com/images/logo.png')
		if b:makerequest(ico,b,'wb')

	def banhtvItems1(url):
		from resources.lib.servers import gibberishAES
		link=''
		b=xread(url)
		id=xsearch('"modelId":"(.+?)"',b,result=xsearch('<input id="film_id".+?value="(.+?)">',b))
		keyAES='banhtv.com4590481877'+id
		for link in re.findall('data-link="(.+?)"',b):
			try:
				link=gibberishAES(link,keyAES)
				j=json.loads(xread('http://banhtv.com'+link))
				j=[j[i] for i in j.keys() if isinstance(j[i],list) and j[i]]
			except:j=[]
			items=[]
			for m in j:
				items+=[{'link':i.get('file'),'label':i.get('label','')} for i in m if i.get('file')]
			link=googleItems(items)
			if link:break
		return link
	
	def banhtvItems2(url):
		from resources.lib.servers import gibberishAES
		b=xread(url)
		id=xsearch('"modelId":"(.+?)"',b,result=xsearch('<input id="film_id".+?value="(.+?)">',b))
		s=xsearch('playerSetting *= *(.+?);\s*\$',b)
		j=json.loads(s)
		j=[j[i] for i in j.keys() if isinstance(j[i],list) and j[i]]

		keyAES='banhtv.com4590481877'+id
		items=[]
		for m in j:
			items+=[{'link':gibberishAES(i.get('file',''),keyAES),'label':i.get('label')} for i in m if i.get('file','')]
		return items
	
	def fixURL(url):
		return 'http://banhtv.com'+url if not url.startswith('http') else url
	
	def itemDir(s):
		title=xtitle(s)
		href=xhref(s)
		img=ximg(s)
		if not title or not href:return
		label=[re.sub('<.+?>','',i) for i in re.findall('(<span.+?/span>)',s)]
		label=' '.join(' '.join(i for i in label if i not in title).split())
		title=title+' [COLOR green]%s[/COLOR]'%label
		if re.search('.ồng .iếng',title):title='[COLOR gold]LT[/COLOR] '+title
		elif re.search('.huyết .inh',title):title='[COLOR gold]TM[/COLOR] '+title
		if not re.search('[T|t]ập \d+|\d+/',title):dir=False;q='play'
		else:dir=True;q='eps';title=namecolor(title,c)
		addir_info(title,fixURL(href),img,img,mode,1,q,dir)
		
	def banhtvPage(url):
		b=xread(url)
		#s=xsearch('(<ul class="list-film".+?/ul>)',b)
		for s in [i for i in re.findall('(<li.+?/li>)',b,re.S) if '"icon-play"' in i]:itemDir(s)
		
		href=xsearch('<a href="([^"]+?)"[^>]+?rel="next">',b)
		if href:
			s=xsearch('(<div class="pagination".+?/div)',b)
			pages=max(int(i) for i in re.findall('>(\d+?)</a>',s))
			title=namecolor('Trang tiếp theo ... %d/%d'%(page+1,pages),'lime')
			addir_info(title,fixURL(href),img,'',mode,page+1,query,True)
	
	if query=='banhtv.com':
		b=getHome('banhtv.html','http://banhtv.com/')

		title=namecolor("Search trên banhtv.com","lime")
		addir_info(title,'banhtv.com',ico,'',mode,1,'search',True)
		
		s=xsearch('(<ul id="main-menu".+?class="login dropdown">)',b,1,re.S)
		for s in [i for i in s.split('<li class="">') if '"Trang chủ"' not in i]:
			title=xtitle(s)
			href=xhref(s)
			if '<ul' in s:addir_info(namecolor(title,c),s,ico,'',mode,1,'menu',True)
			else:addir_info(namecolor(title,c),fixURL(href),ico,'',mode,1,'page',True)
		
		add_sep_item('--------- PHIM HOT ---------')
		s=xsearch('(<ul id="film-hot".+?/ul>)',b,1,re.S)
		for s in re.findall('(<li.+?/li>)',s,re.S):itemDir(s)

	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP" or url=="banhtv.com":
		if query=="INP":query=make_mySearch('',url,'','','','Input')
		if not query.strip():return
		page=1
		banhtvPage('http://banhtv.com/tim-kiem.html?q=%s'%urllib.quote_plus(query))
	
	elif query=="menu":
		for href,title in re.findall('href="(.+?)">(.+?)</a>',url):
			addir_info(namecolor(title,c),fixURL(href),ico,'',mode,1,'page',True)
	
	elif query=='page':banhtvPage(url)

	elif query=='eps':
		b=xread(url)
		name=xsearch('<title>(.+?)</title>',b,result=namecolor(name)).replace('Xem phim ','')
		s=xsearch('(<ul class="episodes".+?/ul>)',b,1,re.S)
		for href,epi in re.findall('<a href="(.+?)" title="(.+?)">',s):
			addir_info(epi+' '+name,fixURL(href),img,'',mode,1,'play')
		if not s:addir_info(name,url,img,fanart,mode,1,'play')
			
	elif query=='play':#decodeLink
		link=banhtvItems(url)
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','banhtv.com')
		
def vnzoom(name,url,img,fanart,mode,page,query):
	from resources.lib.servers import vnZoom;vnz=vnZoom()
	ico=os.path.join(iconpath,'vnzoom.png');c='cyan'
	if not os.path.isfile(ico):
		b=vnz.vread('http://www.vn-zoom.com/forumdisplay.php?f=26')
		href=xsearch('href="http://www.vn-zoom.com/"><img src="(.+?)"',b)
		b=xread(href)
		if b:makerequest(ico,b,'wb')
	#b=xread(url,{'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36','Cookie':'bb_sessionhash=e1f705ebae364ce45a7694ce643700a3; bb_forumpwd=cfd75ccae02eec2584d0776def081c522b0645e1a-1-%7Bi-656_s-32-.00715437aef5b91782723c77bf9adf59._%7D'});'SC1TTCZMV89A' in b
	
	if query=='Home':
		b=vnz.vread('http://www.vn-zoom.com/forumdisplay.php?f=26')
		p='<h2 class="forumtitle"><a href="http://www.vn-zoom.com/f(\d+?)/">(.+?)</a></h2>'
		I=['666','658','655','584','656','657','319','659','29','585','662','731','672','716','27']
		for href,title in [i for i in re.findall(p,b) if i[0] in I]:
			href='http://www.vn-zoom.com/forumdisplay.php?f=%s&page=1'%href
			addir_info(namecolor(s2c(title.strip()),c),href,ico,'',mode,1,'room',True)
	
	elif query=='room':
		b=vnz.vread(url)
		for s in ['<a class="title'+i for i in b.split('<a class="title') if 'class="author"' in i]:
			title=xsearch('<a class="title[^>]+?>([^<]+?)</a>',s)
			label=xsearch('class="username.+?" title="(.+?)"',s).replace('Started by ','').replace('on ','')
			if label:title='[COLOR cyan]%s[/COLOR] %s'%(label,title)
			href=xhref(s)
			addir_info(title,href,ico,'',mode,1,'page',True)
		lp=xsearch('(\d+)\.html',xsearch('href="([^"]+?)" title="Trang Cuối',b))
		if lp:
			title=namecolor('Trang tiếp theo: %d/%s'%(page+1,lp),'lime')
			url=re.sub('page=\d+','page=%d'%(page+1),url)
			addir_info(title,url,ico,'',mode,page+1,'room',True)
	
	elif query=='page':
		b=vnz.vread(url,user=True);print len(b)
		srvs=['fshare.vn','4share.vn','tenlua.vn','subscene.com','phudeviet.org','youtube.com']
		def abc(u):return [i for i in srvs if i in u]
		for s in re.findall('(<ol id="posts".+?/ol>)',b,re.S):
			imgs=re.findall('<img style="max-width[^>]+src="(.+?)"',s)
			for i in re.findall('(<pre.+?/pre>)',s):
				img=imgs[0]
				items=re.findall('<a href="(.+?)" target="_blank" rel="nofollow">(.+?)</a>',i)
				if not items:
					title=namecolor(name)
					items=[(m,title) for m in re.findall('>(http.+?)<',i) if abc(m)]
				for href,title in items:
					addir_info(title,href,img,'',mode,1)

try:#Container.SetViewMode(num) addir:name,link,img,fanart,mode,page,query,isFolder
	myfolder=s2u(myaddon.getSetting('thumuccucbo'))
	if not os.path.exists(myfolder):myfolder=joinpath(datapath,'myfolder')
except:myfolder=joinpath(datapath,'myfolder')
thumucrieng=''.join(s for s in myaddon.getSetting('thumucrieng').split()).upper()
if not thumucrieng or len(thumucrieng)<10:thumucrieng='RDA4FHXVE2UU'
thumucrieng='https://www.fshare.vn/folder/'+thumucrieng
subsfolder=myaddon.getSetting('subsfolder')
if not subsfolder:subsfolder=joinpath(addonDataPath,'subs')
xsharefolder=os.path.join(addonDataPath,'xshare')
params=get_params();mode=page=0;temp=[];url=name=fanart=img=date=query=action=end=text=''
#print sys.argv[2],sys.argv[0]
try:url=urllib.unquote_plus(params["url"])
except:pass#http://www.dailymotion.com/video/k2Z6NnXtz8r2PUgJfMA 227414
try:name=urllib.unquote_plus(params["name"])
except:pass
try:img=urllib.unquote_plus(params["img"])
except:pass#b.replace('\r\n', '\n')
try:fanart=urllib.unquote_plus(params["fanart"])
except:pass#xbmcsetResolvedUrl(link,sub)
try:mode=int(params["mode"])
except:pass#xbmc.executebuiltin("Container.Refresh")
try:page=int(params["page"])
except:pass#xbmc.executebuiltin("Container.Update")
try:query=urllib.unquote_plus(params["query"])
except:pass#urllib.unquote
try:text=urllib.unquote_plus(params["text"])
except:pass#urllib.unquote

#dialog = xbmcgui.Dialog()
#d = dialog.input('Enter secret code', type=xbmcgui.INPUT_ALPHANUM)
log('========================================================================')
log("Mode: %d"%mode)
log("Name: %s"%name)
log("URL: %s"%url[:200])
log("Image: %s"%img)
log("Query: %s"%query)
log("Page: %d"%page)
log('========================================================================')

try:bakData=json.loads(xrw('sysmenu.dat'))
except:bakData={}
bakName=urllib2.hashlib.md5('%d%d%s%s%s'%(mode,page,query,name,url)).hexdigest()
myList=bakData.get(bakName)
if not myList:bakData[bakName]=[]

if myList:
	for name,url,img,fanart,mode,page,query,dir,menu in myList:
		addir_info(u2s(name),url,img,fanart,mode,page,query,dir,menu=menu)
elif name=='HideXshareMainMenuItem':hideMenuItem(page)
elif not mode:#xbmc.executebuiltin("Dialog.Close(all, true)")
	folders=(addonDataPath,datapath,iconpath,myfolder,tempfolder,subsfolder,xsharefolder)
	for folder in folders:
		if not os.path.exists(folder):os.mkdir(folder)
	xmlheader='<?xml version="1.0" encoding="utf-8">\n'
	items=[(datapath,'search.xml'),(datapath,'hdvietnam.xml'),(datapath,'favourites.xml'),
		(datapath,'phimmoi.xml'),(datapath,'fpt.xml'),(myfolder,'mylist.xml')]
	for i,j in items:
		file=joinpath(i,j)
		if not os.path.isfile(file):xrw(file,xmlheader)
	
	open_category("MMN");endxbmc();xrw('sysmenu.dat',json.dumps({}))
	if os.path.isfile(joinpath(data_path,'checkdatabase.txt')):database_download()
	if myaddon.getSetting('auto_update')=='true' and checkupdate('xshare_auto_update.dat',5,datapath):
		makerequest(joinpath(datapath,"xshare_auto_update.dat"),'','w')
		xshare_auto_update();delete_files(tempfolder)		
elif mode==1:end=vaphim(name,url,img,fanart,mode,page,query)
elif mode==2:end=google_search(url,query,mode,page)
elif mode==3:end=resolve_url(url,name=name)
elif mode==4:vp_phimmoi()
elif mode==5:vp_xemnhieu()
elif mode==6:ifiletv(name,url,img,fanart,mode,page,query)
elif mode==7:end=fptplay(name,url,img,fanart,mode,page,query,text)
elif mode==8:end=hdvietnam(name,url,img,fanart,mode,page,query)
elif mode==9:make_mySearch(name,url,img,fanart,mode,query)
elif mode==10:open_category(query)
elif mode==11:make_myFshare(name,url,img,fanart,mode,query)
elif mode==12:make_mylist(name,url,img,fanart,mode,query)
elif mode==13:end=xshare_search(name,url,query,mode,page)
elif mode==15:end=id_2url(name,url,img,mode,page,query)
elif mode==16:end=play_maxspeed_link(url)
elif mode==17:end=megabox(name,url,img,fanart,mode,page,query)
elif mode==18:dangcaphd(name,url,img,mode,page,query)
elif mode==19:pubvn(name,url,img,fanart,mode,page,query)
elif mode==20:end=vp_update(auto=False)
elif mode==21:vuahd(name,url,img,fanart,mode,page,query)
elif mode==22:hdviet(name,url,img,mode,page,query)
elif mode==23:end=hayhaytv(name,url,img,fanart,mode,page,query)
elif mode==24:phimmoi(name,url,img,mode,page,query)
elif mode==25:end=fcine(name,url,img,fanart,mode,page,query)
elif mode==26:kenh88(name,url,img,fanart,mode,page,query,text)
elif mode==27:phimdata(name,url,img,mode,page,query)
elif mode==28:phim47(name,url,img,fanart,mode,page,query,text)
elif mode==29:phimsot(name,url,img,mode,page,query)
elif mode==30:hdonline(name,url,img,fanart,mode,page,query,bakName,bakData)
elif mode==31:end=ifile_update()
elif mode==32:phim3s(name,url,img,mode,page,query)
elif mode==33:kphim(name,url,img,mode,page,query)
elif mode==34:end=taiphimhdnet(name,url,img,fanart,mode,page,query)
elif mode==35:phimnhanh(name,url,img,mode,page,query)
elif mode==36:bilutv(name,url,img,mode,page,query)
elif mode==37:anime47(name,url,img,mode,page,query)
elif mode==38:doc_Trang4share(url)#38
elif mode==39:phim14(name,url,img,fanart,mode,page,query,text)
elif mode==40:phimmedia(name,url,img,mode,page,query)
elif mode==41:tvhay(name,url,img,mode,page,query)
elif mode==42:nhacdj(name,url,img,fanart,mode,page,query)
elif mode==43:end=phimbathu(name,url,img,fanart,mode,page,query)
elif mode==44:hdsieunhanh(name,url,img,fanart,mode,page,query)
elif mode==45:chiasenhac(name,url,img,fanart,mode,page,query)
elif mode==46:nhaccuatui(name,url,img,fanart,mode,page,query)
elif mode==47:daklak47(name,url,img)
elif mode==48:imovies(name,url,img,fanart,mode,page,query)
elif mode==49:imax(name,url,img,fanart,mode,page,query)
elif mode==50:htvonline(name,url,img,fanart,mode,page,query)
elif mode==51:music(name,url,img,fanart,mode,page,query)
elif mode==52:myNAS(name,url,img,fanart,mode,page,query)
elif mode==53:taiphimhd(name,url,img,fanart,mode,page,query)
elif mode==54:vietsubhd(name,url,img,fanart,mode,page,query)
elif mode==55:mphim(name,url,img,fanart,mode,page,query)
elif mode==56:vtvgo(name,url,img,fanart,mode,page,query)
elif mode==57:vungtv(name,url,img,fanart,mode,page,query)
elif mode==58:biphim(name,url,img,fanart,mode,page,query)
elif mode==59:banhtv(name,url,img,fanart,mode,page,query)
elif mode==88:servers_list(name,url,img,fanart,mode,page,query)
elif mode==89:television(name,url,img,fanart,mode,page,query,text)
elif mode==90:end=fsharePage(name,url,img,fanart,query)
elif mode==91:main_menu(url,page,mode,query)
elif mode==92:vp_list(name,url,img,mode,page,query)
elif mode==93:vp_chonloc()
elif mode==94:end=subscene(name,url,query)
elif mode==95:tenlua_getlink(url)
elif mode==96:end=doc_thumuccucbo(name,url,img,fanart,mode,query)
elif mode==97:doc_list_xml(url,name,page)
elif mode==98:end=youtube(name,url,img,fanart,mode,page,query,text)
elif mode==98:vnzoom(name,url,img,fanart,mode,page,query)
elif mode==99:myaddon.openSettings();end='ok'
elif mode>100:myFavourites(name,url,img,fanart,mode,page,query)
if not end or end not in 'no-ok-fail':endxbmc()
#https://vip.clip.vn/