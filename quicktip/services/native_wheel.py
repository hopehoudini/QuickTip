import tkinter as tk,threading,queue,math
class NativeWheel:
 def __init__(self,on_choose):self.on_choose=on_choose;self.q=queue.Queue();self.last_prompts=[];self.last_x=0;self.last_y=0;self.ready=threading.Event();threading.Thread(target=self._run,daemon=True).start();self.ready.wait()
 def _run(self):
  self.root=tk.Tk();self.root.withdraw();self.root.overrideredirect(True);self.root.attributes('-topmost',True);self.root.configure(bg='#17213b');self.canvas=tk.Canvas(self.root,width=420,height=420,bg='#17213b',highlightthickness=0);self.canvas.pack();self.ready.set();self.root.after(30,self._poll);self.root.mainloop()
 def _poll(self):
  try:
   while 1:
    item=self.q.get_nowait();item[0](*item[1:])
  except queue.Empty: pass
  self.root.after(30,self._poll)
 def show(self,x,y,prompts):self.q.put((self._show,x,y,prompts))
 def _show(self,x,y,prompts):
  self.last_prompts,self.last_x,self.last_y=prompts,x,y;self.canvas.delete('all');self.canvas.create_oval(2,2,418,418,fill='#17213b',outline='#7187e8',width=2);n=max(1,len(prompts))
  for i,p in enumerate(prompts):
   a=i*2*math.pi/n-math.pi/2;cx=210+math.cos(a)*150;cy=210+math.sin(a)*150;self.canvas.create_rectangle(cx-48,cy-28,cx+48,cy+28,fill='#2d4278',outline='#6b82e2',tags=p.id);self.canvas.create_text(cx,cy,text=p.title[:12],fill='white',tags=p.id)
  self.canvas.create_text(210,210,text='松开选择',fill='#b9c6f2');self.root.geometry(f'+{int(x-210)}+{int(y-210)}');self.root.deiconify();self.root.lift()
 def select_at(self,x,y):
  if self.last_prompts:
   a=math.atan2(y-self.last_y,x-self.last_x)+math.pi/2;i=int(round((a%(2*math.pi))/(2*math.pi/len(self.last_prompts))))%len(self.last_prompts);self.on_choose(self.last_prompts[i].id)
 def hide(self):self.q.put((self._hide,))
 def _hide(self):self.root.withdraw()

