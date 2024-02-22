#!/usr/bin/env python3

import json
import argparse
import os,sys

def readjson():
    with open(args.json,'r',encoding='utf-8') as file:
        jsonconfig = json.load(file)
    return jsonconfig

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="APTS readout(Triggering)",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-j','--json',help='Json file to initialize',default="../json_kek/apts_info.json")

    args=parser.parse_args()

    jsonconfig = readjson()
    sw_path = jsonconfig['SW_path']
    proximity = jsonconfig['TRG']['Proximity']
    apts = jsonconfig['TRG']['APTS']
    trigger_threshold = jsonconfig['TRG']['Trigger_threshold']
    daq_serial = jsonconfig['TRG']['DAQ_serial']    
    nevents = jsonconfig['TRG']['Events']

    mycmd = sw_path + "./apts_readout.py {} {} -ty int -tt {} --serial {} -n {}".format(proximity, apts,trigger_threshold,daq_serial,nevents)
    os.system(mycmd)
