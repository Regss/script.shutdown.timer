# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui
import time
from datetime import datetime, timedelta

ADDON               = xbmcaddon.Addon()
ADDON_ID            = ADDON.getAddonInfo('id')
ADDON_NAME          = ADDON.getAddonInfo('name')
ADDON_ICON          = ADDON.getAddonInfo('icon')
ADDON_LANG          = ADDON.getLocalizedString

interval = 1 # interval in seconds
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
    
    if timer is not None and (timer - timedelta(seconds=30)) < now and (switch + timedelta(seconds = 5)) < now:
        
        secs = (int((timer - now).total_seconds())) % 60
        
        b = xbmcgui.DialogProgress()
        b.create(ADDON_NAME, 'Susspend')
        
        for i in range(secs):
            if (b.iscanceled()):
                b.close()
                resetTimer()
                xbmc.executebuiltin('XBMC.RunScript(' + ADDON_ID + ')')
                return
            
            p = int((float(100) / float(secs)) * float(i))
            b.update(p, ADDON_LANG(32103) + ' ' + str(secs - i) + ' ' + ADDON_LANG(32102))
            xbmc.sleep(1000)
        
        xbmc.executebuiltin('Notification(' + ADDON_NAME + ', ' + ADDON_LANG(32105).encode('utf-8') + ', 5000, ' + ADDON_ICON + ')')
        b.close()
        resetTimer()
        xbmc.executebuiltin(actions[int(ADDON.getSetting('action'))])
        
def resetTimer():
    xbmcgui.Window(10000).clearProperty(ADDON_ID + '_timer')

resetTimer()
    
while(not xbmc.abortRequested):
    checkTimer()
    xbmc.sleep(1000)
