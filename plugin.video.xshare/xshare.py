# -*- coding: utf-8 -*-
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,urllib,re,os,unicodedata,datetime,random,json
import CommonFunctions as common

myaddon = xbmcaddon.Addon(); home = myaddon.getAddonInfo('path')
icon_path = xbmc.translatePath(os.path.join( home,'resources/media/'))
data_path = xbmc.translatePath(os.path.join( home,'resources/data/'))
datapath = xbmc.translatePath(os.path.join( xbmc.translatePath(myaddon.getAddonInfo('profile')),'data/'))
sys.path.append(xbmc.translatePath(os.path.join(home, 'resources', 'lib')))
import urlfetch
thumucrieng = 'https://www.fshare.vn/folder/'+myaddon.getSetting('thumucrieng')
thumuccucbo =  myaddon.getSetting('thumuccucbo');copyxml = myaddon.getSetting('copyxml')
if not os.path.exists(thumuccucbo):thumuccucbo=xbmc.translatePath( os.path.join(data_path,'list_xml/'))
phim18 = myaddon.getSetting('phim18');lastweekupdate=myaddon.getSetting('lastweekupdate')
rows = int(myaddon.getSetting('sodonghienthi'))
googlesearch=myaddon.getSetting('googlesearch')
if not os.path.exists(xbmc.translatePath(myaddon.getAddonInfo('profile'))):
	os.mkdir(xbmc.translatePath(myaddon.getAddonInfo('profile')))
if not os.path.exists(datapath):os.mkdir(datapath)

media_ext=['aif','iff','m3u','m4a','mid','mp3','mpa','ra','wav','wma','3g2','3gp','asf','asx','avi','flv','mov','mp4','mpg','mkv','m4v','rm','swf','vob','wmv','bin','cue','dmg','iso','mdf','toast','vcd','ts','flac']
hd = {'User-Agent' : 'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0','Cookie':''}
color={'Fshare':'[COLOR gold]','PhimFshare':'[COLOR khaki]','4share':'[COLOR blue]','TenLua':'[COLOR fuchsia]','fpt':'[COLOR orange]','trangtiep':'[COLOR lime]','search':'[COLOR lime]'}

def mess(message, timeShown=5000):
	xbmc.executebuiltin((u'XBMC.Notification("%s","%s",%s,%s)'%('Xshare',message,timeShown,icon_path+'icon.png')).encode("utf-8"))

def addir(name,link,img='',fanart='',mode=0,page=0,query='',isFolder=False):
	ok=True
	item = xbmcgui.ListItem(name,iconImage=img,thumbnailImage=img)
	if query.split('?')[0] in ['google','web','ID','File']:
		if query.split('?')[0] =='ID':call=15
		else:call=mode
		query=query.split('?')[1]
		command='RunPlugin(plugin://%s/?mode=%d&url=%s&query=%s&page=2)'%(myaddon.getAddonInfo('id'),call,link,query)
		command=[('[COLOR orangered]Xóa mục này[/COLOR]',command)]
		item.addContextMenuItems(command)
	item.setInfo(type="Video", infoLabels={"title":name})
	item.setProperty('Fanart_Image',fanart)
	u=sys.argv[0]+"?url="+urllib.quote_plus(link)+"&img="+urllib.quote_plus(img)+"&fanart="+urllib.quote_plus(fanart)+"&mode="+str(mode)+"&page="+str(page)+"&query="+query+"&name="+name
	if not isFolder:item.setProperty('IsPlayable', 'true')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=isFolder)
	return ok

def make_request(url, headers={'User-Agent':'xshare'}):
	try:
		response = urlfetch.get(url,headers=headers)
		hd['Cookie'] = response.headers.get('set-cookie')
		body = response.body#unicode: body=response.text
		response.close()
	except: mess('Make Request Error: %s'%url);body=''
	return body

def no_accent(s):
	s = s.decode('utf-8')
	s = re.sub(u'Đ', 'D', s)
	s = re.sub(u'đ', 'd', s)
	return unicodedata.normalize('NFKD', unicode(s)).encode('ASCII', 'ignore')

def tenlua_get_detail_and_starting(idf,h={'User-Agent':'xshare'}):
	data='[{"a":"filemanager_builddownload_getinfo","n":"'+idf+'","r":'+str(random.random())+'}]'
	try:
		response = urlfetch.post('https://api2.tenlua.vn/',data=data,headers=h,follow_redirects = False)
		link=json.loads(response.body)[0]
	except:link={'type':'none'}
	return link

def resolve_url(url,xml=False):
	if 'fshare.vn' in url.lower():hd['Cookie'] = loginfshare();url_out="https://www.fshare.vn/logout"
	elif '4share.vn' in url.lower():hd['Cookie'] = login4share();url_out="http://up.4share.vn/index/logout"
	elif 'tenlua.vn' in url.lower():
		hd['Cookie'] = logintenlua()
		try:
			if re.search('\w{14,20}',url):id_=re.search('\w{14,20}',url).group(0)
			else: id_=url.split('/download/')[1].split('/')[0]
			url=tenlua_get_detail_and_starting(id_,hd)['dlink']
		except:mess(u'Không get được max speed link!');return
	response = urlfetch.get(url, headers=hd, follow_redirects=False)
	if response.status == 302: url = response.headers['location']
	elif response.status == 200 and 'fshare.vn' in url.lower():
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
			pw = common.getUserInput('Hãy nhập mật khẩu của file này')
			if pw is None or pw=='':mess(u'Không get được max speed link!');return 'fail'
			data=urllib.urlencode({'fs_csrf':fs_csrf.group(2),'FilePwdForm[pwd]':pw})
			response=urlfetch.post(url,headers=hd,data=data,follow_redirects=False)
			if response.status == 302: url = response.headers['location']
			else:
				data={'speed':'fast','fs_csrf':fs_csrf.group(2)}
				href='https://www.fshare.vn/download/index';data=urllib.urlencode(data)
				try:url=urlfetch.post(href,headers=hd,data=data,follow_redirects=False).json['url'].encode('utf-8')
				except:url='fail'
		else:url='fail'
	elif response.status == 200 and '4share.vn' in url.lower():
		try:url = re.compile("<a href='(.+?)'> FileDownload").findall(response.body)[0]
		except:url='fail'
	else: mess("Get link that bai") ; url='fail'
	if myaddon.getSetting('logoutf')=="true":
		try:urlfetch.get("https://www.fshare.vn/logout",headers=hd,follow_redirects=False)
		except:print "Logout fail"
	if url=='fail':mess(u'Không get được max speed direct link!');return 'fail'
	if xml:return url
	if os.path.splitext(url)[1][1:].lower() not in media_ext:mess('sorry! this is not a media file');return 'fail'
	item = xbmcgui.ListItem(path=url);xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item);return ''

def loginfshare():
	url = "https://www.fshare.vn/login"
	form_fields = {
		"LoginForm[email]": myaddon.getSetting('usernamef'), 
		"LoginForm[password]": myaddon.getSetting('passwordf'),"LoginForm[rememberMe]": "0",
		"fs_csrf": re.search('value="(.+?)".*name="fs_csrf',make_request(url)).group(1)}
	response = urlfetch.post(url=url,headers=hd,data=urllib.urlencode(form_fields), follow_redirects=False)
	if response.status==302:mess(u'Login Fshare.vn thành công',timeShown=100);f=response.cookiestring
	else:mess(u'Login Fshare.vn không thành công');f=''
	return f
	
def login4share():
	url = 'http://up.4share.vn/index/login'
	form_fields = {"username":myaddon.getSetting('username4'),"password":myaddon.getSetting('password4')}
	response=urlfetch.post(url=url,headers=hd,data=urllib.urlencode(form_fields),follow_redirects=False)
	if response.status==302:mess(u'Login 4share.vn thành công');f=response.cookiestring
	else:mess(u'Login 4share.vn không thành công');f=''
	return f
	urlfetch.get("http://up.4share.vn/index/logout",headers=hd, follow_redirects=False)

def logintenlua():
	url = 'https://api2.tenlua.vn/';user=myaddon.getSetting('usernamet');pw=myaddon.getSetting('passwordt')
	form_fields = '[{"a":"user_login","user":"'+user+'","password":"'+pw+'","permanent":"true"}]'
	try:response=urlfetch.post(url=url,data=form_fields,follow_redirects=False)
	except:mess(u'Không truy cập được tenlua.vn');return ''
	if response.body=='[-1]':mess(u'Login tenlua.vn không thành công');f=''
	else:mess(u'Login tenlua.vn thành công');f=response.headers.get('set-cookie')
	return f
    
def logouttenlua():
	url = 'https://api2.tenlua.vn/'
	urlfetch.response(url=url,method='POST',headers=hd,data=urllib.urlencode({"a":"user_logout"}),follow_redirects=False)
	
def trangtiep(query,items):
	if 'Trang' in query.split('?')[0]:
		trang=int(query.split('?')[0].split('Trang')[1])
		query=query.split('?')[1]
	else:trang=1
	del items[0:(trang-1)*rows]
	trang+=1
	return trang,query,items
	
def google_search_api(url='',query='',page=0,mode=0,items=[]):
	fstring_search=datapath+"string_search.xml"
	colo={'Fshare':color['Fshare'],'4share':color['4share'],'TenLua':color['TenLua']}
	icon={'Fshare':icon_path+'Fshare.png','4share':icon_path+'4share.png','TenLua':icon_path+'TenLua.png','Icon':icon_path+'Icon.png'}
	if page==0:#Load search_file.xml
		if not os.path.isfile(fstring_search):
			makerequest(fstring_search,string='<?xml version="1.0" encoding="utf-8">\n',attr='w')
		name='%sGoogle[/COLOR] trên %s%s: [/COLOR]Nhập chuỗi tìm kiếm mới'%(color['search'],colo[url],url)
		addir(name,url,icon['Icon'],mode=mode,page=1,isFolder=True)
		items = re.findall('<a search="Google" server="%s">(.+?)</a>'%url,makerequest(fstring_search))
		trang,query,items=trangtiep(query,items)
		for string in items:
			addir(string,url,icon[url],query='google?'+string,page=3,mode=mode,isFolder=True)
			if (items.index(string)>rows) and (len(items)>int(rows*1.2)): 
				name=color['trangtiep']+'Trang tiep theo...trang %d[/COLOR]'%trang
				addir(name,url,icon[url],query='Trang'+str(trang)+'?'+query,mode=mode,page=0,isFolder=True)
				break
	elif page==1:
		string_search = common.getUserInput('Google: Hãy nhập chuỗi cần tìm trên %s.vn'%url)
		if string_search is None or string_search=='':return 'no'
		query = ' '.join(s for s in string_search.split(' ') if s!='')
		makerequest(fstring_search,string='<a search="Google" server="%s">%s</a>\n'%(url,query),attr='a')
		google_search_api(url,query=query,page=3)
	elif page == 2:#Xóa 1 mục search cũ có string=query
		items = re.findall('<a search="(.+?)" server="(.+?)">(.+?)</a>',makerequest(fstring_search))
		rows_string='<?xml version="1.0" encoding="utf-8">\n'
		for search,server,string in items:
			if string!=query or server!=url or search!="Google":
				rows_string+='<a search="%s" server="%s">%s</a>\n'%(search,server,string)
		if makerequest(fstring_search,string=rows_string,attr='w'):mess(u'Đã xóa mục: %s'%query.decode('utf-8'))
		else:mess(u'[COLOR orangered]Chưa xóa được mục: "%s"'%search_file.decode('utf-8'))
		xbmc.executebuiltin("Container.Refresh")
	elif page>2:
		if googlesearch=='Web':return google_search_web(url,query,page,items)
		google = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=large&'
		if '?' in query:
			if len(query.split('?'))==3:return google_search_web(url,query,page,items)
			start=query.split('?')[1];query=query.split('?')[0]
		else:start='0'
		string_search = urllib.quote_plus('"'+query+'"')
		href=google+'start=%s&q=site:%s.vn+%s'%(start,url.lower(),string_search)
		print href
		json=urlfetch.get(href,headers=hd).json
		if json['responseStatus']==403:
			mess(u'Google: nghi ngờ lạm dụng Dịch vụ. Tự động chuyển sang web search')
			return google_search_web(url,query,page,items)
		data=json['responseData']
		if not data or not data['results']:mess(u'Không tìm được tên phim phù hợp');return 'no'
		currentPage=int(data['cursor']['currentPageIndex'])+1;nextPage=0
		if not data['results']: results=[]
		else:results=data['results']
		for i in results:
			if url=='TenLua' and re.search('\w{16,20}/(.*)\Z',i['url'].encode('utf-8')):
				name=re.search('\w{16,20}/(.*)\Z',i['url'].encode('utf-8')).group(1)
			else: name=i['titleNoFormatting'].encode('utf-8')
			name=re.sub('<.{1,10}>|.{4,8}.vn|- ','',name.split(':')[0]).strip()
			if name and not 'Forum' in name:items.append((name,i['url'].encode('utf-8')));print i['url'].encode('utf-8')
		  
		for i in data['cursor']['pages']:
			if int(i['label'])>int(currentPage):
				nextPage=i['label'];start=i['start'];break
		if int(nextPage)>int(currentPage) and len(items)<rows and int(nextPage)<100:
			google_search_api(url,query=query+'?'+start.strip(),page=page,items=items)
		else:
			for name,link in sorted(items,key=lambda l:l[0]):addirs(name,link,icon[url])
			if int(nextPage)>int(currentPage):
				name=color['trangtiep']+'Trang tiep theo...trang %s[/COLOR]'%str(page-1)
				addir(name,url,icon[url],mode=mode,query=query+'?'+start.strip(),page=page+1,isFolder=True)
	return ''
	
def google_search_web(url='',query='',page=0,items=[]):
	google = 'https://www.google.com.vn';num='8';nextStart=''
	if '?' in query:start=query.split('?')[1];query=query.split('?')[0]
	else:start='0';page=3
	query = ' '.join(s for s in query.split(' ') if s!='')
	string_search = urllib.quote_plus('"'+query+'"')
	href=google+'/search?hl=en&ie=utf-8&oe=utf-8&num=%s&start=%s&q=site:%s.vn+%s'%(num,start,url.lower(),string_search)
	print href
	body=urlfetch.get(href).body
	if '<TITLE>302 Moved</TITLE>' in body:mess(u'Google từ chối dịch vụ do bạn đã truy cập quá nhiều');return 'no'
	#links=re.findall('(https?://www.fshare.vn/\w{4,6}/\w{10,20})["|&].*">(.+?)</a></h3>',body)
	links=re.findall('<a href=".url.q=(.+?)["|&].*">(.+?)</a></h3>',body)
	for link,name in links:
		name=re.sub('<.{1,10}>|.{4,8}.vn|..hare|- ','',name.split(':')[0]).strip()
		if name and not 'Forum' in name:items.append((name,link));print link
	for i in re.findall('start=(\d{1,4})',body):
		if int(i)>int(start):nextStart=i;break
	if nextStart and len(items)<rows and int(start)<100:google_search_web(url,query+'?'+nextStart,page,items)
	elif len(items)>0:
		for name,link in sorted(items,key=lambda l:l[0]):addirs(name,link,icon_path+'%s.png'%url);print link
		if nextStart:
			name=color['trangtiep']+'Trang tiep theo...trang %s[/COLOR]'%str(page-1)
			addir(name,url,icon_path+'%s.png'%url,mode=2,query=query+'?'+nextStart+'?web',page=page+1,isFolder=True)
			#print body
	return ''

def open_category(query): #category.xml
	pattern='<a server="(...)" category="(.+?)" mode="(..)" color="(.*?)" icon="(.*?)">(.+?)</a>'
	items=re.findall(pattern,makerequest(data_path+'category.xml'))
	if query in 'VPH-IFI-PFS' :
		if not download_data():return
		elif query=='PFS':updatePFS()
		elif query=='VPH':vp_update_rss()
	for server,category,mode,colo,icon,name in items:
		if (server!=query) or (("18" in category) and (phim18=="false")):continue
		if query=='VPH' and mode!='10':q='vaphim-1.xml'
		elif query=='IFI' and mode!='10':q='ifiletv-1.xml'
		else:q=category
		name='[COLOR '+colo+']'+name+'[/COLOR]';icon=icon_path+icon
		addir(name,category,icon,home+'/fanart.jpg',mode=int(mode),page=0,query=q,isFolder=(mode!='16'))

def main_menu(category,page,mode,query): #Doc list tu vaphim-?.xml hoac ifiletv.xml
	filenow = q = query;
	filenext=q.rsplit('.')[0].rsplit('-')[0]+'-'+str(int(q.rsplit('.')[0].rsplit('-')[1])+1)+'.'+q.rsplit('.')[1]
	items = doc_xml(datapath+filenow,para=category)
	del items[0:page*rows]
	for id,img,fanart,href,name in items:
		if ('18+' not in name) or (phim18=="true"):addirs(name,href,img,fanart)
		if (items.index((id,img,fanart,href,name))>rows) and (len(items)>int(rows*1.2)): break
	if len(items) < int(rows/2) and (filenext in os.listdir(datapath)):
		main_menu(category,0,mode,filenext)
	elif len(items) > int(rows*1.2):
		addir(color['trangtiep']+'Trang tiep theo...[/COLOR]',category,home+'/icon.png',mode=mode,page=page+1,query=query,isFolder=True)
	elif len(items) <= int(rows*1.2) and (filenext in os.listdir(datapath)):
		addir(color['trangtiep']+'Trang tiep theo...[/COLOR]',category,home+'/icon.png',mode=mode,page=0,query=filenext,isFolder=True)

def doc_xml(url,filename='',para=''): 
	if (datapath in url) or (thumuccucbo in url):body=makerequest(url)
	else:body=make_request(resolve_url(url,xml=True), headers=hd)
	
	if ('vaphim' in url) or ('ifiletv' in url): # doc file trong thu muc data
		if not para:r="<a id_tip=\"(.*?)\" id=\"(.+?)\" category=\"(.*?)\" img=\"(.*?)\" fanart=\"(.*?)\" href=\"(.+?)\">(.+?)</a>"
		elif para=='post1': r="id=\"(.+?)\""
		elif para[:6]=='search':
			r="<a id_tip=\"(.*?)\" id=\"(.+?)\" category=\"(.*?)\" img=\"(.*?)\" fanart=\"(.*?)\" href=\"(.+?)\">(.*"+para[7:]+".*)</a>"
			item1=re.compile(r, re.I).findall(body);id1=[]
			item2=re.compile(r, re.I).findall(no_accent(body))
			for i in item1:id1.append((i[1]))
			for i in item2:
				if i[1] not in id1:item1.append((i))
			return sorted(item1,key=lambda l:l[1], reverse=True)
		else: # Doc theo category
			r="<a.*id=\"(.+?)\" category=\".*"+para+".*\" img=\"(.*?)\" fanart=\"(.*?)\" href=\"(.+?)\">(.+?)</a>"
		items = sorted(re.compile(r).findall(body),key=lambda l:l[1], reverse=True)
	else: # Doc cac list xml khac
		r="<a.+id=\"(.*?)\".+href=\"(.+?)\".+img=\"(.*?)\".+fanart=\"(.*?)\".*>(.+?)</a>"
		items = re.compile(r).findall(body)
		if len(items)<1:items = re.compile(".+()href=\"(.+?)\".+img=\"(.*?)\".*()>(.+?)</a>").findall(body)
		if len(items)<1:items = re.compile(".+()href=\"(.+?)\".*()()>(.+?)</a>").findall(body)
		if (copyxml=="true") and ('http' in url) and (len(items)>0) :
			filename=no_accent(filename)
			filename = filename[:filename.lower().find('.xml')+4].replace('[COLOR gold]','').replace('[/COLOR]','')
			if not os.path.isfile(thumuccucbo+filename):
				f=open(thumuccucbo+filename,'w')
				f.write('<?xml version="1.0" encoding="utf-8">\n')
				for id,href,img,fanart,name in items:
					f.write('<a id="'+id+'" href="'+href+'" img="'+img+'" fanart="'+fanart+'">'+name+'</a>\n')
				f.close()
				mess(u'Đã ghi file %s vào Thư mục riêng trên máy'%filename)
	return items
	
def update_xml(items_new,items_old,filename): #update vaphim,ifiletv xml
	items = sorted(items_new+items_old,key=lambda l:l[1],reverse=True)
	content='<?xml version="1.0" encoding="utf-8">\n'
	for id_tip,id_htm,category,img,fanart,href,fullname in items:
		content+='<a id_tip="%s" id="%s" category="%s" img="%s" fanart="%s" href="%s">%s</a>\n'%(id_tip,id_htm,category,img,fanart,href,fullname)
	try:
		f=open(datapath+filename,'w')
		f.write(content);f.close()
		mess(u"Đã cập nhật được %d phim"%len(items_new))
	except: mess(u'Đã xảy ra lỗi cập nhật')
	return

def vp_update():
	items_old, id_old = read_items_old("vaphim-1.xml")
	mess(u'Đang kiểm tra dữ liệu cập nhật của Vaphim...')

	new_items = vaphim_page('http://vaphim.com/category/phim-2/');items_new=[]
	for id_tip,id_htm,category,href in new_items:
		if id_htm not in id_old:
			try:
				for img,fanart,href,fullname in vp2fshare(href): # vp2fshare:img,fanart,href,fullname
					items_new.append((id_tip,id_htm,category,img,fanart,href,fullname))
			except:
				print "=== Loi === "+href+" \n"
				continue
	if items_new:update_xml(items_new,items_old,"vaphim-1.xml")
	else:mess(u'Không có phim mới...')
	return 'ok'

def download_data():
	check=True
	if not os.path.isfile(datapath+"vaphim-1.xml"):
		mess(u'Đang download danh mục Vaphim.com, ifile.tv')
		for filename in os.listdir(datapath):
			if filename in ['ifiletv-1.xml','vaphim-2.xml','data.zip','phimfshare.xml']:
				try:os.remove(os.path.join(datapath, filename))
				except:return False
		data=re.search('href="(.+?)" title="data.zip"',urlfetch.get('https://www.fshare.vn/folder/GZCI8AHAQJ75').body)
		if not data:mess(u'Không download được data files!');check=False
		else:
			data=data.group(1)
			url=resolve_url(data.replace('http:','https:'),True)
			if url=='fail':mess(u'Bạn hãy set user,pass acc VIP Fshare');check=False
			else:
				body=urlfetch.get(url).body
				tempfile = os.path.join(datapath, "data.zip")
				f = open(tempfile, "wb");f.write(body);f.close()
				xbmc.sleep(500)
				xbmc.executebuiltin(('XBMC.Extract("%s","%s")' % (tempfile, datapath,)), True)
		if not os.path.isfile(datapath+"vaphim-1.xml"):
			mess(u'Không tải được dữ liệu vaphim.com.ifile.tv,phimfshare.com!')
			check=False
	return check
	
def vp_update_rss():
	from xml.etree import ElementTree as etree
	id_old=re.findall('id="(\d{5})" category',makerequest(datapath+"vaphim-1.xml"))
	category={'Phim Lẻ':'phim-le','Phim Bộ':'series','Phim Bộ Hàn':'korean-series','Phim Bộ Hồng Kông':'hongkong-series','Phim Bộ Mỹ':'us-tv-series','Phim Tài Liệu':'documentary','Phim 18+':'18','Hoạt Hình':'animation','Huyền Bí':'mystery','Viễn Tưởng':'sci-fi','3D':'3d','Cao Bồi':'western','Chiến Tranh':'war','Thiếu Nhi':'family','Hài Hước':'comedy','Hành Động':'action','Hình Sự':'crime','Rùng Rợn':'thriller','Tâm Lý':'drama','TVB':'tvb','Kinh Dị':'horror','Lãng Mạn':'romance','Lịch Sử':'history','Phiêu Lưu':'adventure','Thần Thoại':'fantasy','Thuyết Minh':'thuyet-minh-tieng-viet','Hồng Kông':'hongkong','Ấn Độ':'india','Việt Nam':'vietnamese','Hàn Quốc':'korean'}
	url='http://feed.vaphim.com/category/phim-2/feed/'
	reddit_file = urlfetch.get(url).body
	reddit_file = reddit_file.replace('content:encoded','contentencoded')
	try:reddit_root = etree.fromstring(reddit_file);items = reddit_root.findall('channel/item')
	except:mess('Update rss fail',1000);return
	content_new=''
	#reddit_feed=[]
	for item in items:
		idf=re.search('(\d{5})',item.findtext('guid'))
		if idf:idf=idf.group(1)
		else:continue
		if idf in id_old:continue
		name=item.findtext('title')
		pattern='(https?://www.fshare.vn/\w{4,6}/\w{10,14})'
		content=item.findtext('contentencoded')
		img=re.search('img src="(.+?jpg)["|?| ]',content)
		if img:img=re.sub('-134x193','',img.group(1))
		else:img=''
		cat=''
		for i in item.findall('category'):
			if i.text.encode('utf-8') in category:
				cat+=category[i.text.encode('utf-8')]+' '
			else:break
		cat=cat.strip()
		for link in re.findall(pattern,content):
			link=link.lower();idp=re.search('(\w{10,14})',link).group(1)
			if 'fshare.vn/file' in link:url='https://www.fshare.vn/file/%s'%idp.upper()
			else:url='https://www.fshare.vn/folder/%s'%idp.upper()
			content_new+='<a id_tip="" id="%s" category="%s" img="%s" fanart="%s" href="%s">%s</a>\n'%(idf,cat,img,img,url,name)
	if content_new:
		makerequest(datapath+"vaphim-1.xml",string=content_new,attr='a');mess('updated from VaPhim.com')
		mess('Vaphim data Auto update completed')

def vaphim_page(url):
	soup = make_request(url, headers=hd);items_new = []
	items = re.compile('<li class="post-(.+?)">\s*.*\s*<a data="(.+?)" title=.+href="(.+?)">').findall(soup)
	if str('<h2>Search Results</h2>') in soup :return []
	for category,ID,href in items:
		if ('game' not in category) and ('video' not in category) and ('phn-mm' not in category):
			category=' '.join([s[s.find('-')+1:] for s in category.rsplit(' ') if 'category' in s])
			items_new.append(('',ID,category,href))
	return items_new #vaphim_page1(url):'',ID,category,href

def clean_string(string):
	return ''.join(re.split('&\S+',string)).strip()

def vp2fshare(url):
	soup = make_request(url, headers=hd)
	items = re.compile('<meta itemprop=.+"(.+?)"').findall(soup)
	try:
		name = clean_string(items[0])
		img = items[1]
	except:name=img=''
	
	items=re.compile('<a.+<img src=\"(.+?)\?.+size-full').findall(soup)
	try:fanart = items[0]
	except:fanart = ''
	
	items = re.compile("<a.+href=.+(www.fshare.vn.+?)\".*>(.+?)</a>").findall(soup);combs = []
	for href,name2 in items:
		href = 'https://'+href
		name2 = name+' - '+clean_string(name2)
		code = urlfetch.get(url = href, follow_redirects = False).status
		if code == 404:print 'Loi 404: %s'%href;continue
		elif code != 200:err = 'Error fetch Fshare: %s url=%s '%(code,url);print err
		combs.append((img,fanart,href,name2))
	return combs #(img,fanart,href,fullname)

def vp_xemnhieu():
	body = makerequest(data_path+"vp_xemnhieu.xml")
	list_old = re.compile('<a url="(.+?)" img="(.*?)" fanart="(.*?)" href="(.+?)">(.+?)</a>').findall(body)
	url_old = re.compile('<a url="(.+?)"').findall(body)
	
	body = make_request("http://vaphim.com/request/", headers=hd)
	url_new = re.compile('<li><a href="(http://vaphim.com.+?)"').findall(body);list_new=[];ghifile=False
	for urlnew in url_new:
		if urlnew not in url_old: #vp2fshare(url):img,fanart,href,fullname
			for img,fanart,href,fullname in vp2fshare(urlnew): 
				list_new.append((urlnew,img,fanart,href,fullname));ghifile=True
		else:list_new.append((list_old[url_old.index(urlnew)]))
			
	if ghifile:
		content='<?xml version="1.0" encoding="utf-8" mode="91">\n'
		for url,img,fanart,href,name in list_new:
			content='<a url="%s" img="%s" fanart="%s" href="%s">%s</a>\n'%(url,img,fanart,href,name)
			addirs(name,href,img,fanart,url)
		f=open(data_path+"vp_xemnhieu.xml",'w');f.write(content);f.close()
	else:
		for url,img,fanart,href,name in list_new:addirs(name,href,img,fanart,url)

def menu_xml(url,filename='',page=0):
	if not page:items=doc_xml(url,filename=filename);f=open(data_path+'temp.txt','w');f.write(str(items));f.close()
	else:f=open(data_path+'temp.txt');items=eval(f.readlines()[0]);	f.close()
	del items[0:page*rows]
	for id,href,img,fanart,name in items:
		if '47daklak.com' in href: addir(name,href,img,mode=47)
		else: addirs(name,href,img,fanart)
		if (items.index((id,href,img,fanart,name))>rows) and (len(items)>int(rows*1.2)): break
	if len(items) > int(rows*1.2):
		addir('Trang tiep theo...',url,icon_path+'khophim.png',mode=97,page=page+1,isFolder=True)

def daklak47(name,url,img):
	reps = urlfetch.get(url)
	if reps.status==302:
		req=reps.headers['location']
		url = req.replace('http:','https:')
		if 'www.fshare.vn/folder/' in url:mess(u"Chưa xử lý trường hợp đọc folder trên 47daklak.com");return
		else:resolve_url(url)
	else: mess("Khong tim thay link tren "+url)

def phimchon(url,filename,re_string):
	if "index" in url:
		data = urllib.urlencode({'type':'special_filter','filter_by_view_desc':'1'})
		fetch = urlfetch.fetch(url+"/filter",method='POST',headers=hd,data=data,follow_redirects=False)
		hd['Cookie']=fetch.headers.get('set-cookie')
	id_new = re.compile(re_string).findall(urlfetch.fetch(url).body)
	items_old, id_old = read_items_old(filename);items_new=[]
	for ID in id_new:
		try:
			i = id_old.index(ID)
			if ('18+' not in items_old[i][6]) or (phim18=="true"):
				while id_old[i] == ID:	
					addirs(items_old[i][6],items_old[i][5],items_old[i][3],items_old[i][4])
					i+=1
		except:continue

def DocTrangFshare(url,img,fanart,query=''):
	if 'pageIndex' in url:
		pageIndex=int(url.split('?')[1].split('=')[1]);filescount=int(url.split('?')[2].split('=')[1])
		rowscount=int(url.split('?')[3].split('=')[1])
	else:pageIndex=filescount=rowscount=0
	response = urlfetch.fetch(url).body
	try:name=re.search('<title>Fshare - (.+?)</title>',response).group(1)
	except:name='No name'
	name_return=name
	try:files_count=int(re.search('Số lượng:(.+?)</div>',response).group(1))
	except:files_count=filescount
	if '/file/' in url:
		try:size=re.search('width="29".*\s.*<td>(.+?)</td>',response).group(1)
		except:size=''
		items=[(url,name,size)]
	else:
		items = re.compile('<div.+href="(.+?)".+title="(.+?)".*\s*.*\s*.*\s*<div class="pull-left file_size align-right">(.+?)</div>').findall(response)
	for href,name,size in items:
		if ('/folder/' in href) and ('?p=' in href): #Thu muc con
			href=check_id_fshare(name[:name.find(' ')])
			name=name[name.find(' ')+1:]
		if 'www.fshare.vn/file' in href:
			if name[-3:] in 'xmlXML':query='xml'
			if len(size)>2:name=name+" - "+size
		addirs(name,href.replace('http:','https:'),img,fanart,query)
	rowscount+=len(items)
	if ('/folder/' in url) and (rowscount<files_count):
		files_count=str(files_count);rowscount=str(rowscount);page=str(pageIndex+2);pageIndex=str(pageIndex+1)
		url=url.split('?')[0]+'?pageIndex=%s?files_count=%s?rows_count=%s'%(pageIndex,files_count,rowscount)
		print url
		name=color['trangtiep']+'Trang tiep theo...trang %s[/COLOR]'%page
		addir(name,url,img,fanart,mode=90,query=query,isFolder=True)
	return name_return

def DocTrang4share(url):#38
	response=urlfetch.get(url).body
	pattern="<a href='(.+?)' target='.+?'><image src = '.+?'>(.+?)<.*?><td style='text-align: right'>(.+?)</td>"
	pattern+="|<a href='(.+?)'>.*\s.*<image src = '.+?'>(.+?)</a>"
	for href,name,size,folder_link,folder_name in re.findall(pattern,response):
		if href:name=name.strip()+' - '+size.strip();href='http://4share.vn'+href
		else:href='http://4share.vn'+folder_link;name=folder_name.strip()
		addirs(name,href)
	
def doc_thumuccucbo():
	for dirname, dirnames, filenames in os.walk(thumuccucbo):
		for filename in filenames:
			if filename.lower() in "vp_xemnhieu.xml-category.xml-vaphim-1.xml-vaphim-2.xml-search.xml":continue
			filenamefullpath = os.path.join(dirname, filename)
			file_ext = os.path.splitext(filenamefullpath)[1]
			if (file_ext[1:].lower() in media_ext):
				item = xbmcgui.ListItem(filename, iconImage=icon_path+'khophim.png')
				xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=filenamefullpath, listitem=item)
			if (file_ext[1:].lower() == 'xml'):addirs(filename,filenamefullpath,query='xml')

def Mo_maxspeed_link(): 
	query = common.getUserInput('Hãy nhập max speed link của Fshare, 4share hoặc tênlửa','')
	if query is None or query=='':return 'no'
	query = query.replace(' ','')
	if len(query)<50:mess(u'Bạn nhập link ID chưa đúng: '+query);return 'no'
	item = xbmcgui.ListItem(path=query)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

def lay_link_tenlua(href):
	if re.search('\w{14,20}',href):idf=re.search('\w{14,20}',href).group(0)
	else:return
	response=tenlua_get_detail_and_starting(idf)
	if response["type"]=="none": mess(u'Không truy cập được tenlua.vn')
	elif response["type"]=="file":
		name=response['n'].encode('utf-8');url="https://www.tenlua.vn/download/"+idf
		addir(name,url,mode=3)
	elif response["type"]=="folder":
		for item in response['content']:
			lay_link_tenlua(item['link'])
	
def addirs(name,href,img='',fanart='',query=''):
		if query=='xml':addir(color['Fshare']+name+'[/COLOR]',href,img,fanart,mode=97,isFolder=True)
		elif ('www.fshare.vn/file' in href) and ('Ph\xe1\xbb\xa5 \xc4\x90\xe1\xbb\x81 Vi\xe1\xbb\x87t' not in name):
			addir(name,href,img,fanart,mode=3,query=query)
		elif 'www.fshare.vn/folder' in href:
			addir(color['Fshare']+name+'[/COLOR]',href,img,fanart,mode=90,query=query,isFolder=True)
		elif '4share.vn/d/' in href:
			addir(color['4share']+name+'[/COLOR]',href,img,fanart,mode=38,query=query,isFolder=True)
		elif '4share.vn' in href:
			addir(name,href,img,fanart,mode=3,query=query)
		elif 'tenlua.vn/fm/folder/' in href or '#download' in href:
			addir(color['TenLua']+name+'[/COLOR]',href,img,fanart,mode=95,query=query,isFolder=True)
		elif 'tenlua.vn' in href:
			addir(name,href,img,fanart,mode=3,query=query)

def check_id_fshare(ID):
	ID=ID.upper()
	if re.search('download_folder',urlfetch.fetch('https://www.fshare.vn/folder/'+ID).body):
		url='https://www.fshare.vn/folder/'+ID
	elif re.search('pull-right file_info',urlfetch.fetch('https://www.fshare.vn/file/'+ID).body):
		url='https://www.fshare.vn/file/'+ID
	else:url=''
	return url

def makerequest(file,string='',attr='r'):
	if attr=='r':
		try:f=open(file);body=f.read();f.close()
		except:mess('Loi mo file: %s'%file);body=''
	else:
		if 'unicode' in str(type(string)):string=string.encode('utf-8')
		try:f=open(file,attr);f.write(string);f.close();body='ok'
		except:mess('Loi mo file: %s'%file);body=''
	return body

def mo_id_file(url,name='',mode=0,page=0,query=''):
	fstring_search=datapath+"string_search.xml";fresult_search=datapath+'result_search.xml'
	colo={'Vaphim':color['Fshare'],'Ifile':color['4share']}
	icon={'Fshare':icon_path+'Fshare.png','4share':icon_path+'4share.png','TenLua':icon_path+'TenLua.png'}
	if query=='Myshare':query=thumucrieng;page=3
	if page==0:#Load id_file.xml, query=['Fshare','4share','TenLua']
		if not os.path.isfile(fstring_search):
			makerequest(fstring_search,string='<?xml version="1.0" encoding="utf-8">\n',attr='w')
		addir('Nhập '+color[url]+url+'[/COLOR] ID mới','',icon[url],mode=mode,query=query,page=1,isFolder=True)
		items = re.findall('<a search="ID" server="(.+%s.+)">(.+?)</a>'%url.lower(),makerequest(fstring_search))
		trang,query,items=trangtiep(query,items)
		for href,name in items:
			addirs(name,href,icon[query],query='ID?'+query)
			if (items.index((href,name))>rows) and (len(items)>int(rows*1.2)):
				name=color['trangtiep']+'Trang tiep theo...trang %d[/COLOR]'%trang
				addir(name,url,mode=mode,page=trang,query='Trang'+str(trang)+'?'+query,isFolder=True)
				break
	elif page == 1:#Nhập ID mới
		id_ = common.getUserInput('Hãy nhập chuỗi "xxxxxxxxxxxx" ID link của '+query)
		if id_ is None or id_=='':return 'no'
		id_ = id_.replace(' ','').strip().upper()
		if len(id_)<10:mess(u'Bạn nhập ID link chưa đúng: '+id_);return 'no'
		write_id=True
		if query=='Fshare':
			url=check_id_fshare(id_)
			if url:name=DocTrangFshare(url,icon[query],'')
			else:write_id=False
		elif query=='4share':
			share4_f='http://4share.vn/f/';share4_d='http://4share.vn/d/'
			if urlfetch.get(share4_f+query).status==200:url=share4_f+id_
			elif urlfetch.get(share4_d+query).status==200:url=share4_d+id_
			name=re.compile('<center>Filename.*<strong>(.+?)</strong>.*<strong>(.+?)</strong>').findall(make_request(url))
			try:name=name[0][0]+' - '+name[0][1];
			except:mess(u'Không tìm được link có ID: '+id_);write_id=False
			addirs(name,url,icon[query])
		elif query=='TenLua':
			response=tenlua_get_detail_and_starting(id_)
			if response["type"]=="none": mess(u'Không tìm được link có ID: '+id_);write_id=False
			elif response["type"]=="file":name=response['n'];url="https://www.tenlua.vn/download/"+id_
			elif response["type"]=="folder":name=response["folder_name"];url="https://www.tenlua.vn/fm/folder/"+id_
			addirs(name,url,icon[query])
		if write_id:
			string='<a search="ID" server="%s">%s</a>\n'%(url,name)
			makerequest(fstring_search,string=string,attr='a')
	elif page == 2:#Xóa 1 ID cũ có href=url
		items = re.compile('<a search="(.+?)" server="(.+?)">(.+?)</a>').findall(makerequest(fstring_search))
		rows_string='<?xml version="1.0" encoding="utf-8">\n';name=''
		for search,server,string in items:
			if server!=url or search!="ID":
				rows_string+='<a search="%s" server="%s">%s</a>\n'%(search,server,string)
			else:name=string
		if makerequest(fstring_search,string=rows_string,attr='w'):mess(u'Đã xóa mục: %s'%name.decode('utf-8'))
		else:mess(u'[COLOR orangered]Chưa xóa được mục: "%s"'%search_file.decode('utf-8'))
		xbmc.executebuiltin("Container.Refresh")
	elif page == 3:#Mở thư mục chia sẻ trên Fshare
		DocTrangFshare(query,icon_path+'fshare.png','')
	return ''

def ifile_tv_page(url):
	items=[]
	try: 
		r='id="(.+?)".*\s.*\s.*<a href="(.+?)".*\s.*src="(.+?)".\s*</a>\s*</div>\s*.*\s.*"red">(.+?)</font>'
		item = re.compile(r).findall(make_request(url))
		for id_tip,href,img,name in item:
			http='http://ifile.tv';href=http+href;id_htm=href.rsplit('.')[2];img=http+img;name=name.strip()
			items.append((id_tip,id_htm,href,img,name))
	except:print 'ifile_tv_page Error: '+ url
	return items #id_tip,id_htm,href,img,name

def ifile_tv_4share(url):
    items = []
    try:
        body = make_request(url)
        href = re.compile("href='(http://4share.+?)'").findall(body)
        
        try: fanart = re.search("<img src= '(.+?)' style='width: 100%'>",body).group(1)
        except:fanart=''
        catalog = ' '.join([i.rpartition('/')[2].rsplit('.')[0] for i in re.compile("href='/(.+?)'>.+?</a></u>").findall(body)])
        for url4share in href:
            try:
                url4share = urllib.unquote(url4share);name2=''
                if len(url4share.rpartition('/')[0])>20:name2=url4share.rpartition('/')[2]
                items.append((url4share,'http://ifile.tv'+fanart,name2,catalog))
            except:print 'url4share Error: '+ url4share;continue
    except:print 'ifile_tv_4share Error: '+ url
    return items

def ifile_update():
	items_old, id_old = read_items_old("ifiletv-1.xml")
	mess(u'Đang kiểm tra dữ liệu cập nhật của ifile.tv...')
	items_new = []#id_tip,id_htm,href,img,name
	for id_tip,id_htm,href,img,name in ifile_tv_page('http://ifile.tv/') :
		if id_htm not in id_old:
			try:
				for url4share,fanart,name2,catalog in ifile_tv_4share(href):
					if name2 != '':fullname = name+' - '+name2
					else:fullname=name
					items_new.append((id_tip,id_htm,catalog,img,fanart,url4share,fullname))
			except:print "=== Loi === "+href+" \n";continue
	if items_new:update_xml(items_new,items_old,"ifiletv-1.xml")
	else:mess(u'Không có phim mới...')
	return 'ok'
	
def read_items_old(filename):
	items_old = doc_xml(datapath+filename);id_old=[]
	for i in items_old:id_old.append((i[1]))
	return items_old, id_old

def read_all_filexml(fn="vaphim-1.xml",string_search='',lists=[],index=[]):
	while fn in os.listdir(datapath):
		if string_search:lists = lists+doc_xml(datapath+fn,para='search:'+string_search)
		else:lists = lists+doc_xml(datapath+fn)
		fn = fn.rsplit('.')[0].rsplit('-')[0]+'-'+str(int(fn.rsplit('.')[0].rsplit('-')[1])+1)+'.'+fn.rsplit('.')[1]
	if not string_search:
		for id_tip,id_htm,category,img,fanart,url,name in lists:index.append((id_htm))
	return lists,index

def search_noibo(name,url,mode,page,query):
	server={'vaphim-1.xml':'Fshare','ifiletv-1.xml':'4share'}
	colo={'vaphim-1.xml':color['Fshare'],'ifiletv-1.xml':color['4share']}
	icon={'vaphim-1.xml':icon_path+'Fshare.png','ifiletv-1.xml':icon_path+'4share.png'}
	fstring_search=datapath+"string_search.xml"
	tempfile=data_path+'temp.txt'
	if page==0:#Search link Fshare trên dữ liệu nội bộ
		string='%sSearch %slink %s[/COLOR][/COLOR] trên dữ liệu nội bộ: Nhập chuỗi tìm kiếm mới'%(color['search'],colo[url],server[url])
		addir(string,url,icon[url],mode=mode,page=1,query=query,isFolder=True)
		items = re.findall('<a search="File" server="%s">(.+?)</a>'%server[url],makerequest(fstring_search))
		trang,query,items=trangtiep(query,items)
		for string in items:
			addir(string,url,icon[url],query='File?'+string,page=3,mode=mode,isFolder=True)
			if (items.index(string)>rows) and (len(items)>int(rows*1.2)): 
				name=color['trangtiep']+'Trang tiep theo...trang %d[/COLOR]'%trang
				addir(name,url,icon[url],query='Trang'+str(trang)+'?'+query,mode=mode,page=0,isFolder=True)
				break
	elif page==1:
		string = common.getUserInput('Nhập chuổi tên phim cần tìm link %s trên dữ liệu nội bộ'%server[url])
		if not string or string.strip()=='':return 'no'
		string = ' '.join(s for s in string.split(' ') if s!='' and s!='"' and s!="'")
		makerequest(fstring_search,string='<a search="File" server="%s">%s</a>\n'%(server[url],string.replace('"',"'")),attr='a')
		search_noibo(string,url,mode,page=3,query=query)
	elif page==3:
		if '?' in query:
			f=open(tempfile);items=eval(f.readlines()[0]);f.close()
		else:
			string = ".*".join(name.split())
			items,index=read_all_filexml(fn=url,string_search=string)
			if not items:mess(u'Không tìm thấy phim nào có chuổi phù hợp');return 'no'
			makerequest(tempfile,string=str(items),attr='w')
		trang,query,items=trangtiep(query,items)
		for id_tip,id_htm,catalog,img,fanart,link,name in items:
			if ('18+' not in name) or (phim18=="true"):addirs(name,link,img,fanart)
			if (items.index((id_tip,id_htm,catalog,img,fanart,link,name))>rows) and (len(items)>int(rows*1.2)): 
				addir(color['trangtiep']+'Trang tiep theo...trang %d[/COLOR]'%trang,url,icon[url],mode=mode,page=3,query='Trang'+str(trang)+'?'+query,isFolder=True)
				break
	return ''
	
def search_web_detail(string,server,mode):
	items_new=[]
	if server=='Vaphim':
		items = vaphim_page('http://vaphim.com/?s=%s'%urllib.quote_plus(string))
		if not items:
			mess(u'Không tìm được tên phim phù hợp. Nếu có thể, hãy thay thế cụm từ tìm kiếm bằng tiếng Anh hoặc tiếng Việt có dấu')
			return []
		items_xml,id_xml = read_all_filexml()
		for id_tip,id_htm,category,href in items:
			if id_htm in id_xml:
				index = id_xml.index(id_htm)
				while id_xml[index] == id_htm:
					items_new.append((items_xml[index]));index +=1 
			else:
				for img,fanart,link,name in vp2fshare(href):
					items_new.append((id_tip,id_htm,category,img,fanart,link,name))
	elif server=='Ifile':
		href = 'http://ifile.tv/search?search_module=phim&search_name=1&'
		href += 'search_content=1&time_sort=new&search_string="%s"'%urllib.quote_plus(string)
		bodys = re.findall("<td>(.*?)</b>",urlfetch.fetch(href).body);items = []
		for body in bodys:
			items+=re.findall("<a.+href='(.+?)'.+src='(.+?)'.+(\d\d\d\d\d).+>(.+?)</a>",body)
		if not items:mess(u'Không tìm được tên phim phù hợp');return []
		items_xml,id_xml = read_all_filexml(fn="ifiletv-1.xml")
		for href,img,id_htm,name in items:
			if id_htm in id_xml:
				index = id_xml.index(id_htm)
				while id_xml[index] == id_htm:
					items_new.append((items_xml[index]));index +=1 
			else:
				for url4share,fanart,name2,catalog in ifile_tv_4share('http://ifile.tv'+href):
					items_new.append(('',id_htm,catalog,img,fanart,url4share,name))
	elif server=='TenLua':
		if 'Trang' in string.split('?')[0]:
			trang=int(string.split('?')[0].split('Trang')[1])
			string=string.split('?')[1]
		else:trang=1
		pattern = '<a server="TenLua" page="%d" string="%s">(.+?)</a>'%(trang,string)
		res = re.search(pattern,makerequest(datapath+'result_search.xml'))
		if res:
			items=eval(res.group(1))
			for name,href in items:addirs(name,href,icon_path+'tenlua.png')
			name=color['trangtiep']+'Trang tiep theo...trang %d[/COLOR]'%(trang+1)
			addir(name,url,icon_path+'tenlua.png',mode=mode,page=3,query='Trang%d'%(trang+1)+'?'+query,isFolder=True)
			return ''
		href='https://api2.tenlua.vn/search?keyword=%s&page=%d'%(urllib.quote_plus(string),trang)
		response = urlfetch.get(href).json
		if int(response['pagging']['total'])==0:mess(u'Không tìm được tên phim phù hợp');return []
		new_result=[]
		for item in response['items']:
			if item is None or item['ext'] not in media_ext:continue
			id_=item['h']
			res=tenlua_get_detail_and_starting(id_)
			if res["type"]=="none": print item['h'];continue
			elif res["type"]=="file":name=res['n'];href="https://www.tenlua.vn/download/%s"%id_
			elif res["type"]=="folder":name=res["folder_name"];href="https://www.tenlua.vn/fm/folder/%s"%id_
			new_result.append((name,href))
			addirs(name,href,icon_path+'tenlua.png')
		if new_result:
			new_string='<a server="TenLua" page="%d" string="%s">%s</a>\n'%(trang,string,str(new_result))
			makerequest(datapath+'result_search.xml',string=new_string,attr='a')
		if int(response['pagging']['pages'])>trang:
			name=color['trangtiep']+'Trang tiep theo...trang %d[/COLOR]'%(trang+1)
			addir(name,url,icon_path+'tenlua.png',mode=mode,page=3,query='Trang%d'%(trang+1)+'?'+query,isFolder=True)
	return items_new
	
def search_web(url='',query='',mode=0,page=0,items=[]):#13
	fstring_search=datapath+"string_search.xml";fresult_search=datapath+'result_search.xml'
	colo={'Vaphim':color['Fshare'],'Ifile':color['4share'],'TenLua':color['TenLua']}
	icon={'Vaphim':icon_path+'Fshare.png','Ifile':icon_path+'4share.png','TenLua':icon_path+'tenlua.png'}
	if page==0:
		if not os.path.isfile(fresult_search):
			makerequest(fresult_search,string='<?xml version="1.0" encoding="utf-8">\n',attr='w')
		if not os.path.isfile(fstring_search):
			makerequest(fstring_search,string='<?xml version="1.0" encoding="utf-8">\n',attr='w')
		string='%sSearch[/COLOR] trên %s%s: [/COLOR]Nhập chuỗi tìm kiếm mới'%(color['search'],colo[url],url)
		addir(string,url,icon[url],mode=mode,page=1,isFolder=True)
		items = re.findall('<a search="Web" server="%s">(.+?)</a>'%url,makerequest(fstring_search))
		trang,query,items=trangtiep(query,items)
		for string in items:
			addir(string,url,icon[url],query='web?'+string,page=3,mode=mode,isFolder=True)
			if (items.index(string)>rows) and (len(items)>int(rows*1.2)): 
				name=color['trangtiep']+'Trang tiep theo...trang %d[/COLOR]'%trang
				addir(name,url,icon[url],query='Trang'+str(trang)+'?'+query,mode=mode,page=0,isFolder=True)
				break
	elif page==1:
		query = common.getUserInput('Nhập chuổi tên phim cần tìm trên %s'%url)
		if not query:return 'no'
		query = ' '.join(s for s in query.split(' ') if s!='' and s!='"' and s!="'")
		makerequest(fstring_search,string='<a search="Web" server="%s">%s</a>\n'%(url,query.replace('"',"'")),attr='a')
		items=search_web_detail(query,url,mode)
		if items and url!='TenLua':
			string='<a server="%s" string="%s">%s</a>\n'%(url,query.replace('"',"'"),str(items))
			makerequest(fresult_search,string=string,attr='a')
			search_web(url,query,mode,3,items)
		else:return 'no'
	elif page == 2:#Xóa 1 mục
		rows_string='<?xml version="1.0" encoding="utf-8">\n'
		items = re.findall('<a server="(.+?)" string="(.+?)">(.+?)</a>',makerequest(fresult_search))
		for server,string,result in items:
			if string!=query or url not in server:
				rows_string+='<a server="%s" string="%s">%s</a>\n'%(server,string,result)
		if makerequest(fresult_search,string=rows_string,attr='w'):
			rows_string='<?xml version="1.0" encoding="utf-8">\n'
			items = re.findall('<a search="(.+?)" server="(.+?)">(.+?)</a>',makerequest(fstring_search))
			rows_string='<?xml version="1.0" encoding="utf-8">\n'
			for search,server,string in items:
				if string!=query or server!=url or search!="Web":
					rows_string+='<a search="%s" server="%s">%s</a>\n'%(search,server,string)
			if makerequest(fstring_search,string=rows_string,attr='w'):mess(u'Đã xóa mục: %s'%query.decode('utf-8'))
			else:mess(u'[COLOR orangered]Chưa xóa được mục: "%s"'%search_file.decode('utf-8'))
		xbmc.executebuiltin("Container.Refresh")
	elif page==3:
		if url=='TenLua':search_web_detail(query,url,mode);return ''
		if len(items)==0 or '?' in query:
			if '?' in query:string=query.split('?')[1]
			else:string=query
			res=re.search('<a server="%s" string="%s">(.+?)</a>'%(url,string),makerequest(fresult_search))
			if res:items=eval(res.group(1))
			else:
				items=search_web_detail(string,url,mode)
				if items:
					string='<a server="%s" string="%s">%s</a>\n'%(url,string.replace('"',"'"),str(items))
					makerequest(fresult_search,string=string,attr='a')
		trang,query,items=trangtiep(query,items)
		for id_tip,id_htm,catalog,img,fanart,href,name in items:
			if ('18+' not in name) or (phim18=="true"):addirs(name,href,img,fanart)
			if (items.index((id_tip,id_htm,catalog,img,fanart,href,name))>rows) and (len(items)>int(rows*1.2)): 
				addir(color['trangtiep']+'Trang tiep theo...trang %d[/COLOR]'%trang,url,icon[url],mode=mode,page=3,query='Trang'+str(trang)+'?'+query,isFolder=True)
				break
	return ''
	
def updatePFS():#6+
	from xml.etree import ElementTree as etree
	url='http://phimfshare.com/external.php?type=RSS2'
	reddit_file = urlfetch.get(url).body
	reddit_file = reddit_file.replace('content:encoded','contentencoded')
	try:reddit_root = etree.fromstring(reddit_file);items = reddit_root.findall('channel/item')
	except:mess('Update rss fail',1000);return
	content_new=''
	fphimfshare=datapath+'phimfshare.xml'
	content_old=makerequest(fphimfshare)
	idf_old=re.findall('<a id="(.+?)" server',content_old)
	for item in items:
		idf=re.search('-(\d{5})',item.findtext('link'))
		if not idf or idf.group(1) in idf_old:continue
		idf=idf.group(1)
		name=re.sub('\[.*\]|\(.*\)|\|.*','',item.findtext('title')).strip()
		content=item.findtext('contentencoded')
		img=re.search('img src="(.+?jpg)["|?| ]',content)
		if img:img=img.group(1)
		else:img=''
		for server,link in getlinkPFS(content):
			if link not in content_new:
				content_new+='<a id="%s" server="%s" href="%s" img="%s">%s</a>\n'%(idf,server,link,img,name)
	if content_new:
		makerequest(fphimfshare,string=content_new,attr='a')
		mess('PhimFshare.com data Auto update completed')

def getlinkPFS(content):#6+
	items=[]
	pattern='(https?://www.fshare.vn/\w{4,6}/\w{10,14})|(http://4share.vn/./\w{14,20})|(https?://w?w?w?/?tenlua.vn/.*?)[ |"|<]'
	for links in re.findall(pattern,content):
		if links:
			for link in links:
				idp=re.search('(\w{10,20})',link)
				if idp:
					link=link.lower();idp=idp.group(1)
					if 'fshare.vn/file' in link:url='https://www.fshare.vn/file/%s'%idp.upper();server="Fshare"
					elif 'fshare.vn/folder' in link:url='https://www.fshare.vn/folder/%s'%idp.upper();server="Fshare"
					elif 'tenlua.vn' in link and ('folder/' in link or '#download' in link) and len(idp)>16:
						url='https://tenlua.vn/fm/folder/%s'%idp;server="TenLua"
					elif 'tenlua.vn' in link and len(idp)>16:url='https://tenlua.vn/download/%s'%idp;server="TenLua"
					elif '4share.vn' in link:url=link;server="4share"
					else:continue
					items.append((server,url))
	return items
	
def phimFshare(name,url,mode,page,query):#6
	fphimfshare=datapath+'phimfshare.xml'
	home='http://phimfshare.com/'
	if query=='Search':
		search_string = common.getUserInput('Nhập chuổi tên phim cần tìm trên phimfshare.com')
		if not search_string or not search_string.strip():return 'no'
		search_string = urllib.quote_plus(" ".join(search_string.replace('"','').replace("'","").split()))
		url='https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&'
		url+='rsz=filtered_cse&num=15&hl=vi&prettyPrint=false&source=gcsc&gss=.com&'
		url+='sig=23952f7483f1bca4119a89c020d13def&cx=005609294674567689888:qyuk9aoqwmg&q='+search_string
		url+='&googlehost=www.google.com&callback=google.search.Search.apiary'
		body=urlfetch.get(url).body
		items =re.findall('()"url":"(http://phimfshare.com/.+?)"()()',body)
		if not items:mess(u'Không tìm thấy phim có chứa chuổi tìm kiếm');return 'no'
	elif query=='PhimMoi':
		body=urlfetch.get(home).body
		items=re.findall('()<a href="(.+?)" ()class="title">(.+?)</a>',body)
	else:
		if home not in url:url=home+url+'/'
		body=urlfetch.get(url).body
		pattern='<img class="preview" src="(.+?)" style=.+?<a title="" class="title" href="(.+?)" id="thread_title_(.+?)">(.+?)</a>'
		items=re.findall(pattern,body)
		#if not items:items=re.compile('()<a href="(.+?)" class="title">(.+?)</a>').findall(body);page=1
	
	content_old=makerequest(fphimfshare);content_new=''
	for img,href,idf,name in items:
		if not idf or len(idf)<5:
			idf=re.search('-(\d{5})',href)
			if idf:idf=idf.group(1)
			else:continue
		items_old=re.findall('<a id="%s" server="(.+?)" href="(.+?)" img="(.*?)">(.+?)</a>'%idf,content_old)
		if items_old:
			for ser_,href_,img_,name_ in items_old:
				addirs(color[ser_]+ser_+'[/COLOR] - '+name_,href_,img_,img_)
		else:
			mess(href.split('/')[len(href.split('/'))-2],1)
			response=urlfetch.get(href).body
			temp=re.search('<title> (.+?)</title>',response)
			if temp:name=temp.group(1)
			elif not name:continue
			if not img:
				temp=re.search('<img src="(.+?)" border="0" alt="" />',response)
				if temp:img=temp.group(1)
			name=name.split('] ')[len(name.split('] '))-1].replace('MuLtI','').replace('Fshare','').strip()
			for server,link in getlinkPFS(response):
				if link not in content_new:
					content_new+='<a id="%s" server="%s" href="%s" img="%s">%s</a>\n'%(idf,server,link,img,name)
				addirs(color['%s'%server]+'%s[/COLOR] - %s'%(server,name),link,img,img)
	if content_new:makerequest(fphimfshare,string=content_new,attr='a')
	href=re.search('<a rel="next" href="(.+?)" title=".+?">',body)
	if href:
		if not page:page=1
		url=href.group(1);page+=1;name=color['trangtiep']+'Trang tiếp theo - Trang '+str(page)+' ...[/COLOR]'
		addir(name,url,icon_path+'fshare.png',mode=mode,page=page,query=query,isFolder=True)
	return ''

def fptplay(url,page=1,query=''):
	fpt="http://fptplay.net"
	if url==fpt:
		addir(color['search']+"Search trên fptplay.net[/COLOR]","http://fptplay.net/search/",icon_path+"fptplay.png",mode=7,page=1,query="node0",isFolder=True)
		items=re.compile('<a href="(/the-loai/.+?)"\s+class="\d.*">(.+?)</a>').findall(urlfetch.get(url).body)
		for href,name in items:
			addir(color['fpt']+name+"[/COLOR]",fpt+href,icon_path+"fptplay.png",mode=7,query="node1",isFolder=True)
			if name=='Tổng Hợp':break
	elif query=="node0":
		if page==1:
			search_string = common.getUserInput("Nhập chuổi tên phim cần tìm trên "+fpt)
			if not search_string or not search_string.strip():return "no"
			search_string = urllib.quote_plus(" ".join(search_string.replace('"','').replace("'","").split()))
			link=url=fpt+'/search/'+search_string
		else :link=url+'/'+str(page)
		body=urlfetch.get(link).body
		items=re.compile('<a href="(.+?)" title="(.+?)".+\s+<img src="(.+?)"').findall(body)
		if len(items)==0:mess(u'Không có kết quả nào');return 'no'
		for href,title,img in items:
			links=re.compile('<a data="(/getvod/.+)" href.+\s.+\s+>(.+?)</a>').findall(urlfetch.get(fpt+href).body)
			if len(links)>1:
				query="node3?"+title+"?"+img.split('?')[0]
				addir(color['fpt']+title+"[/COLOR]",fpt+href,img,img,mode=7,page=1,query=query,isFolder=True)
			else:
				#link = urlfetch.get("http://fptplay.net"+"/getvod"+href.split('video')[1]).body
				link = fpt+"/getvod"+href.split('video')[1]
				addir(title,link,img.split('?')[0],img.split('?')[0],mode=7,query="play")
		if len(items)>20:
			page=page+1;url=url;name=color['trangtiep']+"Trang tiếp theo - Trang "+str(page)+"[/COLOR]"
			addir(name,url,icon_path+"fptplay.png",mode=7,page=page,query="node0",isFolder=True)
	elif query=="node1":
		items=re.compile('href="(/the-loai-more/.+)">\s+<span class="pull-left" >(.+?)</span >').findall(urlfetch.get(url).body)
		for href,name in items:
			addir(color['fpt']+name+"[/COLOR]",fpt+href,icon_path+"fptplay.png",mode=7,page=1,query="node2",isFolder=True)
	elif query=="node2":
		url_structure='http://fptplay.net/get_all_vod_structure/news/'+url.split('/')[4]+'/'
		videos=urlfetch.get(url_structure+str(page)).json
		for video in videos["videos_list"]:
			img=video['banner_thumb'].encode('utf-8');name=clean_string(video['title'].encode('utf-8'))
			href=video['link_video'].encode('utf-8');query="node3?"+name+"?"+img
			links=re.compile('<a data="(/getvod/.+)" href.+\s.+\s+>(.+?)</a>').findall(urlfetch.get(fpt+href).body)
			if len(links)>1:
				addir(color['fpt']+name+"[/COLOR]",fpt+href,img,img,mode=7,page=1,query=query,isFolder=True)
				continue
			u=re.search('/(?P<_id>\d.*)/(?P<slug_title>.+?)/(?P<chap>.+?)',href)
			if u:link = "http://fptplay.net"+"/getvod/"+u.group('_id')+"/"+u.group('slug_title')+"/"+u.group('chap')
			else:link='';continue
			#link=urlfetch.get(link).body
			addir(name,link,img,img,mode=7,query="play")
		if len(urlfetch.get(url_structure+str(page+1)).json["videos_list"])>0:
			addir(color['trangtiep']+"Trang tiếp theo - Trang "+str(page+1)+"[/COLOR]",url,icon_path+"fptplay.png",mode=7,page=page+1,query="node2",isFolder=True)
	elif "node3" in query:
		name=query.split("?")[1];img=query.split("?")[2]
		links=re.compile('<a data="(/getvod/.+)" href.+\s.+\s+>(.+?)</a>').findall(urlfetch.get(url).body)
		for data,chap in links:
			#link=urlfetch.get(fpt+data).body
			addir(chap+" - "+name,fpt+data,img,img,mode=7,query="play")
	elif query=='play':
		url=urlfetch.get(url).body
		item = xbmcgui.ListItem(path=url)
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	return ''
	
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
date = datetime.date.today().isocalendar()
thisweek = '%0*d%0*d'%(4,date[0],2,date[1])
weekday = datetime.date.today().weekday() 
url=name=fanart=img=date=query=end=''
mode=page=0

try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:img=urllib.unquote_plus(params["img"])
except:pass
try:fanart=urllib.unquote_plus(params["fanart"])
except:pass
try:date=urllib.unquote_plus(params["date"])
except:pass
try:mode=int(params["mode"])
except:pass
try:page=int(params["page"])
except:pass
try:query=urllib.unquote_plus(params["query"])
except:pass#urllib.unquote
try:
	if lastweekupdate<thisweek and weekday>2:myaddon.setSetting('lastweekupdate',thisweek);vp_update()
	if lastweekupdate<thisweek and weekday>4:myaddon.setSetting('lastweekupdate',thisweek);ifile_update()
except:pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "query: "+str(query)
print "page: "+str(page)

if mode==0 or mode=='':open_category("MMN")
elif mode==2:end=google_search_api(url,query,page,mode)
elif mode==3:end=resolve_url(url)
elif mode==4:phimchon('http://vaphim.com','vaphim-1.xml','data="(.+?)" title')
elif mode==5:vp_xemnhieu()
elif mode==6:end=phimFshare(name,url,mode,page,query)
elif mode==7:end=fptplay(url,page,query)
elif mode==10:open_category(query)
elif mode==11:end=search_noibo(name,url,mode,page,query)
elif mode==13:end=search_web(url,query,mode,page)
elif mode==15:end=mo_id_file(url,name,mode,page,query)
elif mode==16:end=Mo_maxspeed_link()
elif mode==20:end=vp_update()
elif mode==31:end=ifile_update()
elif mode==34:phimchon("http://ifile.tv/phim","ifiletv-1.xml",'href=".+(\d\d\d\d\d).+" class="mosaic-backdrop"')
elif mode==35:phimchon("http://ifile.tv/phim/index","ifiletv-1.xml",'href=".+(\d\d\d\d\d).+" class="mosaic-backdrop"')
elif mode==36:end=search_noibo(query)
elif mode==38:DocTrang4share(url)#38
elif mode==39:DocTrangifiletv(url)
elif mode==47:daklak47(name,url,img)
elif mode==90:DocTrangFshare(url,img,fanart)
elif mode==91:main_menu(url,page,mode,query)
elif mode==95:lay_link_tenlua(url)
elif mode==96:doc_thumuccucbo()
elif mode==97:menu_xml(url,name,page)
elif mode==99:myaddon.openSettings();end='ok'

#xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)
if end == '':xbmcplugin.endOfDirectory(int(sys.argv[1]))
'''
https://urlfetch.readthedocs.org/en/v0.5.3/examples.html
Thay toàn bộ code của xshare 2.22, không sử dụng thư viện BeautifulSoup mà thay băng thư viện Re. 
Cho nên quá trình web Scraping sẽ nhanh hơn.
Fix: 
- Hỗ trợ Get link VIP Fshare ở chế độ "Không kích hoạt tải trực tiếp"
- Mở Folder ID Fshare trong mục "Mở link theo ID"
- Đọc folder Fshare không hạn chế số lượng files
Bổ sung: 
- Hỗ trợ play file Fshare có pass.
- Thêm tính năng google search trên fshare,4share,tênlửa
- Ghi lại lịch sử tìm kiếm, mở ID file
- Thêm menu ngữ cảnh cho lịch sử tìm kiếm, mở ID file
- Auto rss update Vaphim.com
- Get phim từ các Server http://phimfshare.com, http://fptplay.net, https:\\tenlua.vn
- Fix lật trang PhimFshare.com

THZA19WGMT Pass: thanhcoti
'''