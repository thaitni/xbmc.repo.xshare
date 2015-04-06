# -*- coding: utf-8 -*-
import os,re,xbmc,xbmcaddon,xbmcgui,xbmcplugin,unicodedata,urllib,urllib2
from datetime import date

addon = xbmcaddon.Addon()
service = addon.getAddonInfo('id')

home = xbmc.translatePath(addon.getAddonInfo('path')).decode("utf-8")
libpath = xbmc.translatePath(os.path.join(home, 'resources', 'lib')).decode("utf-8")
tempath = xbmc.translatePath(os.path.join( xbmc.translatePath(addon.getAddonInfo('profile')),'temp'))
if not os.path.exists(xbmc.translatePath(addon.getAddonInfo('profile'))):
	os.mkdir(xbmc.translatePath(addon.getAddonInfo('profile')))
if not os.path.exists(tempath):os.mkdir(tempath)
subscene = "http://subscene.com"
sys.path.append(libpath)
import urlfetch
hd={'User-Agent':'Mozilla/5.0'}
def mess(message, timeShown=5000, title='Xshare'):
	xbmc.executebuiltin((u'XBMC.Notification("%s","%s",%s)'%(title,message,timeShown)).encode("utf-8"))

def no_accent(s):
	s = s.decode('utf-8')
	s = re.sub(u'Đ', 'D', s)
	s = re.sub(u'đ', 'd', s)
	return unicodedata.normalize('NFKD', unicode(s)).encode('ASCII', 'ignore')

def make_request(url):
	try:
		response = urllib2.urlopen(url)
		body = response.read()
		strip_unicode = re.compile("([^-_a-zA-Z0-9!@#%&=,/'\";:~`\$\^\*\(\)\+\[\]\.\{\}\|\?<>\\]+|[^\s]+)")
		body = strip_unicode.sub('', body)
		response.close()
	except:body=None
	return body
	
def find_movie(title,film_year):
	href = subscene+'/subtitles/title?q='+urllib.quote_plus(title)+'&r=true'
	pattern=".*".join(title.split(' ')).lower();url = None
	for link,name,year in re.findall('<a href="(/subtitles/.+)">(.+)\((\d\d\d\d)\)</a>',urlfetch.get(href).body):
		name=no_accent(name).replace("&","and").replace("&#39;","").lower()
		if film_year and re.search(pattern,name) and year==film_year:url=link;break
		elif not film_year:
			film_year1=str(date.today().year)
			if re.search(pattern,name) and year==film_year1:url=link;break
	if not url and re.search('S\d\d',title):
		e=re.search('S(\d\d)',title).group(1)
		thutu={'01':'First','02':'Second','03':'Third','04':'Fourth','05':'Fifth','06':'sixth','07':'Seventh','08':'Eighth','09':'ninth'}
		seasons=["Specials","First","Second","Third","Fourth","Fifth","Sixth","Seventh","Eighth","Ninth","Tenth","Eleventh","Twelfth","Thirteenth","Fourteenth","Fifteenth","Sixteenth","Seventeenth","Eighteenth","Nineteenth","Twentieth","Twenty-first","Twenty-second","Twenty-third","Twenty-fourth","Twenty-fifth","Twenty-sixth","Twenty-seventh","Twenty-eighth","Twenty-ninth"]

		title=re.sub('S\d\d.*','%s season'%seasons[int(e)],title)
		url=find_movie(title,film_year)
	return url

def find_phudeviet(title,film_year):
	href='http://phudeviet.org/findfilm/?select=1&film_name=%s'%urllib.quote_plus(title)
	pattern=".*".join(title.split(' ')).lower();url = None
	for link,name in re.findall('<td class="td6"><.+?><a href="(.+?)">(.+?)</a></td>',urlfetch.get(href).body):
		name=no_accent(name).replace("&","and").replace("&#39;","").lower()
		if film_year and re.search(pattern,name) and film_year in name:url=link;break
		elif not film_year:
			film_year1=str(date.today().year)
			if re.search(pattern,name) and film_year1 in name:url=link;break
	if not url and re.search('S\d\d',title):
		e=int(re.search('S(\d\d)',title).group(1))
		title=re.sub('S\d\d.*','season %d'%e,title)
		url=find_phudeviet(title,film_year)
	if not film_year and not url:
		film_year=str(date.today().year-1)
		url=find_phudeviet(title,film_year)
	return url

def google_find_phudeviet(title,film_year):
	pattern=".*".join(title.split(' ')).lower();url = None
	hd={'User-Agent':'Mozilla/5.0','Accept-Language':'en-US,en;q=0.8,vi;q=0.6'}
	string_search = urllib.quote_plus('"'+title+'"')
	href='http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=large&start=0&'
	href+='q=site:phudeviet.org+%s'%string_search
	json=urlfetch.get(href,headers=hd).json
	if json['responseStatus']==403:print 'Google: response status 403'
	else:
		data=json['responseData']
		if not data or not data['results']:print 'Google not data["results"]'
		else:
			results=data['results']
			for result in results:
				if 'http://phudeviet.org/film' in result['url']:
					title=result['titleNoFormatting']
					link=result['url']
					title=title.replace("&","and").replace("&#39;","").lower()
					if re.search(pattern,title) and film_year in title:url=link;break
	if url:print 'google_find_phudeviet: %s'%url
	return url

def search_movie(title, year, filename):
	title=title.replace("&","and").replace("&#39;","").strip();subtitles=[];subs=[]
	subspage_url = find_movie(title, year)
	if subspage_url:
		url = subscene+subspage_url
		print 'aaaa',url
		pattern='<a href="(/subtitles/.+?)">\s+<span class=".+?">\s*(.+?)\s+</span>\s+<span>\s+(.+?)\s+</span>'
		subs=re.findall(pattern,urlfetch.get(url=url,headers={'Cookie':'LanguageFilter=13,45'}).body)
		
	phudeviet_url = find_phudeviet(title, year)
	if not phudeviet_url:
		phudeviet_url = google_find_phudeviet(title,year)
	if phudeviet_url:
		pattern_pdv='<td class="td4".+"(.+png)">.+\s+<td class="td1".+href="(.+?)">(.+?)<.+td>'
		for lang,href,filename in re.findall(pattern_pdv,urlfetch.get(phudeviet_url).body):
			if 'Anh.png' in lang:lang="English"
			else:lang="Phudeviet"
			subs.append((href,lang,filename))
	if len(subs) == 0:
		url='http://subscene.com/subtitles/release?q=%s'%title.replace(' ','.')+'.'+year
		pattern='<a href="(/subtitles/.+?)">\s+<span class=".+?">\s*(.+?)\s+</span>\s+<span>\s+(.+?)\s+</span>'
		subs=re.findall(pattern,urlfetch.get(url=url,headers={'LanguageFilter':'13,45'}).body)
		if subs:mess(u'List subs này có chứa sub có tên phim gần đúng!')

	if len(subs) == 0:
		mess(u'Không tìm thấy phụ đề của Video: %s'%title)
	
	fn = os.path.splitext(filename)[0].split('.x264')[0].replace(' ','.').replace('-','.').replace('*','.')
	ratlist=fn.split('.')
	for link,lang,name in subs:
		name=name.strip().replace(' ','.');rat=1;label='vie'
		if 'Vietnam' in lang:img='vi';url=subscene+link
		elif 'Phude' in lang:img='vi';url=link;name='[COLOR lime]phudeviet.org[/COLOR]: '+name
		else:img='en';url=subscene+link
		for i in ratlist:
			try:
				if re.search(i,name):rat+=1
			except:pass
		#filename:name,link:url,label:label,img:img,rating:str(rat)
		subtitles.append((name,url,label,img,str(rat)))
	items=list()
	for fn,link,label,img,rating in sorted(subtitles,cmp=lambda x,y:cmp(x[0],y[3]),reverse=True):
		item = xbmcgui.ListItem(label=label,label2=fn,iconImage=rating,thumbnailImage=img)
		url="plugin://%s/?action=download&link=%s&filename=%s&img=%s"%(service,link,fn,img)
		items.append((url, item, False))
	xbmcplugin.addDirectoryItems(int(sys.argv[1]), items);mess(u'Movie: %s'%filename,20000,'Xshare: Movie year - %s'%year)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def download(link,img):
	sub_list=[];downloadlink=''
	if 'phudeviet.org' in link:
		match = re.search('<a href="(http://phudeviet.org/download/.+?)">',make_request(link))
		if match:
			response=urlfetch.post(match.group(1))
			if response.status==302:downloadlink=response.headers['location']
	else:
		pattern='<a href="(.+?)" rel="nofollow" onclick="DownloadSubtitle.+">'
		match = re.search(pattern,make_request(link))
		if match:downloadlink=subscene + match.group(1)
	if not downloadlink:mess(u'Không tìm được maxspeed link sub');return
		
	typeid="srt"
	for f in os.listdir(tempath):
		delfile = os.path.join(tempath, f)
		try:os.remove(delfile)
		except:pass
	body=urlfetch.get(downloadlink).body
	tempfile = os.path.join(tempath, "subtitle.sub")
	f = open(tempfile, "wb");f.write(body);f.close()
	f = open(tempfile, "rb");f.seek(0);fread=f.read(1);f.close()
	if fread == 'R':	typeid = "rar"
	elif fread == 'P':typeid = "zip"
	
	tempfile = os.path.join(tempath, "subtitle." + typeid)
	os.rename(os.path.join(tempath, "subtitle.sub"), tempfile)

	if typeid in "rar-zip":
		xbmc.sleep(500)
		xbmc.executebuiltin(('XBMC.Extract("%s","%s")' % (tempfile, tempath,)).encode('utf-8'), True)

	exts = [".srt", ".sub", ".txt", ".smi", ".ssa", ".ass"]
	for f in os.listdir(tempath):
		file = os.path.join(tempath, f)
		if os.path.splitext(file)[1] in exts:
			sub_list.append(file)
			if img=='en':
				mess(u'Google đang dịch sub từ tiếng Anh sang tiếng Việt', timeShown=10000)
				try:
					tempfile=xshare_trans(file)
					os.remove(file)
					os.rename(tempfile,file)
					mess(u'Đã dịch xong sub từ tiếng Anh sang tiếng Việt') 
				except:mess(u'Không dịch được sub từ tiếng Anh sang tiếng Việt') 
	if len(sub_list) == 0:mess(u'Không tìm thấy sub')
	return sub_list
	
def xshare_trans(sourcefile):
	tempfile = os.path.join(tempath, "temp"+os.path.splitext(sourcefile)[1])
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
	body= urlfetch.fetch(url=url,headers=hd).body
	body=body.replace(',,"en"','').replace('[[[','').replace(']]]','')
	result=''
	for i in body.split('],['):
		research=re.search('"(.+?)","(.+?)"',i)
		if research:result+=research.group(1)+' '
		else:print '%s :not research'%i
	return result.replace('Xshare','xshare').split('xshare')
	
def get_params():
	param = {}
	paramstring = sys.argv[2]
	if len(paramstring) >= 2:
		params = paramstring
		cleanedparams = params.replace('?', '')
		if (params[len(params) - 1] == '/'):params = params[0:len(params) - 2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:param[splitparams[0]] = splitparams[1]

	return param

params = get_params()

if params['action'] == 'search':
	item = {}
	item['file_original_path'] = urllib.unquote(xbmc.Player().getPlayingFile().decode('utf-8'))
	filename = os.path.basename(re.split('/\w+.m3u8',item['file_original_path'])[0]).rpartition('.')[0]
	item['title'], item['year'] = xbmc.getCleanMovieTitle(filename)
	if item['title'] == "":
		item['title'] = normalizeString(xbmc.getInfoLabel("VideoPlayer.Title"))
	item['title'] = re.sub('\[.*\]','',item['title'])
	filename = re.sub('\[.*\]','',filename)
	print 'xshare -------------------------------------------------------------------'
	print 'xshare file_original_path : %s'%item['file_original_path']
	print 'xshare filename : %s'%filename
	print 'xshare title : %s'%item['title']
	print 'xshare year : %s'%item['year']
	search_movie(item['title'], item['year'], filename)
elif params['action'] == 'download':
	subs = download(params["link"],params["img"])
	for sub in subs:
		listitem = xbmcgui.ListItem(label=sub)
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sub, listitem=listitem, isFolder=False)
		