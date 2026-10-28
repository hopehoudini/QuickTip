import uuid,json
from quicktip.models.prompt import Prompt
class PromptViewModel:
 def __init__(self,repo,clipboard,paste,focus=None):
  self.repo,self.clipboard,self.paste_service,self.focus=repo,clipboard,paste,focus;self.prompts=repo.load();self.settings_path=repo.path.parent/'settings.json';self.hotkey='ctrl+space'
  try:
   if self.settings_path.exists():self.hotkey=json.loads(self.settings_path.read_text(encoding='utf-8')).get('hotkey',self.hotkey)
  except Exception:pass
  self.on_change=None
 def enabled_prompts(self):return [p for p in self.prompts if p.enabled]
 def snapshot(self):return {'prompts':[p.to_dict() for p in self.prompts],'slots':[p.to_dict() for p in self.enabled_prompts()],'hotkey':self.hotkey}
 def add(self,title,content):self.prompts.append(Prompt(str(uuid.uuid4()),title.strip() or '未命名',content));self.commit()
 def update(self,pid,title,content,enabled=True):
  for p in self.prompts:
   if p.id==pid:p.title,p.content,p.enabled=title,content,enabled
  self.commit()
 def remove(self,pid):self.prompts=[p for p in self.prompts if p.id!=pid];self.commit()
 def set_hotkey(self,value):self.hotkey=value;self.settings_path.write_text(json.dumps({'hotkey':value},ensure_ascii=False),encoding='utf-8')
 def select(self,pid):
  p=next((x for x in self.prompts if x.id==pid),None)
  if not p:return False
  self.clipboard.copy(p.content)
  if self.focus:self.focus.restore()
  return self.paste_service.paste(p.content)
 def commit(self):self.repo.save(self.prompts);self.on_change and self.on_change(self.snapshot())

