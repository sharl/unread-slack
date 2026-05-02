# -*- coding: utf-8 -*-
import io
import ctypes
import threading
import time

from PIL import Image, ImageEnhance
from bs4 import BeautifulSoup as bs
from pystray import Icon, Menu, MenuItem
import darkdetect as dd
import requests
import win32gui

TITLE = 'unread Slack messages'
INTERVAL = 1
BASE_URL = 'https://slack.com'
PreferredAppMode = {
    'Light': 0,
    'Dark': 1,
}
# https://github.com/moses-palmer/pystray/issues/130
ctypes.windll['uxtheme.dll'][135](PreferredAppMode[dd.theme()])


class taskTray:
    def __init__(self):
        self.running = False

        session = requests.Session()
        with session.get(BASE_URL) as r:
            soup = bs(r.content, 'html.parser')
            link_tag = soup.find('link', id='favicon')
            favicon = link_tag.get('href') if link_tag else None
            if favicon:
                self.icon_image = Image.open(io.BytesIO(session.get(favicon).content))
                self.dimm_image = ImageEnhance.Brightness(self.icon_image.convert('RGB')).enhance(0.6).convert('L')

        menu = Menu(
            MenuItem(TITLE, lambda: False),
            MenuItem('Exit', self.stopApp),
        )
        self.app = Icon(name=TITLEE, title=TITLE, icon=self.dimm_image, menu=menu)

    def doTask(self):
        def check_unread_slack():
            found = False

            def callback(hwnd, _):
                nonlocal found
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd).strip()
                    if title and 'Slack' in title:
                        if title.startswith((
                                '(*)',
                                'Slack - (*)',
                        )):
                            found = True
                            return False
                return True

            try:
                win32gui.EnumWindows(callback, None)
            except Exception:
                pass
            return found

        while self.running:
            begin = time.time()
            if check_unread_slack():
                self.app.icon = self.icon_image
                self.app.title = 'Slack - Unread message detected'
            else:
                self.app.icon = self.dimm_image
                self.app.title = 'Slack - No unread messages'
            elapsed = time.time() - begin
            time.sleep(max(0, INTERVAL - elapsed))

    def stopApp(self):
        self.running = False
        self.app.stop()

    def runApp(self):
        self.running = True

        task_thread = threading.Thread(target=self.doTask)
        task_thread.start()

        self.app.run()


if __name__ == '__main__':
    taskTray().runApp()
