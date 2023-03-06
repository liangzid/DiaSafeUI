"""
======================================================================
DIALOGUE_NEW ---

New version of dialog windows.

    Author: Zi Liang <liangzid@stu.xjtu.edu.cn>
    Copyright © 2023, ZiLiang, all rights reserved.
    Created: 27 二月 2023
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
# import pickle
# import os
# from os.path import join, exists
# from collections import Counter,OrderedDict
# from bisect import bisect
# from copy import deepcopy
# import pickle

# import sys
# # sys.path.append("./")
# from tqdm import tqdm

# import numpy as np

# import argparse
# import logging

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

class Message():
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type

class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment="start"
        self.controls=[
                ft.CircleAvatar(
                    content=ft.Text(self.get_initials(message.user_name)),
                    color=ft.colors.WHITE,
                    bgcolor=self.get_avatar_color(message.user_name),
                ),
                ft.Column(
                    [
                        ft.Text(message.user_name, weight="bold"),
                        ft.Text(message.text, selectable=True),
                    ],
                    tight=True,
                    spacing=5,
                ),
            ]

    def get_initials(self, user_name: str):
        return user_name[:1].capitalize()

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]


class DialogueFlow(UserControl):
    def __init__(self):
        super().__init__()
        self.time_ls=[]
        self.history=""

    def build(self):
        self.error_dialog = flet.AlertDialog(
                    title=Text("INVALID INPUTS!"),
                        on_dismiss=lambda e: print("Dialog dismissed!"))

        # self.dialogue_flow=ft.ListView(expand=True,
        #                                spacing=10,
        #                                auto_scroll=True)
        self.dialogue_flow=ft.Column(controls=[])
        
        self.inp_fields=TextField(hint_text="Just Begin Chatting!",
                                  on_submit=self.run_send,
                                  expand=True,
                                  autofocus=True,
                                  shift_enter=True,
                                  min_lines=1,
                                  max_lines=5,
                                  filled=True,
                                  )

        self.send_bttn=ElevatedButton(icon=icons.SEND,text="Send",
                                      on_click=self.run_send,
                                      )
        self.send_bttn.horizontal_alignment=flet.CrossAxisAlignment.END
        self.send_stat=Column()

        self.is_use_safety=flet.Switch(label="Safety Mode On",
                                     value=False)

        return Column(
            # width=400,

            controls=[
            self.dialogue_flow,
                # ft.Container(
                #     content=self.dialogue_flow,
                #     border=ft.border.all(1,ft.colors.OUTLINE),
                #     border_radius=5,
                #     padding=10,
                #     expand=True,
                #     ),
                Row(controls=[
                    self.inp_fields,
                    Row(controls=[
                        self.send_bttn,
                        self.send_stat,
                        ]),
                        ]),
                self.is_use_safety,
                self.error_dialog,
            ]
        )
    # print(1)

    def run_send(self,e):
        # first get send value.
        sended_utterance=self.inp_fields.value
        print(f"Sended utterance: {sended_utterance}")
        sended_utterance=sended_utterance.replace("?","")
        self.history+="User say: "+sended_utterance+". You say: "

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
        url+=f"dialogue/context_{sended_utterance}"
        x=1 if self.is_use_safety.value else 0
        url+=f"withSafety_{x}"
        t=Thread(target=self.wait,args=(1,))
        self.waiting=1
        # t.start()
        signal=requests.get(url).status_code
        if signal!=200:
            self.waiting=0
            self.error_dialog.open=True
            self.send_stat.controls=[]
            self.update()
            return -1
        response=self.get_response(requests.get(url).text)
        # response.split("You say: ")[-1]
        self.history+=response+" "
        # if len(self.history.split(" "))>64:
        #     self.history=" ".join(self.history.split(" ")[-64:])
        # elif len(self.history)>64:

        # then just add it to the dialogue flow 
        current_time=arrow.utcnow()
        self.time_ls.append(current_time)
        message=Message(user_name="Chatbot",text=response,message_type="")
        self.dialogue_flow.controls.append(\
                                ChatMessage(message))
        # self.send_stat.controls=[Text(value="✔")]
        self.waiting=0
        self.update()

    def get_response(self,rawtext):
        rawtext=json.loads(rawtext)["response"]
        print(rawtext)
        return rawtext

    def wait(self,_):
        while 1:
            if self.waiting==1:
                self.send_stat.controls=[ProgressRing()]
                time.sleep(0.8)
                self.update()
            else:
                break



def main(page: Page):
    page.title = "Show Demo"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"
    page.update()

    # create application instance
    app = DialogueFlow()
    # one_utter=OneUtterance(text="hello world.",time="12:00",is_me=True)

    # add application's root control to the page
    page.add(app)
    # page.add(one_utter)
    page.update()


## running entry
if __name__=="__main__":
    flet.app(target=main,port=80, view=ft.WEB_BROWSER)
    print("EVERYTHING DONE.")
