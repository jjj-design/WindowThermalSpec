import nbimporter
import unittest
import csv
import sys
import math

sys.path.append('../')
from module import sun_position

TEST_DIRECTORY = './test/test_case/'

class TestCalcNDayNHourFunction(unittest.TestCase):
    
    # 正しい値が返ってくるかどうかのテスト    
    def test_assert(self):
        f = open(TEST_DIRECTORY + 'NDayNHour.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [float(d) for d in row]
            Hour00, NdayA, NhourA = tuple(row_float)
            with self.subTest(Hour00 = Hour00):
                actual = sun_position.calc_NDayNHour(Hour00)
                expected = (NdayA, NhourA)
                self.assertAlmostEqual(actual[0], expected[0], delta=0.000000001)
                self.assertAlmostEqual(actual[1], expected[1], delta=0.000000001)

class TestCalcTTFunction(unittest.TestCase):
    
    # 正しい値が返ってくるかどうかのテスト    
    def test_assert(self):
        NDT = 6
        for NHour in range(0,24):
            for MM in range(0,NDT):
                actual = sun_position.calc_TT(NHour, NDT, MM)
                expected = NHour + MM / 6
                self.assertAlmostEqual(actual, expected, delta=0.000000001)

class TestCalcDeltadFunction(unittest.TestCase):
    
    # 正しい値が返ってくるかどうかのテスト    
    def test_assert(self):

        f = open(TEST_DIRECTORY + 'deltad.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [float(d) for d in row]
            case, NDay, deltadA = tuple(row_float)
            with self.subTest(case = case):
                actual = math.degrees(sun_position.calc_deltad(NDay))
                expected = deltadA
                self.assertAlmostEqual(actual, expected, delta=0.000000001)

class TestCalcEedFunction(unittest.TestCase):
    
    # 正しい値が返ってくるかどうかのテスト
    def test_assert(self):
        
        f = open(TEST_DIRECTORY + 'eed.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [float(d) for d in row]
            case, NDay, eedA = tuple(row_float)
            with self.subTest(case = case):
                actual = sun_position.calc_eed(NDay)
                expected = eedA
                self.assertAlmostEqual(actual, expected, delta=0.000000001)

class TestCalcTdtFunction(unittest.TestCase):

    # 正しい値が返ってくるかどうかのテスト
    def test_assert(self):
    
        f = open(TEST_DIRECTORY + 'Tdt.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [float(d) for d in row]
            case, Longitude, NDay, TT, TdtA = tuple(row_float)
            with self.subTest(case = case):
                actual = math.degrees(sun_position.calc_Tdt(math.radians(Longitude),
                                                            sun_position.calc_eed(NDay),
                                                            TT,
                                                            math.radians(135.0)))
                expected = TdtA
                self.assertAlmostEqual(actual, expected, delta=0.000000001)

class TestCalcSinhFunction(unittest.TestCase):

    # 正しい値が返ってくるかどうかのテスト
    def test_assert(self):
    
        f = open(TEST_DIRECTORY + 'sinh.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [float(d) for d in row]
            case, Latitude, Longitude, NDay, TT, sinhA = tuple(row_float)
            with self.subTest(case = case):
                actual = sun_position.calc_hs(math.radians(Latitude),
                                              sun_position.calc_deltad(NDay),
                                              sun_position.calc_Tdt(math.radians(Longitude),
                                                                    sun_position.calc_eed(NDay),
                                                                    TT,
                                                                    math.radians(135.0)
                                                                    )
                                              )[1]
                expected = sinhA
                self.assertAlmostEqual(actual, expected, delta=0.000000001)

class TestCalcCoshFunction(unittest.TestCase):

    # 正しい値が返ってくるかどうかのテスト
    def test_assert(self):
    
        f = open(TEST_DIRECTORY + 'cosh.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [float(d) for d in row]
            case, Latitude, Longitude, NDay, TT, coshA = tuple(row_float)
            with self.subTest(case = case):
                actual = sun_position.calc_hs(math.radians(Latitude),
                                              sun_position.calc_deltad(NDay),
                                              sun_position.calc_Tdt(math.radians(Longitude),
                                                                    sun_position.calc_eed(NDay),
                                                                    TT,
                                                                    math.radians(135.0)
                                                                    )
                                              )[2]
                expected = coshA
                self.assertAlmostEqual(actual, expected, delta=0.000000001)

class TestCalcHsdtAFunction(unittest.TestCase):

    # 正しい値が返ってくるかどうかのテスト
    def test_assert(self):
    
        f = open(TEST_DIRECTORY + 'hsdt.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [float(d) for d in row]
            case, Latitude, Longitude, NDay, TT, hsdtA = tuple(row_float)
            with self.subTest(case = case):
                hs = sun_position.calc_hs(math.radians(Latitude),
                                          sun_position.calc_deltad(NDay),
                                          sun_position.calc_Tdt(math.radians(Longitude),
                                                                sun_position.calc_eed(NDay),
                                                                TT,
                                                                math.radians(135.0)
                                                                )
                                         )[0]
                actual = math.degrees(hs)
                expected = hsdtA
                self.assertAlmostEqual(actual, expected, delta=0.000000001)

class TestCalcAzsdtFunction(unittest.TestCase):

    # 正しい値が返ってくるかどうかのテスト
    def test_assert(self):

        f = open(TEST_DIRECTORY + 'Azsdt.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [float(d) for d in row]
            case, Latitude, Longitude, NDay, TT, AzsdtA = tuple(row_float)
            with self.subTest(case = case):
                deltad = sun_position.calc_deltad(NDay)
                eed = sun_position.calc_eed(NDay)
                Tdt = sun_position.calc_Tdt(math.radians(Longitude), eed, TT, math.radians(135.0)) 
                hs, sin_hs, cos_hs = sun_position.calc_hs(math.radians(Latitude),
                                                          deltad, Tdt)
                actual = math.degrees(
                        sun_position.calc_Azs(math.radians(Latitude),
                                              deltad, Tdt, hs)
                        )
                expected = AzsdtA
                self.assertAlmostEqual(actual, expected, delta=0.000000001)
            
class TestCalcAzwjFunction(unittest.TestCase):
    
    # 正しい値が返ってくるかどうかのテスト
    def test_assert(self):

        test_list = [
                ('北北東', -157.5),
                ('北東', -135.0),
                ('東北東', -112.5),
                ('東', -90.0),
                ('東南東', -67.5),
                ('南東', -45.0),
                ('南南東', -22.5),
                ('南', 0.0),
                ('南南西', 22.5),
                ('南西', 45.0),
                ('西南西', 67.5),
                ('西', 90.0),
                ('西北西', 112.5),
                ('北西', 135.0),
                ('北北西', 157.5),
                ('北', 180.0),
                (-179.0, -179.0),
                (180.0, 180.0),
                ]
        for i, row in enumerate(test_list):
            azimuth, azwjA = tuple(row)
            with self.subTest(azimuth=azimuth, azwjA=azwjA):
                actual = sun_position.calc_Azwj(azimuth)
                expected = azwjA
                self.assertEqual(actual,expected)

    # 間違った値が指定された場合にエラーが返ってくるかのテスト
    # -180以下、および、180より大の値は許容されていない。
    def test_exception(self):
        azimuth = -180.1
        with self.assertRaises(ValueError) as cm:
            sun_position.calc_Azwj(azimuth)
            the_exception = cm.exception
            self.assertEqual(the_exception.error_code, 3)

class TestCalcAzwjdtFunction(unittest.TestCase):

    # 正しい値が返ってくるかどうかのテスト
    def test_assert(self):

        f = open(TEST_DIRECTORY + 'Azwjdt.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [float(d) for d in row]
            case, Azwj, Latitude, Longitude, NDay, TT, AzwjdtA = tuple(row_float)
            with self.subTest(case = case):
                deltad = sun_position.calc_deltad(NDay)
                eed = sun_position.calc_eed(NDay)
                Tdt = sun_position.calc_Tdt(math.radians(Longitude), eed, TT, math.radians(135.0)) 
                hs, sinh, cosh = sun_position.calc_hs(math.radians(Latitude),
                                                      deltad, Tdt)
                Azsdt = math.degrees(
                        sun_position.calc_Azs(math.radians(Latitude),
                                              deltad, Tdt, hs)
                        )
                actual = sun_position.calc_Azwjdt(Azwj, Azsdt)
                expected = AzwjdtA
                self.assertAlmostEqual(actual, expected, delta=0.000000001)

class SetWSSizeFunction(unittest.TestCase):
    
    # 正しい値が返ってくるかどうかのテスト
    def test_assert(self):
        
        def convert(v):
            try:
                return float(v)
            except:
                return v

        f = open(TEST_DIRECTORY + 'WSSize.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [ convert(d) for d in row]
            case = row_float[0]
            with self.subTest(case):
                WSSizeA = row_float[1:19]
                WSSize1 = row_float[19:]
                if case < 35:
                    WSSize = sun_position.set_WSSize(WSSize1)
                    difWSSize = [a-b for (a,b) in zip(WSSize, WSSizeA)]
                    actual = max(max(difWSSize),abs(min(difWSSize)))
                    self.assertAlmostEqual(actual, 0.0, delta=0.000000001)
                else:
                    with self.assertRaises(ValueError) as cm:
                        sun_position.set_WSSize(WSSize1)
                        the_exception = cm.exception
                        self.assertEqual(the_exception.error_code, 3)
                        