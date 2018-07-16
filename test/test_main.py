import nbimporter
import csv
import unittest
import sys

sys.path.append('../')
from module import Shading_Correction_Factor_Main as SCFMain

TEST_DIRECTORY = './test/test_case/'

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
                actual = SCFMain.calc_Azwj(azimuth)
                expected = azwjA
                self.assertEqual(actual,expected)

    # 間違った値が指定された場合にエラーが返ってくるかのテスト
    # -180以下、および、180より大の値は許容されていない。
    def test_exception(self):
        azimuth = -180.1
        with self.assertRaises(ValueError) as cm:
            SCFMain.calc_Azwj(azimuth)
            the_exception = cm.exception
            self.assertEqual(the_exception.error_code, 3)


class TestMain(unittest.TestCase):
    
    def test_assert(self):
        f = open(TEST_DIRECTORY + 'AllTest01.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            case = int(row[0])
            Path00 = row[1]
            FileName00 = row[2]
            FileName01 = row[3]
            ClimateZone = int(row[4])
            NDT = int(row[5])
            etaID = int(row[6])
            Azimuth = {
                    'S' : '南',
                    'SW': '南西',
                    'W' : '西',
                    'NW': '北西',
                    'N' : '北',
                    'NE': '北東',
                    'E' : '東',
                    'SE': '南東'
                    }[row[7]]
            WSSize = [float(r) for r in row[8:-2]]
            SCFhA, SCFcA = [float(r) for r in row[-2:] ]
            with self.subTest(case = case):
                # テスト時間がかかるため便宜的にiは4までとする。
                if i < 5:
                    SCF = SCFMain.Calc_ShadingCorrectionFactor(Path00, FileName00, FileName01, ClimateZone, NDT, etaID, Azimuth, WSSize )
                    SCFh, SCFc = SCF[2][-1][-1], SCF[2][-2][-1]
                    print(case)
                    self.assertAlmostEqual(SCFh, SCFhA, delta=0.000000001)
                    self.assertAlmostEqual(SCFc, SCFcA, delta=0.000000001)

if __name__ == "__main__":
    unittest.main()
