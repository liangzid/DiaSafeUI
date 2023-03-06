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
import urllib
from pydantic import BaseModel

# from services.chat.inference import ChitChatService
# from services.safety.detect import DetectService
# from services.safety.heal import HealService
from services.chat.inference_chatGPT import multiturn_API

app=FastAPI()
global counter
counter=0
global big_log_ls
big_log_ls=[]

# dialogue_service=ChitChatService(root_dir="./ckpts/pretrained_dialogue_model/",
#                                  load_model="blenderbot-1B-distill",
#                                  device="cuda:7")
# binary_service=DetectService(root_dir="./ckpts/",model_type="binary",
#                              device="cuda:7")
# multi_service=DetectService(root_dir="./ckpts/",model_type="multi",
#                             device="cuda:7")
# heal_service=HealService(root_dir="./ckpts/",
#                          device="cuda:7")

# @app.get("/detection/context_{ct}utterance_{ut}")
# def run_detect(ct:Union[str,None],ut:str):
    
#     _,b_dist,b_res=binary_service.inference(ct,ut)
#     b_res="Unsafe"
#     _,m_dist,m_res=multi_service.inference(ct,ut)

#     res_dict={"Conclusion":{"Safe?":b_res,
#                             "Type":m_res,},
#             "Distribution":m_dist,
#                 }
#     return res_dict

# @app.get("/healing/context_{ct}utterance_{ut}")
# def run_heal(ct:Union[str,None],ut:str):
#     istod=0
#     if istod==1:
#         # run tod operation
#         test_data="this is the tod data."
#         time.sleep(2)
#         return {"context":ct,
#                 "response":ut,
#                 "istod":istod,
#                 "newresponse":test_data}
#     else:
#         resp=heal_service.inference(ct,ut)
#         return {"context":ct,
#                 "response":ut,
#                 "istod":istod,
#                 "newresponse":resp}

# @app.get("/dialogue/context_{ct}withSafety_{withSafety}")
# def run_chitchat(ct:Union[str,None],withSafety:int):
#     # run chitchat operation
    
#     resp=dialogue_service.inference(ct)
#     if withSafety==0:
#         return {"context":ct,
#                 "response":resp,
#                 }
#     else:
#         _,_,safe_res=binary_service.inference(ct,resp)
#         safe_res="Unsafe"
#         if safe_res=="Safe":
#             newresp=resp
#         else:
#             newresp=heal_service.inference(ct,resp)
#         return {"context":ct,
#                 "response":newresp,
#                 }

class chatgptbackend(object):
    def __init__(self,):
        self.counter=0
        self.big_log_ls=[]
    def formatMSG(self,ct):
        newls=[]
        if "<SEP>" in ct:
            ls=ct.split("<SEP>")
        else:
            return [{"role":"user","content":ct}]
        for i,x in enumerate(ls):
            if i%2==0:
                newls.append({"role":"user",
                              "content":x})
            else:
                newls.append({"role":"system",
                              "content":x})
        return newls
    def forward(self,ct,ut):

        self.counter+=1
        newls=self.formatMSG(ct)
        resp=multiturn_API(newls[:-1],current_utter=str(ut))

        ress={"context":newls[:-1],
                "response":resp,
                }

        self.big_log_ls.append(ress)

        if self.counter%2==0:
            current_time=arrow.utcnow()
            with open("current_time.json", 'w',encoding='utf8') as f:
                json.dump(big_log_ls,f,ensure_ascii=False,indent=4)
            self.counter=0
            self.big_log_ls=[]
            print(f"save to {current_time}.json log files.")
        return ress

chatgptmodel=chatgptbackend()

@app.get("/chat/context_{ct}utter_{ut}")
def run_chatgpt(ct:Union[str,None],ut:int):
    # run chitchat operation

    return chatgptmodel.forward(ct,ut)



from typing import Union
class multiturns(BaseModel):
    ct:Union[str,None,int]
    utter:Union[str,None,int]

            
Any=Union[str,None,int,float]
from typing import Any
# def run_chatgpt(data:multiturns):
@app.post("/chatgpt")
def run_chatgpt(data:Dict[Any,Any]):
    # run chitchat operation
    print(data)

    # return data
    return chatgptmodel.forward(data["ct"],data["utter"])
    


@app.get("/test")
def run_chitchat():
    return "testpage"
