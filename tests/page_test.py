import unittest
import sys
sys.path.append('../')

from brmanga.page import Page

#https://cdn.plaquiz.xyz/uploads/s/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai/1/1.jpg
#https://cdn.plaquiz.xyz/uploads/s/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai/1/3.png
#https://cdn.plaquiz.xyz/uploads/s/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai/1/4.png

class PageTest(unittest.TestCase):

    def test_sort(self):
        urls = (
            "https://cdn.plaquiz.xyz/uploads/s/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai/1/1.jpg",
            "https://cdn.plaquiz.xyz/uploads/s/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai/1/3.png",
            "https://cdn.plaquiz.xyz/uploads/s/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai/1/4.png"
        )

        page1 = Page(urls[0])
        page3 = Page(urls[1])
        page4 = Page(urls[2])

        self.assertLess(page1, page3)
        self.assertLess(page1, page4)

        self.assertLess(page3, page4)
        self.assertGreater(page3, page1)

        self.assertGreater(page4, page3)
        self.assertGreater(page4, page1)

        self.assertEqual(page1, page1)
        self.assertEqual(page3, page3)
        self.assertEqual(page4, page4)

        self.assertNotEqual(page1, page3)
        self.assertNotEqual(page1, page4)
        self.assertNotEqual(page3, page4)

        pages = sorted([page3, page1, page4])

        self.assertEqual(page1, pages[0])
        self.assertEqual(page3, pages[1])
        self.assertEqual(page4, pages[2])

    
    def test_download(self):
        page = Page("https://cdn.plaquiz.xyz/uploads/s/shingeki-no-eroko-san-hen-na-oneesan-wa-danshikousei-to-nakayoku-naritai/1/4.png")
        image = page.download()

        self.assertIsNotNone(image)


if __name__ == "__main__":
    unittest.main()
