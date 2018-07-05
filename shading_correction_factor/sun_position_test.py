import sun_position

import unittest
import csv

class TestCalcNDayNHourFunction(unittest.TestCase):
    
    # 正しい値が返ってくるかどうかのテスト    
    def test_assert(self):
        f = open('./test_case/NDayNHour.csv','r',encoding='utf8')
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

class TestCalcTT(unittest.TestCase):
    
    # 正しい値が返ってくるかどうかのテスト    
    def test_assert(self):
        NDT = 6
        for NHour in range(0,24):
            for MM in range(0,NDT):
                actual = sun_position.calc_TT(NHour, NDT, MM)
                expected = NHour + MM / 6
                self.assertAlmostEqual(actual, expected, delta=0.000000001)

class TestCalcDeltad(unittest.TestCase):
    
    # 正しい値が返ってくるかどうかのテスト    
    def test_assert(self):

        f = open('./test_case/deltad.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [float(d) for d in row]
            case, NDay, deltadA = tuple(row_float)
            with self.subTest(case = case):
                actual = sun_position.calc_deltad(NDay)
                expected = deltadA
                self.assertAlmostEqual(actual, expected, delta=0.000000001)

class TestCalcEed(unittest.TestCase):
    
    # 正しい値が返ってくるかどうかのテスト
    def test_assert(self):
        
        f = open('./test_case/eed.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [float(d) for d in row]
            case, NDay, eedA = tuple(row_float)
            with self.subTest(case = case):
                actual = sun_position.calc_eed(NDay)
                expected = eedA
                self.assertAlmostEqual(actual, expected, delta=0.000000001)

class TestCalcTdt(unittest.TestCase):

    # 正しい値が返ってくるかどうかのテスト
    def test_assert(self):
    
        f = open('./TestConfig01/Tdt.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [float(d) for d in row]
            case, Longitude, NDay, TT, TdtA = tuple(row_float)
            with self.subTest(case = case):
                actual = sun_position.calc_Tdt(Longitude, sun_position.calc_eed(NDay), TT)
                expected = TdtA
                self.assertAlmostEqual(actual, expected, delta=0.000000001)

class TestCalcSinh(unittest.TestCase):

    # 正しい値が返ってくるかどうかのテスト
    def test_assert(self):
    
        f = open('./TestConfig01/sinh.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [float(d) for d in row]
            case, Latitude, Longitude, NDay, TT, sinhA = tuple(row_float)
            with self.subTest(case = case):
                actual = sun_position.calc_sinh(Latitude, sun_position.calc_deltad(NDay),
                                                sun_position.calc_Tdt(Longitude, sun_position.calc_eed(NDay), TT) )
                expected = sinhA
                self.assertAlmostEqual(actual, expected, delta=0.000000001)


    
if __name__ == "__main__":
    unittest.main()