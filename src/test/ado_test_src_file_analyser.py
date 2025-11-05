import unittest

from src import ado_test_src_file_analyser


class TestFileParserTestCase(unittest.TestCase):

    def test_parse_possible_java_test_file(self):
        file_ut = "resources/CalculatorTest.java"
        results = ado_test_src_file_analyser.parse_possible_test_file(filepath=file_ut)
        poss_tests = results["possibleTests"]
        poss_duds = results["possibleDudTests"]
        self.assertIsNotNone(results)
        self.assertEqual(poss_tests, 4, f"Unexpected number of tests found in file '{file_ut}'!")
        self.assertEqual(poss_duds, 1, f"Unexpected number of dud tests found in file '{file_ut}'!")

    def test_parse_possible_python_test_file(self):
        file_ut = "resources/sample_test.py"
        results = ado_test_src_file_analyser.parse_possible_test_file(filepath=file_ut)
        poss_tests = results["possibleTests"]
        poss_duds = results["possibleDudTests"]
        self.assertIsNotNone(results)
        self.assertEqual(poss_tests, 3, f"Unexpected number of tests found in file '{file_ut}'!")
        self.assertEqual(poss_duds, 1, f"Unexpected number of dud tests found in file '{file_ut}'!")


if __name__ == '__main__':
    unittest.main()
