""" daily timer graphical interface """
import tkinter as tk
import tkinter.font as tkFont

class colors:
    black = "#000000"
    yellow = "#f2dc4e"
    red = "#eb4034"
    green = "#2cc743"

class interface:
    timer = 0

    def __init__(self) -> None:
        self.window = tk.Tk()

        # window
        self.window.title("Daily Timer")
        self.window.configure(
            background = "#F0F0F0",
            width = 300,
            height = 350,
        )
        self.window.resizable(False, False)
        self.window.geometry((
            f"{self.window['width']}x{self.window['height']}"
            f"+{(self.window.winfo_screenwidth() - self.window['width']) // 2}"
            f"+{(self.window.winfo_screenheight() - self.window['height']) // 2}"
        ))

        # timer
        self.label_timer = tk.Label(
            self.window,
            font = tkFont.Font(family='Helvetica', weight="bold",size=70),
            text = "00:00",
            background = "#f0f0f0",
        )
        self.label_timer.place(x=0,y=0,width=300,height=100)

        # message
        self.text_users = tk.Message(
            self.window,
            background = "#ffffff",
            font = tkFont.Font(family='Helvetica',size=12),
        )
        self.text_users.place(x=10,y=100,width=280,height=200)

        lines = [f"user {x} 00:00" for x in range(10)]
        self.text_users["text"] = "\n".join(lines)

        # buttons
        buttons_font = tkFont.Font(family='Helvetica',size=9)

        button_toggle=tk.Button(
            self.window,
            background = "#e9e9ed",
            font = buttons_font,
            text = "Start/Pause",
            command = self.button_toggle_command,
        )
        button_toggle.place(x=20,y=310,width=80,height=30)

        button_next=tk.Button(
            self.window,
            background = "#e9e9ed",
            font = buttons_font,
            text = "Next",
            command = lambda: self.button_next_command(self.timer),
        )
        button_next.place(x=120,y=310,width=70,height=30)

        button_previous=tk.Button(
            self.window,
            background = "#e9e9ed",
            font = buttons_font,
            text = "Previous",
            command = self.button_previous_command,
        )
        button_previous.place(x=210,y=310,width=70,height=30)

    def update_timer(self, seconds: int, color: colors = None) -> None:
        if color:
            self.label_timer["foreground"] = color
        self.label_timer["text"] = f"{seconds//60:02d}:{seconds%60:02d}"

    ############### debug functions ###############
    def button_toggle_command(self):
        # black
        self.timer += 1
        if self.label_timer["fg"] == colors.black:
            self.update_timer(self.timer, colors.green)
        else:
            self.update_timer(self.timer, colors.black)
        print("button_toggle_command")
    def button_next_command(self, timer_value):
        # yellow
        # self.timer += 5
        self.update_timer(timer_value, colors.yellow)
        print("button_next_command")
    def button_previous_command(self):
        # red
        self.timer += 10
        self.update_timer(self.timer, colors.red)
        print("button_previous_command")
    ###############################################
