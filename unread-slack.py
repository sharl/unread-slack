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
import win32con
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
            MenuItem(TITLE, self.setForeground, default=True),
            MenuItem('Exit', self.stopApp),
        )
        self.app = Icon(name=TITLE, title=TITLE, icon=self.dimm_image, menu=menu)

    def _scan_slack_window(self):
        target_hwnd = []

        def callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd).strip()
                if 'Slack' in title and title.startswith(('(*)', 'Slack - (*)', 'Slack - *')):
                    target_hwnd.append(hwnd)
                    return False
            return True

        try:
            win32gui.EnumWindows(callback, None)
        except Exception:
            pass

        return target_hwnd[0] if target_hwnd else None

    def setForeground(self):
        hwnd = self._scan_slack_window()
        if hwnd:
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)

    def doTask(self):
        while self.running:
            begin = time.time()
            if self._scan_slack_window():
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
