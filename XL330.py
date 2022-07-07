from DynamixelProtocol2 import *

# EEPROM Data
ADDR_MODEL_NUM = 0
SIZE_MODEL_NUM = 2
ADDR_MODEL_INFO = 2
SIZE_MODEL_INFO = 4
ADDR_FIRM_VER = 6
SIZE_FIRM_VER = 1
ADDR_ID = 7
ADDR_ID_H = 0
SIZE_ID = 1
ADDR_BAUD_RATE = 8
SIZE_BAUD_RATE = 1
ADDR_RET_DELAY_TIME = 9
SIZE_RET_DELAY_TIME = 1
ADDR_DRIVE_MODE = 10
SIZE_DRIVE_MODE = 1
ADDR_OP_MODE = 11
SIZE_OP_MODE = 1
ADDR_SHADOW_ID = 12
SIZE_SHADOW_ID = 1
ADDR_PROTOCOL_TYPE = 13
SIZE_PROTOCOL_TYPE = 1
ADDR_HOME_OFFSET = 20
SIZE_HOME_OFFSET = 4
ADDR_MOVING_THRESH = 24
SIZE_MOVING_THRESH = 4
ADDR_TEMP_LIMIT = 31
SIZE_TEMP_LIMIT = 1
ADDR_MAX_V_LIMIT = 32
SIZE_MAX_V_LIMIT = 2
ADDR_MIN_V_LIMIT = 34
SIZE_MIN_V_LIMIT = 2
ADDR_PWM_LIMIT = 36
SIZE_PWM_LIMIT = 2
ADDR_CURRENT_LIMIT = 38
SIZE_CURRENT_LIMIT = 2
ADDR_VEL_LIMIT = 44
SIZE_VEL_LIMIT = 4
ADDR_MAX_POS_LIMIT = 48
SIZE_MAX_POS_LIMIT = 4
ADDR_MIN_POS_LIMIT = 52
SIZE_MIN_POS_LIMIT = 4
ADDR_STARTUP_CONF = 60
SIZE_STARTUP_CONF = 1
ADDR_PWM_SLOPE = 62
SIZE_PWM_SLOPE = 1
ADDR_SHUTDOWN = 63
SIZE_SHUTDOWN = 1

# RAM Data
ADDR_TORQ_ENA = 64
SIZE_TORQ_ENA = 1
ADDR_LED = 65
SIZE_LED = 1
ADDR_STAT_RET_LEV = 68
SIZE_STAT_RET_LEV = 1
ADDR_REG_INST = 69
SIZE_REG_INST = 1
ADDR_HW_ERR_STAT = 70
SIZE_HW_ERR_STAT = 1
ADDR_V_I_GAIN = 76
SIZE_V_I_GAIN = 2
ADDR_V_P_GAIN = 78
SIZE_V_P_GAIN = 2
ADDR_POS_D_GAIN = 80
SIZE_POS_D_GAIN = 2
ADDR_POS_I_GAIN = 82
SIZE_POS_I_GAIN = 2
ADDR_POS_P_GAIN = 84
SIZE_POS_P_GAIN = 2
ADDR_FF_SECON_GAIN = 88
SIZE_FF_SECON_GAIN = 2
ADDR_FF_FIRST_GAIN = 90
SIZE_FF_FIRST_GAIN = 2
ADDR_BUS_WATCHDOG = 98
SIZE_BUS_WATCHDOG = 1
ADDR_GOAL_PWM = 100
SIZE_GOAL_PWM = 2
ADDR_GOAL_CURRENT = 102
SIZE_GOAL_CURRENT = 2
ADDR_GOAL_VEL = 104
SIZE_GOAL_VEL = 2
ADDR_PROF_ACCEL = 108
SIZE_PROF_ACCEL = 2
ADDR_PROF_VEL = 112
SIZE_PROF_VEL = 2
ADDR_GOAL_POS = 116
SIZE_GOAL_POS = 4
ADDR_REALTIME_TICK = 120
SIZE_REALTIME_TICK = 2
ADDR_MOVING = 122
SIZE_MOVING = 1
ADDR_MOVING_STAT = 123
SIZE_MOVING_STAT = 1
ADDR_PRESENT_PWM = 124
SIZE_PRESENT_PWM = 2
ADDR_PRESENT_CURRENT = 126
SIZE_PRESENT_CURRNET = 2
ADDR_PRESENT_VEL = 128
SIZE_PRESENT_VEL = 2
ADDR_PRESENT_POS = 132
SIZE_PRESENT_POS = 4
ADDR_VEL_TRAJEC = 136
SIZE_VEL_TRAJEC = 4
ADDR_POS_TRAJEC = 140
SIZE_POS_TRAJEC = 4
ADDR_PRESENT_INPUT_V = 133
SIZE_PRESENT_INPUT_V = 2
ADDR_PRESENT_TEMP = 146
SIZE_PRESENT_TEMP = 1
ADDR_BACKUP_READY = 147
SIZE_BACKUP_READY = 1
# INDIRECT ADDR 1~20
# FROM 168 ~ 206
# EACH 2 BYTE SIZE
# INDIRECT DATA 1~20
# FROM 208 ~ 227
# EACH 1 BYTE SIZE

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