import unittest
import sys
import os
sys.path.append('../brmanga')
from service import retrieve_mangas

class ServiceTest(unittest.TestCase):

    def test_retrieve_mangas(self):
        manga_list = retrieve_mangas()

        self.assertTrue(len(manga_list) > 0)


if __name__ == "__main__":
    unittest.main()
