import unittest
import copy
import EDID


class EDIDTests(unittest.TestCase):
    VALID_EDID_DATA = [
        # http://kodi.wiki/view/Creating_and_using_edid.bin_via_xorg.conf
        bytearray.fromhex('''
		00 ff ff ff ff ff ff 00  4c 2d bc 03 00 00 00 00
		2f 11 01 03 80 10 09 78  0a ee 91 a3 54 4c 99 26
		0f 50 54 21 08 00 81 80  a9 40 01 01 01 01 01 01
		01 01 01 01 01 01 02 3a  80 18 71 38 2d 40 58 2c
		45 00 a0 5a 00 00 00 1e  66 21 50 b0 51 00 1b 30
		40 70 36 00 a0 5a 00 00  00 1e 00 00 00 fd 00 17
		3d 1a 4c 17 00 0a 20 20  20 20 20 20 00 00 00 fc
		00 53 41 4d 53 55 4e 47  0a 20 20 20 20 20 01 d3
		02 03 27 f1 4b 90 1f 04  13 05 14 03 12 20 21 22
		23 09 07 07 83 01 00 00  e2 00 0f e3 05 03 01 67
		03 0c 00 20 00 b8 2d 01  1d 00 72 51 d0 1e 20 6e
		28 55 00 a0 5a 00 00 00  1e 01 1d 00 bc 52 d0 1e
		20 b8 28 55 40 a0 5a 00  00 00 1e 01 1d 80 18 71
		1c 16 20 58 2c 25 00 a0  5a 00 00 00 9e 01 1d 80
		d0 72 1c 16 20 10 2c 25  80 a0 5a 00 00 00 9e 00
		00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 0d
		'''.replace('\n', ' ').replace('\t', ' ')),

        # http://flipthatbit.net/2011/04/ddc2-interface-crafting-your-own-edid/
        bytearray.fromhex('''
        00 FF FF FF FF FF FF 00  1A 82 00 01 00 00 00 01
        0C 15 01 02 08 11 0D 78  05 00 00 00 00 00 00 00
        00 00 00 20 00 00 31 40  01 01 01 01 01 01 01 01
        01 01 01 01 01 01 00 00  00 FC 00 66 6C 69 70 74
        68 61 74 62 69 74 30 31  00 00 00 00 00 00 00 00
        00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
        00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
        00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 0A
        '''.replace('\n', ' ').replace('\t', ' ')),

        # iMac (Retina 5K, 27-inch, Late 2014)
        bytearray.fromhex('''
        00 ff ff ff ff ff ff 00  06 10 03 ae 26 68 e7 ce
        0c 18 01 04 b5 3c 22 78  22 c8 05 a7 55 4b a0 26
        0c 50 54 00 00 00 01 01  01 01 01 01 01 01 01 01
        01 01 01 01 01 01 00 00  00 10 00 00 00 00 00 00
        00 00 00 00 00 00 00 00  00 00 00 10 00 00 00 00
        00 00 00 00 00 00 00 00  00 00 00 00 00 fc 00 69
        4d 61 63 0a 20 20 20 20  20 20 20 20 00 00 00 00
        00 00 00 00 00 00 00 00  00 00 00 00 00 00 02 ea
        02 03 1e 81 70 fa 10 00  00 12 7a 31 fc 78 bd cc
        02 90 88 51 d3 68 fa 10  00 f5 f9 fa ff ff 00 00
        00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
        00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
        00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
        00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
        00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
        00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 92
        70 13 79 03 00 03 00 14  80 6e 01 84 ff 13 9f 00
        2f 80 1f 00 3f 0b 51 00  02 00 04 00 00 00 00 00
        00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
        00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
        00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
        00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
        00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
        00 00 00 00 00 00 00 00  00 00 00 00 00 00 c7 90
        '''.replace('\n', ' ').replace('\t', ' '))
    ]

    def testCheckChecksumValid(self):
        for data in self.VALID_EDID_DATA:
            edid = EDID.EDID(data=data)
            self.assertTrue(edid.checkChecksum())

    def testCheckChecksumInvalid(self):
        edid = EDID.EDID(data=self.VALID_EDID_DATA[0])
        edid[127] = 0
        self.assertFalse(edid.checkChecksum())

    def testCalculateChecksum(self):
        edid = EDID.EDID(data=bytearray(128))
        edid[-1] = 42

        edid.calculateChecksum()
        self.assertEqual(edid[127], 0x00)

    def testCalculateChecksum2(self):
        edid = EDID.EDID(data=bytearray(128))
        edid[0] = 1

        edid.calculateChecksum()
        self.assertEqual(edid[127], 255)

    def testCheckHeaderValid(self):
        for data in self.VALID_EDID_DATA:
            edid = EDID.EDID(data=data)
            self.assertTrue(edid.checkHeader())

    def testCheckHeaderInvalid(self):
        edid = EDID.EDID(data=bytearray(128))
        self.assertFalse(edid.checkHeader())

    def testSetHeader(self):
        edid = EDID.EDID(data=bytearray(128))
        edid.setHeader()
        self.assertEqual(edid[0:8],
                         bytearray.fromhex('00 FF FF FF FF FF FF 00'))

    def testSetManufacturerID(self):
        edid = EDID.EDID(data=bytearray(128))
        edid.setManufacturerID('SAM')
        self.assertEqual(edid[8:10], bytearray.fromhex('4C 2D'))

    def testGetManufacturerID(self):
        manufacturerIDs = ['SAM', 'FTB', 'APP']
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = EDID.EDID(data=data)
            self.assertEqual(edid.getManufacturerID(), manufacturerIDs[key])

    def testSetManufacturerProductCode(self):
        edid = EDID.EDID(data=bytearray(128))
        edid.setManufacturerProductCode(956)
        self.assertEqual(edid[10:12], bytearray.fromhex('BC 03'))

    def testGetManufacturerProductCode(self):
        manufacturerProductCodes = [956, 256, 44547]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = EDID.EDID(data=data)
            self.assertEqual(
                edid.getManufacturerProductCode(),
                manufacturerProductCodes[key])

    def testSetSerialNumber(self):
        edid = EDID.EDID(data=bytearray(128))
        edid.setSerialNumber(12345678)
        self.assertEqual(edid[12:16], bytearray.fromhex('4E 61 BC 00'))

    def testGetSerialNumber(self):
        serialNumbers = [0, 16777216, 3471271974]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = EDID.EDID(data=data)
            self.assertEqual(edid.getSerialNumber(), serialNumbers[key])

    def testSetWeekOfManufacture(self):
        edid = EDID.EDID(data=bytearray(128))
        edid.setWeekOfManufacture(15)
        self.assertEqual(edid[16], 15)

    def testGetWeekOfManufacture(self):
        weekOfManufactures = [47, 12, 12]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = EDID.EDID(data=data)
            self.assertEqual(
                edid.getWeekOfManufacture(),
                weekOfManufactures[key])

    def testSetYearOfManufacture(self):
        edid = EDID.EDID(data=bytearray(128))
        edid.setYearOfManufacture(2016)
        self.assertEqual(edid[17], 26)

    def testGetYearOfManufacture(self):
        yearOfManufactures = [2007, 2011, 2014]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = EDID.EDID(data=data)
            self.assertEqual(
                edid.getYearOfManufacture(),
                yearOfManufactures[key])

    def testSetEdidVersion(self):
        edid = EDID.EDID(data=bytearray(128))
        edid.setEdidVersion(1)
        self.assertEqual(edid[18], 1)

    def testGetEdidVersion(self):
        edidVersions = [1, 1, 1]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = EDID.EDID(data=data)
            self.assertEqual(edid.getEdidVersion(), edidVersions[key])

    def testSetEdidRevision(self):
        edid = EDID.EDID(data=bytearray(128))
        edid.setEdidRevision(3)
        self.assertEqual(edid[19], 3)

    def testGetEdidRevision(self):
        edidRevisions = [3, 2, 4]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = EDID.EDID(data=data)
            self.assertEqual(edid.getEdidRevision(), edidRevisions[key])

    def testSetVideoInputParametersBitmap(self):
        edid = EDID.EDID(data=bytearray(128))
        edid.setVideoInputParametersBitmap(0x80)
        self.assertEqual(edid[20], 0x80)

    def testGetVideoInputParametersBitmap(self):
        videoInputParametersBitmaps = [0x80, 0x08, 0xB5]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = EDID.EDID(data=data)
            self.assertEqual(
                edid.getVideoInputParametersBitmap(),
                videoInputParametersBitmaps[key])

    def testSetMaximumHorizontalImageSize(self):
        edid = EDID.EDID(data=bytearray(128))
        edid.setMaximumHorizontalImageSize(0x80)
        self.assertEqual(edid[21], 0x80)

    def testGetMaximumHorizontalImageSize(self):
        maximumHorizontalImageSizes = [16, 17, 60]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = EDID.EDID(data=data)
            self.assertEqual(
                edid.getMaximumHorizontalImageSize(),
                maximumHorizontalImageSizes[key])

    def testSetMaximumVerticalImageSize(self):
        edid = EDID.EDID(data=bytearray(128))
        edid.setMaximumVerticalImageSize(0x80)
        self.assertEqual(edid[22], 0x80)

    def testGetMaximumVerticalImageSize(self):
        maximumVerticalImageSizes = [900, 1300, 3400]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = EDID.EDID(data=data)
            self.assertEqual(
                edid.getMaximumVerticalImageSize(),
                maximumVerticalImageSizes[key])

    def testSetDisplayGamma(self):
        edid = EDID.EDID(data=bytearray(128))
        edid.setDisplayGamma(2.2)
        self.assertEqual(edid[23], 120)

    def testGetDisplayGamma(self):
        displayGammas = [2.2, 2.2, 2.2]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = EDID.EDID(data=data)
            self.assertEqual(edid.getDisplayGamma(), displayGammas[key])

    def testSetSupportedFeaturesBitmap(self):
        edid = EDID.EDID(data=bytearray(128))
        edid.setSupportedFeaturesBitmap(10)
        self.assertEqual(edid[24], 10)

    def testGetSupportedFeaturesBitmap(self):
        supportedFeaturesBitmaps = [0x0A, 0x05, 0x22]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = EDID.EDID(data=data)
            self.assertEqual(
                edid.getSupportedFeaturesBitmap(),
                supportedFeaturesBitmaps[key])
