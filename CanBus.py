import mcp2515
import can
import time



is_found = [False] * 7
data = [0.0] * 15

def index(x):
    if x == 0x6B0:
        return 0
    if x == 0x80001B6E:
        return 5
    if x == 0x8000106E:
        return 4
    if x == 0x8000096E:
        return 1
    if x == 0x80000E6E:
        return 2
    if x == 0x80000F6E:
        return 3
    if x == 0x80003A6E:
        return 6
    return -1

def convert(index_info, can_msg_data):
    global data
    global is_found

    if index_info == 1:
        motor_rpm = int.from_bytes(can_msg_data[0:4], byteorder='big', signed=True)
        motor_ampere = int.from_bytes(can_msg_data[4:6], byteorder='big', signed=True)
        motor_duty_cycle = int.from_bytes(can_msg_data[6:8], byteorder='big', signed=True)

        data[4] = motor_rpm * 1.0
        data[9] = motor_ampere * 0.1
        data[11] = motor_duty_cycle * 0.001

    elif index_info == 4:
        motor_mosfet_temp = int.from_bytes(can_msg_data[0:2], byteorder='big', signed=True)
        motor_temp = int.from_bytes(can_msg_data[2:4], byteorder='big', signed=True)
        motor_input_current = int.from_bytes(can_msg_data[4:6], byteorder='big', signed=True)

        data[7] = motor_mosfet_temp * 0.1
        data[8] = motor_temp * 0.1
        data[10] = motor_input_current * 0.1


def results_print():
    print(f"# {int(time.time())}", end="")
    for i in range(4, 12):
        print(f"#{data[i]}", end="")
    print()

def check_all_data():
    global is_found
    for i in range(1, 7):
        if not is_found[i]:
            return
    is_found = [False] * 7
    results_print()
    time.sleep(0.2)

def main():
    bus = can.interface.Bus(channel='can0', bustype='socketcan')

    print("------- CAN Read ----------")
    print("ID  DLC   DATA")

    global is_found
    is_found = [False] * 7

    while True:
        message = bus.recv()
        index_info = index(message.arbitration_id)

        if index_info != -1:
            is_found[index_info] = True
            convert(index_info, message.data)
            check_all_data()

if __name__ == "__main__":
    main()


