import time
from Xlib import display, X
import pyxhook

last_window_name = None

def get_active_window_name():
    disp = display.Display()
    NET_WM_NAME = disp.intern_atom('_NET_WM_NAME')
    NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
    
    try:
        window_id = disp.get_property(NET_ACTIVE_WINDOW, X.AnyPropertyType, 0, 4096).value[0]
        window = disp.create_resource_object('window', window_id)
        window_name = window.get_wm_name()
        window.change_attributes(event_mask=X.FocusChangeMask)
        return window_name
    except X.error.XError:  # Simplistic error handling.
        return None

def on_event(event):
    global last_window_name
    current_window_name = get_active_window_name()
    if current_window_name != last_window_name:
        print(f"Janela/aba mudou para: {current_window_name}")
        last_window_name = current_window_name

hookman = pyxhook.HookManager()
hookman.KeyDown = on_event
hookman.HookKeyboard()
hookman.start()

while True:
    time.sleep(0.1)
