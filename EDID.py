#!/usr/bin/env python3

import re


class EDID(bytearray):
    HEADER = bytearray.fromhex('00 FF FF FF FF FF FF 00')

    def __init__(self, data=None, version=None):
        if data:
            self[:] = data
            return

        self[:] = bytearray(128)
        self.setHeader()

        if version:
            self.setEdidVersion(int(version))
            self.setEdidRevision(int((version-int(version))*10))

        # set all standard timing information to invalid
        for index in range(0, 8):
            self.setStandardTimingInformation(index, None, None, None)

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

    def getVersion(self):
        return float(self.getEdidVersion())+float(self.getEdidRevision())/10.0

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

    def setChromaticityCoordinatesRed(
            self, X, Y):
        if ((not isinstance(X, float)) or (not isinstance(Y, float))):
            return TypeError

        if ((not (X >= 0 and X <= 1.0)) or (not (Y >= 0 and Y <= 1.0))):
            raise ValueError

        Xint = int(round(X * 1024, 0))
        Yint = int(round(Y * 1024, 0))

        self[25] = (((Xint & 0x03) | (Yint & 0x03)) << 4) | (self[25] & 0x0F)

        self[27] = Xint >> 2
        self[28] = Yint >> 2

    def setChromaticityCoordinatesGreen(
            self, X, Y):
        if ((not isinstance(X, float)) or (not isinstance(Y, float))):
            return TypeError

        if ((not (X >= 0 and X <= 1.0)) or (not (Y >= 0 and Y <= 1.0))):
            raise ValueError

        Xint = int(round(X * 1024, 0))
        Yint = int(round(Y * 1024, 0))

        self[25] = (((Xint & 0x03) | (Yint & 0x03)) << 0) | (self[25] & 0xF0)

        self[29] = Xint >> 2
        self[30] = Yint >> 2

    def setChromaticityCoordinatesBlue(
            self, X, Y):
        if ((not isinstance(X, float)) or (not isinstance(Y, float))):
            return TypeError

        if ((not (X >= 0 and X <= 1.0)) or (not (Y >= 0 and Y <= 1.0))):
            raise ValueError

        Xint = int(round(X * 1024, 0))
        Yint = int(round(Y * 1024, 0))

        self[26] = (((Xint & 0x03) | (Yint & 0x03)) << 4) | (self[25] & 0x0F)

        self[31] = Xint >> 2
        self[32] = Yint >> 2

    def setChromaticityCoordinatesWhite(
            self, X, Y):
        if ((not isinstance(X, float)) or (not isinstance(Y, float))):
            return TypeError

        if ((not (X >= 0 and X <= 1.0)) or (not (Y >= 0 and Y <= 1.0))):
            raise ValueError

        Xint = int(round(X * 1024, 0))
        Yint = int(round(Y * 1024, 0))

        self[26] = (((Xint & 0x03) | (Yint & 0x03)) << 0) | (self[25] & 0xF0)

        self[33] = Xint >> 2
        self[34] = Yint >> 2

    def getChromaticityCoordinatesRed(self):
        X = round(((self[27] << 2) | ((self[25] >> 6) & 0x03)) / 1024.0, 3)
        Y = round(((self[28] << 2) | ((self[25] >> 4) & 0x03)) / 1024.0, 3)

        return X, Y

    def getChromaticityCoordinatesGreen(self):
        X = round(((self[29] << 2) | ((self[25] >> 2) & 0x03)) / 1024.0, 3)
        Y = round(((self[30] << 2) | ((self[25] >> 0) & 0x03)) / 1024.0, 3)

        return X, Y

    def getChromaticityCoordinatesBlue(self):
        X = round(((self[31] << 2) | ((self[26] >> 6) & 0x03)) / 1024.0, 3)
        Y = round(((self[32] << 2) | ((self[26] >> 4) & 0x03)) / 1024.0, 3)

        return X, Y

    def getChromaticityCoordinatesWhite(self):
        X = round(((self[33] << 2) | ((self[26] >> 2) & 0x03)) / 1024.0, 3)
        Y = round(((self[34] << 2) | ((self[26] >> 0) & 0x03)) / 1024.0, 3)

        return X, Y

    # Established timing bitmap. Supported bitmap for (formerly) very common
    # timing modes (35-37)

    def setEstablishedTimingBitmap(self, establishedTimingBitmap):
        if not isinstance(establishedTimingBitmap, int):
            raise TypeError
        if not (establishedTimingBitmap >=
                0 and establishedTimingBitmap <= 0xFFFFFF):
            raise ValueError

        self[35:38] = establishedTimingBitmap.to_bytes(3, byteorder='big')

    def getEstablishedTimingBitmap(self):
        return int.from_bytes(self[35:38], byteorder='big')

    # Standard timing information (38-53)

    def setStandardTimingInformation(self, index, resolutionX, ratio, verticalFrequency):
        if (resolutionX == None) and (ratio == None) and (verticalFrequency == None):
            self[38+2*index+0] = 1
            self[38+2*index+1] = 1
            return

        if not isinstance(resolutionX, int):
            raise TypeError
        if not isinstance(ratio, float):
            raise TypeError
        if not isinstance(verticalFrequency, int):
            raise TypeError

        if not (resolutionX >= 256
                and resolutionX <= 2288 and resolutionX % 8 == 0):
            raise ValueError
        if not (verticalFrequency >=
                60 and verticalFrequency <= 123):
            raise ValueError

        self[38+2*index+0] = (resolutionX>>3)-31

        if (ratio == 1.0):
            if (self.getVersion() < 1.3):
                self[38+2*index+1] = 0
            else:
                raise ValueError
        elif (ratio == 16.0/10.0):
            if (self.getVersion() >= 1.3):
                self[38+2*index+1] = 0
            else:
                raise ValueError
        elif (ratio == 4.0/3.0):
            self[38+2*index+1] = 1 << 6
        elif (ratio == 5.0/4.0):
            self[38+2*index+1] = 2 << 6
        elif (ratio == 16.0/9.0):
            self[38+2*index+1] = 3 << 6

        self[38+2*index+1] = self[38+2*index+1] | (verticalFrequency-60)

    def getStandardTimingInformation(self, index):
        # check for invalid entry
        if (self[38+2*index+0] == 1) and (self[38+2*index+1] == 1):
            return None, None, None

        resolutionX = 8*(31+self[38+2*index+0])
        ratioRaw = self[38+2*index+1] >> 6
        if (ratioRaw == 0) and (self.getVersion() < 1.3):
            ratio = 1.0
        elif (ratioRaw == 0):
            ratio = 16.0/10.0
        elif (ratioRaw == 1):
            ratio = 4.0/3.0
        elif (ratioRaw == 2):
            ratio = 5.0/4.0
        elif (ratioRaw == 3):
            ratio = 16.0/9.0
        else:
            ratio = None
        verticalFrequency = 60 + (self[38+2*index+1] & 0x3F)

        return resolutionX, ratio, verticalFrequency

    def setNumberOfExtensions(self, numberOfExtensions):
        if not isinstance(numberOfExtensions, int):
            raise TypeError

        if not (numberOfExtensions >= 0
            and numberOfExtensions <= 0xFF):
            raise ValueError

        self[126] = numberOfExtensions

    def getNumberOfExtensions(self):
        return self[126]

    def writeToFile(self, filename):
        with open(filename, 'wb') as f:
            f.write(self)


def main():
    print(round(0.5, 0))

    edid = EDID(version=1.3)

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

    edid.setDisplayGamma(2.2)

    edid.setStandardTimingInformation(0, 640, 4.0/3.0, 60)

    edid.setVideoInputParametersBitmap(0x80)

    edid.calculateChecksum()
    edid.writeToFile('edid.dat')

if __name__ == "__main__":
    main()
