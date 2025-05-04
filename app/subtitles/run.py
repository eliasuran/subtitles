from typing import Any, Dict, List
from app.lib.tk_wrapper import TkWrapper
from app.subtitles.subtitles import Subtitles


class Runner:
    def __init__(self,subtitles: List[Dict[str, Any]]):
        self.tkw = TkWrapper()
        self.s = Subtitles(subtitles,self.tkw)


    def run(self):
        self.s.update_subtitle()
        self.tkw.root.mainloop()
