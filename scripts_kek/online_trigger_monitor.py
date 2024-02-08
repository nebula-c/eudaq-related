#!/usr/bin/env python3

import json
import argparse
import os,sys

def readjson():
    with open(args.json,'r',encoding='utf-8') as file:
        jsonconfig = json.load(file)
    return jsonconfig

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Online monitor for trigger board",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-j','--json',help='Json file to initialize',default="../json_kek/online_trigger_monitor.json")
    args=parser.parse_args()

    jsonconfig = readjson()
    
    sw_path = jsonconfig["SW_path"]
    sw_file = jsonconfig["SW_file"]
    datafile = jsonconfig["Datafile"]
    Port = jsonconfig["Port"]

    with open(os.path.join(sw_path,datafile),"r") as file:
        content = file.read()
    content=content.strip("\n")

    lines = content.split("\n")
    data = list()
    isnew = False
    data_for_time = list()
    times = list()

    for line in lines:
        if line[0] == '$':
            continue
        if line[0] == '#':
            isnew = True
            mytime = int(line[1:])
            times.append(mytime)
            continue
        else :
            data_for_time.append(line)
        if isnew == True:
            data.append(data_for_time)
            data_for_time = list()
            isnew = False


    print(len(times))
    print("===================================")
    print(len(data))
