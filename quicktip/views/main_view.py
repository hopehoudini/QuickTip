from pathlib import Path
import webview
from quicktip.views.api import QuickTipApi
class MainView:
    def __init__(self, vm): self.vm=vm; self.window=None
    def show(self):
        self.window = webview.create_window('QuickTip 提示词管理', str(Path(__file__).parent / 'index.html'), js_api=QuickTipApi(self.vm), width=900, height=620, resizable=True)
        return self.window
