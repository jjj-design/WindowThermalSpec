import nbimporter
import unittest
import csv
import numpy as np
import sys
import math

sys.path.append('../')
from module import climate
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
                actual = climate.calc_NDayNHour(Hour00)
                expected = (NdayA, NhourA)
                self.assertAlmostEqual(actual[0], expected[0], delta=0.000000001)
                self.assertAlmostEqual(actual[1], expected[1], delta=0.000000001)

class TestCalcTTFunction(unittest.TestCase):
    
    # 正しい値が返ってくるかどうかのテスト    
    def test_assert(self):
        NDT = 6
        for NHour in range(0,24):
            for MM in range(0,NDT):
                actual = climate.calc_TT(NHour, NDT, MM)
                expected = NHour + MM / 6
                self.assertAlmostEqual(actual, expected, delta=0.000000001)

class TestCalcNhFunction(unittest.TestCase):
    
    # 正しい値が返ってくるかどうかのテスト    
    def test_assert(self):
        f = open(TEST_DIRECTORY + 'Nh.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [float(d) for d in row]
            case, Latitude, Longitude, NDay, NHour, NDT, NhA = tuple(row_float)
            with self.subTest(case = case):
                sinh = [sun_position.calc_hs(
                        math.radians(Latitude),
                        sun_position.calc_deltad(NDay),
                        sun_position.calc_Tdt(math.radians(Longitude),
                                              sun_position.calc_eed(NDay),
                                              climate.calc_TT(NHour, NDT, MM),
                                              math.radians(135.0))
                        )[1] for MM in range(int(NDT))
                        ]
                prev_sinh = [sun_position.calc_hs(
                        math.radians(Latitude),
                        sun_position.calc_deltad(NDay),
                        sun_position.calc_Tdt(math.radians(Longitude),
                                              sun_position.calc_eed(NDay),
                                              climate.calc_TT(NHour-1, NDT, MM),
                                              math.radians(135.0))
                        )[1] for MM in range(int(NDT))
                        ]
                actual = climate.calc_Nh(sinh, prev_sinh, NDT)
                expected = NhA
                self.assertAlmostEqual(actual, expected, delta=0.000000001)
    
    # NDT = 1 だった場合のテスト
    def test_NDT_is_1_assert(self):

        latitude = 35
        longitude = 135
        nday = 121
        NDT = 1
        
        nhour1 = 6
        sinh = [sun_position.calc_hs(
                math.radians(latitude),
                sun_position.calc_deltad(nday),
                sun_position.calc_Tdt(math.radians(longitude),
                                      sun_position.calc_eed(nday),
                                      climate.calc_TT(nhour1, NDT, MM),
                                      math.radians(135.0))
                )[1] for MM in range(int(NDT))
                ]
        actual1 = climate.calc_Nh(sinh, None, NDT)
        expected1 = 1
        self.assertAlmostEqual(actual1, expected1, delta=0.000000001)

        nhour2 = 5
        sinh = [sun_position.calc_hs(
                math.radians(latitude),
                sun_position.calc_deltad(nday),
                sun_position.calc_Tdt(math.radians(longitude),
                                      sun_position.calc_eed(nday),
                                      climate.calc_TT(nhour2, NDT, MM),
                                      math.radians(135.0))
                )[1] for MM in range(int(NDT))
                ]
        actual2 = climate.calc_Nh(sinh, None, NDT)
        expected2 = 0
        self.assertAlmostEqual(actual2, expected2, delta=0.000000001)
    
    # NDT が1以外の奇数を指定された場合にエラーが発生することを確認するためのテスト
    def test_exception(self):
        with self.assertRaises(ValueError) as cm:
            climate.calc_Nh(None, None, 5)
            the_exception = cm.exception
            self.assertEqual(the_exception.error_code, 3)

class TestCalcSdhmFunction(unittest.TestCase):
    
    # 正しい値が返ってくるかどうかのテスト    
    def test_assert(self):
        f = open(TEST_DIRECTORY + 'Sdhm.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [float(d) for d in row]
            case, MM, NDT, sinh, Sh, Shp, Nh, Nhp, SdhmA = tuple(row_float)
            with self.subTest(case = case):
                actual = climate.calc_Sdhm(MM, NDT, sinh, Sh, Shp, Nh, Nhp)
                expected = SdhmA
                self.assertAlmostEqual(actual, expected, delta=0.000000001)

class TestGetIncidentAngleCharacteristicsFunction(unittest.TestCase):
    
    def compare(self, actual_row, expected_row):
        self.assertAlmostEqual(actual_row[0], expected_row[0], delta=0.000000001)
        self.assertAlmostEqual(actual_row[1], expected_row[1], delta=0.000000001)
        self.assertAlmostEqual(actual_row[2], expected_row[2], delta=0.000000001)
        self.assertAlmostEqual(actual_row[3][0], expected_row[3][0], delta=0.000000001)
        self.assertAlmostEqual(actual_row[3][1], expected_row[3][1], delta=0.000000001)
        self.assertAlmostEqual(actual_row[3][2], expected_row[3][2], delta=0.000000001)
        self.assertAlmostEqual(actual_row[3][3], expected_row[3][3], delta=0.000000001)
        self.assertAlmostEqual(actual_row[3][4], expected_row[3][4], delta=0.000000001)
        self.assertAlmostEqual(actual_row[3][5], expected_row[3][5], delta=0.000000001)
        self.assertAlmostEqual(actual_row[3][6], expected_row[3][6], delta=0.000000001)
        self.assertAlmostEqual(actual_row[3][7], expected_row[3][7], delta=0.000000001)
    
    def test_assert(self):
        iac = climate.get_incident_angle_characteristics()
        actual_row = [1, iac.eta_max, iac.eta_isr, np.array(iac.eta_kk)]
        expected_row = [1, 0.88, 0.808, np.array([0, 2.392, 0, -3.8636, 0, 3.7568, 0, -1.3952])]
        self.compare(actual_row, expected_row)
       
class TestCalcEtajdtFunction(unittest.TestCase):
    
    # 正しい値が返ってくるかどうかのテスト    
    def test_assert(self):
        f = open(TEST_DIRECTORY + 'etajdt.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [float(d) for d in row]
            case, Azwjdt, cosh = row_float[0:3]
            etakk = row_float[3:11]
            etajdtA = row_float[-1] 
            with self.subTest(case = case):
                costheta = climate.calc_costheta(Azwjdt, cosh)
                actual = climate.calc_etajdt(costheta, etakk)
                expected = etajdtA
                self.assertAlmostEqual(actual, expected, delta=0.000000001)

    
if __name__ == "__main__":
    unittest.main()
