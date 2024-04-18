import time
import pygetwindow as gw
from pyvda import VirtualDesktop, AppView

# 用于存储已经最大化并且已经移动到新虚拟桌面的窗口的句柄
maximized_windows = set()

# 用于存储新创建的虚拟桌面对象
desktops = {}

def manage_windows():
    global maximized_windows, desktops
    for win in gw.getAllWindows():
        if win.isMaximized and win._hWnd not in maximized_windows:
            # 如果窗口最大化并且之前没有处理过
            new_desktop = VirtualDesktop.create()  # 创建新的虚拟桌面
            AppView(hwnd=win._hWnd).move(new_desktop)  # 移动窗口到新的虚拟桌面
            new_desktop.go()  # 切换到新的虚拟桌面
            maximized_windows.add(win._hWnd)  # 记录这个窗口已经处理过
            desktops[win._hWnd] = new_desktop  # 存储这个窗口对应的虚拟桌面
        elif not win.isMaximized and win._hWnd in maximized_windows:
            # 如果窗口不再最大化并且之前处理过
            desktops[win._hWnd].remove()  # 删除之前创建的虚拟桌面
            del desktops[win._hWnd]  # 从字典中删除这个虚拟桌面的记录
            maximized_windows.remove(win._hWnd)  # 从集合中删除这个窗口的记录

while True:
    manage_windows()
    time.sleep(0.1)
