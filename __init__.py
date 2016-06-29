#!/usr/bin/env python
# -*- coding: utf-8 -*-

# DOCKER WORDPRESS TRAY INDICATOR PLUGIN
# ------------------------------------------------------------------------------
# @TODO:
# 1. Activate/Deactivate item if WP running
# 2. JSON configuration file

import os
import signal
import json

from urllib2 import Request, urlopen, URLError

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify


APPINDICATOR_ID = 'myappindicator'

print(os.path.dirname(__file__))

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.dirname(__file__) + '/wp.svg', appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    item_start = gtk.MenuItem('Start WordPress')
    item_start.connect('activate', start_wordpress)
    menu.append(item_start)
    item_stop = gtk.MenuItem('Stop WordPress')
    item_stop.connect('activate', stop_wordpress)
    menu.append(item_stop)
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu


def start_wordpress(_):
    os.system('docker run -p 80:80 -d --name wordpress eugeneware/docker-wordpress-nginx')
    notify.Notification.new("Docker WordPress", 'Запущен Wordpress на http://localhost', None).show()

def stop_wordpress(_):
    os.system('docker kill wordpress && docker rm -f wordpress')
    notify.Notification.new("Docker WordPress", 'Контейнер остановлен', None).show()

def quit(_):
    notify.uninit()
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
