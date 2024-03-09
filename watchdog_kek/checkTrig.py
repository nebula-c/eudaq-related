#!/usr/bin/env python3

import serial
import serial.tools.list_ports
import sys
import numpy as np
from time import sleep
from datetime import datetime
import argparse
sys.path.append("/home/hipex/ITS3/trigger/software")
import trigger
from readtrgincnts import *

def getScintTrig(port="/dev/serial/by-id/usb-CERN_ITS3_Trigger_Board_0011-if01-port0", dt=10, condition_input=condition("Rxxx")):
    trg=trigger.Trigger(port)
    latch(trg,0)
    na=read(trg)
    t=datetime.now()
    latch(trg,1)
    nb=read(trg)
    na0=na
    nb0=nb
    i=0
    # print(f"na: {na}, nb: {nb}")
    sleep(dt)
    latch(trg,0)
    nap=read(trg)
    tp=datetime.now()
    latch(trg,1)
    nbp=read(trg)
    dt=tp-t
    dna=nap-na
    dnb=nbp-nb
    dn=dna+dnb
    sys.stdout.flush()
    ns =['%12d'%np.sum(nap-na0+nbp-nb0)]
    if isinstance(condition_input, tuple):
        condition_input = [condition_input]
    ns+=['%10d'%np.sum(dn[c[1]]) for c in condition_input]
    # print(float(ns[1]))
    return float(ns[1])


if __name__=='__main__':
    parser=argparse.ArgumentParser(description='check trigger counters')
    parser.add_argument('--port','-p',help='path to serial port', default="/dev/serial/by-id/usb-CERN_ITS3_Trigger_Board_0011-if01-port0")
    parser.add_argument('--n-readings','-n',type=int,default=1,help='number of readings (0=inf, default=1)')
    parser.add_argument('--dt','-d',type=float,default=2,help='rough time between readings in seconds (default: 1)')    
    parser.add_argument('condition',nargs='*',type=condition,help='condition to be counted (examples: "xxx1", "xxxR", "x(01)x1")', default=condition("xxxR"))
    args = parser.parse_args()

    # print(getScintTrig(args.port,args.dt,args.condition))
    print(getScintTrig(port=args.port, dt=args.dt, condition_input=args.condition))
