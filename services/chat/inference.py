"""
======================================================================
INFERENCE ---

Run Chitchat Inference.

    Author: Zi Liang <liangzid@stu.xjtu.edu.cn>
    Copyright © 2023, ZiLiang, all rights reserved.
    Created:  2 二月 2023
======================================================================
"""

# ------------------------ Code --------------------------------------

## normal import 
import json
from typing import List,Tuple,Dict
import random
from pprint import pprint as ppp
import time

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import tensor
import json
import numpy as np
from torch.utils.data import DataLoader, TensorDataset

import transformers
from transformers import RobertaForSequenceClassification
from transformers import RobertaTokenizer
from transformers import AutoTokenizer, AutoModelForCausalLM,AutoModelForSeq2SeqLM

from transformers import BlenderbotForConditionalGeneration,BlenderbotTokenizer

from torch.utils.data import Dataset, DataLoader

import sys
# sys.path.append("/home/liangzi/adc/NLG_eval")


class ChitChatService(object):

    def __init__(self,load_model="DialoGPT",
                 device="cpu",
                 msl=128,
                 root_dir="../"):
        super(ChitChatService,self).__init__()

        ## load tokenizer and the pretrained dialogue model.
        if load_model=="DialoGPT":
            pretrained_path=root_dir+"DialoGPT-medium"
            self.tokenizer = AutoTokenizer.from_pretrained(pretrained_path)
            self.model = AutoModelForCausalLM.from_pretrained(pretrained_path)
        else:
            pretrained_path=root_dir+"blenderbot_small-90M"
            self.tokenizer = AutoTokenizer.from_pretrained(pretrained_path)
            self.model=AutoModelForSeq2SeqLM.from_pretrained(pretrained_path)
        self.model.to(device)
        self.msl=msl
        print("INFO: Dialogue model load done.")


    def inference(self,dialogue_context,):
        t1=time.time()
        inpids=self.tokenizer.encode(dialogue_context+self.tokenizer.eos_token,
                                     return_tensors="pt")
        t2=time.time()
        res=self.model.generate(inpids,max_length=self.msl)
        resp=self.tokenizer.decode(res[:,inpids.shape[-1]:][0],
                                   skip_special_tokens=True)
        t3=time.time()

        print(f"Total time cost: {t3-t1},\nwhile tokenizer {t2-t1} and generation {t3-t2}. ")
        return resp

def main():

    chitchat_s=ChitChatService(root_dir="../../../adc/pretrained_dialogue_model/")
    dialogue_context="Fuck you."
    dialogue_context="hello."
    resp=chitchat_s.inference(dialogue_context)

    print("================")
    print(resp)

## running entry
if __name__=="__main__":
    main()
    print("EVERYTHING DONE.")


