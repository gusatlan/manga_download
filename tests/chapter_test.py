import unittest
import sys
import os
sys.path.append('../')

from brmanga.chapter import Chapter

#https://www.brmangas.net/ler/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai-14-5-online/
#Capítulo 14.5

#https://www.brmangas.net/ler/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai-7-5-online/
#Capítulo 7.5

#https://www.brmangas.net/ler/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai-7-online/
#Capítulo 7

#https://www.brmangas.net/ler/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai-20-online/
#Capítulo 20

class ChapterTest(unittest.TestCase):

    def test_extract_chapter_name(self):
        chapter = Chapter(
            url = "https://www.brmangas.net/ler/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai-14-5-online/",
            chapter_name = "Capítulo 14.5",
            manga_path = "/tmp/mangas"
        )

        self.assertEqual("chapter-0014_5.pdf", chapter.chapter_file_name)
    

    def test_chapter_sort(self):
        chapters = sorted([
            Chapter(
                url="https://www.brmangas.net/ler/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai-14-5-online/",
                chapter_name="Capítulo 14.5",
                manga_path = "/tmp/mangas"
            ),
            Chapter(
                url="https://www.brmangas.net/ler/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai-7-5-online/",
                chapter_name="Capítulo 7.5",
                manga_path = "/tmp/mangas"
            ),
            Chapter(
                url="https://www.brmangas.net/ler/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai-7-online/",
                chapter_name="Capítulo 7",
                manga_path = "/tmp/mangas"
            ),
            Chapter(
                url="https://www.brmangas.net/ler/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai-20-online/",
                chapter_name="Capítulo 20",
                manga_path = "/tmp/mangas"
            )
        ])

        self.assertEqual(7.0, chapters[0].id)
        self.assertEqual(7.5, chapters[1].id)
        self.assertEqual(14.5, chapters[2].id)
        self.assertEqual(20.0, chapters[3].id)
    

    def test_paths(self):
        chapter = Chapter(
            url = "https://www.brmangas.net/ler/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai-14-5-online/",
            chapter_name = "Capítulo 14.5",
            manga_path = "/tmp/mangas"
        )

        self.assertFalse(os.path.exists(os.path.join(chapter.manga_path)))
        chapter.mkdir()
        self.assertTrue(os.path.exists(os.path.join(chapter.manga_path)))

        os.removedirs(os.path.join(chapter.manga_path))

    
    def test_extract_chapter_url_images(self):
        chapter = Chapter(
                url="https://www.brmangas.net/ler/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai-14-5-online/",
                chapter_name="Capítulo 14.5",
                manga_path = "/tmp/mangas"
            )
        urls = chapter.extract_url_pages()

        self.assertTrue(len(urls) > 12)
    

    def test_save_chapter(self):
        chapter = Chapter(
            url="https://www.brmangas.net/ler/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai-14-5-online/",
            chapter_name="Capítulo 14.5",
            manga_path = "/tmp/mangas"
        )

        chapter.save_chapter_content()

        filename = chapter.chapter_full_path
        self.assertTrue(os.path.exists(filename))
        #os.remove(filename)


if __name__ == "__main__":
    unittest.main()
