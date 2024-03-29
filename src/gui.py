""" daily timer graphical interface """

import tkinter as tk
import tkinter.font as tkFont
from dataclasses import dataclass

from src import interfaces

@dataclass
class Colors(interfaces.ColorsInterface):
    """ colors definition """
    def __init__(self, mode):
        if mode == "dark":
            self.window_background = "#1e1e1e"  # dark grey
            self.text_background = "#252526"    # light grey
            self.button_background = "#333333"    # light grey
            self.button_foreground = "#ffffff"  # black
            self.normal = "#ffffff"             # white
            self.pause = "#2cc743"              # green
            self.warning = "#f2dc4e"            # yellow
            self.overtime = "#eb4034"           # red
        else:
            self.window_background = "#f0f0f0"  # light grey
            self.text_background = "#ffffff"    # white
            self.button_background = "#e9e9ed"  # grey
            self.button_foreground = "#000000"  # black
            self.normal = "#000000"             # black
            self.pause = "#2cc743"              # green
            self.warning = "#f2dc4e"            # yellow
            self.overtime = "#eb4034"           # red

class Interface(interfaces.UiInterface):
    """ Tkinter interface """
    timer = 0

    def __init__(self, theme_mode:str, core: interfaces.CoreInterface, start_time: int) -> None:
        self.window = tk.Tk()
        self.colors = Colors(theme_mode)
        self.core = core
        # update core ui object
        self.core.gui = self
        self.core.running_color = self.colors.normal

        ### window
        self.window.title("Daily Timer")
        self.window.configure(
            background = self.colors.window_background,
            width = 300,
            height = 550,
        )
        self.window.resizable(False, False)
        self.window.geometry((
            f"{self.window['width']}x{self.window['height']}"
            f"+{(self.window.winfo_screenwidth() - self.window['width']) // 2}"
            f"+{(self.window.winfo_screenheight() - self.window['height']) // 2}"
        ))

        ### timer
        self.label_timer = tk.Label(
            self.window,
            font = tkFont.Font(family="Helvetica", weight="bold",size=70),
            # text = "00:00",
            text = f"{start_time//60:02d}:{start_time%60:02d}",
            background = self.colors.window_background,
            foreground= self.colors.pause,
        )
        self.label_timer.place(x=0,y=0,width=300,height=100)

        ### user list
        self.number_users = 10
        self.current_user = 0
        self.start_scroll = 0
        self.end_scroll = self.number_users - 1
        self.text_users = tk.Message(
            self.window,
            background = self.colors.text_background,
            foreground= self.colors.normal,
            font = tkFont.Font(family="Courier",size=12),
            anchor="w",
        )
        self.text_users.place(x=10,y=100,width=280,height=400)

        ### buttons
        buttons_font = tkFont.Font(family="Helvetica",size=9)

        button_toggle=tk.Button(
            self.window,
            background = self.colors.button_background,
            foreground = self.colors.button_foreground,
            highlightthickness = 0,
            font = buttons_font,
            text = "Start/Pause",
            command = self.core.toogle_timer,
        )

        button_next=tk.Button(
            self.window,
            background = self.colors.button_background,
            foreground= self.colors.button_foreground,
            highlightthickness = 0,
            font = buttons_font,
            text = "Next",
            command = self.core.next_user,
        )
        
        button_previous=tk.Button(
            self.window,
            background = self.colors.button_background,
            foreground= self.colors.button_foreground,
            highlightthickness = 0,
            state="normal",
            font = buttons_font,
            text = "Previous",
            command = self.core.previous_user
        )
        
        ## Button order
        # button_toggle.place(x=20,y=510,width=80,height=30)
        # button_next.place(x=120,y=510,width=70,height=30)
        # button_previous.place(x=210,y=510,width=70,height=30)
        ## reorder
        button_previous.place(x=20,y=510,width=70,height=30)
        button_toggle.place(x=110,y=510,width=80,height=30)
        button_next.place(x=210,y=510,width=70,height=30)
        

    def update_timer(self, seconds: int, color: str = "") -> None:
        """ Updates Timer label value and color """
        if color:
            self.label_timer["foreground"] = color
        self.label_timer["text"] = f"{seconds//60:02d}:{seconds%60:02d}"

    def update_timer_color(self, color: str) -> None:
        """ Updates Timer color """
        self.label_timer["foreground"] = color

    def update_users(self, users: list, current: int):
        """ Update user list texts """
        # number of lines fewer or equal than window size.
        if len(users) <= self.number_users:
            self.text_users["text"] = "\n".join(users)

        # scroll window
        direction = current - self.current_user
        if direction > 0:
            if abs(direction) == len(users) -1:
                # jump from start to end
                self.end_scroll = len(users) -1
                self.start_scroll = self.end_scroll - (self.number_users -1)
            elif current == self.end_scroll -1 and self.end_scroll+1 != len(users):
                # near window right limit
                self.start_scroll += 1
                self.end_scroll += 1

        if direction < 0:
            if abs(direction) == len(users) -1:
                # jump from end to start
                self.start_scroll = 0
                self.end_scroll = self.number_users -1
            elif current == self.start_scroll +1 and self.start_scroll-1 != -1:
                # near window left limit
                self.start_scroll -= 1
                self.end_scroll -= 1

        # update users window
        self.current_user = current
        self.text_users["text"] = "\n".join(users[self.start_scroll:self.end_scroll+1])
