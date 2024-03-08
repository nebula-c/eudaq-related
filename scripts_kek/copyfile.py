#!/usr/bin/env python3

import json
import argparse
import os,sys
import time
import datetime

def readjson():
    with open(args.json,'r',encoding='utf-8') as file:
        jsonconfig = json.load(file)
    return jsonconfig

def get_latest_file(filedir):
    files = os.listdir(filedir)
    latest_file = None
    latest_mtime = 0

    for file in files:
        filepath = os.path.join(filedir,file)
        if os.path.isfile(filepath):
            mtime = os.path.getmtime(filepath)
            if mtime > latest_mtime:
                latest_mtime = mtime
                latest_file = filepath

    return latest_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="For copy raw file periodically",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-j','--json',help='Json file to initialize',default="../json_kek/copyfile.json")
    args=parser.parse_args()

    jsonconfig = readjson()
    
    period = jsonconfig['period']
    newfile = jsonconfig['newfilename']
    newfiledir = jsonconfig['newfilepath']
#    filedir = jsonconfig['filepath']
    filedir = "/home/hipex/data/" + datetime.datetime.now().strftime("%Y%m%d")
#    print(filedir)

    start = datetime.datetime.now().replace(microsecond=0)

    myfile = get_latest_file(filedir)
    print("Copy target file : {}".format(myfile))

    while (True):

        now = datetime.datetime.now().replace(microsecond=0)
        dt = now-start
        dt = int(dt.total_seconds())

        if dt % period == 0:
            print("Copied time: {}".format(now))
            mycmd = "cp {} {}/{}".format(myfile,newfiledir,newfile)
            os.system(mycmd)
            time.sleep(period*0.95)



