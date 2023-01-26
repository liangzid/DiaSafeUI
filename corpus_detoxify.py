"""
======================================================================
CORPUS_DETOXIFY ---

UI for Detoxify Dialogue Corpus.

    Author: Zi Liang <liangzid@stu.xjtu.edu.cn>
    Copyright © 2023, ZiLiang, all rights reserved.
    Created: 15 一月 2023
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
    FilePicker,
    FilePickerResultEvent,
    ProgressRing
)


class CorpusDetoxifyUI(UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        self.selected_files=Text()

        self.pick_file_dialog=FilePicker(on_result=self.pick_files_result)

        self.upload_bttn=ElevatedButton(text="UPLOAD FILES",
                                    icon=icons.UPLOAD_FILE,
                                    on_click=lambda _:\
                    self.pick_file_dialog.pick_files(allow_multiple=True))

        self.detect_bttn=ElevatedButton(icon=icons.LOCATION_SEARCHING,
                                        text="RUN DETECT",
                                              on_click=self.run_detect)
        self.heal_bttn=ElevatedButton(icon=icons.DATA_SAVER_ON,
                                      text="RUN HEAL",
                                            on_click=self.run_heal)
        self.download_bttn=ElevatedButton(icon=icons.DOWNLOAD,
                                          text="DOWNLOAD",
                                            on_click=self.run_download)
        self.dlg = flet.AlertDialog(
        title=Text("BEGIN DOWNLOADING..."),
            on_dismiss=lambda e: print("Dialog dismissed!"))

        self.clear_bttn=ElevatedButton(icon=icons.RESET_TV,text="CLEAR",
                                            on_click=self.run_clear)
        self.detect_stat=Row(controls=[])
        self.heal_stat=Row(controls=[])

        return Column(
            # width=400,
            controls=[
                Row([Text(value="Update your dialogue corpus...",
                          size=30,
                          text_align=flet.TextAlign.CENTER)],
                    vertical_alignment="center"),

                Column(controls=[
                    self.upload_bttn,
                    self.selected_files,
                ]),

                Row(controls=[
                    self.detect_bttn, self.detect_stat,
                    self.heal_bttn, self.heal_stat,
                ]),

                Row(controls=[
                    self.download_bttn,
                    self.clear_bttn
                    ]),

                self.pick_file_dialog,
                self.dlg,
            ]
        )

    def run_detect(self,e):
        self.detect_res="virtual res for detection."
        print("RUN DETECT")
        waiting_time=5
        self.detect_stat.controls=[ProgressRing()]
        for i in range(waiting_time):
            time.sleep(1)
            self.update()
        self.detect_stat.controls=[Text("✔")]
        self.update()

    def run_heal(self,e):
        print("RUN HEAL")
        waiting_time=10
        self.heal_stat.controls=[ProgressRing()]
        for i in range(waiting_time):
            time.sleep(1)
            self.update()
        self.heal_stat.controls=[Text("✔")]
        self.update()

    def run_download(self,e):
        print("BEGIN DOWNLOADING")
        self.detect_stat.controls=[]
        self.heal_stat.controls=[]
        self.dlg.open=True
        print("Here Execute Download Operation.")
        self.update()
    
    def run_clear(self,e):
        print("RUN CLEAR")
        self.detect_stat.controls=[]
        self.heal_stat.controls=[]
        self.selected_files.value=""
        self.selected_files.update()
        self.update()

    def pick_files_result(self,e:FilePickerResultEvent):
        self.selected_files.value=(
            "\n".join(map(lambda f:f.name, e.files)) if e.files else "Cancelled!"
        )
        self.selected_files.update()


def main(page: Page):
    page.title = "Show Demo"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"
    page.update()

    # create application instance
    app = CorpusDetoxifyUI()

    # add application's root control to the page
    page.add(app)



## running entry
if __name__=="__main__":
    flet.app(target=main)
    print("EVERYTHING DONE.")


