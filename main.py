import ctypes, threading, webview, pystray
from pynput import keyboard, mouse
from PIL import Image, ImageDraw
from quicktip.services.repository import PromptRepository
from quicktip.services.clipboard import ClipboardService
from quicktip.services.paste import PasteService
from quicktip.services.focus import FocusService
from quicktip.services.native_wheel import NativeWheel
from quicktip.viewmodels.prompt_vm import PromptViewModel
from quicktip.views.main_view import MainView
from quicktip.views.api import QuickTipApi
class App:
 def __init__(self):
  self.focus=FocusService(); self.vm=PromptViewModel(PromptRepository(),ClipboardService(),PasteService(),self.focus); self.main=None; self.ctrl=False; self.active=False; self.wheel=NativeWheel(self.choose)
 def choose(self,pid):
  self.close_wheel()
  self.vm.select(pid)
 def show_manager(self,*_):
  if self.main:self.main.show();return
  self.main=MainView(self.vm);self.main.show()
 def show_wheel(self):
  if self.active:return
  self.active=True;self.focus.capture();x,y=mouse.Controller().position;self.wheel.show(x,y,self.vm.enabled_prompts())
 def close_wheel(self): self.active=False;self.wheel.hide()
 def keyboard_loop(self):
  parts=[x.strip().lower() for x in self.vm.hotkey.split('+') if x.strip()]
  mods={'ctrl':'<ctrl>','alt':'<alt>','shift':'<shift>','win':'<cmd>'}
  combo='+'.join([mods.get(x,x if len(x)==1 else '<'+x+'>') for x in parts])
  keyboard.GlobalHotKeys({combo:self.show_wheel}).start()
  pressed=set()
  def name(k):
   if k in (keyboard.Key.ctrl,keyboard.Key.ctrl_l,keyboard.Key.ctrl_r):return 'ctrl'
   if k in (keyboard.Key.alt,keyboard.Key.alt_l,keyboard.Key.alt_r):return 'alt'
   if k in (keyboard.Key.shift,keyboard.Key.shift_l,keyboard.Key.shift_r):return 'shift'
   if k==keyboard.Key.space:return 'space'
   return getattr(k,'char',None) or str(k).replace('Key.','').lower()
  def press(k): pressed.add(name(k))
  def release(k):
   pressed.discard(name(k))
   if self.active and not (pressed & set(parts)):
    x,y=mouse.Controller().position;self.wheel.select_at(x,y);self.close_wheel()
  keyboard.Listener(on_press=press,on_release=release).run()
 def tray(self):
  im=Image.new('RGB',(64,64),(91,124,250));ImageDraw.Draw(im).ellipse((12,12,52,52),fill='white');pystray.Icon('QuickTip',im,'QuickTip',pystray.Menu(pystray.MenuItem('打开管理',self.show_manager),pystray.MenuItem('退出',lambda icon:icon.stop()))).run()
 def run(self):
  threading.Thread(target=self.keyboard_loop,daemon=True).start();threading.Thread(target=self.tray,daemon=True).start();self.show_manager();webview.start(debug=False)
if __name__=='__main__':App().run()

