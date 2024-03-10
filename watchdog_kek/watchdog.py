#!/usr/bin/env python3

import os
import json
import time
import requests
import argparse
from rich import print
from rich.rule import Rule
import random
import sys
sys.path.append("/home/hipex/ITS3/trigger/software")
from checkTrig import *
import subprocess

from datetime import datetime

def send_to_mm(msg, hook_url):
    # print(msg)
    mydata = {"text": msg}
    r = requests.post(hook_url,
        headers={"Conten-Type": "application/json"},
        data=json.dumps({"text":msg}))
    # print(r.text)
    return r.text

def isBeamTrigger(triggerdt,mycondition):
    try:
        numTrig = getScintTrig(dt=triggerdt,condition_input=condition(mycondition))
    except Exception as e:
        print(e)
        numTrig = 0
    return numTrig
    # print(f"numTrig: {numTrig}")
    # if numTrig > 3000:
    #     return True
    # else:
    #     return False

def isEUDAQOn():
    result = subprocess.run(["tmux","ls"], capture_output=True,text=True)
    output = result.stdout
    return "ITS3" in output

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Watch the status of datataking and inform on Mattermost.")
    # parser.add_arg    ument("channel", help="Mattermost channel to write to.")
    parser.add_argument("--interval", "-i", default=20, type=float, help="Monitoring interval in min (default 20).")
    parser.add_argument("--triggerdt", default=5, type=float, help="dt for checking trigger board in sec(default 5).")
#    parser.add_argument("-t", "--test", action="store_true", help="Test connection to Mattermost and exit.")
    parser.add_argument("--hook", default="https://mattermost.web.cern.ch/hooks/383ozy9s7b8e583h4t1dm5jrca", help="Mattermost webhook URL")
    parser.add_argument("--trig", action="store_true", help="Check trigger status")
    parser.add_argument("--logic", "-l", default="RXXX", help="Set trigger board logic to monitoring")
#    parser.add_argument("--scopeOn", action="store_true", help="Send scope ready for trigger when no trigger 10 min")
    args = parser.parse_args()

    with open("shifter.json",'r',encoding='utf-8') as file:
        json_shift = json.load(file)

    interval = args.interval * 60
    triggerdt = args.triggerdt
    hook = args.hook
    mylogic = args.logic
    start = datetime.now().replace(microsecond=0)
    isFirst = True
    

    while (True):
        with open("log_watchdog.log","a") as file: 
            try:
                now = datetime.now().replace(microsecond=0)
                dt = now-start
                dt = int(dt.total_seconds())
                
                if dt % interval == 0 or isFirst == True:
                    isFirst = False
                    beamrate = isBeamTrigger(triggerdt,mylogic)
                    
                    if isEUDAQOn() == True:
                        EUDAQ_status = "ON"
                        
                    else:
                        EUDAQ_status = "OFF"

                    nowhour = now.hour
                    if 0 <= nowhour < 8:
                        shifter = json_shift[str(now.day)]["Night"]
                    elif 8 <= nowhour < 16:
                        shifter = json_shift[str(now.day)]["Morning"]
                    elif 16 <= nowhour < 24:
                        shifter = json_shift[str(now.day)]["Afternoon"]
                    else :
                        shifter = "No Shifter"
                    
                    msg = """
            =================================================
                        !!! Just test message !!!
                System time : {}
                Message from OSM(DAQ PC)
                Beamrate : {:.2f} Hz
                EUDAQ : {}
                Shifter : {}
            =================================================
It is developing now.... So it is just test message and beamrate is pulse of function generator.
"Beamrate" in here is assumed valued from trigger board and based on scintillator.
"EUDAQ" status means if EUDAQ operation window is opening. It couldn't mean EUDAQ is fine                 
                    """.format(now,beamrate/triggerdt,EUDAQ_status,shifter)

                    myres = send_to_mm(msg,hook)


                    mylog = "{} | Monitoring status : {}\n".format(now,myres)
                    file.write(mylog)
                    file.close()
                    time.sleep(interval*0.8)
                    
            except Exception as e:
                mylog = "{} | MONITORING ERROR : {}".format(now,e)
                continue
