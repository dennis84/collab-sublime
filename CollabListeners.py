import os
import sublime
import sublime_plugin
from CollabUtil import *
from CollabPlugin import *

class CollabListener(sublime_plugin.EventListener):
    def on_modified(self, view):
        text = view.substr(sublime.Region(0, view.size()))
        path = get_path(view)
        lang = 'undefined'
        syntax = view.settings().get('syntax')
        if syntax != None:
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
