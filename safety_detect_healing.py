"""
======================================================================
SAFETY_DETECT_HEALING ---

UI for safety Detection and Healing.

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


import flet
from flet import (
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
)

class SafetyHealUI(UserControl):
    
    def __init__(self):
        super().__init__()


    def build(self):
        self.context_ui=TextField(hint_text="与检测回复相关的上下文",
                                  on_submit=self.run_detect,expand=False)
        self.resp_ui=TextField(hint_text="待检测的对话语句",
                                  on_submit=self.run_detect,expand=False)

        self.detect_bttn=ElevatedButton(icon=icons.SEARCH_OFF,text="DETECT",
                                              on_click=self.run_detect)
        self.heal_bttn=ElevatedButton(icon=icons.DATA_SAVER_ON,text="HEAL",
                                            on_click=self.run_heal)

        self.display=Column(spacing=25,controls=[])

        return Column(
            # width=400,
            controls=[
                Row([Text(value="对话检测与修复样例",
                          size=30,
                          text_align=flet.TextAlign.CENTER)],
                    vertical_alignment="center"),
                Column(spacing=25,
                       controls=[
                           self.context_ui,
                           self.resp_ui,
                           Row(alignment="spaceBetween",
                               vertical_alignment="center",
                               controls=[
                                   self.detect_bttn,self.heal_bttn
                               ])
                       ]),
                self.display
            ]
        )
    def run_detect(self,e):
        self.detect_res="virtual res for detection."
        print("RUN DETECT")
        self.display.controls=[
                Column([Text(value="------------"),
                    Text(value=self.context_ui.value),
                    Text(value=self.resp_ui.value),
                    ]),
                Row([Text(value="检测结果："),
                    Text(value=self.detect_res)]),
            ]
        
        self.update()
    def run_heal(self,e):
        self.heal_res="virtual res for healing."
        self.display.controls=[
                Column([Text(value="------------"),
                    Text(value=self.context_ui.value),
                    Text(value=self.resp_ui.value),
                    ]),
                Row([Text(value="修复结果："),
                    Text(value=self.heal_res)]),
            ]
        self.update()

def main(page: Page):
    page.title = "Show Demo"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"
    page.web=True
    page.width=100




    page.update()

    # create application instance
    app = SafetyHealUI()

    # add application's root control to the page
    page.add(app)

## running entry
if __name__=="__main__":
    flet.app(target=main,host=)
    print("EVERYTHING DONE.")


