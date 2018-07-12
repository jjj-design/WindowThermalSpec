import nbimporter
import unittest
import csv
import numpy as np
import sys

sys.path.append('../')
from module import climate

TEST_DIRECTORY = './test/test_case/'

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
                actual = climate.calc_Nh(Latitude, Longitude, NDay, NHour, NDT)
                expected = NhA
                self.assertAlmostEqual(actual, expected, delta=0.000000001)
    
    # NDT = 1 だった場合のテスト
    def test_NDT_is_1_assert(self):

        actual1 = climate.calc_Nh(35, 135, 121, 6, 1)
        expected1 = 1
        self.assertAlmostEqual(actual1, expected1, delta=0.000000001)

        actual2 = climate.calc_Nh(35, 135, 121, 5, 1)
        expected2 = 0
        self.assertAlmostEqual(actual2, expected2, delta=0.000000001)
    
    # NDT が1以外の奇数を指定された場合にエラーが発生することを確認するためのテスト
    def test_exception(self):
        with self.assertRaises(ValueError) as cm:
            climate.calc_Nh(35, 135, 121, 6, 5)
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
