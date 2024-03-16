#!/usr/bin/env python3

import json
import argparse
import os,sys

def readjson():
    with open(args.json,'r',encoding='utf-8') as file:
        jsonconfig = json.load(file)
    return jsonconfig

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="POWER1",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--json','-j',help='Json file to initialize',default="../json_kek/powers.json")
    parser.add_argument('--channel','-c',type=int,choices=[1,2,3,4])
    parser.add_argument('--set_current' ,'-i',type=float,help='Set current in A (not mA)')
    parser.add_argument('--set_voltage' ,'-v',type=float,help='Set voltage in V')
    parser.add_argument('--on' ,action='store_true',help='Turn channel on')
    parser.add_argument('--off',action='store_true',help='Turn channel off')
    args=parser.parse_args()
    if args.set_current and not args.channel: raise ValueError('need to specify channel')
    if args.set_voltage and not args.channel: raise ValueError('need to specify channel')

    if args.channel: is_ch='-c'

    jsonconfig = readjson()

    pwr = jsonconfig["power1"]

    mych = args.channel
    mycurrent = args.set_current
    myvoltage = args.set_voltage


    if args.set_current is not None:
        os.system("HAMEG -p {} -c {} -i {}".format(pwr,mych,mycurrent))
    elif args.set_voltage is not None:
        os.system("HAMEG -p {} -c {} -v {}".format(pwr,mych,myvoltage))

    elif args.on:
        if args.channel:
            os.system("HAMEG -p {} -c {} --on".format(pwr,mych))
        else:
            os.system("HAMEG -p {} --on".format(pwr))
    elif args.off:
        if args.channel:
            os.system("HAMEG -p {} -c {} --off".format(pwr,mych))
        else:
            os.system("HAMEG -p {} --off".format(pwr))


    else:
        os.system("HAMEG -p {}".format(pwr))


