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
import time
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
import flet as ft
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
    ProgressBar,
    ProgressRing,
)
from flet.plotly_chart import PlotlyChart
import plotly.express as px

class SafetyHealUI(UserControl):
    
    def __init__(self):
        super().__init__()


    def build(self):
        self.context_ui=TextField(hint_text="Dialogue Context (Optional)",
                                  on_submit=self.run_detect,expand=False)
        self.resp_ui=TextField(hint_text="Your Utterance to Detect",
                                  on_submit=self.run_detect,expand=False)

        self.detect_bttn=ElevatedButton(icon=icons.SEARCH_OFF,text="DETECT",
                                              on_click=self.run_detect)
        self.heal_bttn=ElevatedButton(icon=icons.DATA_SAVER_ON,text="HEAL",
                                            on_click=self.run_heal)

        self.display=Column(spacing=25,controls=[],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        return Column(
            # width=400,
            controls=[
                Row([Text(value="Cases of Dialogue Detection and Healing",
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
        res_dict={"Conclusion":{"Safe?":"Safe",
                                "Type":"Offending User",},
                "Distribution":{"Offending User":0.13,
                                "Risk Ignorance":0.15,
                                "Unauthorized Expertise":0.45,
                                "Toxicity Agreement":0.24,
                                "Biased Opinion":0.71,
                                "Sensitive Topic Continuation":0.002,
                                },
                }
        self.mode="DEBUG"
        self.mode="TEST"
        self.detect_res="virtual res for detection."
        print("RUN DETECT")
        if self.mode=="DEBUG":
            self.display.controls=[
                    Column([Text(value="------------"),
                        Text(value=self.context_ui.value),
                        Text(value=self.resp_ui.value),
                        ]),
                    Row([Text(value="Detection Results:"),
                        Text(value=self.detect_res)]),
                ]
            self.update()
        else:
            waiting_time=5
            self.display.controls=[Text(value="DETECTING..."),
                                   ProgressBar()]
            for i in range(waiting_time):
                time.sleep(1)
                self.update()

            xls=[x for x,_ in res_dict["Distribution"].items()]
            yls=[y for _,y in res_dict["Distribution"].items()]

            fig=px.bar(x=xls,y=yls,orientation="v",
                       height=300)

            self.display.controls=[
                PlotlyChart(fig,
                            # expand=True
                            ),
                    Row([Text(value="Detection Results："),
                         Text(value=f"Safety: {res_dict['Conclusion']['Safe?']}"),
                         Text(value=f"Unsafe Type: {res_dict['Conclusion']['Type']}"),
                         ]),
                ]
            self.update()

    def run_heal(self,e):
        waiting_time=5
        self.heal_res="virtual res for healing."

        self.display.controls=[Text(value="HEALING..."),
                                ProgressBar()]
        for i in range(waiting_time):
            time.sleep(1)
            self.update()

        self.display.controls=[
                Column([Text(value="------------"),
                    Text(value=self.context_ui.value),
                    Text(value=self.resp_ui.value),
                    ]),
                Row([Text(value="Healing Results:"),
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
    flet.app(target=main)
    print("EVERYTHING DONE.")
