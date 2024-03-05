#!/usr/bin/env python3

import time
from zaber_motion.binary import Connection, Device
from zaber_motion import Units, Library, LogOutputMode

def main():
    Library.set_log_output(LogOutputMode.STDOUT)

    with Connection.open_serial_port("/dev/ttyUSB4") as conn:
        devices = conn.detect_devices()
        device0 = devices[0] #첫 번째 스테이지 모듈 // 세로 mircosteps = 0 일 때, 제일 높은 위치 ~ 최대값을 먼저 파악해야함(세팅마다 다름) -> 가장 밑에 설치하는 세팅에서 대략 365000이 세로 맥스(가장 밑에오는지점)
        device1 = devices[1] #두 번째 스테이지 모듈 // 가로 
        print("Device %d has device ID %d." %(device0.device_address, device0.identity.device_id))
        print("Device %d has device ID %d." %(device1.device_address, device1.identity.device_id))

        device0.stop()
        device1.stop()
        





if __name__ == '__main__':
    main()
