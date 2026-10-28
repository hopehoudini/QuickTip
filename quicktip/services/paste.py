import time,pyperclip
import pyautogui
class PasteService:
 def paste(self,text=None):
  if not text:return False
  pyperclip.copy(text);time.sleep(.1);pyautogui.hotkey('ctrl','v');return True
