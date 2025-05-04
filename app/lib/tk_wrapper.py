import tkinter as tk
import tkinter.font as tkFont

class TkWrapper:
    def __init__(self):
        self.window_width = 1000
        self.window_height = 58
        self.opacity = 0.9
        self.x_position = 540
        self.y_position = 900

        self.root = self.tk_init()
        self.text_widget = self.create_text_widget()

        self.root.after(50, self.enforce_override) 


    def tk_init(self) -> tk.Tk:
        root = tk.Tk()
        root.geometry(f"{self.window_width}x{self.window_height}+{self.x_position}+{self.y_position}")
        root.title("Subtitles")

        root.wm_attributes("-topmost", True)
        root.wm_attributes("-transparent", True)
        root.attributes("-alpha", self.opacity)
        root.configure(bg="black")

        return root


    def enforce_override(self):
        self.root.overrideredirect(True)


    def start_move(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y


    def do_move(self, event):
        x = event.x_root - self._drag_start_x
        y = event.y_root - self._drag_start_y
        self.root.geometry(f"+{x}+{y}")


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


if __name__ == "__main__":
    app = TkWrapper()    
    app.text_widget.insert(tk.END,"xdd","center")
    app.root.mainloop()
