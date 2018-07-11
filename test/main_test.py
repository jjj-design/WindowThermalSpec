import nbimporter
import csv
import unittest

import Shading_Correction_Factor_Main as SCFMain


class TestMain(unittest.TestCase):
    
    def test_assert(self):
        f = open('./TestConfig01/AllTest01.csv','r',encoding='utf8')
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
