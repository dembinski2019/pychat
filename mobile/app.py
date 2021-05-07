from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ListProperty
from kivy.logger import Logger
import json

import websocket
try:
    import thread
except ImportError:
    import _thread as thread
from time import sleep



USER=None
OUTRO = None


class Manager(ScreenManager):
    pass


class Login(Screen):
    def login(self,*args):
        global USER, OUTRO
        USER = self.ids.name.text
        OUTRO = self.ids.outro.text
        if USER: 
            self.manager.current = "chat"
        else:
            self.ids.error.text = "Usuário não encontrado"
        self.ids.name.text = ""
        self.ids.outro.text = ""

class Mensagem(MDBoxLayout):
    color = ListProperty([.4,.4,.4,.3])
    def __init__(self, obj: dict, origem: str ='left', **kwargs):
        super().__init__(**kwargs)
        self.ids.user.text = obj["user"]
        self.ids.user.halign = origem
        self.ids.msg.text = obj["msg"]
        self.ids.msg.halign = origem
        if origem == "right":
            self.color = [.1,.4,.1,.5]


class KivyWebSocket(websocket.WebSocketApp):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = Logger
        self.logger.info('WebSocket: logger initialized')


class Chat(Screen):
    
    def on_pre_enter(self,*args, **kwargs):
        global USER, OUTRO
        self.ws = KivyWebSocket(f"ws://localhost:8000/ws/{USER}/{OUTRO}",
                           on_message=self.on_ws_message,
                           on_error=self.on_ws_error,
                           on_close=self.on_ws_close,)
        self.ws_connection()
        self.logger = Logger
        self.logger.info('App: initiallzed')

    def on_ws_message(self, ws, message):
        obj = json.loads(message)
        self.ids.box.add_widget(Mensagem(obj))
        self.logger.info('WebSocket: {}'.format(message))

    def on_ws_error(self, ws, error):
        self.logger.info('WebSocket: [ERROR]  {}'.format(error))

    def ws_connection(self, **kwargs):
        # start a new thread connected to the web socket
        thread.start_new_thread(self.ws.run_forever, ())

    def on_ws_close(self, *args):
        self.ws.close()
        self.manager.current = 'login'
        self.ids.box.clear_widgets()

    def send_message(self, *args):
        message = self.ids.message.text
        data = {"user":USER, "msg": message}
        self.ids.box.add_widget(Mensagem(data, "right"))
        self.ws.send(message)
        self.ids.message.text = ""


class App(MDApp):
    ...        


if __name__== "__main__":
    app = App()
    app.run()

    