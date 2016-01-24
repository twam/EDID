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

    # Header information (0-19)

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
            raise TypeError
        if not (manufacturerProductCode >=
                0 and manufacturerProductCode <= 0xFFFF):
            raise ValueError

        self[10:12] = manufacturerProductCode.to_bytes(2, byteorder='little')

    def getManufacturerProductCode(self):
        return int.from_bytes(self[10:12], byteorder='little')

    def setSerialNumber(self, serialNumber):
        if not isinstance(serialNumber, int):
            raise TypeError
        if not (serialNumber >=
                0 and serialNumber <= 0xFFFFFFFF):
            raise ValueError

        self[12:16] = serialNumber.to_bytes(4, byteorder='little')

    def getSerialNumber(self):
        return int.from_bytes(self[12:16], byteorder='little')

    def setWeekOfManufacture(self, weekOfManufacture):
        if not isinstance(weekOfManufacture, int):
            raise TypeError
        if not (weekOfManufacture >=
                0 and weekOfManufacture <= 0xFF):
            raise ValueError

        self[16] = weekOfManufacture

    def getWeekOfManufacture(self):
        return self[16]

    def setYearOfManufacture(self, yearOfManufacture):
        if not isinstance(yearOfManufacture, int):
            raise TypeError
        if not (yearOfManufacture >=
                1990 and yearOfManufacture <= 2245):
            raise ValueError

        self[17] = yearOfManufacture - 1990

    def getYearOfManufacture(self):
        return 1990 + self[17]

    def setEdidVersion(self, edidVersion):
        if not isinstance(edidVersion, int):
            raise TypeError
        if not (edidVersion >=
                0 and edidVersion <= 0xFF):
            raise ValueError

        self[18] = edidVersion

    def getEdidVersion(self):
        return self[18]

    def setEdidRevision(self, edidRevision):
        if not isinstance(edidRevision, int):
            raise TypeError
        if not (edidRevision >=
                0 and edidRevision <= 0xFF):
            raise ValueError

        self[19] = edidRevision

    def getEdidRevision(self):
        return self[19]

    # Basic display parameters (20-24)

    def setVideoInputParametersBitmap(self, videoInputParametersBitmap):
        if not isinstance(videoInputParametersBitmap, int):
            raise TypeError
        if not (videoInputParametersBitmap >=
                0 and videoInputParametersBitmap <= 0xFF):
            raise ValueError

        self[20] = videoInputParametersBitmap

    def getVideoInputParametersBitmap(self):
        return self[20]

    def setMaximumHorizontalImageSize(self, maximumHorizontalImageSize):
        if not isinstance(maximumHorizontalImageSize, int):
            raise TypeError
        if not (maximumHorizontalImageSize >=
                0 and maximumHorizontalImageSize <= 0xFF):
            raise ValueError

        self[21] = maximumHorizontalImageSize

    def getMaximumHorizontalImageSize(self):
        return self[21]

    def setMaximumVerticalImageSize(self, maximumVerticalImageSize):
        if not isinstance(maximumVerticalImageSize, int):
            raise TypeError
        if not (maximumVerticalImageSize >=
                0 and maximumVerticalImageSize <= 0xFF):
            raise ValueError

        self[22] = maximumVerticalImageSize

    def getMaximumVerticalImageSize(self):
        return self[22] * 100

    def setDisplayGamma(self, displayGamma):
        if not isinstance(displayGamma, float):
            raise TypeError
        if not (displayGamma >=
                1.0 and displayGamma <= 3.54):
            raise ValueError

        self[23] = int((displayGamma * 100) - 100)

    def getDisplayGamma(self):
        return (float(self[23]) + 100.0) / 100.0

    def setSupportedFeaturesBitmap(self, supportedFeaturesBitmap):
        if not isinstance(supportedFeaturesBitmap, int):
            raise TypeError
        if not (supportedFeaturesBitmap >=
                0 and supportedFeaturesBitmap <= 0xFF):
            raise ValueError

        self[24] = supportedFeaturesBitmap

    def getSupportedFeaturesBitmap(self):
        return self[24]

    # Chromaticity coordinates (25-34)

    # Established timing bitmap. Supported bitmap for (formerly) very common
    # timing modes (35-37)

    # Standard timing information (38-53)

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

    edid.setWeekOfManufacture(120)
    print(edid.getWeekOfManufacture())

    edid.setYearOfManufacture(2016)
    print(edid.getYearOfManufacture())

    edid.setEdidVersion(1)
    print(edid.getEdidVersion())

    edid.setEdidRevision(3)
    print(edid.getEdidRevision())

    edid.setVideoInputParametersBitmap(0x80)

    edid.calculateChecksum()
    edid.writeToFile('edid.dat')

if __name__ == "__main__":
    main()
