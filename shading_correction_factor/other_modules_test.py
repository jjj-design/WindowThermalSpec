import other_modules

import unittest

class TestOtherModules(unittest.TestCase):
    
    def test_calc_Azwj(self):
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
                actual = other_modules.calc_Azwj(azimuth)
                expected = azwjA
                self.assertEqual(actual,expected)

    def test_calc_Azwj_exception(self):
        azimuth = -180.1
        with self.assertRaises(ValueError) as cm:
            other_modules.calc_Azwj(azimuth)
            the_exception = cm.exception
            self.assertEqual(the_exception.error_code, 3)

if __name__ == "__main__":
    unittest.main()