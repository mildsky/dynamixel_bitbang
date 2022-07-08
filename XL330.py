from DynamixelProtocol2 import *
from XL330_EEPROM import *
from XL330_RAM import *
from utils import IntToNBytes, nBytesToInt
import math

class xl330:
    def __init__(self, id, outputPin, inputPin, baud = 57600):
        self.ID = id
        self.io = pi()
        self.OutPin = outputPin
        self.InPin = inputPin
        self.BAUD = baud
        self.io.set_mode(self.OutPin, 1) # 1 is output
        if not self.InPin == None:
            self.io.set_mode(self.InPin, 0) # 0 is input
            self.io.set_pull_up_down(self.InPin, 2) # 2 is internal pull up
            self.io.bb_serial_read_open(self.InPin, self.BAUD)

    def close(self):
        if not self.InPin == None:
            self.io.bb_serial_read_close(self.InPin)
        self.io.stop()

    def sendRecievePacket(self, inst, params=[], params_len=0):
        self.io.wave_clear()
        packet = generate_packet(self.ID, inst, params, params_len)
        packet_len = len(packet)
        self.io.wave_add_serial(
            self.OutPin, 
            self.BAUD,
            packet)
        wid = self.io.wave_create()
        self.io.wave_send_once(wid)
        time.sleep(0.00075*packet_len)
        if not self.InPin == None:
            _, data = self.io.bb_serial_read(self.InPin)
            # print(' '.join('%02x'%b for b in data[packet_len:]))
            return data[packet_len:]
        return None

    def ping(self):
        if self.InPin == None:
            print("You Cannot Ping without Input")
            return None, None, None
        rxPacket = self.sendRecievePacket(INST_PING)
        if not len(rxPacket) == 14:
            print("No RX Packet recieved!!")
            return None, None, None
        id, data, data_len = decode_packet(rxPacket)
        if not data_len == 3:
            print("data length not 3")
        print(f"ID: {id}")
        modelNum = data[0]+(data[1]<<8)
        print(f"Model#: {modelNum}")
        print(f"firmware Ver.: {data[2]}")
        return id, modelNum, data[2]

    def read(self, addr, data_len):
        if not self.InPin == None:
            rxPacket = self.sendRecievePacket(INST_READ, IntToNBytes(addr, 2) + IntToNBytes(data_len, 2), 4)
            if not len(rxPacket) >= 11+data_len:
                print("No RX Packet recieved!!")
                return bytearray(data_len)
            return decode_packet(rxPacket)[1]
        return bytearray(data_len)

    def write(self, addr, data_len, data):
        rxPacket = self.sendRecievePacket(INST_WRITE, IntToNBytes(addr, 2) + IntToNBytes(data, data_len), data_len+2)
        return rxPacket

    def reg_write(self):
        pass

    def action(self):
        pass

def main():
    motor = xl330(1, 18, 23)
    motor.ping()
    motor.write(ADDR_LED, SIZE_LED, 1)
    motor.write(ADDR_TORQ_ENA, SIZE_TORQ_ENA, 1)
    T = 200
    for i in range(T+1):
        motor.write(ADDR_GOAL_POS, SIZE_GOAL_POS, 2048+1024*math.sin(2*i/T*math.pi))
        time.sleep(0.01)
    time.sleep(0.1)
    motor.write(ADDR_TORQ_ENA, SIZE_TORQ_ENA, 0)
    motor.write(ADDR_LED, SIZE_LED, 0)
    data = motor.read(ADDR_PRESENT_TEMP, SIZE_PRESENT_TEMP)
    print(f"current temperature: {nBytesToInt(data, 1)}°C")
    motor.close()
    exit()

if __name__ == "__main__":
    main()