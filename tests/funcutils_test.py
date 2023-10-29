import unittest
import sys
import os
sys.path.append('../brmanga')
from funcutils import get_env, read_download_manga_list

class FuncUtilsTest(unittest.TestCase):

    def test_get_env(self):
        envs = get_env()

        self.assertNotEqual("", envs["download_list"])
        self.assertNotEqual("", envs["download_path"])


    def test_read_list(self):
        manga_list = read_download_manga_list()

        self.assertTrue(len(manga_list) > 0)


if __name__ == "__main__":
    unittest.main()
