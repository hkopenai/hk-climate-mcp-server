import unittest
from tests.test_weather import TestWeatherTools
from tests.test_app import TestApp

def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestWeatherTools))
    suite.addTests(loader.loadTestsFromTestCase(TestApp))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = suite()
    runner.run(test_suite)
