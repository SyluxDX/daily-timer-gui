""" Core class for timer """

from time import sleep
from datetime import datetime, timedelta
from dataclasses import dataclass
from random import shuffle

import src.interfaces
import src.team_statistics
from src.configurations import Configurations

@dataclass
class _usertimer:
    def __init__(self, user: str, seconds: int) -> None:
        self.user = user
        self.seconds = seconds

class UserTimer:
    """ Dataclass for users timers """
    def __init__(self, users_list: list, statistics: dict, randomOrder: bool) -> None:
        # get max len of user name
        max_name = 0
        ## find max lenght of names
        for name in users_list:
            max_name = max(max_name, len(name))
        ## set user in random order if desired
        if randomOrder:
            shuffle(users_list)

        # Create usertimer with trailing whitespaces as padding
        self.users = [
            _usertimer( user+" "*(max_name-len(user) ), 0) for user in users_list
            ]
        self.current = 0

        # initiate stats with current users:
        self.stats = {}
        for user in users_list:
            if user in statistics:
                self.stats[user] = statistics[user]
            else:
                self.stats[user] = ""

    def set_current_timer(self, seconds: int) -> None:
        """ Set/update current user timer """
        self.users[self.current].seconds = seconds

    def next_timer(self) -> int:
        """ Get next user timer value and update current user to that user """
        self.current += 1
        if self.current == len(self.users):
            self.current = 0
        return self.users[self.current].seconds

    def previous_timer(self) -> int:
        """ Get previous user timer value and update current user to that user """
        self.current -= 1
        if self.current < 0:
            self.current = len(self.users)-1
        return self.users[self.current].seconds

    def str_list(self) -> list:
        """ Get all users names, timer and current user as list of strings """
        text = []
        for i, user in enumerate(self.users):
            prefix = "  "
            if i == self.current:
                prefix = "->"
            sline = f"      {self.stats[user.user.strip()]}"
            text.append(
                f"{prefix} {user.user} {user.seconds//60:02d}:{user.seconds%60:02d}\n{sline}"
            )
        return text

    def get_list(self) -> list:
        """ Return list of tuples with users and current timer value, in seconds """
        return [(user.user, user.seconds) for user in self.users]

class Core(src.interfaces.CoreInterface):
    """ Core Timer """
    timer = 0
    loop_run = True
    timer_running = False
    aux_tick = timedelta(seconds=1)
    next_tick = None

    def __init__(
            self, configs: Configurations, gui:src.interfaces.UiInterface, stat_filename: str
    ) -> None:
        self.configs = configs
        self.gui = gui
        self.stat_filename = stat_filename
        self.running_color = gui.colors.normal

        user_stats = {}
        if self.configs.stats_display:
            user_stats = src.team_statistics.read_last_dailies(
                self.stat_filename, self.configs.stats_number
            )
        self.users = UserTimer(configs.participants, user_stats, configs.random)

    def next_user(self) -> None:
        """ update current user and get seconds of the next user """
        self.users.set_current_timer(self.timer)
        self.timer = self.users.next_timer()

        ## set timer color and update timer
        self.update_timer(self.timer)
        new_color = self.compute_color()
        if self.running_color != new_color:
            self.running_color = new_color
            self.gui.update_timer_color(self.running_color)

        self.gui.update_users(self.users.str_list(), self.users.current)
        # reset next tick
        self.next_tick = datetime.utcnow() + self.aux_tick

    def previous_user(self) -> None:
        """ update current user and get seconds from previous user """
        self.users.set_current_timer(self.timer)
        self.timer = self.users.previous_timer()

        ## set timer color and update timer
        self.update_timer(self.timer)
        new_color = self.compute_color()
        if self.running_color != new_color:
            self.running_color = new_color
            self.gui.update_timer_color(self.running_color)
        self.gui.update_users(self.users.str_list(), self.users.current)
        # reset next tick
        self.next_tick = datetime.utcnow() + self.aux_tick

    def toogle_timer(self) -> None:
        """ toogle start/pause for timer """
        self.timer_running = not self.timer_running
        if self.timer_running:
            self.gui.update_timer_color(self.running_color)
            self.next_tick = datetime.utcnow() + self.aux_tick
        else:
            self.gui.update_timer_color(self.gui.colors.pause)

    def update_timer(self, value):
        """ Calculate display timer based on function mode """
        if not self.configs.stopwatch:
            value = abs(self.configs.time - value)
        self.gui.update_timer(value)

    def compute_color(self) -> str:
        """ Returns new timer color based on the timer value (seconds) """
        color = self.gui.colors.normal
        if self.timer >= self.configs.warning:
            color = self.gui.colors.warning
        if self.timer >= self.configs.time:
            color = self.gui.colors.overtime

        return color

    def mainloop(self, ticks: float=0.25) -> None:
        """ Timer main loop """

        self.update_timer(self.timer)
        ## set users list
        self.gui.update_users(self.users.str_list(), self.users.current)

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
                        self.gui.update_timer_color(self.running_color)
                    self.next_tick += self.aux_tick
                    self.update_timer(self.timer)

            # self.ui.update_timer(self.timer)
            sleep(ticks)

        # update last active user timer before writing stats
        self.users.set_current_timer(self.timer)
        src.team_statistics.write_daily_times(self.stat_filename, self.users.get_list())
