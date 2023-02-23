#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 14:50:27 2023

@author: tim
"""

import datetime
import random
import string
import yaml
import json

symbols = string.ascii_letters + string.digits

def code(length):
    return ''.join(random.choice(symbols) for i in range(length))

# https://stackoverflow.com/questions/3844801/check-if-all-elements-in-a-list-are-identical
def all_equal(iterator):
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == x for x in iterator)

# modified from https://yaml-core.narkive.com/20GMqy7V/how-to-force-pyyaml-to-dump-date-with-a-z-at-the-end
yaml.add_representer(datetime.datetime, lambda self, data:
                     self.represent_scalar('tag:yaml.org,2002:str', data.replace(tzinfo=None).isoformat('T') +'Z'))   

f = open("generate-example-input.yaml", "r")

document = f.read()

obj = yaml.safe_load(document)
#print(obj)
#print(obj.keys())

#print(obj["sessions"])

# check slot lists are the same length
slot_lists =  obj["slot_lists"]

lengths = []

for item in slot_lists:
    lengths.append(len(slot_lists[item]["slots"]))

if not all_equal(lengths):
    print("slot lists lengths do not match")
    for item in slot_lists:
        print(item + ": " + len(slot_lists[item]["slots"]))
    exit(1)

slot_count = lengths[0]    

generated_bookings = []    

for name in obj["sessions"]:
 
    session = obj["sessions"][name]
    
    earliest = session["bookings"][0]["start"]
    latest = session["bookings"][0]["end"]
    
    bookings = session["bookings"]
    
    for booking in bookings:
        if booking["start"] < earliest:
            earliest = booking["start"]
        if booking["end"] > latest:
            latest = booking["end"]           
    
    begins=earliest.strftime("%Y-%b-%d-%a-%H%M")
    ends = latest.strftime("%H%M")
    
    for i in range(slot_count):
        user = '-'.join([session["prefix"], begins,ends,session["suffix"], format(i, '03d'),code(6)])
     
        bi = 0
        for booking in bookings:
 
            slot = slot_lists[booking["slot_list"]]["slots"][i]
            policy = slot_lists[booking["slot_list"]]["policy"]
           
            generated_bookings.append({
                    "name": user + "-" + format(bi, '02d'),
                    "user": user,
                    "slot": slot,
                    "policy": policy,
                    "when": {
                            "start": booking["start"].replace(tzinfo=None).isoformat('T') +'Z',
                            "end": booking["end"].replace(tzinfo=None).isoformat('T') +'Z'
                        }
                })
            bi=bi+1
            
            
#print(generated_bookings)         
   

#print(yaml.dump(generated_bookings, default_flow_style=False))
with open(r'generated_bookings.yaml', 'w') as file:
    yaml.dump(generated_bookings, file, default_flow_style=False)
    
with open(r'generated_bookings.json', 'w') as file:
    json.dump(generated_bookings, file)   

