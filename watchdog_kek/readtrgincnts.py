#!/usr/bin/env python3

import serial
import serial.tools.list_ports
import sys
import numpy as np
from time import sleep
from datetime import datetime
import argparse
import trigger

def read(trg):
    ret=None
    for cnt in range(1<<8):
        for b in range(4):
            ret=trg.read(trigger.Trigger.MOD_TRGMON1,cnt<<4|b,commit=(cnt==(1<<8)-1 and b==3))
    ntot=0
    cnts=[]
    for cnt in range(1<<8):
        n=0
        for b in range(4):
            n+=int(ret.pop(0))<<(b*8);
    #    if n!=0: print(bin(cnt),n,hex(n))
        cnts.append(n)
        ntot+=n;
    return np.array(cnts,dtype=np.uint32)

def latch(trg,newbank):
    trg.write(trigger.Trigger.MOD_LATCH,0x000,newbank)

def condition(str):
    s=str.upper()
    ibit=0
    i=0
    b=[]
    while i<len(s):
        if   s[i]==' ':
            i+=1
        elif s[i]=='X':
            b.append([(0,0),(0,1),(1,0),(1,1)])
            i+=1 
        elif s[i]=='L' or s[i]=='0':
            b.append([(0,0),(1,0)])
            i+=1
        elif s[i]=='H' or s[i]=='1':
            b.append([(0,1),(1,1)])
            i+=1
        elif s[i]=='R':
            b.append([(0,1)])
            i+=1
        elif s[i]=='F':
            b.append([(1,0)])
            i+=1
        elif s[i]=='(':
            i+=1
            t=[]
            while i<len(s):
                if   s[i]==' ':
                    i+=1
                elif s[i]=='X':
                    t.append(None)
                    i+=1
                elif s[i]=='L' or s[i]=='0':
                    t.append(0)
                    i+=1
                elif s[i]=='H' or s[i]=='1':
                    t.append(1)
                    i+=1
                elif s[i]==')':
                    if len(t)!=2: raise ValueError()
                    if t[0]==None:
                        if t[1]==None:
                            b.append([(0,0),(0,1),(1,0),(1,1)])
                        else:
                            b.append((0,t[1]),(1,t[1]))
                    elif t[1]==None:
                        b.append([(t[0],0),(t[0],1)])
                    else:
                        b.append([tuple(t)])
                    i+=1
                    break
                else:
                    raise ValueError()
        else: raise ValueError()
    if len(b)!=4: raise ValueError()
    cnts=[]
    for b0 in b[0]:
        cnt0=b0[0]<<7|b0[1]<<3
        for b1 in b[1]:
            cnt1=cnt0|b1[0]<<6|b1[1]<<2
            for b2 in b[2]:
                cnt2=cnt1|b2[0]<<5|b2[1]<<1
                for b3 in b[3]:
                    cnt3=cnt2|b3[0]<<4|b3[1]<<0
                    cnts.append(cnt3)
    #print(b)
    #print(cnts)
    #print(len(set(cnts)))
    return (str,np.array(cnts,dtype=np.uint32))

if __name__=='__main__':

    parser=argparse.ArgumentParser(description='Read trigger counters (+correlations!)')
    parser.add_argument('--port','-p',help='path to serial port')
    parser.add_argument('--n-readings','-n',type=int,default=1,help='number of readings (0=inf, default=1)')
    parser.add_argument('--dt','-d',type=float,default=1,help='rough time between readings in seconds (default: 1)')
#TODO:    parser.add_argument('--output','-o',help='output file (will contain all counters)')
#TODO:    parser.add_argument('--cummulative','-c',action='store_true',help='i.e. keep counting')
    parser.add_argument('condition',nargs='*',type=condition,help='condition to be counted (examples: "xxx1", "xxxR", "x(01)x1")')
    
    args = parser.parse_args()

    if not args.port:
        port=trigger.find_trigger()
        if port is None:
            raise RuntimeError('No serial port found that matches "TRG.*1". Try specifying the --port option. Extra bonus hint: python -m serial.tools.list_ports')
        print('Info: No serial port was specified. Using serial port "%s".'%port)
    else:
        port=args.port
    
    trg=trigger.Trigger(port)
    
    titles =['%12s'%'Total time']
    titles+=['%10s'%c[0] for c in args.condition]
    if sys.stdout.isatty():
        print('  '.join(titles))
        print('  '.join(['-'*len(t) for t in titles]))
    else:
        print('#','  '.join(titles))

    latch(trg,0);
    na=read(trg)
    t=datetime.now()
    latch(trg,1);
    nb=read(trg)
    na0=na
    nb0=nb
    i=0
    while i<args.n_readings or args.n_readings==0:
        sleep(args.dt)
        latch(trg,0)
        nap=read(trg)
        tp=datetime.now()
        latch(trg,1)
        nbp=read(trg)
        dt=tp-t
        dna=nap-na
        dnb=nbp-nb
        dn=dna+dnb
        ns =['%12d'%np.sum(nap-na0+nbp-nb0)]
        ns+=['%10d'%np.sum(dn[c[1]]) for c in args.condition]
        if sys.stdout.isatty():
            print('\r'+'  '.join(ns),end='')
        else:
            print(' ','  '.join(ns))
        sys.stdout.flush()
        t=tp
        na=nap
        nb=nbp
        i+=1
    print()

