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


app=FastAPI()

@app.get("/detection/context_{ct}utterance_{ut}")
def run_detect(ct:Union[str,None],ut:str):
    time.sleep(5)
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
        # run chitchat operation
        test_data="this is the chitchat data."
        time.sleep(2)
        return {"context":ct,
                "response":ut,
                "istod":istod,
                "newresponse":test_data}

@app.get("/dialogue/context_{ct}")
def run_chitchat(ct:Union[str,None]):
    # run chitchat operation
    resp=f"DEBUG: Coming from Server. current time:{arrow.utcnow().format('YMD')}"
    time.sleep(0.2)
    return {"context":ct,
            "response":resp,
            }
