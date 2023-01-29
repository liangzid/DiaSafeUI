"""
======================================================================
DIALOGUE --- 

Example of Dialogue UI.

    Author: Zi Liang <liangzid@stu.xjtu.edu.cn>
    Copyright © 2023, ZiLiang, all rights reserved.
    Created: 14 一月 2023
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


class OneUtterance(UserControl):
    def __init__(self,avatar_path=None,
                 text="",time="",is_me=False):
        super().__init__()
        self.avatar_path=avatar_path
        self.text=text
        self.time=time
        self.is_left=not is_me

    def build(self):
        utter_size=28
        time_size=20


        if self.is_left:
            return Column(
                # width=400,
                controls=[
                    Row(controls=[Text(self.time,size=time_size)]),
                    Row(controls=[
                        Icon(name=icons.MAN,color=colors.BLUE),
                        Text(self.text,size=utter_size),
                        ]
                        ),
                ]
            )
        else:
            ## NOTE!: we set it to the text mode.
            return Column(
                # width=400,
                controls=[
                    Row(controls=[Text(self.time,size=time_size)]),
                    Row(controls=[
                        Icon(name=icons.MAN,color=colors.BLUE),
                        Text("Chatbot: ",color=colors.RED,
                             size=utter_size+2),
                        Text(self.text,size=utter_size),
                        ]
                        ),
                ]
            )

            ## original right mode.
            # return Column(
            #     # width=400,
            #     controls=[
            #         Row(controls=[Text(self.time,size=time_size)]),
            #         Row(controls=[
            #             Text(self.text,size=utter_size),
            #             Icon(name=icons.MAN,color=colors.BLUE),
            #             ]
            #             )
            #     ]
            # )

class DialogueFlow(UserControl):
    def __init__(self):
        super().__init__()
        self.time_ls=[]

    def build(self):
        self.error_dialog = flet.AlertDialog(
                    title=Text("INVALID INPUTS!"),
                        on_dismiss=lambda e: print("Dialog dismissed!"))

        self.dialogue_flow=Column(controls=[])
        self.inp_fields=TextField(hint_text="Just Begin Chatting!",
                                  on_submit=self.run_send,expand=False)
        self.send_bttn=ElevatedButton(icon=icons.SEND,text="Send",
                                      on_click=self.run_send,
                                      )
        self.send_bttn.horizontal_alignment=flet.CrossAxisAlignment.END
        self.send_stat=Column()

        return Column(
            # width=400,
            controls=[
                self.dialogue_flow,
                Row(controls=[
                    self.inp_fields,
                    Row(controls=[
                        self.send_bttn,
                        self.send_stat,
                        ]),
                        ]),
                self.error_dialog,
            ]
        )
    def run_send(self,e):
        # first get send value.
        sended_utterance=self.inp_fields.value
        print(f"Sended utterance: {sended_utterance}")

        # then just add it to the dialogue flow 
        current_time=arrow.utcnow()
        self.time_ls.append(current_time)
        self.dialogue_flow.controls.append(\
                                OneUtterance(text=sended_utterance,
                                time=current_time,
                                is_me=False))
        self.inp_fields.value=""
        self.update()

        url="http://localhost:8000/"
        url+=f"dialogue/context_{sended_utterance}"
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
        # then just add it to the dialogue flow 
        current_time=arrow.utcnow()
        self.time_ls.append(current_time)
        self.dialogue_flow.controls.append(\
                                OneUtterance(text=response,
                                time=current_time,
                                is_me=True))
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


## running entry
if __name__=="__main__":
    flet.app(target=main)
    print("EVERYTHING DONE.")


