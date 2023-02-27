"""
======================================================================
MAIN_ROUTE ---

Design and Route the API query with FastAPI for dialogue healing and
Detection.

    Author: Zi Liang <liangzid@stu.xjtu.edu.cn>
    Copyright © 2023, ZiLiang, all rights reserved.
    Created: 28 一月 2023
======================================================================
"""


# ------------------------ Code --------------------------------------

## normal import 
import json
from typing import List,Tuple,Dict,Union
import random
from pprint import pprint as ppp
# import pickle
# import os
# from os.path import join, exists
# from collections import Counter,OrderedDict
# from bisect import bisect
# from copy import deepcopy
# import pickle

from fastapi import FastAPI
import time
import arrow

from services.chat.inference import ChitChatService
from services.safety.detect import DetectService
from services.safety.heal import HealService

app=FastAPI()

dialogue_service=ChitChatService(root_dir="./ckpts/pretrained_dialogue_model/",
                                 load_model="blenderbot-1B-distill",
                                 device="cuda:7")
binary_service=DetectService(root_dir="./ckpts/",model_type="binary",
                             device="cuda:7")
multi_service=DetectService(root_dir="./ckpts/",model_type="multi",
                            device="cuda:7")
heal_service=HealService(root_dir="./ckpts/",
                         device="cuda:7")

@app.get("/detection/context_{ct}utterance_{ut}")
def run_detect(ct:Union[str,None],ut:str):
    
    _,b_dist,b_res=binary_service.inference(ct,ut)
    b_res="Unsafe"
    _,m_dist,m_res=multi_service.inference(ct,ut)

    res_dict={"Conclusion":{"Safe?":b_res,
                            "Type":m_res,},
            "Distribution":m_dist,
                }
    return res_dict

@app.get("/healing/context_{ct}utterance_{ut}")
def run_heal(ct:Union[str,None],ut:str):
    istod=0
    if istod==1:
        # run tod operation
        test_data="this is the tod data."
        time.sleep(2)
        return {"context":ct,
                "response":ut,
                "istod":istod,
                "newresponse":test_data}
    else:
        resp=heal_service.inference(ct,ut)
        return {"context":ct,
                "response":ut,
                "istod":istod,
                "newresponse":resp}

@app.get("/dialogue/context_{ct}withSafety_{withSafety}")
def run_chitchat(ct:Union[str,None],withSafety:int):
    # run chitchat operation
    
    resp=dialogue_service.inference(ct)
    if withSafety==0:
        return {"context":ct,
                "response":resp,
                }
    else:
        _,_,safe_res=binary_service.inference(ct,resp)
        safe_res="Unsafe"
        if safe_res=="Safe":
            newresp=resp
        else:
            newresp=heal_service.inference(ct,resp)
        return {"context":ct,
                "response":newresp,
                }
