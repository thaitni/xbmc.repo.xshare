# -*- coding: utf-8 -*-
import os,re,xbmc,xbmcaddon,xbmcgui,xbmcplugin,unicodedata,urllib,urllib2
from datetime import date

addon = xbmcaddon.Addon()
service = addon.getAddonInfo('id')

home = xbmc.translatePath(addon.getAddonInfo('path')).decode("utf-8")
libpath = xbmc.translatePath(os.path.join(home, 'resources', 'lib')).decode("utf-8")
xbmc_temp = xbmc.translatePath('special://temp')
tempath = os.path.join(xbmc_temp,'temp')
if not os.path.exists(tempath):
	try:os.mkdir(tempath)
	except:pass
subsfolder = os.path.join(xbmc_temp,'subs')
if not os.path.exists(subsfolder):
	try:os.mkdir(subsfolder)
	except:pass

subscene = "https://subscene.com"
sys.path.append(libpath)
import urlfetch
hd={'User-Agent':'Mozilla/5.0'}
seasons={'01':'First','02':'Second','03':'Third','04':'Fourth','05':'Fifth','06':'Sixth','07':'Seventh','08':'Eighth','09':'Ninth','10':'Tenth','11':'Eleventh','12':'Twelfth','13':'Thirteenth','14':'Fourteenth','15':'Fifteenth','16':'Sixteenth','17':'Seventeenth','18':'Eighteenth','19':'Nineteenth','20':'Twentieth','21':'Twenty-first','22':'Twenty-second','23':'Twenty-third','24':'Twenty-fourth','25':'Twenty-fifth','26':'Twenty-sixth','27':'Twenty-seventh','28':'Twenty-eighth','29':'Twenty-ninth'}

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
	except:body=''
	return body
	
def find_movie(title,film_year):
	href = subscene+'/subtitles/title?q='+urllib.quote_plus(title)+'&r=true'
	try:body=urlfetch.get(href).body
	except:body=''
	pattern=".*".join(title.split()).lower();url = None
	for link,name,year in re.findall('<a href="(/subtitles/.+)">(.+)\((\d\d\d\d)\)</a>',body):
		name=re.sub("&# ","",no_accent(name).replace("&","and")).lower()
		if film_year and re.search(pattern,name) and year==film_year:url=link;break
		elif not film_year:
			film_year1=str(date.today().year)
			if re.search(pattern,name) and year==film_year1:url=link;break
	if not url:
		for link,name,year in re.findall('<a href="(/subtitles/.+)">(.+)\((\d\d\d\d)\)</a>',body):
			name=re.sub("&# ","",no_accent(name).replace("&","and")).lower()
			if re.search(pattern,name):url=link;break
	'''
	if not url and re.search('[S|s]\d\d',title):
		ss=re.search('[S|s](\d\d)',title).group(1)
		newtitle=re.sub('[S|s]\d\d.*','%s season'%seasons[ss],title)
		if not re.search('[S|s]\d\d',newtitle):
			return find_movie(newtitle,film_year)
	'''
	return url

def find_phudeviet(title,film_year):
	href='http://phudeviet.org/findfilm/?select=1&film_name=%s'%urllib.quote_plus(title)
	pattern=".*".join(title.split()).lower();url = None
	for link,name in re.findall('<td class="td6"><.+?><a href="(.+?)">(.+?)</a></td>',urlfetch.get(href).body):
		name=re.sub("&# ","",no_accent(name).replace("&","and")).lower()
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
	pattern=".*".join(title.split()).lower();url = None
	hd={'User-Agent':'Mozilla/5.0','Accept-Language':'en-US,en;q=0.8,vi;q=0.6'}
	string_search = urllib.quote_plus('"'+title+'"')
	href='http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=large&start=0&'
	href+='q=site:phudeviet.org+%s'%string_search
	json=urlfetch.get(href,headers=hd).json
	if json['responseStatus']==403:print 'phudeviet - Google: response status 403'
	else:
		data=json['responseData']
		if not data or not data['results']:print 'phudeviet - Google not data["results"]'
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

def search_movie(item):
	title=item['title'];year=item['year'];filename=item['filename'];mansearchstr=item['mansearchstr']
	if mansearchstr:title=re.sub('\(\w+?\)','',urllib.unquote(mansearchstr));mess('Manual search for string')
	else:title=re.sub('&#.* ','',title.replace("&","and")).strip()
	title=' '.join(s for s in title.split())
	subspage_url=find_movie(title, year);subtitles=[];subs=[]
	pattern='<a href="(/subtitles/.+?)">\s+<span class=".+?">\s*(.+?)\s+</span>\s+<span>\s+(.+?)\s+</span>'
	if subspage_url:
		url=subscene+subspage_url
		subs=re.findall(pattern,urlfetch.get(url=url,headers={'Cookie':'LanguageFilter=13,45'}).body)
	
	if re.search('[S|s]\d\d',item['filename']):
		newtitle=' '.join(s for s in title.split() if not re.search('[S|s]\d\d',s))
		newtitle='%s %s Season'%(newtitle,seasons[re.search('[S|s](\d\d)',item['filename']).group(1)])
		print 'newtitle0: %s'%newtitle
		subspage_url=find_movie(newtitle, year)
		if subspage_url:
			url=subscene+subspage_url
			subs+=re.findall(pattern,urlfetch.get(url=url,headers={'Cookie':'LanguageFilter=13,45'}).body)

	if mansearchstr:
		url=subscene+'/subtitles/release?q='+urllib.quote_plus(title)+'&r=true'
		subs+=re.findall(pattern,urlfetch.get(url=url,headers={'Cookie':'LanguageFilter=13,45'}).body)
		
	if not subs and '-' in title:
		newtitle=' '.join(s for s in re.sub('\(.+?\)','',title.split('-')[1]).split())
		print 'newtitle1: %s'%newtitle
		subspage_url=find_movie(newtitle, year)
		if subspage_url:
			url=subscene+subspage_url
			subs+=re.findall(pattern,urlfetch.get(url=url,headers={'Cookie':'LanguageFilter=13,45'}).body)
		if not subs:
			newtitle=' '.join(s for s in re.sub('\(.+?\)','',title.split('-')[0]).split())
			print 'newtitle2: %s'%newtitle
			subspage_url=find_movie(newtitle, year)
			if subspage_url:
				url=subscene+subspage_url
				subs+=re.findall(pattern,urlfetch.get(url=url,headers={'Cookie':'LanguageFilter=13,45'}).body)
	
	phudeviet_url = find_phudeviet(title, year)
	if not phudeviet_url:
		phudeviet_url = google_find_phudeviet(title,year)
	if phudeviet_url:
		pattern_pdv='<td class="td4".+"(.+png)">.+\s+<td class="td1".+href="(.+?)">(.+?)<.+td>'
		for lang,href,fn in re.findall(pattern_pdv,urlfetch.get(phudeviet_url).body):
			if 'Anh.png' in lang:lang="English"
			else:lang="Phudeviet"
			subs.append((href,lang,fn))
	
	notification=''
	if not subs:
		mess(u'Tìm gần đúng')
		url='http://subscene.com/subtitles/release?q=%s'%title.replace(' ','.')+'.'+year
		pattern='<a href="(/subtitles/.+?)">\s+<span class=".+?">\s*(.+?)\s+</span>\s+<span>\s+(.+?)\s+</span>'
		subs=re.findall(pattern,urlfetch.get(url=url,headers={'Cookie':'LanguageFilter=13,45'}).body)
		if subs:notification=u'tìm gần đúng!'

	if not subs:mess(u'Không tìm thấy phụ đề')
	
	fn = os.path.splitext(filename)[0].split('.x264')[0].replace(' ','.').replace('-','.').replace('*','.')
	ratlist=fn.split('.')
	for link,lang,name in subs:
		name=name.strip().replace(' ','.');rat=1;label='vie'
		if 'Vietnam' in lang:img='vi';url=subscene+link
		elif 'Phude' in lang:img='vi';url=link;name='phudeviet.org '+name
		else:
			img='en';url=subscene+link
			if addon.getSetting('trans_sub')=='false':label='eng'
		for i in ratlist:
			try:
				if re.search(i,name):rat+=1
			except:pass
		subtitles.append((name,url,label,img,str(rat)))
	items=list()
	for fn,link,label,img,rating in sorted(subtitles,cmp=lambda x,y:cmp(x[0],y[3]),reverse=True):
		item = xbmcgui.ListItem(label=label,label2=fn,iconImage=rating,thumbnailImage=img)
		url="plugin://%s/?action=download&link=%s&filename=%s&img=%s"%(service,link,fn,img)
		items.append((url, item, False))
	if items:
		xbmcplugin.addDirectoryItems(int(sys.argv[1]), items)
		if not filename:filename=title
		mess(u'Movie: %s'%filename,20000,'Xshare %s: Movie year - %s '%(notification,year))

def download(link,filename,img):
	sub_list=[];downloadlink=''
	if 'phudeviet.org' in link:
		match = re.search('<a href="(http://phudeviet.org/download/.+?)">',make_request(link))
		if match:
			response=urlfetch.post(match.group(1))
			if response.status==302:downloadlink=response.headers['location']
	else:
		pattern='<a href="(.+?)" rel="nofollow" onclick="DownloadSubtitle.+">';print link
		#body=make_request(link);print len(body)
		try:match = re.search(pattern,urlfetch.get(link).body)
		except:match=''
		if match:downloadlink=subscene + match.group(1)
	if not downloadlink:mess(u'Không tìm được maxspeed link sub');return
	print 'downloadlink: %s'%downloadlink
	
	if os.path.exists(tempath):
		for root, dirs, files in os.walk(tempath, topdown=False):
			for name in files:
				try:os.remove(os.path.join(root, name))
				except:pass
			for name in dirs:
				try:os.rmdir(os.path.join(root, name))
				except:pass
	else:
		try:os.mkdir(tempath)
		except:mess(u'Không tạo được thư mục temp');return []

	try:body=urlfetch.get(downloadlink).body
	except:body=' '
	tempfile = os.path.join(tempath, "subtitle.sub")
	f = open(tempfile, "wb");f.write(body);f.close()
	f = open(tempfile, "rb");f.seek(0);fread=f.read(1);f.close()

	if fread == 'R':	typeid = "rar"
	elif fread == 'P':typeid = "zip"
	else:typeid="srt"
	def rename(fs,fd):
		try:
			if os.path.isfile(fd):os.remove(fd)
			os.rename(fs,fd)
		except:pass
	tempfile = os.path.join(tempath, "subtitle." + typeid)
	rename(os.path.join(tempath, "subtitle.sub"), tempfile)

	if typeid in "rar-zip":
		xbmc.sleep(500)
		try:xbmc.executebuiltin(('XBMC.Extract("%s","%s")' % (tempfile, tempath,)).encode('utf-8'), True)
		except:pass
	exts = [".srt", ".sub", ".txt", ".smi", ".ssa", ".ass"]; trans=True
	
	for root, dirs, files in os.walk(tempath):
		for f in files:
			#f=re.sub(',','',f);
			file = os.path.join(root, f)
			ext=os.path.splitext(f)[1];subfile=os.path.join(subsfolder, filename+ext)
			if ext in exts:
				if img=='en' and addon.getSetting('trans_sub')=='true' and trans:
					mess(u'Google đang dịch sub từ tiếng Anh sang tiếng Việt', timeShown=2000)
					if xshare_trans(file,subfile):mess(u'Đã dịch xong sub từ tiếng Anh sang tiếng Việt')
					else:mess(u'Dịch sub thất bại do Google chặn dịch vụ !!!') 
					trans=False
				else:rename(file, subfile)
				sub_list.append(subfile)
	
	if not sub_list:mess(u'Không tìm thấy sub')
	return sub_list
	
def xshare_trans(fs,fd):
	def trans(s):
		try:s=s.decode('unicode_escape') if '\\' in s else s.decode('utf-8')
		except:pass
		return s

	try:f=open(fs);b=f.read();f.close()
	except:b=' '
	s='';S=''
	u='https://translate.googleapis.com/translate_a/single?ie=UTF-8&oe=UTF-8&client=gtx&sl=en&tl=vi&dt=t&q=%s'
	list_1=b.splitlines();list_2=[];rows=len(list_1);row=0
	hd={'Referer':'https://translate.google.com/','User-Agent':'Mozilla/5.0 (Windows NT 6.3) Chrome/49.0.2623.112 Safari/537.36','Cookie':''}
	progress=xbmcgui.DialogProgress()
	progress.create('Xshare Subtitles','Goolge translating ...')
	for i in list_1:
		row+=1
		if re.search('[a-zA-Z]',i):s=s+' '+i+' xshare';list_2.append('xshare')
		else:list_2.append(i.strip())
		if len(s)>1000 or row==rows:
			progress.update(row*100/rows,'Goolde Translate đang dịch từ tiếng Anh sang tiếng Việt')
			s=' '.join(i for i in s.split())
			tran=urlfetch.get(u%urllib.quote(s),headers=hd)
			if not hd['Cookie']:hd['Cookie']=tran.cookiestring
			xbmc.sleep(1000)#;print tran.body
			try:
				l=eval(tran.body.replace(',,,',',').replace(',,"en"',''))
				S=S+' '.join(i[0] for i in l[0])
			except:pass
			s=''
		if xbmc.abortRequested or progress.iscanceled():break
	progress.close()
	s=' '.join(trans(i) for i in S.split())
	list_3=s.split('xshare');d=0;f=open(fd,'w')
	f.write('0\n00:00:00,000 --> 00:02:00,000\nXshare dich tu ban tieng Anh bang Google translate\n\n')
	for i in list_2:
		try:
			if i=='xshare':f.write(list_3[d].strip().encode('utf-8')+'\n');d+=1
			else:f.write(i+'\n')
		except:pass
	f.close();xbmc.executebuiltin("Dialog.Close(all, true)")
	return True

def xshare_trans1(sourcefile):
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
		else:print '---------------------------------------not research'
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
if params['action'] == 'search' or params['action'] == 'manualsearch':
	item = {}
	item['file_original_path'] = no_accent(urllib.unquote(xbmc.Player().getPlayingFile()))
	try:item['file_original_path'] = no_accent(item['file_original_path'])
	except:item['file_original_path'] = item['file_original_path'].decode('utf-8')
	
	filename = os.path.basename(re.split('/\w+.m3u8',item['file_original_path'])[0]).rpartition('.')[0]
	filename = re.sub('\[.*\]','',filename)
	item['filename']=filename
	
	item['title'], item['year'] = xbmc.getCleanMovieTitle(filename)
	if not item['title']:
		item['title'] = xbmc.getInfoLabel("VideoPlayer.Title")
	item['title'] = no_accent(re.sub('\[\w+?\]','',item['title']))
	
	try:
		print 'xshare -------------------------------------------------------------------'
		print 'xshare file_original_path : %s'%item['file_original_path']
		print 'xshare filename : %s'%filename
		print 'xshare title : %s'%item['title']
		print 'xshare year : %s'%item['year']
		print '--------------------------------------------------------------------------'
	except:pass
	
	item['mansearchstr'] = ''
	if 'searchstring' in params:
		item['mansearchstr'] = params['searchstring']
	search_movie(item)
elif params['action'] == 'download':
	subs = download(params["link"],params["filename"],params["img"])
	for sub in subs:
		listitem = xbmcgui.ListItem(label=sub)
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sub, listitem=listitem, isFolder=False)
xbmcplugin.endOfDirectory(int(sys.argv[1]))