#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 09:40:07 2023

@author: tim
"""
import json

with open("../aws/shellrelay/data/shell2.json") as file:
    shell = json.load(file)    
    
    
with open("../gce-develop/relay/data/status.json") as file:
    status = json.load(file)     
    
    
experiments = {}

for connection in shell:
    if "/" not in connection["topic"]:
        experiments[connection["topic"]] = connection
        
# print(experiments)


# remoteAddr

streams = {}

datas = {}
videos = {}

for stream in status:
    name = stream["topic"].split("-")
    
    if len(name) < 3: #ignore stats channel
        continue
    
    topic = name[0]
    what = name[2]
    
    if stream["remoteAddr"]==experiments[topic]["remoteAddr"]:
        streams[stream["topic"]] = stream
        if what == "video":
            videos[topic] = stream
        if what == "data":
            datas[topic] = stream
        
      
vlist = []

for topic in videos:
    video = (videos[topic])
    vlist.append((video["topic"] + " : " + video["stats"]["tx"]["last"]))

for topic in datas:
    data = (datas[topic])
    vlist.append((data["topic"] + " : " + data["stats"]["tx"]["last"]))
    
vlist.sort()

   
for v in vlist:
    print(v)    
   