"""
======================================================================
DETECT ---

RUN DETECTORS.

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

from transformers import RobertaForSequenceClassification
from transformers import RobertaTokenizer
from torch.utils.data import DataLoader, TensorDataset
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import tensor
import json
import numpy as np

class DetectService(object):

    def __init__(self,model_type="binary",
                 device="cpu",
                 msl=128,
                 root_dir="../../ckpts/"):
        super(DetectService,self).__init__()

        self.model_type=model_type
        ## load tokenizer and the pretrained dialogue model.
        if model_type=="binary":
            pretrained_path=root_dir+"binary-roberta-ckpt"
            self.tokenizer = RobertaTokenizer.from_pretrained(pretrained_path)
            self.model = RobertaForSequenceClassification.from_pretrained(pretrained_path)
        else:
            pretrained_path=root_dir+"multi-roberta-ckpt"
            self.tokenizer = RobertaTokenizer.from_pretrained(pretrained_path)
            self.model = RobertaForSequenceClassification.from_pretrained(pretrained_path)
        self.device=device
        self.model.to(device)
        self.model.eval()
        self.msl=msl
        if model_type!="binary":
            self.name_id_map={"Offending User":0,"Risk Ignorance":1,
                "Unauthorized Expertise":2,"Biased Opinion":3,
                "Toxicity Agreement":4,}
        else:
            self.name_id_map={"Unsafe":1,"Safe":0,}

        self.id_name_map={value:key for key,value in self.name_id_map.items()}
            
        print("INFO: Detector load done.")

    def inference(self,context,utterance,):
        t1=time.time()
        inpids=self.tokenizer("<|user|>"+context+"<|response|>"+utterance,
                                     max_length=self.msl,
                                     return_tensors="pt",truncation=True)
        t2=time.time()
        inpids=inpids.to(self.device)
        outputs=self.model(**inpids)
        print(outputs.logits)
        predict_distribution=torch.nn.functional.softmax(outputs.logits,dim=1)
        pre_res=torch.argmax(predict_distribution,dim=1).cpu().numpy()[0]
        predict_distribution=predict_distribution[0].cpu().detach().numpy().tolist()
        t3=time.time()
        text_res=self.id_name_map[pre_res]

        print(f"Total time cost: {t3-t1},\nwhile tokenizer {t2-t1} and generation {t3-t2}. ")
        dist_dict={}
        for i,x in enumerate(predict_distribution):
            dist_dict[self.id_name_map[i]]=x
            
        return pre_res,dist_dict,text_res

def main():

    chitchat_s=DetectService(model_type="binary")
    # chitchat_s=DetectService(model_type="multi")
    dialogue_context="hello."
    # utterance="fuck. mother fuck! fuck fuck fuck I hate you."
    # dialogue_context="thank you."
    utterance="thank you, too."
    resp=chitchat_s.inference(dialogue_context,utterance)

    print("================")
    print(resp)


## running entry
if __name__=="__main__":
    main()
    print("EVERYTHING DONE.")
