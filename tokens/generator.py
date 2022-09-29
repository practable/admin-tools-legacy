#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 10:05:50 2022

@author: timothy.d.drysdale@gmail.com

To test:
    $ pip install pytest
    $ pytest generator.py
"""

import re
import sys
from datetime import datetime

debug = True
test = True #set true if testing in spyder, so that tests run

def multiplier(x):
    return {
        'd': 86400,
        'h': 3600,
        'm': 60,
        's': 1
    }[x]

def duration_to_seconds(duration):

    pattern = '(([0-9])+[dmhs])'
        
    sec = 0 
    
    match = re.findall(pattern, duration)

    for m in match:
        unit = m[0][-1]
        value = int(m[0][:-1])
        duration = multiplier(unit) * value

        sec += duration
        
        if debug:
            print("%s => %d %s => %ds"%(m[0], value, unit, duration))
    
    return  sec
    


def test_duration_to_seconds():
  
    assert duration_to_seconds("1d") == 24 * 3600
    assert duration_to_seconds("1h") == 3600
    assert duration_to_seconds("1m") == 60    
    assert duration_to_seconds("1s") == 1
    assert duration_to_seconds("1d1h") == 25 * 3600
    assert duration_to_seconds("1d1h1m") == (25 * 3600 + 60)
    assert duration_to_seconds("1d1h1m1s") == (25 * 3600 + 61)
    assert duration_to_seconds("2h30m") == ((2 * 3600) + (30 * 60))
    assert duration_to_seconds("3d16h28m42s") == ((3 * 24 * 3600) + (16 * 3600) + (28 * 60) + 42)
        

# Separate date and time to ease parsing arguments from command line
def token_set(groups, start_date, start_time, every, duration, end_date, end_time):
    
    start_datetime = datetime.strptime(" ".join(start_date, start_time), "%d/%m/%y %H:%M:%S")    
    end_datetime = datetime.strptime(" ".join(end_date, end_time), "%d/%m/%y %H:%M:%S") 
 
    
if __name__ == "__main__":

    if test:
        
        test_duration_to_seconds()    
        
    else:
        
        try:
            group = sys.argv[1]
            startdate = sys.argv[2]
            startime   = sys.argv[3]
            duration = sys.argv[4]
            every = sys.argv[5]
            
        except IndexError:
            raise SystemExit(f"Usage: {sys.argv[0]} <group> <start_date> <start_time> <every> <duration> <end_date> <end_time>")
            
