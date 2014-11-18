import sublime_plugin
from CollabUtil import *
from CollabPlugin import *

class CollabConnectCommand(sublime_plugin.WindowCommand):
    def run(self, local=False):
        self.local = local
        self.window.show_input_panel('Room: ', '', self.on_done, None, None)

    def on_done(self, room):
        room = False if not room else room
        url = False if not self.local else "localhost:9000"
        Co.connect(room, url)

class CollabChangeNickCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel('Nick: ', '', self.on_done, None, None)

    def on_done(self, nick):
        if nick:
            Co.change_nick(nick)

class CollabLeaveCommand(sublime_plugin.WindowCommand):
    def run(self):
        Co.disconnect()
