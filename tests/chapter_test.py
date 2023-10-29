import unittest
import sys
sys.path.append('../')

from brmanga.chapter import Chapter

#https://www.brmangas.net/ler/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai-14-5-online/
#Capítulo 14.5

class ChapterTest(unittest.TestCase):

    def test_extract_chapter_name(self):
        chapter = Chapter(
            url = "https://www.brmangas.net/ler/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai-14-5-online/",
            chapter_name = "Capítulo 14.5",
            manga_path = "/tmp/mangas"
        )

        self.assertEqual("chapter-0014_5.pdf", chapter.chapter_file_name)


if __name__ == "__main__":
    unittest.main()
