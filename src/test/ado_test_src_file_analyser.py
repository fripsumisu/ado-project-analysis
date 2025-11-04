import unittest

from src import ado_test_src_file_analyser


class TestFileParserTestCase(unittest.TestCase):

    def test_parse_possible_test_file(self):
        file_ut = "temp/my-repo/SomeSuchTest.java"
        results = ado_test_src_file_analyser.parse_possible_test_file(filepath=file_ut)
        self.assertIsNotNone(results)  # add assertion here


if __name__ == '__main__':
    unittest.main()
