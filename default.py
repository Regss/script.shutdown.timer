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
ADDON_PATH          = xbmc.translatePath(ADDON.getAddonInfo('path'))
ADDON_LANG          = ADDON.getLocalizedString

timers = [15, 30, 60, 90, 120]

class Timer:
    
    def __init__(self):
        self.start()

    def start(self):
        
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
        
        if switch is None or (switch + timedelta(seconds = 5)) < now:
            xbmcgui.Window(10000).setProperty(ADDON_ID + '_switch', now.strftime('%d-%m-%Y %H:%M:%S'))
            # sprawdz i wyswietl timer
            if timer is None:
                self.notify(ADDON_LANG(32101))
            else:
                self.notify(ADDON_LANG(32106) + ': ' + self.timeDiffToString(timer, now))
            return
        
        xbmcgui.Window(10000).setProperty(ADDON_ID + '_switch', now.strftime('%d-%m-%Y %H:%M:%S'))
        
        for t in range(len(timers)):
            if timer is None or (now + timedelta(minutes = timers[t]) - timedelta(seconds = 5) > timer):
                xbmcgui.Window(10000).setProperty(ADDON_ID + '_timer', (now + timedelta(minutes = timers[t])).strftime('%d-%m-%Y %H:%M:%S'))
                self.notify(ADDON_LANG(32103) + ' ' + str(timers[t]) + ' ' + ADDON_LANG(32104))
                return
                
        xbmcgui.Window(10000).clearProperty(ADDON_ID + '_timer')
        self.notify(ADDON_LANG(32101))
            
    def timeDiffToString(self, startTime, endTime):
        total_secs = int((startTime - endTime).total_seconds())
        secs = total_secs % 60
        total_mins = total_secs / 60
        mins = total_mins % 60
        hours = total_mins / 60
        timer_str = format(hours, '02') + ':' + format(mins, '02') + ':' + format(secs, '02')
        return timer_str
    
    def notify(self, msg, title=ADDON_NAME):
        display = SHOW('script-shutdown.timer-notify.xml', ADDON_PATH, label_title=title, label_text=msg.encode('utf-8'))
        display.doModal()
        del display
        
class SHOW(xbmcgui.WindowXMLDialog):
    
    def __init__(self, xmlFile, resourcePath, label_title, label_text):
        
        self.label_title = label_title
        self.label_text = label_text
        
    def onInit(self):
        self.getControl(10080).setLabel(self.label_title)
        self.getControl(10081).setLabel(self.label_text)
        xbmc.sleep(2000)
        self.close()
        
Timer()