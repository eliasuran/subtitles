import tkinter as tk
import time
from typing import TYPE_CHECKING, Any, Dict, List
if TYPE_CHECKING:
    from app.lib.tk_wrapper import TkWrapper

class Subtitles:
    def __init__(self, subtitles: List[Dict[str, Any]], tkw: 'TkWrapper'):
        self.subtitles = subtitles
        self.start_time = time.time() * 1000
        self.current_subtitle_index = 0
        self.current_time = 0
        self.paused = False
        self.tkw = tkw
        self.tkw.set_subtitle_controller(self)
        
        self.total_duration = self._calculate_total_duration()
        self.update_timeline()
    

    def _calculate_total_duration(self) -> int:
        if not self.subtitles:
            return 0
        return max(subtitle["end"] for subtitle in self.subtitles)
    

    def update_subtitle(self):
        if not self.paused:
            self.current_time = self.current_time + 50
            self.tkw.text_widget.config(state=tk.NORMAL)
            self.tkw.text_widget.delete(1.0, tk.END)
            
            if self.current_subtitle_index >= len(self.subtitles):
                self.tkw.text_widget.config(state=tk.DISABLED)
                return
                
            current_subtitle = self.subtitles[self.current_subtitle_index]
            
            if current_subtitle["start"] <= self.current_time < current_subtitle["end"]:
                self.tkw.text_widget.insert(tk.END, " ".join(current_subtitle["text_list"]), 'center')
            elif self.current_time >= current_subtitle["end"]:
                self.current_subtitle_index += 1
            
            self.tkw.text_widget.config(state=tk.DISABLED)
            
            self.update_timeline()
        
        self.tkw.root.after(50, self.update_subtitle)
    

    def update_timeline(self):
        current_sec = self.current_time / 1000
        total_sec = self.total_duration / 1000
        self.tkw.update_timeline_position(current_sec, total_sec)
    

    def seek_to(self, position_sec: float):
        position_ms = int(position_sec * 1000)
        position_ms = max(0, min(position_ms, self.total_duration))
        self.current_time = position_ms
        self.current_subtitle_index = self._find_subtitle_index_for_time(position_ms)
        self.update_subtitle_display()
        self.update_timeline()
    

    def _find_subtitle_index_for_time(self, time_ms: int) -> int:
        for i, subtitle in enumerate(self.subtitles):
            if subtitle["start"] <= time_ms < subtitle["end"]:
                return i
            if time_ms < subtitle["start"]:
                return i
        return len(self.subtitles)
    

    def update_subtitle_display(self):
        self.tkw.text_widget.config(state=tk.NORMAL)
        self.tkw.text_widget.delete(1.0, tk.END)
        
        if self.current_subtitle_index < len(self.subtitles):
            current_subtitle = self.subtitles[self.current_subtitle_index]
            
            if current_subtitle["start"] <= self.current_time < current_subtitle["end"]:
                self.tkw.text_widget.insert(tk.END, " ".join(current_subtitle["text_list"]), 'center')
        
        self.tkw.text_widget.config(state=tk.DISABLED)
    

    def pause(self):
        self.paused = True
    

    def play(self):
        self.paused = False
    

    def toggle_pause(self):
        if self.paused:
            self.play()
            self.tkw.pause_button.config(text="⏸️")
        else:
            self.pause()
            self.tkw.pause_button.config(text="▶️")
