import unittest
import copy
from edid import Edid, EdidDescriptor


class EdidTests(unittest.TestCase):
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
        '''.replace('\n', ' ').replace('\t', ' ')),

        # Motorola Lapdock
        bytearray.fromhex('''
        00 ff ff ff ff ff ff 00  35 f4 c4 3d 01 00 00 00
        20 14 01 03 80 1a 0e 78  0a fe 75 92 5b 56 91 27
        1f 50 54 00 00 00 01 01  01 01 01 01 01 01 01 01
        01 01 01 01 01 01 20 1c  56 86 50 00 20 30 0e 38
        13 00 00 90 10 00 00 1e  00 00 00 ff 00 30 30 30
        30 30 31 0a 0a 0a 0a 0a  0a 0a 00 00 00 fd 00 32
        4b 1e 55 0f 00 0a 20 20  20 20 20 20 00 00 00 fc
        00 4d 6f 74 6f 41 74 74  61 63 68 0a 20 20 01 02
        02 03 16 71 43 01 03 12  23 09 d7 07 83 01 00 00
        65 03 0c 00 10 00 20 1c  56 86 50 00 20 30 0e 38
        13 00 00 90 10 00 00 1e  7e 1d 56 86 50 00 20 30
        0e 38 13 00 00 90 10 00  00 1e 00 00 00 10 00 1c
        16 20 58 2c 25 00 d7 40  32 00 00 9e 00 00 00 00
        00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
        00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
        00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 1a
        '''.replace('\n', ' ').replace('\t', ' ')),
    ]

    def testCheckChecksumValid(self):
        for data in self.VALID_EDID_DATA:
            edid = Edid(data=data)
            self.assertTrue(edid.checkChecksum())

    def testCheckChecksumInvalid(self):
        edid = Edid(data=self.VALID_EDID_DATA[0])
        edid[127] = 0
        self.assertFalse(edid.checkChecksum())

    def testCalculateChecksum(self):
        edid = Edid(data=bytearray(128))
        # put wrong checksum
        edid[127] = 42

        edid.calculateChecksum()
        self.assertTrue(edid.checkChecksum())
        self.assertEqual(edid[127], 0x00)

    def testCalculateChecksum2(self):
        edid = Edid(data=bytearray(128))
        # change data
        edid[0] = 1

        edid.calculateChecksum()
        self.assertTrue(edid.checkChecksum())
        self.assertEqual(edid[127], 255)

    def testCalculateChecksum3(self):
        edid = Edid(data=bytearray(128))
        for i in range(0, 127):
            edid[i] = 2

        # Databytes: 127 * 2 = 254
        # Checksum: 2
        # Sum: 256 % 256 = 0

        edid.calculateChecksum()
        self.assertTrue(edid.checkChecksum())
        self.assertEqual(edid[127], 2)

    def testCheckHeaderValid(self):
        for data in self.VALID_EDID_DATA:
            edid = Edid(data=data)
            self.assertTrue(edid.checkHeader())

    def testCheckHeaderInvalid(self):
        edid = Edid(data=bytearray(128))
        self.assertFalse(edid.checkHeader())

    def testSetHeader(self):
        edid = Edid(data=bytearray(128))
        edid.initHeader()
        self.assertEqual(edid[0:8],
                         bytearray.fromhex('00 FF FF FF FF FF FF 00'))

    def testSetManufacturerID(self):
        edid = Edid(data=bytearray(128))
        edid.setManufacturerID('SAM')
        self.assertEqual(edid[8:10], bytearray.fromhex('4C 2D'))

    def testGetManufacturerID(self):
        manufacturerIDs = ['SAM', 'FTB', 'APP', 'MOT']
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = Edid(data=data)
            self.assertEqual(edid.getManufacturerID(), manufacturerIDs[key])

    def testSetManufacturerProductCode(self):
        edid = Edid(data=bytearray(128))
        edid.setManufacturerProductCode(956)
        self.assertEqual(edid[10:12], bytearray.fromhex('BC 03'))

    def testGetManufacturerProductCode(self):
        manufacturerProductCodes = [956, 256, 44547, 0x3DC4]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = Edid(data=data)
            self.assertEqual(
                edid.getManufacturerProductCode(),
                manufacturerProductCodes[key])

    def testSetSerialNumber(self):
        edid = Edid(data=bytearray(128))
        edid.setSerialNumber(12345678)
        self.assertEqual(edid[12:16], bytearray.fromhex('4E 61 BC 00'))

    def testGetSerialNumber(self):
        serialNumbers = [0, 16777216, 3471271974, 1]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = Edid(data=data)
            self.assertEqual(edid.getSerialNumber(), serialNumbers[key])

    def testSetWeekOfManufacture(self):
        edid = Edid(data=bytearray(128))
        edid.setWeekOfManufacture(15)
        self.assertEqual(edid[16], 15)

    def testGetWeekOfManufacture(self):
        weekOfManufactures = [47, 12, 12, 32]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = Edid(data=data)
            self.assertEqual(
                edid.getWeekOfManufacture(),
                weekOfManufactures[key])

    def testSetYearOfManufacture(self):
        edid = Edid(data=bytearray(128))
        edid.setYearOfManufacture(2016)
        self.assertEqual(edid[17], 26)

    def testGetYearOfManufacture(self):
        yearOfManufactures = [2007, 2011, 2014, 2010]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = Edid(data=data)
            self.assertEqual(
                edid.getYearOfManufacture(),
                yearOfManufactures[key])

    def testSetEdidVersion(self):
        edid = Edid(data=bytearray(128))
        edid.setEdidVersion(1)
        self.assertEqual(edid[18], 1)

    def testGetEdidVersion(self):
        edidVersions = [1, 1, 1, 1]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = Edid(data=data)
            self.assertEqual(edid.getEdidVersion(), edidVersions[key])

    def testSetEdidRevision(self):
        edid = Edid(data=bytearray(128))
        edid.setEdidRevision(3)
        self.assertEqual(edid[19], 3)

    def testGetEdidRevision(self):
        edidRevisions = [3, 2, 4, 3]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = Edid(data=data)
            self.assertEqual(edid.getEdidRevision(), edidRevisions[key])

    def testGetVersion(self):
        edid = Edid(data=bytearray(128))
        edid.setEdidVersion(1)
        edid.setEdidRevision(3)
        self.assertAlmostEqual(edid.getVersion(), 1.3, places=1)

    def testSetVideoInputParametersBitmap(self):
        edid = Edid(data=bytearray(128))
        edid.setVideoInputParametersBitmap(0x80)
        self.assertEqual(edid[20], 0x80)

    def testGetVideoInputParametersBitmap(self):
        videoInputParametersBitmaps = [0x80, 0x08, 0xB5, 0x80]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = Edid(data=data)
            self.assertEqual(
                edid.getVideoInputParametersBitmap(),
                videoInputParametersBitmaps[key])

    def testSetMaximumHorizontalImageSize(self):
        edid = Edid(data=bytearray(128))
        edid.setMaximumHorizontalImageSize(0x80)
        self.assertEqual(edid[21], 0x80)

    def testGetMaximumHorizontalImageSize(self):
        maximumHorizontalImageSizes = [16, 17, 60, 26]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = Edid(data=data)
            self.assertEqual(
                edid.getMaximumHorizontalImageSize(),
                maximumHorizontalImageSizes[key])

    def testSetMaximumVerticalImageSize(self):
        edid = Edid(data=bytearray(128))
        edid.setMaximumVerticalImageSize(0x80)
        self.assertEqual(edid[22], 0x80)

    def testGetMaximumVerticalImageSize(self):
        maximumVerticalImageSizes = [900, 1300, 3400, 1400]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = Edid(data=data)
            self.assertEqual(
                edid.getMaximumVerticalImageSize(),
                maximumVerticalImageSizes[key])

    def testSetDisplayGamma(self):
        edid = Edid(data=bytearray(128))
        edid.setDisplayGamma(2.2)
        self.assertEqual(edid[23], 120)

    def testGetDisplayGamma(self):
        displayGammas = [2.2, 2.2, 2.2, 2.2]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = Edid(data=data)
            self.assertEqual(edid.getDisplayGamma(), displayGammas[key])

    def testSetSupportedFeaturesBitmap(self):
        edid = Edid(data=bytearray(128))
        edid.setSupportedFeaturesBitmap(10)
        self.assertEqual(edid[24], 10)

    def testGetSupportedFeaturesBitmap(self):
        supportedFeaturesBitmaps = [0x0A, 0x05, 0x22, 0x0A]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = Edid(data=data)
            self.assertEqual(
                edid.getSupportedFeaturesBitmap(),
                supportedFeaturesBitmaps[key])

    def testSetEstablishedTimingBitmap(self):
        edid = Edid(data=bytearray(128))
        edid.setEstablishedTimingBitmap(0x123456)
        self.assertEqual(edid[35:38], bytearray.fromhex('12 34 56'))

    def testGetEstablishedTimingBitmap(self):
        establishedTimingBitmaps = [0x210800, 0x200000, 0, 0]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = Edid(data=data)
            self.assertEqual(
                edid.getEstablishedTimingBitmap(),
                establishedTimingBitmaps[key])

    def testSetChromaticityCoordinatesRed(self):
        edid = Edid(data=bytearray(128))
        edid.setChromaticityCoordinatesRed(0.888, 0.777)
        self.assertEqual(edid[25], 0x10)
        self.assertEqual(edid[27], 0xE3)
        self.assertEqual(edid[28], 0xC7)

    def testSetChromaticityCoordinatesGreen(self):
        edid = Edid(data=bytearray(128))
        edid.setChromaticityCoordinatesGreen(0.888, 0.777)
        self.assertEqual(edid[25], 0x01)
        self.assertEqual(edid[29], 0xE3)
        self.assertEqual(edid[30], 0xC7)

    def testSetChromaticityCoordinatesBlue(self):
        edid = Edid(data=bytearray(128))
        edid.setChromaticityCoordinatesBlue(0.888, 0.777)
        self.assertEqual(edid[26], 0x10)
        self.assertEqual(edid[31], 0xE3)
        self.assertEqual(edid[32], 0xC7)

    def testSetChromaticityCoordinatesWhite(self):
        edid = Edid(data=bytearray(128))
        edid.setChromaticityCoordinatesWhite(0.888, 0.777)
        self.assertEqual(edid[26], 0x01)
        self.assertEqual(edid[33], 0xE3)
        self.assertEqual(edid[34], 0xC7)

    def testGetChromaticityCoordinatesRed(self):
        chromaticityCoordinatesReds = [
            (0.640, 0.330), (0.0, 0.0), (0.655, 0.332), (0.573, 0.358)]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = Edid(data=data)
            coordinates = edid.getChromaticityCoordinatesRed()
            self.assertAlmostEqual(
                coordinates[0],
                chromaticityCoordinatesReds[key][0], places=3)
            self.assertAlmostEqual(
                coordinates[1],
                chromaticityCoordinatesReds[key][1], places=3)

    def testGetChromaticityCoordinatesGreen(self):
        chromaticityCoordinatesGreen = [
            (0.300, 0.600), (0.0, 0.0), (0.295, 0.625), (0.339, 0.568)]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = Edid(data=data)
            coordinates = edid.getChromaticityCoordinatesGreen()
            self.assertAlmostEqual(
                coordinates[0],
                chromaticityCoordinatesGreen[key][0], places=3)
            self.assertAlmostEqual(
                coordinates[1],
                chromaticityCoordinatesGreen[key][1], places=3)

    def testGetChromaticityCoordinatesBlue(self):
        chromaticityCoordinatesBlues = [
            (0.150, 0.060), (0.0, 0.0), (0.148, 0.047), (0.153, 0.124)]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = Edid(data=data)
            coordinates = edid.getChromaticityCoordinatesBlue()
            self.assertAlmostEqual(
                coordinates[0],
                chromaticityCoordinatesBlues[key][0], places=3)
            self.assertAlmostEqual(
                coordinates[1],
                chromaticityCoordinatesBlues[key][1], places=3)

    def testGetChromaticityCoordinatesWhite(self):
        chromaticityCoordinatesWhites = [
            (0.312, 0.329), (0.0, 0.0), (0.313, 0.329), (0.313, 0.329)]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = Edid(data=data)
            coordinates = edid.getChromaticityCoordinatesWhite()
            self.assertAlmostEqual(
                coordinates[0],
                chromaticityCoordinatesWhites[key][0], places=3)
            self.assertAlmostEqual(
                coordinates[1],
                chromaticityCoordinatesWhites[key][1], places=3)

    def testSetStandardTimingInformation(self):
        for index in range(0, 8):
            edid = Edid(version=1.2)
            edid.setStandardTimingInformation(index, 640, 1.0, 70)
            self.assertEqual(edid[38 + 2 * index + 0], 49)
            self.assertEqual(edid[38 + 2 * index + 1], 10)

            edid = Edid(version=1.3)
            edid.setStandardTimingInformation(index, None, None, None)
            self.assertEqual(edid[38 + 2 * index + 0], 1)
            self.assertEqual(edid[38 + 2 * index + 1], 1)

            edid = Edid(version=1.3)
            edid.setStandardTimingInformation(index, 256, 16.0 / 10.0, 80)
            self.assertEqual(edid[38 + 2 * index + 0], 1)
            self.assertEqual(edid[38 + 2 * index + 1], 20)

            edid = Edid(version=1.3)
            edid.setStandardTimingInformation(index, 1024, 4.0 / 3.0, 90)
            self.assertEqual(edid[38 + 2 * index + 0], 97)
            self.assertEqual(edid[38 + 2 * index + 1], 94)

            edid = Edid(version=1.3)
            edid.setStandardTimingInformation(index, 1600, 5.0 / 4.0, 100)
            self.assertEqual(edid[38 + 2 * index + 0], 169)
            self.assertEqual(edid[38 + 2 * index + 1], 168)

            edid = Edid(version=1.3)
            edid.setStandardTimingInformation(index, 1920, 16.0 / 9.0, 120)
            self.assertEqual(edid[38 + 2 * index + 0], 209)
            self.assertEqual(edid[38 + 2 * index + 1], 252)

    def testGetStandardTimingInformation(self):
        standardTimingInformations = [
            [(1280, 5.0 / 4.0, 60), (1600, 4.0 / 3.0, 60)],
            [(640, 4.0 / 3.0, 60)],
            [],
            []
        ]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = Edid(data=data)
            for index in range(0, 8):
                standardTimingInformation = edid.getStandardTimingInformation(
                    index)
                correctStandardTimingInformation = standardTimingInformations[key][
                    index] if index < len(standardTimingInformations[key]) else (None, None, None)

                self.assertEqual(
                    standardTimingInformation[0],
                    correctStandardTimingInformation[0])
                self.assertEqual(
                    standardTimingInformation[1],
                    correctStandardTimingInformation[1])
                self.assertEqual(
                    standardTimingInformation[2],
                    correctStandardTimingInformation[2])

    def testSetNumberOfExtensions(self):
        edid = Edid(version=1.3)
        edid.setNumberOfExtensions(2)
        self.assertEqual(edid[126], 2)

    def testGetNumberOfExtensions(self):
        numberOfExtensions = [1, 0, 2, 1]
        for key, data in enumerate(self.VALID_EDID_DATA):
            edid = Edid(data=data)
            self.assertEqual(
                edid.getNumberOfExtensions(),
                numberOfExtensions[key])


class EdidDescriptorTests(unittest.TestCase):
    OFFSET = 10
    SIZE = 18

    def setUp(self):
        self.parent = bytearray(self.OFFSET + self.SIZE + 5)
        for i in range(0, len(self.parent)):
            self.parent[i] = i

        self.edidDescriptor = EdidDescriptor(self.parent, self.OFFSET)

    def testGetItemIntKeyPositive(self):
        for i in range(0, self.SIZE):
            self.assertEqual(self.edidDescriptor[i], i + self.OFFSET)

    def testGetItemIntKeyPositiveOutOfRange(self):
        with self.assertRaises(IndexError):
            self.edidDescriptor[self.SIZE]

    def testGetItemIntKeyNegative(self):
        for i in range(-self.SIZE, -1):
            self.assertEqual(
                self.edidDescriptor[i],
                i + self.OFFSET + self.SIZE)

    def testGetItemIntKeyNegativeOutOfRange(self):
        with self.assertRaises(IndexError):
            self.edidDescriptor[-self.SIZE - 1]

    def testGetItemSliceKeyPositive(self):
        self.assertEqual(
            self.edidDescriptor[
                1:self.SIZE -
                1],
            bytearray(
                [
                    i for i in range(
                        self.OFFSET +
                        1,
                        self.OFFSET +
                        self.SIZE -
                        1)]))

    def testGetItemSliceKeyPositiveOnlyStart(self):
        self.assertEqual(self.edidDescriptor[1:], bytearray(
            [i for i in range(self.OFFSET + 1, self.OFFSET + self.SIZE)]))

    def testGetItemSliceKeyPositiveOnlyEnd(self):
        self.assertEqual(self.edidDescriptor[:self.SIZE - 1], bytearray(
            [i for i in range(self.OFFSET, self.OFFSET + self.SIZE - 1)]))

    def testGetItemSliceKeyPositiveOutOfRange(self):
        self.assertEqual(self.edidDescriptor[
                         0:self.SIZE + 1], bytearray([i for i in range(self.OFFSET, self.OFFSET + self.SIZE)]))

    def testGetItemSliceKeyMixed(self):
        self.assertEqual(self.edidDescriptor[
                         1:-1], bytearray([i for i in range(self.OFFSET + 1, self.OFFSET + self.SIZE - 1)]))

    def testGetItemSliceKeyNegative(self):
        self.assertEqual(self.edidDescriptor[-self.SIZE + 1:-1], bytearray(
            [i for i in range(self.OFFSET + 1, self.OFFSET + self.SIZE - 1)]))

    def testGetItemSliceKeyNegativeOutOfRange(self):
        self.assertEqual(self.edidDescriptor[-self.SIZE - 1:-1], bytearray(
            [i for i in range(self.OFFSET, self.OFFSET + self.SIZE - 1)]))

    def testSetItemIntKeyPositive(self):
        for i in range(0, self.SIZE):
            self.edidDescriptor[i] = i
            self.assertEqual(self.parent[i + self.OFFSET], i)

    def testSetItemIntKeyNegative(self):
        for i in range(-self.SIZE, -1):
            self.edidDescriptor[i] = -i
            self.assertEqual(self.parent[i + self.OFFSET + self.SIZE], -i)

    def testGetHeader(self):
        self.parent[self.OFFSET + 0] = 1
        self.parent[self.OFFSET + 1] = 2
        self.assertEqual(
            self.edidDescriptor.getHeader(),
            bytearray.fromhex('01 02'))
