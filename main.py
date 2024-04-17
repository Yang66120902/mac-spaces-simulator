import time
import pygetwindow as gw
from pyvda import VirtualDesktop, AppView

created = False
desktop = None
current_desktop = VirtualDesktop.current()

def check_window(title):
    global created, desktop
    try:
        win = gw.getWindowsWithTitle(title)[0]
        if created and not win.isMaximized:
            if desktop is None:
                print("WTF? Desktop is none with created")
                return
            current_desktop.go()
            desktop.remove()
            AppView(hwnd=win._hWnd).move(current_desktop)
            desktop = None
            created = False
        if win.isMaximized:
            if not created:
                desktop = VirtualDesktop.create()
                # win.move(desktop)
                AppView(hwnd=win._hWnd).move(desktop)
                desktop.go()
                created = True
        else:
            created = False
    except IndexError:
        created = False

while True:
    check_window("微信")
    time.sleep(0.1)