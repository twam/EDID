#!/usr/bin/env python3

import re


class EDID(bytearray):
    HEADER = bytearray.fromhex('00 FF FF FF FF FF FF 00')

    def __init__(self, data=bytearray(128)):
        self[:] = data

    def calculateChecksum(self):
        val = 0

        for i in self[0:127]:
            val += i

        self[-1] = (256 - (val % 256)) % 256

    def checkChecksum(self):
        val = 0
        for i in self[0:128]:
            val += i

        return val % 256 == 0

    def checkHeader(self):
        return self[0:8] == self.HEADER

    def setHeader(self):
        self[0:8] = self.HEADER

    def setManufacturerID(self, manufacturerID):
        if not isinstance(manufacturerID, str):
            return TypeError
        if not re.match('^[A-Z]{3}$', manufacturerID):
            return ValueError

        raw = (
            (ord(
                manufacturerID[0]) -
                64) << 10) | (
            (ord(
                manufacturerID[1]) -
                64) << 5) | (
                    (ord(
                        manufacturerID[2]) -
                     64) << 0)

        self[8:10] = (raw.to_bytes(2, byteorder='big'))

    def getManufacturerID(self):
        raw = int.from_bytes(self[8:10], byteorder='big')
        return chr(((raw >> 10) & 0x1F) + 64) + \
            chr(((raw >> 5) & 0x1F) + 64) + chr(((raw >> 0) & 0x1F) + 64)

    def setManufacturerProductCode(self, manufacturerProductCode):
        if not isinstance(manufacturerProductCode, int):
            return TypeError
        if not (manufacturerProductCode >=
                0 and manufacturerProductCode <= 0xFFFF):
            return ValueError

        self[10:12] = manufacturerProductCode.to_bytes(2, byteorder='little')

    def getManufacturerProductCode(self):
        return int.from_bytes(self[10:12], byteorder='little')

    def setSerialNumber(self, manufacturerProductCode):
        if not isinstance(manufacturerProductCode, int):
            return TypeError
        if not (manufacturerProductCode >=
                0 and manufacturerProductCode <= 0xFFFFFFFF):
            return ValueError

        self[12:16] = manufacturerProductCode.to_bytes(4, byteorder='little')

    def getSerialNumber(self):
        return int.from_bytes(self[12:16], byteorder='little')

    def writeToFile(self, filename):
        with open(filename, 'wb') as f:
            f.write(self)


def main():
    edid = EDID()

    edid.setHeader()

    edid.setManufacturerID('ABC')
    print(edid.getManufacturerID())

    edid.setManufacturerProductCode(12345)
    print(edid.getManufacturerProductCode())

    edid.setSerialNumber(12345678)
    print(edid.getSerialNumber())

    edid.calculateChecksum()
    edid.writeToFile('edid.dat')

if __name__ == "__main__":
    main()
