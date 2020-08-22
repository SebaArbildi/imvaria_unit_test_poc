import sys
from unittest import TestLoader, TestSuite
from HtmlTestRunner import HTMLTestRunner

from pydicom_tests.tests.dcmread_tests import DcmReadTest

if __name__:
    dcmread_tests = TestLoader().loadTestsFromTestCase(DcmReadTest)

    pydicom_test_suite = TestSuite([dcmread_tests])

    runner = HTMLTestRunner(output='pydicom_dcmread_tests_results')
    runner.report_title = 'Pydicom Dcmread'
    test_results = runner.run(pydicom_test_suite)

    sys.exit(0) if test_results else sys.exit(1)