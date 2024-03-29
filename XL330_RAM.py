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

# RAM Data
ADDR_TORQ_ENA = 64
SIZE_TORQ_ENA = 1
ADDR_LED = 65
SIZE_LED = 1
ADDR_STAT_RET_LEV = 68
SIZE_STAT_RET_LEV = 1

ADDR_REG_INST = 69
SIZE_REG_INST = 1
# Registered Instruction
# if 1 -> Instruction registered
# if 0 -> No instruction registerd

ADDR_HW_ERR_STAT = 70
SIZE_HW_ERR_STAT = 1
# HW ERROR Status situations
# Bit 7: 0
# Bit 6: 0
# Bit 5: Overload Error
# Bit 4: Electrical Shock Error
# Bit 3: 
# Bit 2: Overheating Error
# Bit 1: 0
# Bit 0: Input Voltage Error

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