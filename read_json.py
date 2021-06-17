# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 16:56:06 2021

@author: dung.pham
"""

import json 
import codecs 
class Essay:
    def __init__(self, essay_topic, extra_topic, model_answer, original_link):
        self.essay_topic = essay_topic 
        self.extra_topic = extra_topic
        self.model_answer = model_answer
        self.original_link = original_link 


f = open("exported_essay_data.json",)

data = json.load(f)

print(data["total"])

essays = data["essays"]

txt_file = codecs.open("exported_essays.txt", "w", "utf-8")

for essay in essays:
    essay_topic = essay["essay_topic"].rstrip("\n")
    if essay_topic:
        txt_file.write(essay_topic +"\n")
txt_file.close()