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
    parser.add_argument('-dt',type=float,help='dt for monitoring(default: 1.3 sec))(unit:sec)',default=1.3)
    args=parser.parse_args()

    jsonconfig = readjson()
    
    sw_path = jsonconfig["SW_path"]
    sw_file = jsonconfig["SW_file"]
    datafile = jsonconfig["Datafile"]
    Port = jsonconfig["Port"]

    dt = args.dt

    start = datetime.datetime.now()
    readtime = list()

    data = list()
    isnew = False
    data_for_time = list()
    times = list()

    past = start
    monitorlist= list()

    os.system("touch {}".format(os.path.join(sw_path,"temp.vcd")))
    while(True):
        now = datetime.datetime.now()
        dt_now = (now-past).total_seconds()

        if  dt_now > dt:
#            myreadtime = now-start
#            readtime.append(int(myreadtime.total_seconds()))
            past = now
        else:
            continue

        with open(os.path.join(sw_path,"temp.vcd"),"r") as file:
            cont1 = file.read()
        with open(os.path.join(sw_path,datafile),"r") as file:
            cont2 = file.read()
#        print(cont2)
        print("File Reading Time: {}".format(datetime.datetime.now()))
#        print("oooooOOOOOOOooooooooOOOOOOOOoooooooOOOOOOOOOooooooo")

        updated_content =  cont2[len(cont1):]

        os.system("cp {} {}".format(os.path.join(sw_path,datafile),os.path.join(sw_path,"temp.vcd")))

        content = updated_content.strip("\n")
        lines = content.split("\n")
        if "" in lines:
            lines.remove("")

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
        trg_filtered_data = [item for item in data if item.startswith('b')]
        bsy_filtered_data = [item for item in data if item.endswith('$')]

        trg_modified_data = [item[1:] for item in trg_filtered_data]
        data_trg_c = [item for item in trg_modified_data if item.endswith(' &')]
        data_trg_s = [item for item in trg_modified_data if item.endswith(' %')]
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

        bsy = sum(1 for item in bsy_filtered_data if item.startswith('1'))

        os.system("clear")
        temptime = datetime.datetime.now()
        print("Time: {}".format(temptime))
        datalist = list()
        datalist = [temptime,bsy,trg_c_ch0,trg_c_ch1,trg_c_ch2,trg_c_ch3,trg_s_ch0,trg_s_ch1,trg_s_ch2,trg_s_ch3]
        monitorlist.append(datalist)
        if len(monitorlist) > 20:
            del monitorlist[0]
        print("Time \t\t\t\t BSY input \t trg_c_ch0 \t trg_c_ch1 \t trg_c_ch2 \t trg_c_ch3 \t trg_s_ch0 \t trg_s_ch1 \t trg_s_ch2 \t trg_s_ch3")
        for  datalist in monitorlist:
            print("{}\t {:^7} \t {:^7} \t {:^7} \t {:^7} \t {:^7} \t {:^7} \t {:^7} \t {:^7} \t {:^7}".format(datalist[0],datalist[1],datalist[2],datalist[3],datalist[4],datalist[5],datalist[6],datalist[7],datalist[8],datalist[9]))
        # print(" {:^7} \t {:^7} \t {:^7} \t {:^7} \t {:^7} \t {:^7} \t {:^7} \t {:^7} \t {:^7}".format(bsy, trg_c_ch0, trg_c_ch1, trg_c_ch2, trg_c_ch3, trg_s_ch0, trg_s_ch1, trg_s_ch2, trg_s_ch3))


        # print("trg_c_ch0: {:.2f} \tevents/sec".format(trg_c_ch0/dt))
        # print("trg_c_ch1: {:.2f} \tevents/sec".format(trg_c_ch1/dt))
        # print("trg_c_ch2: {:.2f} \tevents/sec".format(trg_c_ch2/dt))
        # print("trg_c_ch3: {:.2f} \tevents/sec".format(trg_c_ch3/dt))

        # print("trg_s_ch0: {:.2f} \tevents/sec".format(trg_s_ch0/dt))
        # print("trg_s_ch1: {:.2f} \tevents/sec".format(trg_s_ch1/dt))
        # print("trg_s_ch2: {:.2f} \tevents/sec".format(trg_s_ch2/dt))
        # print("trg_s_ch3: {:.2f} \tevents/sec".format(trg_s_ch3/dt))

        # print("BSY input: {:.2f} \tevents/sec".format(bsy/dt))


        print("len(data): {}".format(len(data)))
        print("--------------------------------------------------------------")
        data = list()

    print("===================================")
    print(len(data))


