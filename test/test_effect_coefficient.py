import nbimporter
import unittest
import csv
import sys

sys.path.append('../')
from module import effect_coefficient

TEST_DIRECTORY = './test/test_case/'

class TestCalcFaFunction(unittest.TestCase):
    
    # 正しい値が帰ってくるかどうかのテスト    
    def test_assert(self):
        test_list = [
                ( 1, 1.0,         2.0,         1.0,         2.0,         0.0, 0.392699082),
                ( 2, 0.000000001, 1.000000001, 0.000000001, 1.000000001, 0.0, 0.392699082),
                ( 3, 0.000000001, 2.000000001, 0.000000001, 1.000000001, 0.0, 1.017540754),
                ( 4, 0.0,         1.0,         0.0,         2.0,         0.0, 0.553255572),
                ( 5, 0.0,         2.0,         0.0,         1.0,         0.0, 1.017540754),
                ( 6, 1.0,         2.0,         1.0,         2.0,         0.1, 0.391076648),
                ( 7, 1.0,         2.0,         1.0,         2.0,         0.2, 0.386303418),
                ( 8, 1.0,         2.0,         1.0,         2.0,         0.5, 0.356352554),
                ( 9, 1.0,         2.0,         1.0,         2.0,         1.0, 0.281697381),
                (10, 1.0,         2.0,         1.0,         2.0,         2.0, 0.157580090),
                (11, 0.000000001, 1.000000001, 0.000000001, 2.0,         0.1, 0.484524567),
                (12, 0.000000001, 2.000000001, 0.000000001, 1.000000001, 0.1, 0.875211158),
                (13, 0.000000001, 1.000000001, 0.000000001, 2.0,         0.5, 0.306168461),
                (14, 0.000000001, 2.000000001, 0.000000001, 1.000000001, 0.5, 0.493349072),
                (15, 0.000000001, 1.000000001, 0.000000001, 2.0,         1.0, 0.187491560),
                (16, 0.000000001, 2.000000001, 0.000000001, 1.000000001, 1.0, 0.261560446),
                (17, 1.0,         2.0,         1.0,         2.0,         0.5, 0.356352554),
                (18, 1.0,         3.0,         1.0,         2.0,         0.6, 0.800498615),
                (19, 1.0,         2.0,         1.0,         2.0,         0.7, 0.327999692),
                (20, 1.0,         3.0,         1.0,         2.0,         0.8, 0.735412913),
                (21, 1.0,         2.0,         1.0,         2.0,         0.9, 0.297173836),
                (22, 1.0,         3.0,         1.0,         2.0,         1.0, 0.667497622)
                ]
        for i, row in enumerate(test_list):
            case, xa, xb, ya, yb, za, fAA = tuple(row)
            with self.subTest(case=case):
                actual = effect_coefficient.calc_fa(xa, xb, ya, yb, za)
                expected = fAA
                self.assertAlmostEqual(actual,expected,delta=0.000000001)

class TestCalcPhiypFunction(unittest.TestCase):
    
    # 正しい値が返ってくるかどうかのテスト    
    def test_assert(self):
        f = open(TEST_DIRECTORY + 'phiyp.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader):
            row_float = [float(d) for d in row]
            case, X1, X2, X3, X1yp, X1ym, X3yp, X3ym, Y1, Y2, Y3, Y1xp, Y1xm, Y3xp, Y3xm, Zxp, Zxm, Zyp, Zym, phiypA = tuple(row_float)
            WSSize = [X1, X2, X3, X1yp, X1ym, X3yp, X3ym, Y1, Y2, Y3, Y1xp, Y1xm, Y3xp, Y3xm, Zxp, Zxm, Zyp, Zym]
            with self.subTest(case = case):
                actual = effect_coefficient.calc_phiyp(WSSize)
                expected = phiypA
                self.assertAlmostEqual(actual,expected,delta=0.000000001)

class TestCalcPhiymFunction(unittest.TestCase):
    
    # 正しい値が返ってくるかどうかのテスト
    def test_assert(self):
        f = open(TEST_DIRECTORY + 'phiym.csv','r',encoding='utf8')
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            row_float = [float(d) for d in row]
            case, X1, X2, X3, X1yp, X1ym, X3yp, X3ym, Y1, Y2, Y3, Y1xp, Y1xm, Y3xp, Y3xm, Zxp, Zxm, Zyp, Zym, phiypA = tuple(row_float)
            WSSize = [X1, X2, X3, X1yp, X1ym, X3yp, X3ym, Y1, Y2, Y3, Y1xp, Y1xm, Y3xp, Y3xm, Zxp, Zxm, Zyp, Zym]
            with self.subTest(case = case):
                actual = effect_coefficient.calc_phiym(WSSize)
                expected = phiypA
                self.assertAlmostEqual(actual,expected,delta=0.000000001)


if __name__ == "__main__":
    unittest.main()