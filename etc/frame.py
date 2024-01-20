#!/usr/bin/env python3

import json
import argparse
import os,sys

def readjson():
    with open(args.jsonfile,'r',encoding='utf-8') as file:
        jsonconfig = json.load(file)
    return jsonconfig

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="APTS readout",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('jsonfile',metavar='JSONFILE',help='Json file to initialize')
    args=parser.parse_args()

    jsonconfig = readjson()


