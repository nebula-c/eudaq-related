#!/usr/bin/env python3

import sys
from multiprocessing import Process
from zaber_motion.binary import Connection

def move_to_home(stage_number):
    with Connection.open_serial_port("/dev/ttyUSB2") as conn:
        devices = conn.detect_devices()
        if stage_number == 0:
            # 모든 무빙 스테이지에 대해 홈 위치로 이동
            for stage in devices:
                stage.home()
            print("Moving all stages to home position.")
        elif stage_number > 0 and stage_number <= len(devices):
            # 해당 스테이지에 대해 홈 위치로 이동
            stage = devices[stage_number - 1]  # 스테이지 번호는 0부터 시작하지 않으므로 1을 빼줍니다.
            stage.home()
            print("Moving stage %d to home position." % stage_number)
        else:
            print("Error: Invalid stage number. Stage number should be between 1 and %d." % len(devices))

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 move_to_home.py [stage_number]")
        return

    try:
        stage_number = int(sys.argv[1])
    except ValueError:
        print("Error: Invalid input")
        return

    move_to_home(stage_number)

if __name__ == '__main__':
    main()
