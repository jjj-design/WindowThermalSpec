import nbimporter
import unittest
import csv
import sys
import math

sys.path.append('../')
from module import sun_position

TEST_DIRECTORY = './test/test_case/'

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

