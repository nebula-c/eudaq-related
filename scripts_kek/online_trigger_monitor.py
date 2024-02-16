#!/usr/bin/env python3

import json
import argparse
import os,sys
import datetime

def readjson():
    with open(args.json,'r',encoding='utf-8') as file:
        jsonconfig = json.load(file)
    return jsonconfig

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Online monitor for trigger board",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-j','--json',help='Json file to initialize',default="../json_kek/online_trigger_monitor.json")
    parser.add_argument('-dt',type=int,help='dt for monitoring(default: 1 sec))(unit:sec)',default=1)
    args=parser.parse_args()

    jsonconfig = readjson()
    
    sw_path = jsonconfig["SW_path"]
    sw_file = jsonconfig["SW_file"]
    datafile = jsonconfig["Datafile"]
    Port = jsonconfig["Port"]

    dt = args.dt

    start = datetime.datetime.now().replace(microsecond=0)
    readtime = list()

    data = list()
    isnew = False
    data_for_time = list()
    times = list()

    past = start

    while(True):
        now = datetime.datetime.now().replace(microsecond=0)
        dt_now = now-past
        dt_now = int(dt_now.total_seconds())
        if  dt_now > dt:
            myreadtime = now-start
            readtime.append(int(myreadtime.total_seconds()))
            past = now
        else:
            continue

        with open(os.path.join(sw_path,datafile),"r") as file:
            content = file.read()
            content = content.strip("\n")
            lines = content.split("\n")

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

        data = sum(data, [])               
        filtered_data = [item for item in data if item.startswith('b')]
        modified_data = [item[1:] for item in filtered_data]
        data_trg_c = [item for item in modified_data if item.endswith(' &')]
        data_trg_s = [item for item in modified_data if item.endswith(' %')]
        trg_c = [item[:-2] for item in data_trg_c]
        trg_s = [item[:-2] for item in data_trg_s]
       
        trg_c = [item.zfill(4) for item in trg_c]
        trg_s = [item.zfill(4) for item in trg_s]
 
        trg_c_ch3 = sum(1 for item in trg_c if '1' in str(item) and str(item)[0] == '1')
        trg_c_ch2 = sum(1 for item in trg_c if '1' in str(item) and str(item)[1] == '1')
        trg_c_ch1 = sum(1 for item in trg_c if '1' in str(item) and str(item)[2] == '1')
        trg_c_ch0 = sum(1 for item in trg_c if '1' in str(item) and str(item)[3] == '1')

        trg_s_ch3 = sum(1 for item in trg_s if '1' in str(item) and str(item)[0] == '1')
        trg_s_ch2 = sum(1 for item in trg_s if '1' in str(item) and str(item)[1] == '1')
        trg_s_ch1 = sum(1 for item in trg_s if '1' in str(item) and str(item)[2] == '1')
        trg_s_ch0 = sum(1 for item in trg_s if '1' in str(item) and str(item)[3] == '1')

#        trg_c_ch3 = [item for item in trg_c if '1' in str(item) and str(item)[0] == '1']
#        trg_c_ch2 = [item for item in trg_c if '1' in str(item) and str(item)[1] == '1']
#        trg_c_ch1 = [item for item in trg_c if '1' in str(item) and str(item)[2] == '1']
#        trg_c_ch0 = [item for item in trg_c if '1' in str(item) and str(item)[3] == '1']

#        trg_s_ch3 = [item for item in trg_s if '1' in str(item) and str(item)[0] == '1']
#        trg_s_ch2 = [item for item in trg_s if '1' in str(item) and str(item)[1] == '1']
#        trg_s_ch1 = [item for item in trg_s if '1' in str(item) and str(item)[2] == '1']
#        trg_s_ch0 = [item for item in trg_s if '1' in str(item) and str(item)[3] == '1']

        print(trg_c_ch3)
        print("len(data): {}".format(len(data)))
        print("--------------------------------------------------------------")
        data = list()

    print(len(times))
    print("===================================")
    print(len(data))


