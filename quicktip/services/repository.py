import json, os, tempfile
from pathlib import Path
from quicktip.models.prompt import Prompt
class PromptRepository:
    def __init__(self):
        self.path = Path(os.environ.get('APPDATA', Path.home())) / 'QuickTip' / 'prompts.json'; self.path.parent.mkdir(parents=True, exist_ok=True)
    def load(self):
        if not self.path.exists():
            items=[Prompt('welcome','欢迎使用','请用三句话总结这段内容，并列出下一步行动。'),Prompt('translate','翻译','请将以下内容翻译成自然、准确的中文：'),Prompt('polish','润色','请润色以下文字，保持原意并让表达更专业：')]; self.save(items); return items
        try: return [Prompt.from_dict(x) for x in json.loads(self.path.read_text(encoding='utf-8'))]
        except (OSError, ValueError, KeyError): return []
    def save(self, prompts):
        payload=json.dumps([p.to_dict() for p in prompts],ensure_ascii=False,indent=2); fd,temp=tempfile.mkstemp(prefix='prompts-',suffix='.json',dir=self.path.parent)
        with os.fdopen(fd,'w',encoding='utf-8') as f: f.write(payload)
        try: os.replace(temp,self.path)
        except OSError:
            self.path.write_text(payload,encoding='utf-8')
            try: os.unlink(temp)
            except OSError: pass
