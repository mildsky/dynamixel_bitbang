def IntToNBytes(number, length):
    ret = []
    number = int(number)
    for i in range(length):
        ret.append(number & 0xff)
        number = number >> 8
    return ret

def nBytesToInt(bytes, length):
    ret = 0
    for i in range(length):
        ret += bytes[i] << (8*i)
    return ret