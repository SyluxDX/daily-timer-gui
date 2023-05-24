""" interfaces to prevent circular module import """
import dataclasses

@dataclasses.dataclass
class ColorsInterface:
    """ colors definition """
    normal = ""
    pause = ""
    warning = ""
    overtime = ""

class UiInterface:
    """ UI Interface """
    colors = ColorsInterface()
    def update_timer(self, seconds: int, color: str=""):
        """ template for function update timer value """
    def update_timer_color(self, color: str):
        """ template for function update timer color """
    def update_users(self, users: list, current: int):
        """ template for function update users """

class CoreInterface:
    """ Core Interface """
    gui: UiInterface
    running_color: str
    def next_user(self):
        """ template for function next user """
    def previous_user(self):
        """ template for function previous user """
    def toogle_timer(self):
        """ template for function toogleing timer pause """
