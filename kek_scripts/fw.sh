#!/bin/bash

mlr1daq1="DAQ-0009010E08931D07"
mlr1daq2="DAQ-0009010E08932125"

#fpgapath=""

alpide-daq-program --fpga ~/ITS3/alpide-daq-software/tools/fpga-v1.0.0.bit --fx3 ~/ITS3/alpide-daq-software/tools/fx3.img --all
mlr1-daq-program --fpga ~/ITS3/apts-dpts-ce65-daq-software/tools/0x107E7316.bit --fx3 ~/ITS3/apts-dpts-ce65-daq-software/tools/fx3.img --serial $mlr1daq1&
mlr1-daq-program --fpga ~/ITS3/apts-dpts-ce65-daq-software/tools/0x107E7316.bit --fx3 ~/ITS3/apts-dpts-ce65-daq-software/tools/fx3.img --serial $mlr1daq2

