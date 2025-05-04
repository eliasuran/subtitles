import tkinter as tk
import tkinter.font as tkFont
from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from app.subtitles.subtitles import Subtitles


class TkWrapper:
    def __init__(self):
        self.window_width = 1000
        self.window_height = 58
        self.settings_height = 118
        self.opacity = 0.9
        self.x_position = 540
        self.y_position = 900

        self.root = self.tk_init()
        self.text_widget = self.create_text_widget()
        self.settings_frame = self.create_settings_frame()
        self.settings_button = self.create_settings_button()
        self.pause_button = self.create_pause_button()

        self.timeline_var = tk.DoubleVar()
        self.user_dragging_timeline = False
        self.timeline = self.create_timeline()

        self.settings_visible = False

        self.hide_menu_buttons()
        self.root.bind("<Enter>",self.show_menu_buttons)
        self.root.bind("<Leave>",self.hide_menu_buttons)

        self.root.after(50, self.enforce_override) 

        self.subtitle_controller: Optional["Subtitles"] = None


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
        self.x_position = x
        self.y_position = y
        self.root.geometry(f"+{x}+{y}")


    def create_text_widget(self):
        text_widget = tk.Text(
            self.root,
            bg="black",
            fg="white",
            width=self.window_width,
            height=1,
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


    def create_settings_frame(self):
        frame = tk.Frame(
            self.root,
            bg="black",
            highlightbackground="gray",
            highlightthickness=1,
            height=60
        )
        frame.pack_propagate(False)
        return frame
    

    def toggle_settings(self):
        if self.settings_visible:
            self.settings_frame.pack_forget()
            self.root.geometry(f"{self.window_width}x{self.window_height}+{self.x_position}+{self.y_position}")
            self.settings_visible = False
        else:
            self.root.geometry(f"{self.window_width}x{self.settings_height}+{self.x_position}+{self.y_position}")
            self.settings_frame.pack(side=tk.BOTTOM,fill=tk.X,expand=False)
            self.settings_visible = True


    def create_settings_button(self):
        button = tk.Button(
            self.root,
            text="⚙️",
            bg="black",
            fg="white",
            relief=tk.FLAT,
            command=self.toggle_settings
        )
        button.place(x=self.window_width-50,y=10)
        return button


    def create_pause_button(self):
        def toggle_pause():
            if self.subtitle_controller:
                self.subtitle_controller.toggle_pause()

        button = tk.Button(
            self.root,
            text="⏸️",
            command=toggle_pause
        )
        button.place(x=self.window_width-100,y=10)
        return button


    def create_timeline(self):
        frame = tk.Frame(self.settings_frame, bg="black")
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.current_time_label = tk.Label(
            frame, 
            text="00:00", 
            bg="black", 
            fg="white"
        )
        self.current_time_label.pack(side=tk.LEFT, padx=5)
        
        self.timeline = tk.Scale(
            frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=self.window_width - 1000,
            bg="black",
            fg="white",
            highlightthickness=0,
            sliderrelief=tk.FLAT,
            sliderlength=10,
            troughcolor="#555555",
            variable=self.timeline_var
        )
        self.timeline.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.timeline.bind("<ButtonPress-1>",self.on_timeline_press)
        self.timeline.bind("<ButtonRelease-1>",self.on_timeline_release)
        
        return self.timeline

    
    def on_timeline_press(self,event=None):
        self.user_dragging_timeline = True


    def on_timeline_release(self, event=None):
        self.user_dragging_timeline = False
        if self.subtitle_controller:
            value = self.timeline_var.get()
            self.subtitle_controller.seek_to(value)


    def update_timeline_position(self, current_time, total_time):
        if hasattr(self, 'timeline') and self.timeline:
            if self.timeline.cget('to') != total_time and total_time > 0:
                self.timeline.config(to=total_time)

            if not self.user_dragging_timeline:
                self.timeline_var.set(current_time)
            
            current_min = int(current_time // 60)
            current_sec = int(current_time % 60)
            
            self.current_time_label.config(text=f"{current_min:02d}:{current_sec:02d}")


    def show_menu_buttons(self, event=None):
        self.settings_button.place(x=self.window_width-50,y=10)
        self.pause_button.place(x=self.window_width-100,y=10)


    def hide_menu_buttons(self, event=None):
        self.settings_button.place_forget()
        self.pause_button.place_forget()


    def set_subtitle_controller(self,subtitle_controller):
        self.subtitle_controller = subtitle_controller 


if __name__ == "__main__":
    app = TkWrapper()    
    app.text_widget.insert(tk.END,"xdd","center")
    app.root.mainloop()
