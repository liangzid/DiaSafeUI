"""
======================================================================
MAINUI ---

Main UI for Dialogue Safety Demo Show.

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

import flet
from flet import (
    Icon,
    Checkbox,
    Column,
    ElevatedButton,
    FloatingActionButton,
    NavigationBar,
    NavigationDestination,
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

from dialogue import DialogueFlow
from safety_detect_healing import SafetyHealUI
from corpus_detoxify import CorpusDetoxifyUI

def main(page:Page):
    page.title = "对话检测与修复服务效果展示"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"
    page.update()

    def switch_screen(e):
        e=e.control.selected_index
        # print(f"e is: {e}")
        if e==0:
            show_screen.controls=[chatting_screen]
            show_screen.update()
            page.update()
        elif e==1:
            show_screen.controls=[safe_heal_screen]
            page.update()
        elif e==2:
            show_screen.controls=[corpus_heal_screen]
            page.update()


    navigation_bar=NavigationBar(
        destinations=[
            NavigationDestination(icon=icons.CHAT,
                                    label="Dialogue Demo"),
            NavigationDestination(icon=icons.HEALTH_AND_SAFETY,
                                    label="Detection or Healing"),
            NavigationDestination(icon=icons.BATTERY_SAVER,
                                    label="Corpus Detoxification"),
            ],
        on_change=switch_screen,
        )

    chatting_screen=DialogueFlow()
    safe_heal_screen=SafetyHealUI()
    corpus_heal_screen=CorpusDetoxifyUI()

    page.navigation_bar=navigation_bar
    show_screen=Column(controls=[])
    page.add(show_screen)
    page.update()


## running entry
if __name__=="__main__":
    flet.app(target=main)
    print("EVERYTHING DONE.")


