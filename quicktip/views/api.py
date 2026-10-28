import webview
class QuickTipApi:
 def __init__(self,vm,close_callback=None):self.vm=vm;self.close_callback=close_callback
 def state(self):return self.vm.snapshot()
 def set_hotkey(self,value):self.vm.set_hotkey(value);return self.state()
 def add_prompt(self,title,content):self.vm.add(title,content);return self.state()
 def update_prompt(self,pid,title,content,enabled=True):self.vm.update(pid,title,content,enabled);return self.state()
 def delete_prompt(self,pid):self.vm.remove(pid);return self.state()
 def choose(self,pid):
  r={'pasted':self.vm.select(pid)}
  if self.close_callback:self.close_callback()
  return r
 def close(self):
  if self.close_callback:self.close_callback()
  return True
