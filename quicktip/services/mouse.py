from pynput import mouse
class MouseService:
    def position(self): return mouse.Controller().position
