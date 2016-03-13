# -*- coding: utf-8 -*-

import xbmc, xbmcaddon, addon, re, os

my_addon=addon.addon()
tempfolder=xbmc.translatePath('special://temp')
xsharefolder=os.path.join(tempfolder,'xshare')
def mess(message='',title='',timeShown=5000):
	if not message:xbmc.executebuiltin("Dialog.Close(all, true)")
	else:
		title=': [COLOR blue]%s[/COLOR]'%title if title else ''
		s0='[COLOR green][B]Xshare[/B][/COLOR]'+title
		s1='[COLOR red]%s[/COLOR]'%message if '!' in message else u'[COLOR gold]%s[/COLOR]'%message
		icon=my_addon.icon
		xbmc.executebuiltin((u'XBMC.Notification(%s,%s,%s,%s)'%(s0,s1,timeShown,icon)).encode("utf-8"))

def xshare_read(fn):
	try:f=open(os.path.join(xsharefolder,fn));content=f.read();f.close()
	except:content=''
	return content

def xshare_write(fn,content):
	if not content:return
	try:f=open(os.path.join(xsharefolder,fn),'w');f.write(content);f.close()
	except:pass

def get_input(title=u"", default=u""):
	result = ''
	keyboard = xbmc.Keyboard(default, title)
	keyboard.doModal()
	if keyboard.isConfirmed():
		result = keyboard.getText()
	return result.strip()

def xsearch(pattern,string,group=1,flags=0,result=''):
	try:s=re.search(pattern,string,flags).group(group)
	except:s=result
	return s

def s2u(s):return s.decode('utf-8') if isinstance(s,str) else s
def u2s(s):return s.encode('utf-8') if isinstance(s,unicode) else s
def unescape(string):return ' '.join(re.sub('&.+;',xsearch('&(\w).+;',s,1),s) for s in string.split())
