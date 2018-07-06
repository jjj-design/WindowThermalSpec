import direct_solar_area

import unittest
import csv

class TestCalcAoh0pFunction(unittest.TestCase):
    
    # 正しい値が返ってくるかどうかのテスト    
    def test_assert(self):
        f = open('./TestConfig01/Aoh0p.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [float(d) for d in row]
            case, XX, YY = row_float[0:3]
            WSSize = row_float[3:-3]
            Azw, hs, Aoh0pA = row_float[-3:]
            with self.subTest(case = case):
                actual = direct_solar_area.calc_Aoh0p(XX, YY, WSSize, Azw, hs)
                expected = Aoh0pA
                self.assertAlmostEqual(actual, expected, delta=0.000000001)
                
class TestCalcAsf0pFunction(unittest.TestCase):                
                
    # 正しい値が返ってくるかどうかのテスト    
    def test_assert(self):
        f = open('./TestConfig01/Asf0p.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [float(d) for d in row]
            case, XX, YY = row_float[0:3]
            WSSize = row_float[3:-3]
            Azw, hs, Asf0pA = row_float[-3:]
            with self.subTest(case = case):
                actual = direct_solar_area.calc_Asf0p(XX, YY, WSSize, Azw, hs)
                expected = Asf0pA
                self.assertAlmostEqual(actual, expected, delta=0.000000001)

class TestCalcAxpFunction(unittest.TestCase):
    
    # 正しい値が返ってくるかどうかのテスト    
    def test_assert(self):
        f = open('./TestConfig01/Axp.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [float(d) for d in row]
            case = row_float[0]
            WSSize = row_float[1:-3]
            Azw, hs, AxpA = row_float[-3:]
            with self.subTest(case = case):
                actual = direct_solar_area.calc_Axp(WSSize, Azw, hs)
                expected = AxpA
                self.assertAlmostEqual(actual, expected, delta=0.000000001)

class TestCalcAoh0mFunction(unittest.TestCase):

    # 正しい値が返ってくるかどうかのテスト    
    def test_assert(self):
        f = open('./TestConfig01/Aoh0m.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [float(d) for d in row]
            case, XX, YY = row_float[0:3]
            WSSize = row_float[3:-3]
            Azw, hs, Aoh0mA = row_float[-3:]
            with self.subTest(case = case):
                actual = direct_solar_area.calc_Aoh0m(XX, YY, WSSize, Azw, hs)
                expected = Aoh0mA
                self.assertAlmostEqual(actual, expected, delta=0.000000001)

class TestCalcAsf0mFunction(unittest.TestCase):

    # 正しい値が返ってくるかどうかのテスト    
    def test_assert(self):
        f = open('./TestConfig01/Asf0m.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [float(d) for d in row]
            case, XX, YY = row_float[0:3]
            WSSize = row_float[3:-3]
            Azw, hs, Asf0mA = row_float[-3:]
            with self.subTest(case = case):
                actual = direct_solar_area.calc_Asf0m(XX, YY, WSSize, Azw, hs)
                expected = Asf0mA
                self.assertAlmostEqual(actual, expected, delta=0.000000001)

class TestCalcAxmFunction(unittest.TestCase):

    # 正しい値が返ってくるかどうかのテスト    
    def test_assert(self):
        f = open('./TestConfig01/Axm.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [float(d) for d in row]
            case = row_float[0]
            WSSize = row_float[1:-3]
            Azw, hs, AxmA = row_float[-3:]
            with self.subTest(case = case):
                actual = direct_solar_area.calc_Axm(WSSize, Azw, hs)
                expected = AxmA
                self.assertAlmostEqual(actual, expected, delta=0.000000001)
    
if __name__ == "__main__":
    unittest.main()