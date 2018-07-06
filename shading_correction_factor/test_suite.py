import unittest

# 個別のテスト
import climate_test
import direct_solar_area_test
import effect_coefficient_test
import sun_position_test

def suite():

    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(climate_test.TestCalcNhFunction))
    test_suite.addTest(unittest.makeSuite(climate_test.TestCalcSdhmFunction))
    test_suite.addTest(unittest.makeSuite(climate_test.TestInputIncidentAngleCharacteristicsFunction))
    test_suite.addTest(unittest.makeSuite(climate_test.TestCalcEtajdtFunction))

    test_suite.addTest(unittest.makeSuite(direct_solar_area_test.TestCalcAoh0pFunction))
    test_suite.addTest(unittest.makeSuite(direct_solar_area_test.TestCalcAsf0pFunction))
    test_suite.addTest(unittest.makeSuite(direct_solar_area_test.TestCalcAxpFunction))
    test_suite.addTest(unittest.makeSuite(direct_solar_area_test.TestCalcAoh0mFunction))
    test_suite.addTest(unittest.makeSuite(direct_solar_area_test.TestCalcAsf0mFunction))
    test_suite.addTest(unittest.makeSuite(direct_solar_area_test.TestCalcAxmFunction))

    test_suite.addTest(unittest.makeSuite(effect_coefficient_test.TestCalcFaFunction))
    test_suite.addTest(unittest.makeSuite(effect_coefficient_test.TestCalcPhiypFunction))
    test_suite.addTest(unittest.makeSuite(effect_coefficient_test.TestCalcPhiymFunction))

    test_suite.addTest(unittest.makeSuite(sun_position_test.TestCalcNDayNHourFunction))
    test_suite.addTest(unittest.makeSuite(sun_position_test.TestCalcTTFunction))
    test_suite.addTest(unittest.makeSuite(sun_position_test.TestCalcDeltadFunction))
    test_suite.addTest(unittest.makeSuite(sun_position_test.TestCalcEedFunction))
    test_suite.addTest(unittest.makeSuite(sun_position_test.TestCalcTdtFunction))
    test_suite.addTest(unittest.makeSuite(sun_position_test.TestCalcSinhFunction))
    test_suite.addTest(unittest.makeSuite(sun_position_test.TestCalcCoshFunction))
    test_suite.addTest(unittest.makeSuite(sun_position_test.TestCalcHsdtAFunction))
    test_suite.addTest(unittest.makeSuite(sun_position_test.TestCalcAzsdtFunction))
    test_suite.addTest(unittest.makeSuite(sun_position_test.TestCalcAzwjFunction))
    test_suite.addTest(unittest.makeSuite(sun_position_test.TestCalcAzwjdtFunction))
    test_suite.addTest(unittest.makeSuite(sun_position_test.SetWSSizeFunction))


    return test_suite

if __name__ == "__main__":
    mySuite = suite()
    unittest.TextTestRunner().run(mySuite)