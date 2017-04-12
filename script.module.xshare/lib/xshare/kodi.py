import xbmc, xbmcaddon, xbmcplugin, xbmcgui, os, sys

addon          = xbmcaddon.Addon()
PATH           = "plugin://" + addon.getAddonInfo('id')
endDir         = xbmcplugin.endOfDirectory
setContent     = xbmcplugin.setContent
listItem       = xbmcgui.ListItem
setResolvedUrl = xbmcplugin.setResolvedUrl
executebuiltin = xbmc.executebuiltin
xshareFolder   = os.path.join( xbmc.translatePath("special://masterprofile/"), "xshare" )
xshareKey      = "z9M2xoA93ZUSA7CX5x4h0IjQLDFVvRG7JYXbWmgB"
subsFolder     = os.path.join( xshareFolder,'subs' )
iconsFolder    = os.path.join( xshareFolder,'icons' )



for folder in [xshareFolder, subsFolder, iconsFolder]:
	if not os.path.exists(folder):
		try    : os.mkdir(folder)
		except : pass

def log(s, level=xbmc.LOGNOTICE):
	#xbmc.log("{0}: {1}".format(addon.getAddonInfo("name"), msg))
	from utils import u2s
	if isinstance(s, basestring):
		xbmc.log(u2s(s), level)
	
	elif isinstance(s, list):
		for i in s:
			if not isinstance(i, basestring):
				i = str(i)
			xbmc.log(u2s(i), level)
	
	elif isinstance(s, dict):
		for i in s:
			if not isinstance(s[i], basestring):
				s[i] = str(s[i])
			xbmc.log('{}: {}'.format(i, u2s(s[i])), level)
	else:
		xbmc.log(str(s), level)

def mess(message='', title='', timeShown=5000):
	if message:
		from utils import u2s
		message = u2s(message)
		title   = ': [COLOR blue]%s[/COLOR]' % title if title else ''
		s0      = '[COLOR green][B]Xshare[/B][/COLOR]'+title
		
		if '!' in message:
			s1  = '[COLOR red]%s[/COLOR]' % message
		else:
			s1  = '[COLOR gold]%s[/COLOR]' % message
		
		ico = os.path.join(addon.getAddonInfo('path'),'icon.png')
		xbmc.executebuiltin(('XBMC.Notification(%s,%s,%s,%s)' % (s0, s1, timeShown, ico)))
	
	else:
		xbmc.executebuiltin("Dialog.Close(all, true)")

def get_input(title=u"", default=u""):
	result = ''
	keyboard = xbmc.Keyboard(default, title)
	keyboard.doModal()
	if keyboard.isConfirmed():
		result = keyboard.getText()
	if not result:result = ''
	return result.strip()

def add_sep_item(s):
	try    : label = '[COLOR lime]{:-^80}[/COLOR]'.format(s)
	except : label = '[COLOR lime]----------' + s + '----------[/COLOR]'
	icon = os.path.join(addon.getAddonInfo('path'),'icon.png')
	addir(label,'sepItem',icon,'No',1)

def addir(name, url, img='', mode='', page=1, query='', isFolder=False, menu=[]):
	def addMenu(menu):
		items = []
		for item in menu:
			label, name, url, img, mode, page, query = item
			arg = {
				'name' : u2s(name),
				'url'  : url,
				'img'  : img,
				'mode' : mode,
				'page' : page,
				'query':query
			}
			command = 'RunPlugin(%s?%s)'%(PATH, urlencode(arg))
			color = 'red' if 'emove' in query or 'elete' in query else 'lime'
			label = '[COLOR %s]%s[/COLOR]' % (color, label)
			items.append((label,command))
		return items

	from urllib import urlencode
	from utils import u2s, s2c
	
	name = u2s(s2c(name))
	
	servers = [
		("fshare.vn", "gold"),
		("vaphim.com", "gold"),
		("fsharefilm.com", "FFF08080"),
		("taiphimhd.net", "FF1E90FF"),
		("fcine.net", "orangered"),
		("subscene.com", "green")
	]
	
	srv = [i for i in servers if i[0] in str(url)]
	
	
	if 'fshare.vn' in str(url):
		mode = 'fshare.vn'
		if '/file/' in str(url):
			name = '[COLOR gold]Fshare [/COLOR] ' + name
			query = 'play'
			isFolder = False
		else:
			name = '[COLOR gold]Fshare %s[/COLOR] ' % name
			query = 'folder'
			isFolder = True
	
	elif 'fsharefilm.com' in str(url):
		if '/xem-phim/' in str(url):
			isFolder = False
		else:
			srv = srv[0]
			name = '[COLOR %s]%s[/COLOR] ' % (srv[1], srv[0].split('.')[0]) + name
			mode = srv[0]
			isFolder = True
			
	elif srv:
		srv = srv[0]
		name = '[COLOR %s]%s[/COLOR] ' % (srv[1], srv[0].split('.')[0]) + name
		mode = srv[0]
		isFolder = True
	
	if not img:
		img = os.path.join(addon.getAddonInfo('path'),'icon.png')
	
	listitem = listItem(name, iconImage=img, thumbnailImage=img)
	if not isFolder and url!='sepItem':
		listitem.setInfo(type="video", infoLabels={})
		listitem.setProperty('IsPlayable', 'true')
	
	if menu:
		if isinstance(menu,basestring):
			url += '|%s' % menu
		else:
			listitem.addContextMenuItems(addMenu(menu))
	
	args = {
		'name' : name,
		'url'  : url,
		'img'  : img,
		'mode' : mode,
		'page' : page,
		'query':query
	}
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),PATH+'?'+urlencode(args),listitem,isFolder)

