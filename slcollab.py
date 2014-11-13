import os
import sublime
import sublime_plugin
from collab import Collab

Co = Collab()

def get_path(view):
    path = view.file_name()
    return path if path != None else '[No Name]'

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

class CollabListener(sublime_plugin.EventListener):
    def on_modified(self, view):
        text = view.substr(sublime.Region(0, view.size()))
        path = get_path(view)
        lang = os.path.basename(view.settings().get('syntax'))
        lang = os.path.splitext(lang)[0].lower()
        Co.update(text, path, lang)

    def on_selection_modified(self, view):
        path = get_path(view)
        y, x = view.rowcol(view.sel()[0].a)
        Co.update_cursor(x + 1, y + 1, path)

    def on_activated(self, view):
        self.on_modified(view)
        self.on_selection_modified(view)