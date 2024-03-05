import sys
import time
from zaber_motion.binary import Connection, Device
from zaber_motion import Units, Library, LogOutputMode

def move_relative(stage_number, microsteps):
    with Connection.open_serial_port("/dev/ttyUSB3") as conn:
        devices = conn.detect_devices()
        if stage_number == 0:
            # 모든 무빙 스테이지에 대해 절대 위치로 이동
            for stage in devices:
                stage.move_relative(microsteps)
            print("Moving all stages to relative position: %d microsteps." % microsteps)
        elif stage_number > 0 and stage_number <= len(devices):
            # 해당 스테이지에 대해 절대 위치로 이동
            stage = devices[stage_number - 1]  # 스테이지 번호는 0부터 시작하지 않으므로 1을 빼줍니다.
            stage.move_relative(microsteps)
            print("Moving stage %d to relative position: %d microsteps." % (stage_number, microsteps))
        else:
            print("Error: Invalid stage number. Stage number should be between 1 and %d." % len(devices))

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 move_rel.py [stage_number] [microsteps]")
        return

    try:
        stage_number = int(sys.argv[1])
        microsteps = int(sys.argv[2])
    except ValueError:
        print("Error: Invalid input")
        return

    move_relative(stage_number, microsteps)

if __name__ == '__main__':
    main()
