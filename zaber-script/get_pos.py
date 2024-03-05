#!/usr/bin/env python3

import sys
import time
from zaber_motion.binary import Connection, Device
from zaber_motion import Library, LogOutputMode

def get_stage_position(stage_number):
    with Connection.open_serial_port("/dev/ttyUSB2") as conn:
        devices = conn.detect_devices()
        if stage_number == 0:
            # 모든 무빙 스테이지에 대해 현재 위치 출력
            for index, stage in enumerate(devices, start=1):
                current_position = stage.get_position()
                print("Current position of stage %d: %d microsteps." % (index, current_position))
        elif stage_number > 0 and stage_number <= len(devices):
            # 해당 스테이지에 대해 현재 위치 출력
            stage = devices[stage_number - 1]  # 스테이지 번호는 0부터 시작하지 않으므로 1을 빼줍니다.
            current_position = stage.get_position()
            print("Current position of stage %d: %d microsteps." % (stage_number, current_position))
        else:
            print("Error: Invalid stage number. Stage number should be between 1 and %d." % len(devices))

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 get_pos.py [stage_number]")
        return

    try:
        stage_number = int(sys.argv[1])
    except ValueError:
        print("Error: Invalid input")
        return

    get_stage_position(stage_number)

if __name__ == '__main__':
    main()
