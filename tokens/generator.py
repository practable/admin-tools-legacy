#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 10:05:50 2022

@author: timothy.d.drysdale@gmail.com

To test:
    $ pip install pytest
    $ pytest generator.py
"""

import jwt
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta

#dateformat = "%d-%m-%y %H:%M:%S"
dateformat = "%Y-%m-%dT%H:%M:%SZ"

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
    
    start_datetime = datetime.strptime('2022-10-01T07:00:00Z', dateformat)
    end_datetime = datetime.strptime('2022-10-10T19:00:00Z', dateformat)
    every_seconds = 24 * 3600
    duration_seconds = 3 * 24 * 3600
    starts = start_datetimes(start_datetime, every_seconds, duration_seconds, end_datetime)    
    
    assert starts == [
        datetime.strptime('2022-10-01T07:00:00Z', dateformat),
        datetime.strptime('2022-10-02T07:00:00Z', dateformat),
        datetime.strptime('2022-10-03T07:00:00Z', dateformat),
        datetime.strptime('2022-10-04T07:00:00Z', dateformat),       
        datetime.strptime('2022-10-05T07:00:00Z', dateformat),
        datetime.strptime('2022-10-06T07:00:00Z', dateformat),          
        datetime.strptime('2022-10-07T07:00:00Z', dateformat),  
        ]
    
    duration_seconds = 1 * 24 * 3600
    starts = start_datetimes(start_datetime, every_seconds, duration_seconds, end_datetime)   
    assert starts == [
        datetime.strptime('2022-10-01T07:00:00Z', dateformat),
        datetime.strptime('2022-10-02T07:00:00Z', dateformat),
        datetime.strptime('2022-10-03T07:00:00Z', dateformat),
        datetime.strptime('2022-10-04T07:00:00Z', dateformat),       
        datetime.strptime('2022-10-05T07:00:00Z', dateformat),
        datetime.strptime('2022-10-06T07:00:00Z', dateformat),          
        datetime.strptime('2022-10-07T07:00:00Z', dateformat),  
        datetime.strptime('2022-10-08T07:00:00Z', dateformat),          
        datetime.strptime('2022-10-09T07:00:00Z', dateformat),      
        ]   
    
    start_datetime = datetime.strptime('2022-10-01T07:00:00Z', dateformat)
    end_datetime = datetime.strptime('2022-10-01T09:00:00Z', dateformat)
    
    every_seconds = 3600
    duration_seconds = 3600
    starts = start_datetimes(start_datetime, every_seconds, duration_seconds, end_datetime)   
    assert starts == [
        datetime.strptime('2022-10-01T07:00:00Z', dateformat),
        datetime.strptime('2022-10-01T08:00:00Z', dateformat)
        ]

def create_token(groups, start, duration_seconds, audience="https://book.practable.io"):
    
    p = subprocess.run(["./user-token.sh", audience, groups, start, str(duration_seconds)], capture_output=True)
    return p.stdout[:-1]

def get_secret():
    
    secret = ""
    
    try:
        f = open("%s/secret/book.pat"%(os.path.expanduser('~')), "r")
        secret = f.read()
        f.close()
    except:
        raise ValueError('No secret found')
    
    return secret.rstrip("\n") 
    
def test_create_token() :
    # test with far future date
    token = create_token("truss everyone", "2122-10-12T07:20:50Z", 86400)

    secret = ""
    verify = False
    try:
        secret = get_secret()
        verify = True
    except ValueError:
        print("Warning: not verifying JWT signature")

    #remove newlines from token and secret
    payload = jwt.decode(token, 
                         secret, 
                         audience="https://book.practable.io", 
                         algorithms=["HS256"], 
                         options={"verify_signature": verify, 
                                  "verify_nbf": False}
                         )
   
    assert payload["groups"] == ['truss', 'everyone']
    assert payload["nbf"] == 4821232850
    assert payload["exp"] == 4821232850 +  86400
    if debug:
        if verify:
            print("Signature verified (%d chars)"%(len(secret)))
        print(payload)
    
# Separate date and time to ease parsing arguments from command line
def create_token_set(groups, start_date, start_time, every, duration, end_date, end_time):
    
    start_datetime = datetime.strptime(" ".join(start_date, start_time), dateformat)    
    end_datetime = datetime.strptime(" ".join(end_date, end_time), dateformat) 
    every_seconds = duration_to_seconds(every)
    duration_seconds = duration_to_seconds(duration)
    
    starts = start_datetimes(start_datetime, every_seconds, duration_seconds, end_datetime)   
    tokens = {}
    for start in starts:
        tokens.append(create_token(groups, start, duration_seconds))
    return tokens   

def time_code(start, day, hour, minute):
    code = ""
    if day:
        code += "-".join([start.strftime('%a'),str(start.day), start.strftime('%b')])
    if hour:
        hr = str(start.hour) + "h"
        if code != "":
            code = "-".join([code, hr])
        else:
            code = hr
    if minute:
        mn = str(start.minute) + "m"
        code +=  mn
            
    return code

def test_time_code():
    start = datetime.strptime('2022-10-01T07:00:00Z', dateformat)
    day = True
    hour = False
    minute = False
    
    if debug:
        print(time_code(start, day, hour, minute))
        
    assert time_code(start, day, hour, minute) == "Sat-1-Oct"        
    
    day = False
    hour = True
    minute = False

    if debug:
        print(time_code(start, day, hour, minute))
    
    assert time_code(start, day, hour, minute) == "7h"  
    
    day = False
    hour = True
    minute = True

    if debug:
        print(time_code(start, day, hour, minute))
    
    assert time_code(start, day, hour, minute) == "7h0m"   
    
    day = True
    hour = True
    minute = True

    if debug:
        print(time_code(start, day, hour, minute))
   
    assert time_code(start, day, hour, minute) == "Sat-1-Oct-7h0m"      

def time_codes(code, starts, every_seconds, duration_seconds):
  
    codes = []
    day = False
    hour = False
    minute = False
    
    if every_seconds >= 24 * 3600:
        day = True
    elif every_seconds >= 3600:
        hour = True
    else:
        hour = True
        minute = True
        
    for start in starts:
        codes.append("-".join(code, time_code(start, day, hour, minute)))

    return time_codes   


def test_time_codes():
    
    starts = [ datetime.strptime('2022-10-01T07:00:00Z', dateformat),
              datetime.strptime('2022-10-02T07:00:00Z', dateformat)
             ]
              
    codes = time_codes("test", starts, True, False, False)

    assert codes == [ "test-Sat-1-Oct", "test-Sun-2-Oct"]    
    
if __name__ == "__main__":

    if test:
        
        test_duration_to_seconds()
        test_start_datetimes()
        test_create_token()
        test_time_code()
        
    else:
        
        try:
            group = sys.argv[1]
            startdate = sys.argv[2]
            startime   = sys.argv[3]
            duration = sys.argv[4]
            every = sys.argv[5]
            
        except IndexError:
            raise SystemExit(f"Usage: {sys.argv[0]} <group> <start_date> <start_time> <every> <duration> <end_date> <end_time>")
            
