"""
======================================================================
DIALOGUE_CHATGPT ---

dialogue ui for chatpgt

    Author: Zi Liang <liangzid@stu.xjtu.edu.cn>
    Copyright © 2023, ZiLiang, all rights reserved.
    Created:  6 March 2023
======================================================================
"""


# ------------------------ Code --------------------------------------

## normal import 
import json
from typing import List,Tuple,Dict
import random
from pprint import pprint as ppp
from threading import Thread
import requests

from dialogue_new import Message,ChatMessage,DialogueFlow

import arrow
import time

import flet
import flet as ft
from flet import (
    Icon,
    Checkbox,
    Column,
    ElevatedButton,
    FloatingActionButton,
    IconButton,
    OutlinedButton,
    Page,
    Row,
    Tab,
    Tabs,
    Text,
    TextField,
    UserControl,
    colors,
    icons,
    FilePicker,
    FilePickerResultEvent,
    ProgressRing,
)
import urllib
from urllib.parse import quote as qt

class NewFlow(DialogueFlow):
    def __init__(self):
        super().__init__()
        self.history=""

    def run_send(self,e):
        # first get send value.
        sended_utterance=self.inp_fields.value
        # sended_utterance=sended_utterance.replace("?","")
        print(f"Sended utterance: {sended_utterance} {type(sended_utterance)}")
        self.history+=sended_utterance
        print(f"history: {self.history} {type(self.history)}")

        # then just add it to the dialogue flow 
        current_time=arrow.utcnow()
        self.time_ls.append(current_time)
        message=Message(user_name="User",text=sended_utterance,message_type="")
        self.dialogue_flow.controls.append(\
                                ChatMessage(message))
        self.inp_fields.value=""
        self.update()

        url="http://localhost:8000/"
        # url+=f"dialogue/context_{self.history}"
        # url+=f"chat/context_{qt(self.history)}utter_{qt(sended_utterance)}"
        url+=f"chatgpt"
        t=Thread(target=self.wait,args=(1,))
        self.waiting=1
        # t.start()
        # res=requests.post(url,
                # {"ct":qt(self.history),"utter":qt(sended_utterance)})
        res=requests.post(url,json=
                {"ct":self.history,
                 "utter":sended_utterance+". Note: less than 80 words."})
        signal=res.status_code
        if signal!=200:
            self.waiting=0
            self.error_dialog.open=True
            self.send_stat.controls=[]
            self.update()
            return -1
        response=self.get_response(res.text)
        # response.split("You say: ")[-1]
        self.history+="<SEP>"+response+"<SEP>"
        # if len(self.history.split(" "))>64:
        #     self.history=" ".join(self.history.split(" ")[-64:])
        # elif len(self.history)>64:

        # then just add it to the dialogue flow 
        current_time=arrow.utcnow()
        self.time_ls.append(current_time)
        message=Message(user_name="ChatGPT",text=response,message_type="")
        self.dialogue_flow.controls.append(\
                                ChatMessage(message))
        # self.send_stat.controls=[Text(value="✔")]
        self.waiting=0
        self.update()


def main(page: Page):
    page.title = "ChatGPT demo"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"
    page.update()

    # create application instance
    app = NewFlow()
    # one_utter=OneUtterance(text="hello world.",time="12:00",is_me=True)

    # add application's root control to the page
    page.add(app)
    # page.add(one_utter)
    page.update()

## running entry
if __name__=="__main__":
    flet.app(target=main,port=3933, view=ft.WEB_BROWSER)
    print("EVERYTHING DONE.")


