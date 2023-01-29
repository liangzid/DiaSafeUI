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
import requests
from threading import Thread
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
        self.allow_run_waiting=0
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
        self.error_dialog = flet.AlertDialog(
                    title=Text("INVALID INPUTS!"),
                        on_dismiss=lambda e: print("Dialog dismissed!"))
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
                               ]),
                            ]),
                self.error_dialog,
                self.display
            ]
        )
    def run_detect(self,e):
        self.res_dict=None
        # self.mode="DEBUG"
        self.mode="TEST"
        self.detect_res="virtual res for detection."
        print("RUN DETECT")
        if self.mode=="DEBUG":
            url="http://localhost:8000/"
            url+=f"detection/context_{self.context_ui.value}"+\
                f"utterance_{self.resp_ui.value}"
            t=Thread(target=self.wait,args=("DETECTING...",))
            self.allow_run_waiting=1
            t.start()
            signal=requests.get(url).status_code
            if signal!=200:
                self.allow_run_waiting=0
                self.error_dialog.open=True
                self.display.controls=[]
                self.update()
                return -1
            self.res_dict=requests.get(url).text
            self.res_dict=json.loads(self.res_dict)
            print(self.res_dict)
        else:
            url="http://localhost:8000/"
            url+=f"detection/context_{self.context_ui.value}"+\
                f"utterance_{self.resp_ui.value}"
            t=Thread(target=self.wait,args=("DETECTING...",))
            self.allow_run_waiting=1
            t.start()
            signal=requests.get(url).status_code
            if signal!=200:
                self.allow_run_waiting=0
                self.error_dialog.open=True
                self.display.controls=[]
                self.update()
                return -1
            self.res_dict=requests.get(url).text
            self.res_dict=json.loads(self.res_dict)
            print(self.res_dict)

        xls=[x for x,_ in self.res_dict["Distribution"].items()]
        yls=[y for _,y in self.res_dict["Distribution"].items()]

        fig=px.bar(x=xls,y=yls,orientation="v",
                    height=300)

        self.display.controls=[
            PlotlyChart(fig,
                        # expand=True
                        ),
                Column([Text(value="Detection Results：",size=30,),
                        Row([Text(value=f"Safety:",
                                  size=28,),
                             Text(value=f"{self.res_dict['Conclusion']['Safe?']}",
                                  size=30,italic=True,),
                             ]),
                        Row([Text(value=f"Unsafe Type:",
                                  size=25,),
                             Text(value=f"{self.res_dict['Conclusion']['Type']}",
                                  size=25,italic=True,),
                             ])
                        ]),
            ]
        self.allow_run_waiting=0
        self.update()
        self.res_dict=None

    def wait(self,label="DETECTING..."):
        while self.res_dict is None:
            if self.allow_run_waiting==1:
                # print("now go to a new circle.")
                self.display.controls=[Text(value=label),
                                    ProgressBar()]
                time.sleep(0.8)
                self.update()
            else:
                # print("now break")
                self.update()
                break

    def run_heal(self,e):
        waiting_time=5
        self.heal_res="None"
        self.res_dict=None

        self.display.controls=[Text(value="HEALING..."),
                                ProgressBar()]

        # for i in range(waiting_time):
        #     time.sleep(1)
        #     self.update()

        url="http://localhost:8000/"
        url+=f"healing/context_{self.context_ui.value}"+\
            f"utterance_{self.resp_ui.value}"
        t=Thread(target=self.wait,args=("HEALING...",))
        self.allow_run_waiting=1
        t.start()
        signal=requests.get(url).status_code
        if signal!=200:
            self.allow_run_waiting=0
            self.error_dialog.open=True
            self.display.controls=[]
            self.update()
            return -1
        self.res_dict=requests.get(url).text
        self.res_dict=json.loads(self.res_dict)
        print(self.res_dict)
        self.heal_res=self.res_dict["newresponse"]

        self.display.controls=[
                Row([Text(value="Healing Results:",size=28,),
                    Text(value=self.heal_res,size=25,italic=True)]),
            ]
        self.allow_run_waiting=0
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
