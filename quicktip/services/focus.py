import ctypes
class FocusService:
    def __init__(self): self.hwnd=None
    def capture(self): self.hwnd=ctypes.windll.user32.GetForegroundWindow()
    def restore(self):
        if self.hwnd: ctypes.windll.user32.SetForegroundWindow(self.hwnd)
