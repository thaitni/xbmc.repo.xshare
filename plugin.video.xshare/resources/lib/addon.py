# -*- coding: utf-8 -*-

import xbmc, xbmcaddon, os

class addon:

    def __init__(self):
		self.addon			= xbmcaddon.Addon()
		self.info			= self.addon.getAddonInfo
		self.name			= self.info('name')
		self.version		= self.info('version')
		self.get_setting	= self.addon.getSetting
		self.set_setting	= self.addon.setSetting

		self.src_path		= xbmc.translatePath(self.info('path'))
		self.data_path		= xbmc.translatePath(self.info('profile'))
		self.temp_path		= xbmc.translatePath('special://temp')

		self.data_folder	= os.path.join(self.data_path,'data')
		self.icon_folder	= os.path.join(self.data_path,'icon')
		self.icon			= os.path.join(self.icon_folder,'icon.png')
