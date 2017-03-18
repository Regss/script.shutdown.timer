# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui
import time
import json
from datetime import datetime, timedelta

ADDON               = xbmcaddon.Addon()
ADDON_ID            = ADDON.getAddonInfo('id')
ADDON_NAME          = ADDON.getAddonInfo('name')
ADDON_ICON          = ADDON.getAddonInfo('icon')
ADDON_LANG          = ADDON.getLocalizedString

ADDON_PATH          = xbmc.translatePath(ADDON.getAddonInfo('path'))
actions = ['Suspend', 'ShutDown', 'Quit']

def checkTimer():
    now = datetime.now()
        
    try:
        timer_prop = xbmcgui.Window(10000).getProperty(ADDON_ID + '_timer')
        timer = datetime(*(time.strptime(timer_prop, '%d-%m-%Y %H:%M:%S')[0:6]))
    except:
        timer = None
        
    try:
        switch_prop = xbmcgui.Window(10000).getProperty(ADDON_ID + '_switch')
        switch = datetime(*(time.strptime(switch_prop, '%d-%m-%Y %H:%M:%S')[0:6]))
    except:
        switch = None
    
    if timer is not None and (timer - timedelta(seconds=31)) < now and (switch + timedelta(seconds = 5)) < now:
        
        secs = (int((timer - now).total_seconds())) % 60
        
        if secs > 0:
            if secs % 10 == 0:
                display = SHOW('script-shutdown.timer-notify.xml', ADDON_PATH, label_title=ADDON_NAME, label_text=ADDON_LANG(32103) + ' ' + str(secs) + ' ' + ADDON_LANG(32102))
                display.doModal()
                del display
        else:
            resetTimer()
            display = SHOW('script-shutdown.timer-notify.xml', ADDON_PATH, label_title=ADDON_NAME, label_text=ADDON_LANG(32105))
            display.doModal()
            del display
            xbmc.executebuiltin(actions[int(ADDON.getSetting('action'))])
        
def resetTimer():
    xbmcgui.Window(10000).clearProperty(ADDON_ID + '_timer')

class Monitor(xbmc.Monitor):
    def __init__(self):
        resetTimer()
            
    def onNotification(self, sender, method, data):
        data = json.loads(data)
        if 'System.OnWake' in method:
            resetTimer()

class SHOW(xbmcgui.WindowXMLDialog):
    
    def __init__(self, xmlFile, resourcePath, label_title, label_text):
        
        self.label_title = label_title
        self.label_text = label_text
        
    def onInit(self):
        self.getControl(10080).setLabel(self.label_title)
        self.getControl(10081).setLabel(self.label_text)
        
        xbmc.sleep(3000)
        self.close()
        
monitor = Monitor()

while(not xbmc.abortRequested):
    checkTimer()
    xbmc.sleep(1000)
