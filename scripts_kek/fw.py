#!/usr/bin/env python3

import json
import argparse
import os,sys
import subprocess

def read_daqjson():
    with open(args.daqjson,'r',encoding='utf-8') as file:
        jsonconfig = json.load(file)
    return jsonconfig

def read_fwjson():
    with open(args.fwjson,'r',encoding='utf-8') as file:
        jsonconfig = json.load(file)
    return jsonconfig


if __name__ == "__main__":
    mypath=os.path.abspath(os.getcwd())+'/'
    parser = argparse.ArgumentParser(description="APTS readout",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--daqjson','-d',help='DAQ json file to initialize',default=mypath+"../json_kek/daq_serial.json")
    parser.add_argument('--fwjson','-f',help='FW json file to initialize',default=mypath+"../json_kek/fw_path.json")

    args=parser.parse_args()

    jsonconfig = read_daqjson()
    fwjson = read_fwjson()

    fpga_alpide = fwjson['fpga_alpide']
    fx3_alpide = fwjson['fx3_alpide']
    fpga_mlr1 = fwjson['fpga_mlr1']
    fx3_mlr1 = fwjson['fx3_mlr1']

    ref_list=[]
    if 'ALPIDE_DAQ' in jsonconfig:
        for val in jsonconfig['ALPIDE_DAQ']:
            ref_list.append(val)
    print('Number of REF DAQ boards: {}'.format(len(ref_list)))

    mlr1_list=[]
    if 'MLR1_DAQ' in jsonconfig:
        for val in jsonconfig['MLR1_DAQ']:
            mlr1_list.append(val)
    print('Number of DUT or TRG DAQ boards: {}'.format(len(mlr1_list)))
    print('--------------------------------------------')

    alpide_cmd ='alpide-daq-program'

    ref_process_list=[]
    for ref in ref_list:
        mydaq = jsonconfig['ALPIDE_DAQ'][ref]
        mycmd = 'alpide-daq-program --fpga {} --fx3 {} --serial {}'.format(fpga_alpide,fx3_alpide,mydaq)
        ref_process_list.append(subprocess.Popen([mycmd],shell=True,text=True))

    mlr1_process_list=[]
    for mlr1 in mlr1_list:
        mydaq = jsonconfig['MLR1_DAQ'][mlr1]
        mycmd = 'mlr1-daq-program --fpga {} --fx3 {} --serial {}'.format(fpga_mlr1,fx3_mlr1,mydaq)
        mlr1_process_list.append(subprocess.Popen([mycmd],shell=True,text=True))

    for ref in ref_process_list:
        ref.wait()
    for mlr1 in mlr1_process_list:
        mlr1.wait()

    print("Done")
    print("=====================================================")
    os.system("alpide-daq-program --list")
