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

        if self.is_left:
            return Column(
                # width=400,
                controls=[
                    Row(controls=[Text(self.time,size=8)]),
                    Row(controls=[
                        Icon(name=icons.MAN,color=colors.BLUE),
                        Text(self.text),
                        ]
                        )
                ]
            )
        else:
            return Column(
                # width=400,
                controls=[
                    Row(controls=[Text(self.time,size=8)]),
                    Row(controls=[
                        Text(self.text),
                        Icon(name=icons.MAN,color=colors.BLUE),
                        ]
                        )
                ]
            )

class DialogueFlow(UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        self.dialogue_flow=Column(controls=[])
        self.inp_fields=TextField(hint_text="Just Begin Chatting!",
                                  on_submit=self.run_send,expand=False)
        self.send_bttn=ElevatedButton(icon=icons.SEND,text="Send",
                                      on_click=self.run_send,
                                      )
        self.send_bttn.horizontal_alignment=flet.CrossAxisAlignment.END

        return Column(
            # width=400,
            controls=[
                self.dialogue_flow,
                self.inp_fields,
                self.send_bttn,
            ]
        )
    def run_send(self,e):
        # first get send value.
        sended_utterance=self.inp_fields.value
        print(f"Sended utterance: {sended_utterance}")

        # then just add it to the dialogue flow 
        self.dialogue_flow.controls.append(\
                                OneUtterance(text=sended_utterance,
                                time=arrow.utcnow().humanize(),
                                is_me=False))
        self.inp_fields.value=""
        self.update()

        response=self.get_response(sended_utterance)
        # then just add it to the dialogue flow 
        self.dialogue_flow.controls.append(\
                                OneUtterance(text=response,
                                time=arrow.utcnow().humanize(),
                                is_me=True))
        self.update()
    def get_response(self,utterance):
        return "This is a new Response."


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


