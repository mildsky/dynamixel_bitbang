from DynamixelProtocol2 import *
from XL330_EEPROM import *
from XL330_RAM import *

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

    def ping(self):
        pass

    def read(self):
        pass

    def write(self):
        pass

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
        time.sleep(0.05)
        if not self.InPin == None:
            count, data = self.io.bb_serial_read(self.InPin)
            print(' '.join('%02x'%b for b in data[packet_len:]))
            return data[packet_len:]
        return None

    def close(self):
        if not self.InPin == None:
            self.io.bb_serial_read_close(self.InPin)
        self.io.stop()

def main():
    myDynamixel = xl330(1, 18, 23)
    myDynamixel.sendRecievePacket(INST_PING)
    time.sleep(0.1)
    myDynamixel.sendRecievePacket(INST_WRITE, [ADDR_LED, 0, 1], SIZE_LED+2)
    time.sleep(1)
    myDynamixel.sendRecievePacket(INST_WRITE, [ADDR_LED, 0, 0], SIZE_LED+2)
    time.sleep(1)

    myDynamixel.close()
    exit()

if __name__ == "__main__":
    main()