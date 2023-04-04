""" interfaces to prevent circular module import """


class ColorsInterface:
    """ colors definition """
    normal = ""
    pause = ""
    warning = ""
    overtime = ""   

class UiInterface:
    """ UI Interface """
    colors = ColorsInterface()
    def update_timer(self, timer:int):
        """ template for function update timer value """
    def update_timer_color(self, color: str):
        """ template for function update timer color """
    def update_users(self, users: str):
        """ template for function update users """

class CoreInterface:
    """ Core Interface """
    ui: UiInterface
    running_color: str
    def next_user(self):
        """ template for function next user """
    def previous_user(self):
        """ template for function previous user """
    def toogle_timer(self):
        """ template for function toogleing timer pause """
