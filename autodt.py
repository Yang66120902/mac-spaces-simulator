import time
import pygetwindow as gw
from pyvda import VirtualDesktop, AppView

# To store handles for windows that have been maximized and have been moved to the new virtual desktop
maximized_windows = set()

# Use to store the newly created virtual desktop objects
desktops = {}

def manage_windows():
    global maximized_windows, desktops
    for win in gw.getAllWindows():
        if win.isMaximized and win._hWnd not in maximized_windows:
            # If the window is maximized and is not processed before
            new_desktop = VirtualDesktop.create()  # Create a new virtual desktop
            AppView(hwnd=win._hWnd).move(new_desktop)  # Move the window to the new virtual desktop
            new_desktop.go()  # Switch to a new virtual desktop
            maximized_windows.add(win._hWnd)  # Record that this window has been processed
            desktops[win._hWnd] = new_desktop  # Stores the virtual desktop corresponding to this window
        elif not win.isMaximized and win._hWnd in maximized_windows:
            # If the window is no longer maximized and was processed before
            desktops[win._hWnd].remove()  # Delete a previously created virtual desktop
            del desktops[win._hWnd]  # Remove the record of this virtual desktop from the dictionary
            maximized_windows.remove(win._hWnd)  # Remove the record of this window from the collection

while True:
    manage_windows()
    time.sleep(0.1)
