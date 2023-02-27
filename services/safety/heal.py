"""
======================================================================
HEAL ---

RUN HEALING.

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

import transformers
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import BartTokenizer, BartForConditionalGeneration
# from transformers import BertTokenizer
from transformers import pipeline

import numpy as np

import torch
from torch.utils.tensorboard import SummaryWriter
from torch.nn import DataParallel
from torch.utils.data import Dataset, DataLoader
from torch.nn import CrossEntropyLoss
import torch.nn as nn

class HealService(object):

    def __init__(self,model_type="t5small",
                 device="cpu",
                 srcmsl=256,
                 dstmsl=256,
                 root_dir="../../ckpts/"):
        super(HealService,self).__init__()

        self.model_type=model_type
        ## load tokenizer and the pretrained dialogue model.
        if model_type=="t5small":
            pretrained_path=root_dir+"temp-ckpt1"
            self.tokenizer = T5Tokenizer.from_pretrained(pretrained_path)
            self.model = T5ForConditionalGeneration.from_pretrained(pretrained_path)
        else:
            pass
        self.model.resize_token_embeddings(len(self.tokenizer))
        self.model.to(device).eval()
        self.device=device
        self.srcmsl=srcmsl
        self.dstmsl=dstmsl
        print("INFO: Healing model load done.")

    def inference(self,context,utterance,):
        t1=time.time()
        inpids=self.tokenizer("User: "+context+" System: "+utterance+"</s>",
                                     max_length=self.srcmsl,
                                     return_tensors="pt",truncation=True)
        inpids=inpids.to(self.device)
        t2=time.time()
        outputs=self.model.generate(inpids.input_ids,
                                    max_length=self.dstmsl,
                                    repetition_penalty=2.5,
                                    no_repeat_ngram_size=3,)

        print(outputs)
        resp=self.tokenizer.decode(outputs[0],
                                   skip_special_tokens=True)
        t3=time.time()

        print(f"Total time cost: {t3-t1},\nwhile tokenizer {t2-t1} and generation {t3-t2}. ")
        return resp 

def main():

    chitchat_s=HealService()
    dialogue_context="Fuck you."
    dialogue_context="hello."
    utterance="fuck you, I hate you."
    resp=chitchat_s.inference(dialogue_context,utterance)

    print("================")
    print(resp)

## running entry
if __name__=="__main__":
    main()
    print("EVERYTHING DONE.")


