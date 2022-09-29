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
from datetime import datetime, timedelta

dateformat = "%d-%m-%y %H:%M:%S"
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

def start_datetimes(start_datetime, every_seconds, duration_seconds, end_datetime):

    starts = [start_datetime]
    
    while(1):
        next_start = starts[-1] + timedelta(0,every_seconds)
        next_end = next_start + timedelta(0,duration_seconds)
        if next_end <= end_datetime:
            starts.append(next_start)
        else:
            break
        
    return starts    

def test_start_datetimes():
    
    start_datetime = datetime.strptime('01-10-22  7:00:00', dateformat)
    end_datetime = datetime.strptime('10-10-22  19:00:00', dateformat)
    every_seconds = 24 * 3600
    duration_seconds = 3 * 24 * 3600
    starts = start_datetimes(start_datetime, every_seconds, duration_seconds, end_datetime)    
    assert starts == [
        datetime.strptime('01-10-22 07:00:00', dateformat),
        datetime.strptime('02-10-22 07:00:00', dateformat),
        datetime.strptime('03-10-22 07:00:00', dateformat),
        datetime.strptime('04-10-22 07:00:00', dateformat),       
        datetime.strptime('05-10-22 07:00:00', dateformat),
        datetime.strptime('06-10-22 07:00:00', dateformat),          
        datetime.strptime('07-10-22 07:00:00', dateformat),  
        ]
    duration_seconds = 1 * 24 * 3600
    starts = start_datetimes(start_datetime, every_seconds, duration_seconds, end_datetime)   
    assert starts == [
        datetime.strptime('01-10-22 07:00:00', dateformat),
        datetime.strptime('02-10-22 07:00:00', dateformat),
        datetime.strptime('03-10-22 07:00:00', dateformat),
        datetime.strptime('04-10-22 07:00:00', dateformat),       
        datetime.strptime('05-10-22 07:00:00', dateformat),
        datetime.strptime('06-10-22 07:00:00', dateformat),          
        datetime.strptime('07-10-22 07:00:00', dateformat),  
        datetime.strptime('08-10-22 07:00:00', dateformat),          
        datetime.strptime('09-10-22 07:00:00', dateformat),     
        ]   
    
    start_datetime = datetime.strptime('01-10-22  07:00:00', dateformat)
    end_datetime = datetime.strptime('01-10-22  09:00:00', dateformat)
    every_seconds = 3600
    duration_seconds = 3600
    starts = start_datetimes(start_datetime, every_seconds, duration_seconds, end_datetime)   
    assert starts == [
        datetime.strptime('01-10-22 07:00:00', dateformat),
        datetime.strptime('01-10-22 08:00:00', dateformat)
        ]

# Separate date and time to ease parsing arguments from command line
def token_set(groups, start_date, start_time, every, duration, end_date, end_time):
    
    start_datetime = datetime.strptime(" ".join(start_date, start_time), dateformat)    
    end_datetime = datetime.strptime(" ".join(end_date, end_time), dateformat) 
    every_seconds = duration_to_seconds(every)
    duration_seconds = duration_to_seconds(duration)
    
    starts = start_datetimes(start_datetime, every_seconds, duration_seconds, end_datetime)   
    
    #for start in starts:
        
   
 
    
if __name__ == "__main__":

    if test:
        
        test_duration_to_seconds()
        test_start_datetimes()
        
    else:
        
        try:
            group = sys.argv[1]
            startdate = sys.argv[2]
            startime   = sys.argv[3]
            duration = sys.argv[4]
            every = sys.argv[5]
            
        except IndexError:
            raise SystemExit(f"Usage: {sys.argv[0]} <group> <start_date> <start_time> <every> <duration> <end_date> <end_time>")
            
