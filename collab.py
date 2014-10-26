import sublime
import sublime_plugin
import os
import json
import uuid
import websocket
import threading

def is_connected(func):
    def decorated(*args, **kwargs):
        if Co.connected:
            func(*args, **kwargs)
    return decorated

def get_path(view):
    path = view.file_name()
    return path if path != None else 'undefined'

class CollabConnectCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel('Room: ', '', self.on_done, None, None)

    def on_done(self, room):
        Co.connect(False if not room else room)

class CollabChangeNickCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel('Nick: ', '', self.on_done, None, None)

    def on_done(self, nick):
        if nick:
            Co.updateNick(nick)

class CollabLeaveCommand(sublime_plugin.WindowCommand):
    def run(self):
        Co.disconnect()

class CollabListener(sublime_plugin.EventListener):
    @is_connected
    def on_modified(self, view):
        text = view.substr(sublime.Region(0, view.size()))
        path = get_path(view)
        lang = os.path.basename(view.settings().get('syntax'))
        lang = os.path.splitext(lang)[0].lower()
        Co.update(text, path, lang)

    @is_connected
    def on_selection_modified(self, view):
        path = get_path(view)
        y, x = view.rowcol(view.sel()[0].a)
        Co.updateCursor(x + 1, y + 1, path)

class Connection(threading.Thread):
    def __init__(self, ws):
        threading.Thread.__init__(self)
        self.ws = ws

    def run(self):
        self.ws.run_forever()

class Collab:
    def __init__(self):
        self.current_buffer = ''
        self.connected = False

    def on_open(self, ws):
        self.connected = True
        print 'Joined: ' + self.room

    def on_error(self, ws, error):
        self.disconnect()

    def connect(self, room=False):
        if room == False:
            self.room = str(uuid.uuid4()).split('-')[-1]
        else:
            self.room = room

        self.ws = websocket.WebSocketApp(
            'ws://radiant-dusk-8167.herokuapp.com/' + self.room,
            on_open = self.on_open,
            on_error = self.on_error)

        self.co = Connection(self.ws)
        self.co.start()

    @is_connected
    def disconnect(self):
        self.connected = False
        self.ws.close()
        self.co.close()

    def update(self, buffer, path, lang):
        if buffer != self.current_buffer:
            self.current_buffer = buffer
            self._send_message('code', {
                'content': buffer,
                'file': path,
                'lang': lang
            })

    def updateCursor(self, x, y, path):
        self._send_message('cursor', {'x': x, 'y': y, 'file': path})

    def updateNick(self, name):
        self._send_message('change-nick', {'name': name})

    @is_connected
    def _send_message(self, t, d):
        self.ws.send(t + json.dumps(d))

Co = Collab()
