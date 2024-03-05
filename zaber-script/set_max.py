import sys
from zaber_motion.binary import Connection
from zaber_motion.binary import binary_settings

def set_max_position(stage_number, max_position):
    with Connection.open_serial_port("/dev/ttyUSB2") as conn:
        devices = conn.detect_devices()
        if stage_number == 0:
            # 모든 무빙 스테이지에 대해 maximum position 설정
            for stage in devices:
                stage.settings.set(binary_settings.BinarySettings.MAXIMUM_POSITION, max_position)
            print("Setting maximum position for all stages to %d." % max_position)
        elif stage_number > 0 and stage_number <= len(devices):
            # 해당 스테이지에 대해 maximum position 설정
            stage = devices[stage_number - 1]  # 스테이지 번호는 0부터 시작하지 않으므로 1을 빼줍니다.
            stage.settings.set(binary_settings.BinarySettings.MAXIMUM_POSITION, max_position)
            print("Setting maximum position for stage %d to %d." % (stage_number, max_position))
        else:
            print("Error: Invalid stage number. Stage number should be between 1 and %d." % len(devices))

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 set_max.py [stage_number] [max_position]")
        return

    try:
        stage_number = int(sys.argv[1])
        max_position = int(sys.argv[2])
    except ValueError:
        print("Error: Invalid input")
        return

    set_max_position(stage_number, max_position)

if __name__ == '__main__':
    main()
