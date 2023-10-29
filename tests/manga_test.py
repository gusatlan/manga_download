import unittest
import sys
import os
sys.path.append('../brmanga')
from manga import Manga

#https://www.brmangas.net/manga/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai-online/


class MangaTest(unittest.TestCase):


    def test_extract_path(self):
        manga1 = Manga(
            url = "https://www.brmangas.net/manga/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai-online/",
            url_suffix = "-online",
            root_path = "/tmp/mangas"
        )

        manga2 = Manga(
            url = "https://www.brmangas.net/manga/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai-online",
            url_suffix = "-online",
            root_path = "/tmp/mangas"
        )

        path = os.path.join("/", "tmp", "mangas", "shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai")

        self.assertEqual(path, manga1.manga_path)
        self.assertEqual(path, manga2.manga_path)
        self.assertEqual(manga1.manga_path, manga2.manga_path)


    def test_extract_urls(self):
        manga = Manga(
            url = "https://www.brmangas.net/manga/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai-online/",
            url_suffix = "-online",
            root_path = "/tmp/mangas"
        )

        urls = manga.extract_url_chapters()
        self.assertTrue(len(urls) > 0)
    

    def test_build_chapters(self):
        manga = Manga(
            url = "https://www.brmangas.net/manga/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai-online/",
            url_suffix = "-online",
            root_path = "/tmp/mangas"
        )

        chapters = manga.build_chapters()
        self.assertTrue(len(chapters) > 0)


if __name__ == "__main__":
    unittest.main()
