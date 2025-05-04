import tkinter as tk
import tkinter.font as tkFont
import time

class SubtitlesClass:
    def __init__(self, subtitles):
        self.subtitles = subtitles
        self.window_width = 1000
        self.window_height = 58
        self.start_time = 0
        self.current_subtitle_index = 0
        self.opacity = 0.9
        self.x_position = 400
        self.y_position = 400

        self.root = self.tk_init()
        self.text_widget = self.create_text_widget()


    def tk_init(self) -> tk.Tk:
        root = tk.Tk()
        root.geometry(f"{self.window_width}x{self.window_height}+{self.x_position}+{self.y_position}")
        root.title("Subtitles")

        root.wm_attributes("-topmost", True)
        root.wm_attributes("-transparent", True)
        root.attributes("-alpha", self.opacity)
        root.configure(bg="black")

        return root
    

    def update_subtitle(self):
        current_time = (time.time() * 1000) - self.start_time
        
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        
        if self.current_subtitle_index >= len(self.subtitles):
            self.text_widget.config(state=tk.DISABLED)
            return
            
        current_subtitle = self.subtitles[self.current_subtitle_index]
        
        if current_subtitle["start"] <= current_time < current_subtitle["end"]:
            self.text_widget.insert(tk.END, " ".join(current_subtitle["text_list"]), 'center')
        elif current_time >= current_subtitle["end"]:
            self.current_subtitle_index += 1
        
        self.text_widget.config(state=tk.DISABLED)
        
        self.root.after(50, self.update_subtitle)


    def create_text_widget(self):
        text_widget = tk.Text(
            self.root,
            bg="black",
            fg="white",
            width=self.window_width,
            height=self.window_height,
            wrap=tk.WORD,
            borderwidth=0,
            border=0,
            highlightthickness=0,
            relief=tk.FLAT,
            font=tkFont.Font(family="Arial", size=30, weight="normal"),
            cursor="arrow"
        )
        text_widget.tag_configure('center', justify='center')
        text_widget.pack(pady=2, padx=2, fill=tk.BOTH, expand=True)

        text_widget.bind("<Button-1>", lambda e: "break")
        text_widget.bind("<B1-Motion>", lambda e: "break")
        text_widget.bind("<Double-Button-1>", lambda e: "break")
        text_widget.bind("<Triple-Button-1>", lambda e: "break")
        text_widget.bind("<FocusIn>", lambda e: text_widget.master.focus()) 

        text_widget.bind("<ButtonPress-1>", self.start_move)
        text_widget.bind("<B1-Motion>", self.do_move)

        return text_widget


    #TODO: make own class for tkinter stuff
    def enforce_override(self):
        self.root.overrideredirect(True)


    def start_move(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y


    def do_move(self, event):
        x = event.x_root - self._drag_start_x
        y = event.y_root - self._drag_start_y
        self.root.geometry(f"+{x}+{y}")


    def start(self) -> None:
        self.start_time = time.time() * 1000
        self.update_subtitle()
        self.root.after(50, self.enforce_override) 
        self.root.mainloop()
    

def go(subtitles):
    s = SubtitlesClass(subtitles)
    s.start()
