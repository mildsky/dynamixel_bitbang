# Copyright 2022 Lee Jun jun8572@kaist.ac.kr
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from Dynamixel import *
from DynamixelProtocol2 import *
from XL330_EEPROM import *
from XL330_RAM import *
from utils import IntToNBytes, nBytesToInt

def main():
    motors = []
    for i in range(6):
        motors.append(dynamixel(i+1, 18))
    
    for motor in motors:
        motor.write(ADDR_LED, SIZE_LED, 1)
 
    motors[0].write(ADDR_OP_MODE, SIZE_OP_MODE, 4)
    motors[1].write(ADDR_OP_MODE, SIZE_OP_MODE, 4)
    motors[2].write(ADDR_OP_MODE, SIZE_OP_MODE, 4)

    motors[0].write(ADDR_TORQ_ENA, SIZE_TORQ_ENA, 1)
    motors[1].write(ADDR_TORQ_ENA, SIZE_TORQ_ENA, 1)
    motors[2].write(ADDR_TORQ_ENA, SIZE_TORQ_ENA, 1)

    motors[0].write(ADDR_GOAL_POS, SIZE_GOAL_POS, 8196)
    # time.sleep(3)
    motors[1].write(ADDR_GOAL_POS, SIZE_GOAL_POS, 8196)
    # time.sleep(3)
    motors[2].write(ADDR_GOAL_POS, SIZE_GOAL_POS, 8196)
    time.sleep(3)
    motors[0].write(ADDR_GOAL_POS, SIZE_GOAL_POS, 0)
    # time.sleep(3)
    motors[1].write(ADDR_GOAL_POS, SIZE_GOAL_POS, 0)
    # time.sleep(3)
    motors[2].write(ADDR_GOAL_POS, SIZE_GOAL_POS, 0)
    time.sleep(3)

    motors[0].write(ADDR_TORQ_ENA, SIZE_TORQ_ENA, 0)
    motors[1].write(ADDR_TORQ_ENA, SIZE_TORQ_ENA, 0)
    motors[2].write(ADDR_TORQ_ENA, SIZE_TORQ_ENA, 0)
    
    motors[0].write(ADDR_OP_MODE, SIZE_OP_MODE, 3)
    motors[1].write(ADDR_OP_MODE, SIZE_OP_MODE, 3)
    motors[2].write(ADDR_OP_MODE, SIZE_OP_MODE, 3)
    
    for motor in motors:
        motor.write(ADDR_LED, SIZE_LED, 0)   

    for motor in motors:
        motor.close()




if __name__ == "__main__":
    main()