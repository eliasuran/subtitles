import tkinter as tk
import time

from app.lib.tk_wrapper import TkWrapper

class Subtitles:
    def __init__(self, subtitles):
        self.subtitles = subtitles
        self.start_time = 0
        self.current_subtitle_index = 0

        self.tkw = TkWrapper()


    def update_subtitle(self):
        current_time = (time.time() * 1000) - self.start_time
        
        self.tkw.text_widget.config(state=tk.NORMAL)
        self.tkw.text_widget.delete(1.0, tk.END)
        
        if self.current_subtitle_index >= len(self.subtitles):
            self.tkw.text_widget.config(state=tk.DISABLED)
            return
            
        current_subtitle = self.subtitles[self.current_subtitle_index]
        
        if current_subtitle["start"] <= current_time < current_subtitle["end"]:
            self.tkw.text_widget.insert(tk.END, " ".join(current_subtitle["text_list"]), 'center')
        elif current_time >= current_subtitle["end"]:
            self.current_subtitle_index += 1
        
        self.tkw.text_widget.config(state=tk.DISABLED)
        
        self.tkw.root.after(50, self.update_subtitle)


    def start(self) -> None:
        self.start_time = time.time() * 1000
        self.update_subtitle()
        self.tkw.root.mainloop()
