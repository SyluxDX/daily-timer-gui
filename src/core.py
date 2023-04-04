""" Core class for timer """
import src.interfaces
from src.configurations import Configurations
from time import sleep
from datetime import (datetime, timedelta)

class Core(src.interfaces.CoreInterface):
    """ Core Timer """
    timer = 0
    loop_run = True
    timer_running = False
    aux_tick = timedelta(seconds=1)
    next_tick = None

    def __init__(self, configs: Configurations, ui:src.interfaces.UiInterface) -> None:
        self.ui = ui
        self.configs = configs

    def next_user(self) -> None:
        """ template for function next user """
        print("next_user")

    def previous_user(self) -> None:
        """ template for function previous user """
        print("previous_user")

    def toogle_timer(self) -> None:
        """ template for function toogleing timer pause """
        print(" toogle_timer")
        self.timer_running = not self.timer_running
        if self.timer_running:
            self.ui.update_timer_color(self.running_color)
            self.next_tick = datetime.utcnow() + self.aux_tick
        else:
            self.ui.update_timer_color(self.ui.colors.pause)
    
    def update_timer(self, value):
        """ Calculate display timer based on function mode """
        if not self.configs.stopwatch:
            value = abs(self.configs.time - value)
        self.ui.update_timer(value)
    
    def compute_color(self) -> str:
        """ Returns new timer color based on the timer value (seconds) """
        color = self.ui.colors.normal
        if self.timer >= self.configs.warning:
            color = self.ui.colors.warning
        if self.timer >= self.configs.time:
            color = self.ui.colors.overtime

        return color

    def mainloop(self, ticks: float=0.25) -> None:

        self.update_timer(self.timer)

        while self.loop_run:
            if self.timer_running:
                if self.next_tick is None:
                    self.next_tick = datetime.utcnow() + self.aux_tick
                # check tick
                if datetime.utcnow() > self.next_tick:
                    self.timer += 1
                    # check warning/burn threshold
                    new_color = self.compute_color()
                    if self.running_color != new_color:
                        self.running_color = new_color
                        self.ui.update_timer_color(self.running_color)
                    self.next_tick += self.aux_tick
                    self.update_timer(self.timer)

            # self.ui.update_timer(self.timer)
            sleep(ticks)
