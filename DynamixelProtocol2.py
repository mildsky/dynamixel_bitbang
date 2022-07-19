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

import time
from pigpio import pi, OUTPUT, INPUT, PUD_UP, PUD_DOWN, PUD_OFF

VERSION     = 2.0

INST_PING                   = 0x01
INST_READ                   = 0x02
INST_WRITE                  = 0x03
INST_REG_WRITE              = 0x04
INST_ACTION                 = 0x05
INST_FACTORY_RESET          = 0x06
INST_REBOOT                 = 0x08
INST_CLEAR                  = 0x10
INST_CONTROL_TABLE_BACKUP   = 0x20
INST_STATUS                 = 0x55  # response packet
INST_SYNC_READ              = 0x82
INST_SYNC_WRITE             = 0x83
INST_FAST_SYNC_READ         = 0x8A
INST_BULK_READ              = 0x92
INST_BILK_WRITE             = 0x93
INST_FAST_BULK_READ         = 0x9A

ERROR_RESULT_FAIL           = 0x01
ERROR_INSTRUCTION           = 0x02
ERROR_CRC                   = 0x03
ERROR_DATA_RANGE            = 0x04
ERROR_DATA_LENGTH           = 0x05
ERROR_DATA_LIMIT            = 0x06
ERROR_ACCESS                = 0x07

def crc16(data, length):
    crc_table = [
        0x0000, 0x8005, 0x800F, 0x000A, 0x801B, 0x001E, 0x0014, 0x8011,
        0x8033, 0x0036, 0x003C, 0x8039, 0x0028, 0x802D, 0x8027, 0x0022,
        0x8063, 0x0066, 0x006C, 0x8069, 0x0078, 0x807D, 0x8077, 0x0072,
        0x0050, 0x8055, 0x805F, 0x005A, 0x804B, 0x004E, 0x0044, 0x8041,
        0x80C3, 0x00C6, 0x00CC, 0x80C9, 0x00D8, 0x80DD, 0x80D7, 0x00D2,
        0x00F0, 0x80F5, 0x80FF, 0x00FA, 0x80EB, 0x00EE, 0x00E4, 0x80E1,
        0x00A0, 0x80A5, 0x80AF, 0x00AA, 0x80BB, 0x00BE, 0x00B4, 0x80B1,
        0x8093, 0x0096, 0x009C, 0x8099, 0x0088, 0x808D, 0x8087, 0x0082,
        0x8183, 0x0186, 0x018C, 0x8189, 0x0198, 0x819D, 0x8197, 0x0192,
        0x01B0, 0x81B5, 0x81BF, 0x01BA, 0x81AB, 0x01AE, 0x01A4, 0x81A1,
        0x01E0, 0x81E5, 0x81EF, 0x01EA, 0x81FB, 0x01FE, 0x01F4, 0x81F1,
        0x81D3, 0x01D6, 0x01DC, 0x81D9, 0x01C8, 0x81CD, 0x81C7, 0x01C2,
        0x0140, 0x8145, 0x814F, 0x014A, 0x815B, 0x015E, 0x0154, 0x8151,
        0x8173, 0x0176, 0x017C, 0x8179, 0x0168, 0x816D, 0x8167, 0x0162,
        0x8123, 0x0126, 0x012C, 0x8129, 0x0138, 0x813D, 0x8137, 0x0132,
        0x0110, 0x8115, 0x811F, 0x011A, 0x810B, 0x010E, 0x0104, 0x8101,
        0x8303, 0x0306, 0x030C, 0x8309, 0x0318, 0x831D, 0x8317, 0x0312,
        0x0330, 0x8335, 0x833F, 0x033A, 0x832B, 0x032E, 0x0324, 0x8321,
        0x0360, 0x8365, 0x836F, 0x036A, 0x837B, 0x037E, 0x0374, 0x8371,
        0x8353, 0x0356, 0x035C, 0x8359, 0x0348, 0x834D, 0x8347, 0x0342,
        0x03C0, 0x83C5, 0x83CF, 0x03CA, 0x83DB, 0x03DE, 0x03D4, 0x83D1,
        0x83F3, 0x03F6, 0x03FC, 0x83F9, 0x03E8, 0x83ED, 0x83E7, 0x03E2,
        0x83A3, 0x03A6, 0x03AC, 0x83A9, 0x03B8, 0x83BD, 0x83B7, 0x03B2,
        0x0390, 0x8395, 0x839F, 0x039A, 0x838B, 0x038E, 0x0384, 0x8381,
        0x0280, 0x8285, 0x828F, 0x028A, 0x829B, 0x029E, 0x0294, 0x8291,
        0x82B3, 0x02B6, 0x02BC, 0x82B9, 0x02A8, 0x82AD, 0x82A7, 0x02A2,
        0x82E3, 0x02E6, 0x02EC, 0x82E9, 0x02F8, 0x82FD, 0x82F7, 0x02F2,
        0x02D0, 0x82D5, 0x82DF, 0x02DA, 0x82CB, 0x02CE, 0x02C4, 0x82C1,
        0x8243, 0x0246, 0x024C, 0x8249, 0x0258, 0x825D, 0x8257, 0x0252,
        0x0270, 0x8275, 0x827F, 0x027A, 0x826B, 0x026E, 0x0264, 0x8261,
        0x0220, 0x8225, 0x822F, 0x022A, 0x823B, 0x023E, 0x0234, 0x8231,
        0x8213, 0x0216, 0x021C, 0x8219, 0x0208, 0x820D, 0x8207, 0x0202
    ]
    crc_accum = 0x0000
    for j in range(length):
        i = ((crc_accum >> 8) ^ data[j]) & 0xff
        crc_accum = ((crc_accum << 8) ^ crc_table[i]) & 0xffff
    
    return crc_accum

# Instruction Packet
# +-------+-------+-------+--------+--------+-----+-----+----+------+---+------+-----+-----+
# |Header1|Header2|Header3|Reserved|PacketID|Len_L|Len_H|Inst|Param1|***|ParamN|CRC_L|CRC_H|
# +-------+-------+-------+--------+--------+-----+-----+----+------+---+------+-----+-----+
# Header1   = 0xFF
# Header2   = 0xFF
# Header3   = 0xFD
# Reserved  = 0x00
def generate_packet(id, inst, params=[], params_len=0):
    if not len(params) == params_len:
        raise IndexError
    param_Len_L = (len(params)+3) & 0xff
    param_Len_H = ((len(params)+3) >> 8) & 0xff 
    header = [0xff, 0xff, 0xfd, 0x00]
    txPacket = header + [id, param_Len_L, param_Len_H, inst] + params
    crc_accum = crc16(txPacket, len(txPacket))
    CRC_L = crc_accum & 0xff
    CRC_H = (crc_accum >> 8) & 0xff
    txPacket = txPacket + [CRC_L, CRC_H]
    return txPacket

# Status Packet
# +-------+-------+-------+--------+--------+-----+-----+----+-----+------+---+------+-----+-----+
# |Header1|Header2|Header3|Reserved|PacketID|Len_L|Len_H|Inst|Error|Param1|***|ParamN|CRC_L|CRC_H|
# +-------+-------+-------+--------+--------+-----+-----+----+-----+------+---+------+-----+-----+
# Header1   = 0xFF
# Header2   = 0xFF
# Header3   = 0xFD
# Reserved  = 0x00
# Inst      = 0x55 (status)
def decode_packet(packet, verbose=False):
    packet_wo_CRC = packet[:-2]
    crc_accum = crc16(packet_wo_CRC, len(packet_wo_CRC))
    CRC_L = crc_accum & 0xff
    CRC_H = (crc_accum >> 8) & 0xff
    if not ((CRC_L == packet[-2]) and (CRC_H == packet[-1])):
        print("CRC ERROR")
        return None
    if not packet_wo_CRC[:4] == bytearray([0xff, 0xff, 0xfd, 0x00]):
        print("Header ERROR")
        return None
    packet_wo_CRC_Header = packet_wo_CRC[4:]
    if not packet_wo_CRC_Header[3] == 0x55:
        print("Instruction of Status Packet must 0x55!!!")
        return None
    if not packet_wo_CRC_Header[4] == 0x00:
        print(f"ERROR CODE: {packet_wo_CRC_Header[4]:02x}")
        return packet_wo_CRC_Header[4]
    packet_ID = packet_wo_CRC_Header[0]
    data_length = packet_wo_CRC_Header[1] + (packet_wo_CRC_Header[2] << 8) - 4
    data = packet_wo_CRC_Header[5:]
    if verbose:
        print(f"ID: {packet_ID}, len: {data_length}")
        for i, d in enumerate(data):
            print(f"parameter #{i}: {d:02x}")
    return packet_ID, data, data_length