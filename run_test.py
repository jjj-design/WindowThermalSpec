import unittest

# 個別のテスト
#from test import test_sun_position

def get_suite():

#    suite = unittest.TestSuite()

#    suite.addTest(unittest.makeSuite(sun_position_test.TestCalcNDayNHourFunction))
#    suite.addTest(unittest.makeSuite(sun_position_test.TestCalcTTFunction))
#    suite.addTest(unittest.makeSuite(sun_position_test.TestCalcDeltadFunction))
#    suite.addTest(unittest.makeSuite(sun_position_test.TestCalcEedFunction))
#    suite.addTest(unittest.makeSuite(sun_position_test.TestCalcTdtFunction))
#    suite.addTest(unittest.makeSuite(sun_position_test.TestCalcSinhFunction))
#    suite.addTest(unittest.makeSuite(sun_position_test.TestCalcCoshFunction))
#    suite.addTest(unittest.makeSuite(sun_position_test.TestCalcHsdtAFunction))
#    suite.addTest(unittest.makeSuite(sun_position_test.TestCalcAzsdtFunction))
#    suite.addTest(unittest.makeSuite(sun_position_test.TestCalcAzwjFunction))
#    suite.addTest(unittest.makeSuite(sun_position_test.TestCalcAzwjdtFunction))
#    suite.addTest(unittest.makeSuite(sun_position_test.SetWSSizeFunction))

#    return suite

    return unittest.defaultTestLoader.discover("test", pattern="test_*.py")

if __name__ == "__main__":
    suite = get_suite()
    unittest.TextTestRunner().run(suite)