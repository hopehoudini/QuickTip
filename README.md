# QuickTip

Windows 快捷提示词轮盘 MVP，采用 Python + pywebview + HTML/CSS/JavaScript，并按 MVVM 组织。

## 功能
- 系统托盘常驻
- 全局热键：默认按住 `Ctrl+Space` 呼出轮盘
- 鼠标附近 8 槽位环形菜单
- 按住热键移动鼠标选择，松开提交
- 提示词管理窗口：新增、编辑、删除、启停
- 本地 JSON 存储（`%APPDATA%\QuickTip\prompts.json`）
- 复制后尝试粘贴到原活动窗口，失败时保留剪贴板

## 启动
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

开发时可直接运行 `python main.py`。打包：
```powershell
pip install pyinstaller
pyinstaller --noconsole --onefile --name QuickTip main.py
```

## 已知限制
Windows 安全输入框、管理员权限窗口和部分 Electron/远程桌面应用可能拒绝模拟粘贴，此时会回退为复制。全局监听依赖 pynput，杀毒软件可能要求授权。
