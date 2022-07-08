def toNBytes(number, length):
    ret = []
    for i in range(length):
        ret.append(number & 0xff)
        number = number >> 8
    return ret
    