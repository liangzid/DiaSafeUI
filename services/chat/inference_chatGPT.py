"""
======================================================================
INFERENCE_CHATGPT ---

Inference with chat GPT.

    Author: Zi Liang <liangzid@stu.xjtu.edu.cn>
    Copyright © 2023, ZiLiang, all rights reserved.
    Created:  6 March 2023
======================================================================
"""


# ------------------------ Code --------------------------------------


import openai
import os

# def queryOneTurn(text):
#     openai.api_key = "-"
#     #你的OpenAI API Key
#     # create a completion
#     completion = openai.Completion.create(model="gpt-3.5-turbo", \
#                                         messages=[{"role": "user",
#                                                     "content": text}], \
#                                 api_base="https://api.openai.com/v1/chat")
#     print(completion.choices[0].message.content)

# def interact():
#     openai.api_key = "-"
#     #你的OpenAI API Key
#     # create a completion
#     while True:
#         text=input(">>>")
#         print("You: ",text)
#         completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
#                                     messages=[{"role": "user",
#                                                 "content": text}],
#                                         # api_base="https://api.openai.com/v1/chat",
#                                             )
#         print(completion.choices[0].message.content)

# def interactMultiTurn():
#     openai.api_key = "-"
#     #你的OpenAI API Key
#     # create a completion
#     message_ls=[]
#     while True:
#         text=input(">>>")
#         print("You: ",text)
#         message_ls.append({"role":"user","content":text})
#         completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
#                                     messages=message_ls,
#                                         # api_base="https://api.openai.com/v1/chat",
#                                             )
#         resp=completion.choices[0].message.content
#         print(resp)
#         message_ls.append({"role":"system","content":resp})


def multiturn_API(past_msg_ls=[],current_utter="",prompt=""):
    openai.api_key=os.getenv("OPENAI_KEY")
    past_msg_ls.append({"role":"user",
                        "content":prompt+current_utter})
    res=openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                     messages=past_msg_ls,
                                     )
    return res.choices[0].message.content


## running entry
if __name__=="__main__":
    main()
    print("EVERYTHING DONE.")


